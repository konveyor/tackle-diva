package io.tackle.diva;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.callgraph.CallGraph;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSAConditionalBranchInstruction;
import com.ibm.wala.ssa.SSAGotoInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSASwitchInstruction;
import com.ibm.wala.util.intset.BitVector;
import com.ibm.wala.util.intset.IntPair;
import com.ibm.wala.util.strings.StringStuff;

public interface Constraint {

    public abstract class BranchingConstraint implements Constraint {
        Framework fw;

        protected BranchingConstraint(Framework fw) {
            this.fw = fw;
        }

        public abstract Set<IntPair> fallenThruBranches();

        public abstract Set<IntPair> takenBranches();

        public abstract BranchingConstraint defaultConstraint();

        public Map<Integer, BitVector> reachingInstrs;

        public Map<Integer, BitVector> reachingInstrs() {
            if (reachingInstrs != null) {
                return reachingInstrs;
            }

            reachingInstrs = new HashMap<>();
            CallGraph cg = fw.callgraph();
            Set<IntPair> fallenThru = fallenThruBranches();
            Set<IntPair> taken = takenBranches();

            Set<CGNode> nodes = new HashSet<>();
            for (IntPair key : fallenThru) {
                nodes.add(cg.getNode(key.getX()));
            }
            for (IntPair key : taken) {
                nodes.add(cg.getNode(key.getX()));
            }

            for (CGNode n : nodes) {
                BitVector visited = new BitVector();
                BitVector todo = new BitVector();

                IR ir = n.getIR();
                int i = 0;

                todo.set(i);

                while (!todo.isZero()) {
                    i = todo.nextSetBit(0);
                    todo.clear(i);
                    visited.set(i);
                    if (i >= ir.getInstructions().length)
                        continue;
                    SSAInstruction instr = ir.getInstructions()[i];

                    if (instr instanceof SSAConditionalBranchInstruction) {
                        IntPair key = IntPair.make(n.getGraphNodeId(), i);
                        if (!fallenThru.contains(key)) {
                            SSAConditionalBranchInstruction c = (SSAConditionalBranchInstruction) instr;
                            if (c.getTarget() >= 0 && !visited.contains(c.getTarget())) {
                                todo.set(c.getTarget());
                            }
                        }
                        if (taken.contains(key)) {
                            continue;
                        }
                    } else if (instr instanceof SSASwitchInstruction) {
                        SSASwitchInstruction c = (SSASwitchInstruction) instr;
                        for (int l : c.getCasesAndLabels()) {
                            int j = c.getTarget(l);
                            if (!visited.contains(j)) {
                                todo.set(j);
                            }
                        }
                        if (!visited.contains(c.getDefault())) {
                            todo.set(c.getDefault());
                        }
                    } else if (instr instanceof SSAGotoInstruction) {
                        SSAGotoInstruction c = (SSAGotoInstruction) instr;
                        if (c.getTarget() >= 0 && !visited.contains(c.getTarget())) {
                            todo.set(c.getTarget());
                        }
                    }
                    if (instr == null || instr.isFallThrough()) {

                        if (!visited.contains(i + 1)) {
                            todo.set(i + 1);
                        }
                    }
                }
                reachingInstrs.put(n.getGraphNodeId(), visited);
            }
            return reachingInstrs;
        }

        @Override
        public boolean forbids(Constraint other) {
            if (this.category().equals(other.category()) && this.type().equals(other.type())) {
                return true;
            }

            if (other instanceof BranchingConstraint) {
                if (this.type().compareTo(other.type()) > 0) {
                    return false;
                }
                return !this.covers((BranchingConstraint) other) && !((BranchingConstraint) other).covers(this);

            } else if (other instanceof EntryConstraint) {
                CGNode m = ((EntryConstraint) other).node();
                return !Util.any(reachingInstrs().keySet(), k -> fw.isReachable(m, fw.callgraph().getNode(k)));
            }

            return false;
        }

