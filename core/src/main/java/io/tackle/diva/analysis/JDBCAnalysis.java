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
                Trace.Val sql = null;
                if (false && ref.getDeclaringClass().getName() == Constants.LJavaSqlConnection) {
                    if (ref.getName() == Constants.prepareStatement || ref.getName() == Constants.prepareCall) {
                        SSAAbstractInvokeInstruction instr = trace.instrFromSite(site);
                        sql = trace.getDef(instr.getUse(1));
                    }
                } else if (ref.getDeclaringClass().getName() == Constants.LJavaSqlPreparedStatement
                        && (ref.getName() == Constants.executeQuery || ref.getName() == Constants.executeUpdate)
                        && ref.getNumberOfParameters() == 0
                        || ref.getDeclaringClass().getName() == Constants.LJavaSqlCallableStatement
                                && ref.getName() == Constants.execute) {

                    sql = analyzeJdbc(fw, trace, site);
                }
                if (sql != null) {
                    if (!fw.txStarted()) {
                        fw.reportSqlStatement(trace, "BEGIN");
                    }
                    analyzeSqlStatement(fw, trace, sql);
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

    public static Trace.Val analyzeJdbc(Framework fw, Trace trace, CallSiteReference site) {
        Trace.Val sql = trace.new Val("??");

        SSAInstruction instr = trace.instrFromSite(site);

        Set<IntPair> visited = new HashSet<>();
        int self = instr.getUse(0);
        Trace.Val v = getReceiverUseOrDef(trace, instr, visited);
        outer: while (true) {
            if (v == null || !v.isInstr())
                break;
            instr = v.instr();
            if (instr instanceof SSAPhiInstruction) {
                IntPair key = null;
                for (int k = 0; k < 2; k++) {
                    Trace.Val vk = v.getDef(instr.getUse(k));
                    if (vk.isConstant())
                        continue;
                    int bbid = v.trace().node().getIR().getBasicBlockForInstruction(vk.instr()).getNumber();
                    key = IntPair.make(v.trace().node().getGraphNodeId(), bbid);
                    if (visited.contains(key)) {
                        continue;
                    } else {
                        visited.add(key);
                        v = vk;
                        continue outer;
                    }
                }

            } else if (instr instanceof SSAGetInstruction) {
                v = PointerAnalysis.fromInits(fw, v.trace(), (SSAGetInstruction) instr);
                continue;

            } else if ((instr instanceof SSAAbstractInvokeInstruction || instr instanceof SSAReturnInstruction)
                    && instr.getNumberOfUses() > 0 && instr.getUse(0) == self) {
                v = getReceiverUseOrDef(v.trace(), instr, visited);
                continue;

            } else if (instr instanceof SSAAbstractInvokeInstruction) {
                SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) instr;
                MethodReference mref = invoke.getDeclaredTarget();
                if (mref.getDeclaringClass().getName() == Constants.LJavaSqlConnection
                        && (mref.getName() == Constants.prepareStatement || mref.getName() == Constants.prepareCall)) {
                    sql = v.getDef(instr.getUse(1));
                    break;

                } else if (!fw.classHierarchy().getPossibleTargets(mref).isEmpty()) {
                    for (IMethod m : fw.classHierarchy().getPossibleTargets(mref)) {
                        CGNode n = fw.callgraph().getNode(m, v.trace().node().getContext());
                        if (n == null)
                            continue;
                        SSAInstruction[] instrs = n.getIR().getInstructions();
                        for (int i = instrs.length - 1; i >= 0; i--) {
                            if (instrs[i] == null)
                                continue;
                            if (instrs[i] instanceof SSAReturnInstruction) {
                                Trace parent = new Trace(v.trace().node(), v.trace().parent());
                                parent.setSite(invoke.getCallSite());
                                v = new Trace(n, parent).new Val(instrs[i]);
                                self = instrs[i].getUse(0);
                                continue outer;
                            }
                        }
                    }
                }
            }
            break;
        }
        return sql;
    }

    public static void analyzeSqlStatement(Framework fw, Trace trace, Trace.Val v) {
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
            if (value.constant() == null)
                return "??";
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
            Trace.Val v = PointerAnalysis.fromInits(fw, value.trace(), (SSAGetInstruction) instr);
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
                    Trace.Val lastVal = getReceiverUseOrDef(value.trace(), instr, visited);
                    return calculateReachingString(fw, lastVal, visited);
                } else if (mref.getName() == Constants.append) {
                    Trace.Val lastVal = getReceiverUseOrDef(value.trace(), instr, visited);
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
                            Trace parent = new Trace(value.trace().node(), value.trace().parent());
                            parent.setSite(((SSAAbstractInvokeInstruction) instr).getCallSite());
                            Trace.Val v = new Trace(n, parent).getDef(((SSAReturnInstruction) instrs[i]).getUse(0));
                            return calculateReachingString(fw, v, visited);
                        }
                    }
                }

            }
        }

        return "??";
    }

    public static Trace.Val getReceiverUseOrDef(Trace trace, SSAInstruction instr, Set<IntPair> visited) {
        IR ir = trace.node().getIR();
        return getReceiverUseOrDef(ir.getBasicBlockForInstruction(instr), trace, instr.iIndex(), instr.getUse(0),
                visited);
    }

    public static Trace.Val getReceiverUseOrDef(ISSABasicBlock bb, Trace trace, int index, int number,
            Set<IntPair> visited) {
        IR ir = trace.node().getIR();
        int i = bb.getFirstInstructionIndex() <= index && index <= bb.getLastInstructionIndex() ? index - 1
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
                if (!invoke.isStatic() && invoke.getUse(0) == number) {
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
            return getReceiverUseOrDef(pred, trace, index, number, visited);
        }
        return null;
    }

    public static void getDataflowForVal(Trace.Val val) {

    }

}
