/*
Copyright IBM Corporation 2021

Licensed under the Eclipse Public License 2.0, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
 */

package io.tackle.diva;

import java.util.HashMap;
import java.util.Map;

import com.ibm.wala.cast.java.ipa.callgraph.JavaSourceAnalysisScope;
import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.ssa.ISSABasicBlock;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSACheckCastInstruction;
import com.ibm.wala.ssa.SSAGetInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSANewInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.ssa.SSAReturnInstruction;
import com.ibm.wala.ssa.SymbolTable;
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.util.intset.BitVector;

public class Trace extends Util.Chain<Trace> {

    public interface Visitor {
        void visitCallSite(Trace trace);

        void visitNode(Trace trace);

        void visitInstruction(Trace trace, SSAInstruction instr);

        default void visitExit(Trace trace) {
        }

        default Visitor with(Visitor other) {
            Visitor self = this;
            return new Visitor() {

                @Override
                public void visitCallSite(Trace trace) {
                    self.visitCallSite(trace);
                    other.visitCallSite(trace);
                }

                @Override
                public void visitNode(Trace trace) {
                    self.visitNode(trace);
                    other.visitNode(trace);
                }

                @Override
                public void visitExit(Trace trace) {
                    self.visitExit(trace);
                    other.visitExit(trace);
                }

                @Override
                public void visitInstruction(Trace trace, SSAInstruction instr) {
                    self.visitInstruction(trace, instr);
                    other.visitInstruction(trace, instr);
                }
            };
        }
    }

    @FunctionalInterface
    public interface CallSiteVisitor extends Visitor {
        @Override
        default void visitNode(Trace trace) {
        }

        @Override
        default void visitInstruction(Trace trace, SSAInstruction instr) {
        }
    }

    @FunctionalInterface
    public interface NodeVisitor extends Visitor {
        @Override
        default void visitCallSite(Trace trace) {
        }

        @Override
        default void visitInstruction(Trace trace, SSAInstruction instr) {
        }
    }

    @FunctionalInterface
    public interface InstructionVisitor extends Visitor {
        @Override
        default void visitNode(Trace trace) {
        }

        @Override
        default void visitCallSite(Trace trace) {
        }
    }

    final CallSiteReference site;
    final Cache cache;

    public static class Cache {
        public Cache(CGNode node) {
            this.node = node;
        }

        final CGNode node;
        Context context;
        BitVector reachingInstrs;
        Object[] ud;
        Map<CallSiteReference, Trace> callLog;
    }

    public CGNode node() {
        return cache.node;
    }

    public Trace parent() {
        return next;
    }

    public CallSiteReference site() {
        return site;
    }

    public Context context() {
        return cache.context;
    }

    public Map<CallSiteReference, Trace> callLog() {
        return cache.callLog;
    }

    public Trace updateSite(CallSiteReference site) {
        return new Trace(this.cache, site, this.next);
    }

    public void logCall(Trace callee) {
        if (site == null)
            return;
        if (cache.callLog == null) {
            cache.callLog = new HashMap<>();
        }
        cache.callLog.put(site, callee);
    }

    public void setContext(Context context) {
        this.cache.context = context;
    }

    private Trace(Cache cache, CallSiteReference site, Trace next) {
        super(next);
        this.cache = cache;
        this.site = site;
    }

    public Trace(CGNode node, Trace parent) {
        super(parent);
        this.cache = new Cache(node);
        this.site = null;
    }

    // -------------------------------------------------
    // Interprocedural ud chain
    // -------------------------------------------------

    public class Val {
        final Object content;

        public Val(Object content) {
            super();
            this.content = content;
        }

        public boolean isConstant() {
            return !(content instanceof SSAInstruction || this instanceof ParamVal);
        }

        public Object constant() {
            return content;
        }

        public SSAInstruction instr() {
            return (SSAInstruction) content;
        }

        @Override
        public String toString() {
            return "" + content;
        }

        public Trace trace() {
            return Trace.this;
        }

        public Val getDef(int number) {
            return Trace.this.getDef(number);
        }

        public boolean isParam() {
            return this instanceof ParamVal;
        }

        public boolean isInstr() {
            return !isConstant() && !isParam();
        }

        public int param() {
            return -1;
        }

        public Val getDefOrParam(int number) {
            return Trace.this.getDefOrParam(number);
        }
    }

    public void populateUd() {
        IR ir = cache.node.getIR();
        if (ir == null) {
            return;
        }
        cache.ud = new Object[ir.getSymbolTable().getMaxValueNumber() + 1];
        SSAInstruction[] instrs = ir.getInstructions();
        for (SSAInstruction instr : instrs) {
            if (instr != null && instr.hasDef()) {
                cache.ud[instr.getDef(0)] = instr;
            }
        }
        for (ISSABasicBlock bb : (Iterable<ISSABasicBlock>) () -> ir.getBlocks()) {
            for (SSAPhiInstruction phi : (Iterable<SSAPhiInstruction>) () -> bb.iteratePhis()) {
                cache.ud[phi.getDef()] = phi;
            }
        }
        int param = 0;
        for (int i : ir.getParameterValueNumbers()) {
            cache.ud[i] = param++;
        }
    }

