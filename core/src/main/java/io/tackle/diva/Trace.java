/*
Copyright IBM Corporation 2021

Licensed under the Apache Public License 2.0, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
 */

package io.tackle.diva;

import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.Stack;
import java.util.function.Predicate;

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
import com.ibm.wala.util.intset.IntPair;

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
        if (cache.callLog != null && cache.callLog.containsKey(site)) {
            return cache.callLog.get(site).next;
        }
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

        public Val getReceiverUseOrDef(Set<IntPair> visited) {
            if (isInstr()) {
                return Trace.this.getReceiverUseOrDef(instr(), visited);
            } else {
                return null;
            }
        }

        public Val getReceiverUse(Set<IntPair> visited) {
            if (isInstr()) {
                return Trace.this.getReceiverUse(instr(), visited);
            } else {
                return null;
            }
        }

        public Val reachingValue(Predicate<Val> test) {
            return Trace.reachingValue(this, test);
        }

        public int getBbId() {
            if (content == null)
                return -1;
            if (!(content instanceof SSAInstruction))
                return -1;
            return Trace.this.node().getIR().getBasicBlockForInstruction((SSAInstruction) content).getNumber();
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
                if (caller != null && (int) cache.ud[number] < caller.getNumberOfUses()) {
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
                if (caller != null && (int) cache.ud[number] < caller.getNumberOfUses()) {
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
        return inferType(value, new HashSet<>());
    }

    public TypeReference inferType(Val value, Set<IntPair> visited) {
        if (value == null)
            return null;
        if (value.isConstant())
            return null;
        if (value.isParam()) {
            return value.trace().node().getMethod().getParameterType(value.param());
        }
        if (value.instr() instanceof SSAPhiInstruction) {
            for (int j = 0; j < value.instr().getNumberOfUses(); j++) {
                IntPair key = IntPair.make(value.trace().node().getGraphNodeId(), value.instr().getUse(j));
                if (visited.contains(key))
                    continue;
                visited.add(key);
                TypeReference tref = inferType(value.getDefOrParam(value.instr().getUse(j)), visited);
                if (tref != null)
                    return tref;
            }
            return null;
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

    public boolean in(Framework fw, CallSiteReference site) {
        return in(fw, instrFromSite(site));
    }

    public boolean in(Framework fw, SSAInstruction instr) {
        if (cache.context == null)
            return true;
        if (instr == null || instr.iIndex() < 0)
            return false;
        if (cache.reachingInstrs == null) {
            cache.reachingInstrs = cache.context.calculateReachable(fw, cache.node);
        }
        return cache.reachingInstrs.contains(instr.iIndex());
    }

    public Val getReceiverUseOrDef(SSAInstruction instr, Set<IntPair> visited) {
        IR ir = this.node().getIR();
        Trace.Val v = getReceiverUse(ir.getBasicBlockForInstruction(instr), instr.iIndex(), instr.getUse(0), visited);
        if (v != null)
            return v;
        return getDef(instr.getUse(0));
    }

    public Val getReceiverUse(SSAInstruction instr, Set<IntPair> visited) {
        IR ir = this.node().getIR();
        return getReceiverUse(ir.getBasicBlockForInstruction(instr), instr.iIndex(), instr.getUse(0), visited);
    }

    public Val getReceiverUse(ISSABasicBlock bb, int index, int number, Set<IntPair> visited) {
        IR ir = this.node().getIR();
        int i = bb.getFirstInstructionIndex() <= index && index <= bb.getLastInstructionIndex() ? index - 1
                : bb.getLastInstructionIndex();
        for (; i >= bb.getFirstInstructionIndex(); i--) {
            SSAInstruction s = ir.getInstructions()[i];
            if (s == null)
                continue;
            if (s.hasDef() && s.getDef() == number) {
                if (s instanceof SSAAbstractInvokeInstruction && this.callLog() != null) {
                    SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) ir.getInstructions()[i];
                    if (this.callLog().containsKey(invoke.getCallSite())) {
                        Trace calleeTrace = this.callLog().get(invoke.getCallSite());
                        SSAInstruction[] instrs = calleeTrace.node().getIR().getInstructions();
                        for (int j = instrs.length - 1; j >= 0; j--) {
                            if (instrs[j] == null)
                                continue;
                            if (instrs[j] instanceof SSAReturnInstruction) {
                                return calleeTrace.getReceiverUse(
                                        calleeTrace.node().getIR().getBasicBlockForInstruction(instrs[j]),
                                        instrs[j].iIndex(), instrs[j].getUse(0), visited);
                            }
                        }
                    }
                }
                return null; // def
            }
            if (s instanceof SSAAbstractInvokeInstruction) {
                SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) ir.getInstructions()[i];
                if (!invoke.isStatic() && invoke.getUse(0) == number) {
                    return this.new Val(s);
                }
            }
        }
        for (SSAPhiInstruction phi : (Iterable<SSAPhiInstruction>) () -> bb.iteratePhis()) {
            if (phi.getDef() == number) {
                return null; // def
            }
        }
        if (bb.isEntryBlock()) {
            int ix = 0;
            for (int p : ir.getParameterValueNumbers()) {
                if (p == number)
                    break;
                ix++;
            }
            if (ix < ir.getParameterValueNumbers().length) {
                Trace callerTrace = this.next;
                if (callerTrace != null) {
                    SSAInstruction caller = callerTrace.instrFromSite(callerTrace.site);
                    IR callerIr = callerTrace.node().getIR();
                    return callerTrace.getReceiverUse(callerIr.getBasicBlockForInstruction(caller), caller.iIndex(),
                            caller.getUse(ix), visited);
                }
            }
        }
        Collection<ISSABasicBlock> preds = ir.getControlFlowGraph().getNormalPredecessors(bb);
        for (ISSABasicBlock pred : preds) {
            if (pred.getFirstInstructionIndex() > index)
                continue;
            if (preds.size() > 1) {
                int bbid = pred.getNumber();
                IntPair key = IntPair.make(this.node().getGraphNodeId(), bbid);
                if (visited.contains(key)) {
                    continue;
                }
                visited.add(key);
            }
            Trace.Val v0 = getReceiverUse(pred, index, number, visited);
            if (v0 != null)
                return v0;
        }
        return null;
    }

    public Iterable<Val> receiverUseChain(SSAInstruction instr, int number) {
        IR ir = node().getIR();
        Set<IntPair> visited = new HashSet<>();

        return () -> new Iterator<Val>() {
            Trace.Val use = getReceiverUse(ir.getBasicBlockForInstruction(instr), instr.iIndex(), number, visited);

            @Override
            public boolean hasNext() {
                return use != null && use.isInstr();
            }

            @Override
            public Val next() {
                Val res = use;
                use = use.isInstr() ? use.trace().getReceiverUse(use.instr(), visited) : null;
                return res;
            }
        };
    }

    public static Val reachingValue(Val v, Predicate<Val> test) {
        Set<IntPair> visited = new HashSet<>();
        Stack<Val> todo = new Stack<>();
        todo.add(v);
        while (!todo.isEmpty()) {
            v = todo.pop();
            if (v == null)
                continue;
            if (test.test(v)) {
                return v;
            } else if (v.isInstr() && v.instr() instanceof SSAPhiInstruction
                    || v.instr() instanceof SSACheckCastInstruction) {
                for (int j = 0; j < v.instr().getNumberOfUses(); j++) {
                    IntPair key = IntPair.make(v.trace().node().getGraphNodeId(), v.instr().getUse(j));
                    if (visited.contains(key))
                        continue;
                    visited.add(key);
                    todo.add(v.getDef(v.instr().getUse(j)));
                }
            }
        }
        return null;
    }

    @Override
    public int hashCode() {
        int hash = System.identityHashCode(cache);
        if (site() != null) {
            hash ^= site().hashCode();
        }
        return hash;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || !(o instanceof Trace)) {
            return false;
        }
        Trace other = (Trace) o;
        if (other.cache != this.cache)
            return false;
        if (site == null)
            return other.site == null;
        return this.site.equals(other.site);
    }
}