        public boolean covers(BranchingConstraint that) {
            for (Map.Entry<Integer, BitVector> e : reachingInstrs().entrySet()) {
                CGNode n = fw.callgraph().getNode(e.getKey());
                IR ir = n.getIR();
                SSAInstruction[] instrs = ir.getInstructions();
                BitVector thatReachingInstrs = that.reachingInstrs().getOrDefault(e.getKey(), null);
                BitVector defaultReachingInstrs = defaultConstraint().reachingInstrs().getOrDefault(e.getKey(), null);
                Set<IntPair> thatBranches = that.fallenThruBranches();
                for (int i = 0; i < instrs.length; i++) {
                    if (!(instrs[i] instanceof SSAAbstractInvokeInstruction))
                        continue;
                    if (!e.getValue().contains(i))
                        continue;
                    CallSiteReference site = ((SSAAbstractInvokeInstruction) instrs[i]).getCallSite();
                    String klazz = site.getDeclaredTarget().getDeclaringClass().getName().toString();
                    if (klazz.startsWith("Ljava/") || klazz.startsWith("Ljavax/")) {
                        continue;
                    }

                    if (thatReachingInstrs != null && !thatReachingInstrs.contains(i))
                        return true;
                    if (defaultReachingInstrs != null && defaultReachingInstrs.contains(i))
                        continue;

                    for (CGNode m : fw.callgraph.getPossibleTargets(n, site)) {
                        if (Util.any(thatBranches, p -> fw.isReachable(m, fw.callgraph().getNode(p.getX())))) {
                            return true;
                        }
                    }
                }
            }
            return false;
        }

        public boolean isRelevant() {
            for (Map.Entry<Integer, BitVector> e : reachingInstrs().entrySet()) {
                CGNode n = fw.callgraph().getNode(e.getKey());
                if (fw.relevance.contains(n.getGraphNodeId()))
                    return true;
                IR ir = n.getIR();
                SSAInstruction[] instrs = ir.getInstructions();
                BitVector defaultReachingInstrs = defaultConstraint().reachingInstrs().getOrDefault(e.getKey(), null);
                for (int i = 0; i < instrs.length; i++) {
                    if (!(instrs[i] instanceof SSAAbstractInvokeInstruction))
                        continue;
                    if (!e.getValue().contains(i))
                        continue;
                    CallSiteReference site = ((SSAAbstractInvokeInstruction) instrs[i]).getCallSite();
                    String klazz = site.getDeclaredTarget().getDeclaringClass().getName().toString();
                    if (klazz.startsWith("Ljava/") || klazz.startsWith("Ljavax/")) {
                        continue;
                    }

                    if (defaultReachingInstrs != null && defaultReachingInstrs.contains(i))
                        continue;

                    for (CGNode m : fw.callgraph.getPossibleTargets(n, site)) {
                        if (fw.isRelevant(m))
                            return true;
                    }
                }
            }
            return false;
        }
    }

    class EntryConstraint implements Constraint {

        public EntryConstraint(CGNode node) {
            super();
            this.node = node;
        }

        CGNode node;

        @Override
        public String category() {
            return Report.ENTRY;
        }

        @Override
        public String type() {
            return Report.METHODS;
        }

        @Override
        public String value() {
            IMethod method = node.getMethod();
            return StringStuff.jvmToBinaryName(method.getDeclaringClass().getName().toString()) + "."
                    + method.getName().toString();
        }

        public CGNode node() {
            return node;
        }

        @Override
        public boolean forbids(Constraint other) {
            return other instanceof EntryConstraint;
        }
    }

    class DispatchConstraint implements Constraint {

        IClass base;
        IClass impl;

        public DispatchConstraint(IClass base, IClass impl) {
            this.base = base;
            this.impl = impl;
        }

        @Override
        public String category() {
            return Report.DISPATCH;
        }

        @Override
        public String type() {
            return base.getName().toString();
        }

        @Override
        public String value() {
            return impl.getName().toString();
        }

        @Override
        public boolean forbids(Constraint other) {
            return false;
        }
    }

    default public void report(Report.Named report) {
        report.put(category(), (Report.Named map) -> {
            map.put(type(), (Report values) -> {
                values.add(value());
            });
        });
    }

    public String category();

    public String type();

    public String value();

    public boolean forbids(Constraint other);
}