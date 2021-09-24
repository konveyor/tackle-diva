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

package io.tackle.diva.analysis;

import java.util.HashSet;
import java.util.Set;
import java.util.logging.Logger;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.shrikeBT.BinaryOpInstruction;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.ssa.ISSABasicBlock;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSABinaryOpInstruction;
import com.ibm.wala.ssa.SSAGetInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.ssa.SSAPutInstruction;
import com.ibm.wala.ssa.SSAReturnInstruction;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.util.intset.IntPair;

import io.tackle.diva.Constants;
import io.tackle.diva.Context;
import io.tackle.diva.Framework;
import io.tackle.diva.Trace;

public class JDBCAnalysis {
    static Logger logger = Logger.getLogger(JDBCAnalysis.class.getName());

    public static Context.CallSiteVisitor getTransactionAnalysis(Framework fw, Context context) {
        return context.new CallSiteVisitor() {

            @SuppressWarnings("unused")
            @Override
            public void visitCallSite(Trace trace) {

                CGNode node = trace.node();
                CallSiteReference site = trace.site();
                MethodReference ref = site.getDeclaredTarget();
                int pos = -1;
                if (ref.getDeclaringClass().getName() == Constants.LJavaSqlConnection) {
                    if (ref.getName() == Constants.prepareStatement || ref.getName() == Constants.prepareCall) {
                        pos = 0;
                    } else if (false
                            && (ref.getName() == Constants.executeQuery || ref.getName() == Constants.executeUpdate)
                            && ref.getNumberOfParameters() > 0
                            && ref.getParameterType(0).getName() == Constants.LJavaLangString) {
                        pos = 0;
                    }
                }
                if (pos >= 0) {
                    if (!fw.txStarted()) {
                        fw.reportSqlStatement(trace, "BEGIN");
                    }
                    analyzeSqlStatement(fw, trace, site, pos);
                }

                if (fw.txStarted() && ref.getDeclaringClass().getName() == Constants.LJavaSqlConnection) {
                    if (ref.getName() == Constants.commit) {
                        fw.reportSqlStatement(trace, "COMMIT");
                        fw.reportTxBoundary();
                    } else if (ref.getName() == Constants.rollback) {
                        fw.reportSqlStatement(trace, "ROLLBACK");
                        fw.reportTxBoundary();
                    }
                }
            }

        };
    }

    public static void analyzeSqlStatement(Framework fw, Trace trace, CallSiteReference site, int pos) {
        SSAAbstractInvokeInstruction instr = trace.instrFromSite(site);
        Trace.Val v = trace.getDef(instr.getUse(pos + 1));
        if (v.isConstant()) {
            fw.reportSqlStatement(trace, (String) v.constant());
        } else {
            fw.reportSqlStatement(trace, calculateReachingString(fw, v, new HashSet<>()));
        }
    }

