package io.tackle.diva.analysis;

import java.util.Iterator;
import java.util.function.BiConsumer;

import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ssa.SSAGetInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSANewInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.ssa.SSAPutInstruction;
import com.ibm.wala.types.TypeReference;

import io.tackle.diva.Framework;
import io.tackle.diva.Trace;
import io.tackle.diva.Util;

public class PointerAnalysis {

    public static class Escape extends RuntimeException {
        public Trace.Val val;

        public Escape(Trace.Val value) {
            this.val = value;
        }
    }

    public static Trace.Val fromInits(Framework fw, Trace trace, SSAGetInstruction field) {
        return fromInits(fw, trace, field, true);
    }

    public static Trace.Val fromInits(Framework fw, Trace trace, SSAGetInstruction field, boolean nonnull) {
        if (!field.isStatic()) {
            Trace.Val v = trace.getDef(field.getUse(0));
            if (v.isInstr() && v.instr() instanceof SSAPhiInstruction) {
                Trace.Val v0 = v.getDef(v.instr().getUse(0));
                if (v0.isInstr() && v0.instr() instanceof SSANewInstruction) {
                    v = v0;
                } else {
                    v = v.getDef(v.instr().getUse(1));
                }
            }
            if (v.isInstr() && v.instr() instanceof SSANewInstruction) {
                try {
                    fromDefUse(fw, v, trace.new Val(field), (t, put) -> {
                        if (put.getDeclaredField() == field.getDeclaredField()) {
                            Trace.Val v0 = t.getDef(put.getUse(1));
                            if (v0 != null && (!nonnull || !v0.isConstant() || v0.constant() != null))
                                throw new Escape(v0);
                        }
                    });
                } catch (PointerAnalysis.Escape e) {
                    return e.val;
                }
            } else {
                IClass c = trace.inferType(fw, field.getUse(0));
                if (c == null)
                    return null;
                for (CGNode n : fw.callgraph()) {
                    if (!n.getMethod().isInit())
                        continue;
                    if (c.isInterface()) {
                        if (Util.all(n.getMethod().getDeclaringClass().getAllImplementedInterfaces(), i -> i != c))
                            continue;
                    } else if (Util.all(Util.superChain(n.getMethod().getDeclaringClass()), p -> p != c)) {
                        continue;
                    }
                    try {
                        fw.traverse(new Trace(n, null), (Trace.InstructionVisitor) (Trace t, SSAInstruction instr) -> {
                            if (!(instr instanceof SSAPutInstruction))
                                return;
                            SSAPutInstruction put = (SSAPutInstruction) instr;
                            if (put.getDeclaredField() == field.getDeclaredField()) {
                                throw new PointerAnalysis.Escape(t.getDefOrParam(put.getUse(1)));
                            }
                        }, true);
                    } catch (PointerAnalysis.Escape e) {
                        return e.val;
                    }
                }
            }
        } else {
            TypeReference tref = field.getDeclaredField().getDeclaringClass();
            IClass c = fw.classHierarchy().lookupClass(tref);
            if (c == null)
                return null;

            IMethod m = c.getClassInitializer();
            Iterator<CGNode> ns = fw.callgraph().getNodes(m.getReference()).iterator();
            if (!ns.hasNext())
                return null;
            try {
                fw.traverse(new Trace(ns.next(), null), (Trace.InstructionVisitor) (Trace t, SSAInstruction instr) -> {
                    if (!(instr instanceof SSAPutInstruction))
                        return;
                    SSAPutInstruction put = (SSAPutInstruction) instr;
                    if (put.getDeclaredField() == field.getDeclaredField()) {
                        throw new PointerAnalysis.Escape(t.getDefOrParam(put.getUse(0)));
                    }
                }, true);
            } catch (PointerAnalysis.Escape e) {
                return e.val;
            }
        }
        return null;
    }

    public static void fromDefUse(Framework fw, Trace.Val def, Trace.Val use,
            BiConsumer<Trace, SSAPutInstruction> cont) {
        Iterator<Trace> ds = Util.makeList(def.trace().reversed()).iterator();
        Trace nca = null;
        for (Trace u : Util.makeList(use.trace().reversed())) {
            if (!ds.hasNext())
                break;
            if (u != ds.next())
                break;
            nca = u;
        }
        if (nca == null)
            return;
        int[] phase = new int[] { 0 };
        fw.traverse(nca, (nca.context().new InstructionVisitor() {

            @Override
            public void visitInstruction(Trace trace, SSAInstruction instr) {
                if (phase[0] == 0) {
                    if (instr == def.instr())
                        phase[0]++;
                } else if (phase[0] == 1) {
                    if (instr == use.instr()) {
                        phase[0]++;
                    } else if (instr instanceof SSAPutInstruction) {
                        SSAPutInstruction put = (SSAPutInstruction) instr;
                        cont.accept(trace, put);
                    }
                }
            }
        }), true);
    }

}