    public Val getDef(int number) {
        IR ir = cache.node.getIR();
        if (ir == null) {
            return null;
        }
        SymbolTable sym = ir.getSymbolTable();
        if (sym.isConstant(number)) {
            return new Val(sym.getConstantValue(number));
        }
        if (cache.ud == null) {
            populateUd();
        }
        if (cache.ud[number] instanceof SSAAbstractInvokeInstruction) {
            SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) cache.ud[number];
            if (cache.callLog != null && cache.callLog.containsKey(invoke.getCallSite())) {
                Trace calleeTrace = cache.callLog.get(invoke.getCallSite());
                SSAInstruction[] instrs = calleeTrace.node().getIR().getInstructions();
                for (int i = instrs.length - 1; i >= 0; i--) {
                    if (instrs[i] == null)
                        continue;
                    if (instrs[i] instanceof SSAReturnInstruction) {
                        Trace.Val v = calleeTrace.getDef(((SSAReturnInstruction) instrs[i]).getUse(0));
                        return v;
                    }
                }
            }
        }
        if (cache.ud[number] instanceof SSAInstruction) {
            return new Val(cache.ud[number]);
        }
        if (cache.ud[number] instanceof Integer) {
            // interprocedural resolution of call parameters
            Trace callerTrace = this.next;
            if (callerTrace != null) {
                SSAInstruction caller = callerTrace.instrFromSite(callerTrace.site);
                if (caller != null) {
                    return callerTrace.getDef(caller.getUse((Integer) cache.ud[number]));
                }
            }
        }
        return null;
    }

    public class ParamVal extends Val {
        public ParamVal(Object content) {
            super(content);
        }

        @Override
        public int param() {
            return (Integer) content;
        }
    }

    public Val getDefOrParam(int number) {
        IR ir = cache.node.getIR();
        if (ir == null) {
            return null;
        }
        SymbolTable sym = ir.getSymbolTable();
        if (sym.isConstant(number)) {
            return new Val(sym.getConstantValue(number));
        }
        if (cache.ud == null) {
            populateUd();
        }
        if (cache.ud[number] instanceof SSAAbstractInvokeInstruction) {
            SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) cache.ud[number];
            if (cache.callLog != null && cache.callLog.containsKey(invoke.getCallSite())) {
                Trace calleeTrace = cache.callLog.get(invoke.getCallSite());
                SSAInstruction[] instrs = calleeTrace.node().getIR().getInstructions();
                for (int i = instrs.length - 1; i >= 0; i--) {
                    if (instrs[i] == null)
                        continue;
                    if (instrs[i] instanceof SSAReturnInstruction) {
                        Trace.Val v = calleeTrace.getDef(((SSAReturnInstruction) instrs[i]).getUse(0));
                        return v;
                    }
                }
            }
        }
        if (cache.ud[number] instanceof SSAInstruction) {
            return new Val(cache.ud[number]);
        }
        if (cache.ud[number] instanceof Integer) {
            // interprocedural resolution of call parameters
            Trace callerTrace = this.next;
            if (callerTrace != null) {
                SSAInstruction caller = callerTrace.instrFromSite(callerTrace.site);
                if (caller != null) {
                    return callerTrace.getDefOrParam(caller.getUse((Integer) cache.ud[number]));
                }
            }
            return this.new ParamVal(cache.ud[number]);
        }
        return null;
    }

    public TypeReference inferType(SSAInstruction instr) {
        TypeReference ref = null;
        if (instr instanceof SSAGetInstruction)
            ref = ((SSAGetInstruction) instr).getDeclaredFieldType();
        if (instr instanceof SSANewInstruction)
            ref = ((SSANewInstruction) instr).getConcreteType();
        if (instr instanceof SSAAbstractInvokeInstruction)
            ref = ((SSAAbstractInvokeInstruction) instr).getDeclaredResultType();
        if (instr instanceof SSACheckCastInstruction)
            ref = ((SSACheckCastInstruction) instr).getDeclaredResultType();
        return ref;
    }

    public TypeReference inferType(Val value) {
        if (value == null)
            return null;
        if (value.isConstant()) {
            return null;
        } else if (value.isParam()) {
            return value.trace().node().getMethod().getParameterType(value.param());
        } else {
            return inferType(value.instr());
        }
    }

    public TypeReference inferType(int number) {
        return inferType(getDefOrParam(number));
    }

    public IClass inferType(Framework fw, int number) {
        TypeReference ref = inferType(number);
        if (ref == null) {
            return null;
        }
        return fw.classHierarchy().lookupClass(ref);
    }

    public SSAAbstractInvokeInstruction instrFromSite(CallSiteReference site) {
        if (cache.node.getMethod().getDeclaringClass().getClassLoader()
                .getReference() == JavaSourceAnalysisScope.SOURCE) {
            // SSAInstruction instr =
            // node.getIR().getInstructions()[site.getProgramCounter()];
            // if (!(instr instanceof SSAAbstractInvokeInstruction)) {
            // System.out.println("HERE");
            // }
            return cache.node.getIR().getCalls(site)[0];
        }
        for (SSAInstruction i : cache.node.getIR().getInstructions()) {
            // TODO binary search
            if (i instanceof SSAAbstractInvokeInstruction) {
                SSAAbstractInvokeInstruction instr = (SSAAbstractInvokeInstruction) i;
                if (instr.getCallSite() == site)
                    return instr;
            }
        }
        return null;
    }

    public boolean in(CallSiteReference site) {
        return in(instrFromSite(site));
    }

    public boolean in(SSAInstruction instr) {
        if (cache.context == null)
            return true;
        if (cache.reachingInstrs == null) {
            cache.reachingInstrs = cache.context.calculateReachable(cache.node);
        }
        return cache.reachingInstrs.contains(instr.iIndex());
    }

}