    public static String calculateReachingString(Framework fw, Trace.Val value, Set<IntPair> visited) {

        if (value == null) {
            return "??";
        }

        if (value.isConstant()) {
            return value.constant().toString();
        }

        SSAInstruction instr = value.instr();

        if (instr instanceof SSABinaryOpInstruction) {
            SSABinaryOpInstruction bin = (SSABinaryOpInstruction) instr;
            if (bin.getOperator() == BinaryOpInstruction.Operator.ADD) {
                return calculateReachingString(fw, value.getDef(bin.getUse(0)), visited)
                        + calculateReachingString(fw, value.getDef(bin.getUse(1)), new HashSet<>());
            }

        } else if (instr instanceof SSAGetInstruction) {
            Trace.Val v = pointerAnalysis(fw, value.trace(), (SSAGetInstruction) instr);
            if (v != null) {
                return calculateReachingString(fw, v, visited);
            }

        } else if (instr instanceof SSAPhiInstruction) {
            SSAPhiInstruction phi = (SSAPhiInstruction) instr;
            Trace.Val lhs = value.getDef(phi.getUse(0));
            Trace.Val rhs = value.getDef(phi.getUse(1));

            if (lhs.isConstant()) {
                return calculateReachingString(fw, lhs, visited);
            } else if (rhs.isConstant()) {
                return calculateReachingString(fw, rhs, visited);
            }
            IR ir = value.trace().node().getIR();
            int bbid = ir.getBasicBlockForInstruction(lhs.instr()).getNumber();
            IntPair key = IntPair.make(value.trace().node().getGraphNodeId(), bbid);
            if (visited.contains(key)) {
                return calculateReachingString(fw, rhs, visited);
            }
            visited.add(key);
            return calculateReachingString(fw, lhs, visited);

        } else if (instr instanceof SSAAbstractInvokeInstruction) {
            MethodReference mref = ((SSAAbstractInvokeInstruction) instr).getDeclaredTarget();
            if (mref.getDeclaringClass().getName() == Constants.LJavaLangStringBuffer
                    || mref.getDeclaringClass().getName() == Constants.LJavaLangStringBuilder) {

                if (mref.getName() == Constants.toString) {
                    IR ir = value.trace().node().getIR();
                    Trace.Val lastVal = getReceiverUseOrDef(ir.getBasicBlockForInstruction(instr), value.trace(), instr,
                            instr.getUse(0), visited);
                    return calculateReachingString(fw, lastVal, visited);
                } else if (mref.getName() == Constants.append) {
                    IR ir = value.trace().node().getIR();
                    Trace.Val lastVal = getReceiverUseOrDef(ir.getBasicBlockForInstruction(instr), value.trace(), instr,
                            instr.getUse(0), visited);
                    return calculateReachingString(fw, lastVal, visited)
                            + calculateReachingString(fw, value.getDef(instr.getUse(1)), new HashSet<>());
                } else if (mref.getName() == Constants.theInit) {
                    if (mref.getNumberOfParameters() == 0) {
                        return "";
                    }
                    return calculateReachingString(fw, value.getDef(instr.getUse(1)), visited);
                }

            } else if (!fw.classHierarchy().getPossibleTargets(mref).isEmpty()) {
                for (IMethod m : fw.classHierarchy().getPossibleTargets(mref)) {
                    CGNode n = fw.callgraph().getNode(m, value.trace().node().getContext());
                    if (n == null)
                        continue;
                    SSAInstruction[] instrs = n.getIR().getInstructions();
                    for (int i = instrs.length - 1; i >= 0; i--) {
                        if (instrs[i] == null)
                            continue;
                        if (instrs[i] instanceof SSAReturnInstruction) {
                            Trace.Val v = new Trace(n, value.trace())
                                    .getDef(((SSAReturnInstruction) instrs[i]).getUse(0));
                            return calculateReachingString(fw, v, visited);
                        }
                    }
                }

            }
        }

        return "??";
    }

    public static Trace.Val getReceiverUseOrDef(ISSABasicBlock bb, Trace trace, SSAInstruction instr, int number,
            Set<IntPair> visited) {
        IR ir = trace.node().getIR();
        int i = bb.getFirstInstructionIndex() <= instr.iIndex() && instr.iIndex() <= bb.getLastInstructionIndex()
                ? instr.iIndex() - 1
                : bb.getLastInstructionIndex();
        for (; i >= bb.getFirstInstructionIndex(); i--) {
            SSAInstruction s = ir.getInstructions()[i];
            if (s == null)
                continue;
            if (s.hasDef() && s.getDef() == number) {
                return trace.new Val(s);
            }
            if (s instanceof SSAAbstractInvokeInstruction) {
                SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) ir.getInstructions()[i];
                if (invoke.getUse(0) == number) {
                    return trace.new Val(s);
                }
            }
        }
        for (SSAPhiInstruction phi : (Iterable<SSAPhiInstruction>) () -> bb.iteratePhis()) {
            if (phi.getDef() == number) {
                return trace.new Val(phi);
            }
        }
        for (ISSABasicBlock pred : ir.getControlFlowGraph().getNormalPredecessors(bb)) {
            int bbid = pred.getNumber();
            IntPair key = IntPair.make(trace.node().getGraphNodeId(), bbid);
            if (visited.contains(key)) {
                continue;
            }
            visited.add(key);
            return getReceiverUseOrDef(pred, trace, instr, number, visited);
        }
        return null;
    }

    public static class Escape extends RuntimeException {
        public Trace.Val val;

        public Escape(Trace.Val value) {
            this.val = value;
        }
    }

    public static Trace.Val pointerAnalysis(Framework fw, Trace trace, SSAGetInstruction field) {
        if (!field.isStatic()) {
            IClass c = trace.inferType(fw, field.getUse(0));
            if (c == null)
                return null;
            for (CGNode n : fw.callgraph()) {
                if (n.getMethod().getDeclaringClass() != c || !n.getMethod().isInit())
                    continue;
                try {
                    fw.traverse(n, (Trace.NodeVisitor) (Trace t) -> {
                        for (SSAInstruction instr : t.node().getIR().getInstructions()) {
                            if (instr == null || !(instr instanceof SSAPutInstruction))
                                continue;
                            SSAPutInstruction put = (SSAPutInstruction) instr;
                            if (put.getDeclaredField() == field.getDeclaredField()) {
                                throw new Escape(t.getDef(put.getUse(1)));
                            }
                        }
                    }, true);
                } catch (Escape e) {
                    return e.val;
                }
            }
        }
        return null;
    }

}
