package io.tackle.diva.analysis;

import java.util.Iterator;

import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ssa.SSAGetInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSAPutInstruction;
import com.ibm.wala.types.FieldReference;

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
        if (!field.isStatic()) {
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
                    fw.traverse(n, (Trace.InstructionVisitor) (Trace t, SSAInstruction instr) -> {
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
        return null;
    }

    public static Trace.Val fromDefUse(Framework fw, Trace.Val def, Trace.Val use, FieldReference fref) {
        Iterator<Trace> ds = Util.makeList(def.trace().reversed()).iterator();
        Trace nca = null;
        for (Trace u : use.trace().reversed()) {
            if (!ds.hasNext())
                break;
            if (u != ds.next())
                break;
            nca = u;
        }
        if (nca == null)
            return null;
        int[] phase = new int[] { 0 };
        try {
            fw.traverse(nca.node(), (Trace.InstructionVisitor) (Trace t, SSAInstruction instr) -> {
                if (phase[0] == 0) {
                    if (instr == def.instr())
                        phase[0]++;
                } else if (phase[0] == 1) {
                    if (instr == use.instr()) {
                        phase[0]++;
                    } else if (instr instanceof SSAPutInstruction) {
                        SSAPutInstruction put = (SSAPutInstruction) instr;
                        if (put.getDeclaredField() == fref) {
                            throw new PointerAnalysis.Escape(t.getDefOrParam(put.getUse(1)));
                        }
                    }
                }
            }, true);
        } catch (PointerAnalysis.Escape e) {
            return e.val;
        }

        return null;
    }

}
