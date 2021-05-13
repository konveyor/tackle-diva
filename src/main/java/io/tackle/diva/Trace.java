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

import com.ibm.wala.cast.java.ipa.callgraph.JavaSourceAnalysisScope;
import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.ssa.ISSABasicBlock;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.ssa.SymbolTable;
import com.ibm.wala.util.intset.BitVector;

public class Trace extends Util.Chain<Trace> {

    public interface Visitor {
        void visitCallSite(Trace trace);

        void visitNode(Trace trace);

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
            };
        }
    }

    @FunctionalInterface
    public interface CallSiteVisitor extends Visitor {
        @Override
        default void visitNode(Trace trace) {
        }
    }

    @FunctionalInterface
    public interface NodeVisitor extends Visitor {
        @Override
        default void visitCallSite(Trace trace) {
        }
    }

    CGNode node;
    CallSiteReference site;

    public CGNode node() {
        return node;
    }

    public Trace parent() {
        return next;
    }

    public CallSiteReference site() {
        return site;
    }

    public void setSite(CallSiteReference site) {
        this.site = site;
    }

    public void setContext(Context context) {
        this.context = context;
    }

    public Trace(CGNode node, Trace parent) {
        super(parent);
        this.node = node;
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
            return !(content instanceof SSAInstruction);
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
    }

    Context context;
    BitVector reachingInstrs = null;
    Object[] ud = null;

    public void populateUd() {
        IR ir = node.getIR();
        if (ir == null) {
            return;
        }
        ud = new Object[ir.getSymbolTable().getMaxValueNumber() + 1];
        SSAInstruction[] instrs = ir.getInstructions();
        for (SSAInstruction instr : instrs) {
            if (instr != null && instr.hasDef()) {
                ud[instr.getDef(0)] = instr;
            }
        }
        for (ISSABasicBlock bb : (Iterable<ISSABasicBlock>) () -> ir.getBlocks()) {
            for (SSAPhiInstruction phi : (Iterable<SSAPhiInstruction>) () -> bb.iteratePhis()) {
                ud[phi.getDef()] = phi;
            }
        }
        int param = 0;
        for (int i : ir.getParameterValueNumbers()) {
            ud[i] = param++;
        }
    }

    public Val getDef(int number) {
        IR ir = node.getIR();
        if (ir == null) {
            return null;
        }
        SymbolTable sym = ir.getSymbolTable();
        if (sym.isConstant(number)) {
            return new Val(sym.getConstantValue(number));
        }
        if (ud == null) {
            populateUd();
        }
        if (ud[number] instanceof SSAInstruction) {
            return new Val(ud[number]);
        }
        if (ud[number] instanceof Integer) {
            // interprocedural resolution of call parameters
            Trace callerTrace = this.next;
            if (callerTrace != null) {
                SSAInstruction caller = callerTrace.instrFromSite(callerTrace.site);
                return callerTrace.getDef(caller.getUse((Integer) ud[number]));
            }
        }
        return null;
    }

    public SSAAbstractInvokeInstruction instrFromSite(CallSiteReference site) {
        if (node.getMethod().getDeclaringClass().getClassLoader().getReference() == JavaSourceAnalysisScope.SOURCE) {
            return (SSAAbstractInvokeInstruction) node.getIR().getInstructions()[site.getProgramCounter()];
        }
        for (SSAInstruction i : node.getIR().getInstructions()) {
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
        if (context == null)
            return true;
        if (reachingInstrs == null) {
            reachingInstrs = context.calculateReachable(node);
        }
        return reachingInstrs.contains(instrFromSite(site).iIndex());
    }

}