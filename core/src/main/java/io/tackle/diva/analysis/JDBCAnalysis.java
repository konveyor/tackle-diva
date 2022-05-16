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

package io.tackle.diva.analysis;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Stack;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import java.util.logging.Logger;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.shrikeBT.BinaryOpInstruction;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSABinaryOpInstruction;
import com.ibm.wala.ssa.SSACheckCastInstruction;
import com.ibm.wala.ssa.SSAGetInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSANewInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.ssa.SSAReturnInstruction;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.util.intset.BitVectorIntSet;
import com.ibm.wala.util.intset.IntPair;
import com.ibm.wala.util.intset.IntSet;
import com.ibm.wala.util.intset.MutableIntSet;

import io.tackle.diva.Constants;
import io.tackle.diva.Context;
import io.tackle.diva.Framework;
import io.tackle.diva.Trace;

public class JDBCAnalysis {
    static Logger logger = Logger.getLogger(JDBCAnalysis.class.getName());

    public static boolean checkRelevance(IClass c) {
        return c.getName() == Constants.LJavaSqlConnection;
    }

    public static Context.CallSiteVisitor getTransactionAnalysis(Framework fw, Context context) {
        return context.new CallSiteVisitor() {

            @SuppressWarnings("unused")
            @Override
            public void visitCallSite(Trace trace) {

                CGNode node = trace.node();
                CallSiteReference site = trace.site();
                MethodReference ref = site.getDeclaredTarget();
                Trace.Val sql = null;
                List<Trace.Val> seeds = null;
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
                    if (fw.usageAnalysis) {
                        seeds = new ArrayList<>();
                    }
                    sql = analyzeJdbc(fw, trace, site, seeds);

                } else if (ref.getDeclaringClass().getName() == Constants.LJavaSqlStatement
                        && (ref.getName() == Constants.executeQuery || ref.getName() == Constants.executeUpdate)
                        && ref.getNumberOfParameters() == 1) {
                    SSAInstruction instr = trace.instrFromSite(site);
                    sql = trace.getDef(instr.getUse(1));
                }

                if (sql != null) {
                    if (!fw.txStarted()) {
                        fw.reportSqlStatement(trace, "BEGIN");
                    }
                    IntSet uses = null;
                    if (seeds != null && !seeds.isEmpty()) {
                        uses = getUsingOps(fw, seeds);
                    }
                    analyzeSqlStatement(fw, trace, sql, uses);
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

    public static Trace.Val analyzeJdbc(Framework fw, Trace trace, CallSiteReference site, List<Trace.Val> uses) {
        Trace.Val sql = trace.new Val("??");

        SSAInstruction instr = trace.instrFromSite(site);

        Set<IntPair> visited = new HashSet<>();
        int self = instr.getUse(0);
        Trace.Val v = trace.getReceiverUseOrDef(instr, visited);
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
                    int bbid = vk.trace().node().getIR().getBasicBlockForInstruction(vk.instr()).getNumber();
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

            } else if (instr instanceof SSAReturnInstruction) {
                // NOTE: getReceiverUseOrDef doesn't change trace *unless it returns ret-instr*
                // So if v is invoke-instr with the same self as instr, then its receiver use
                self = instr.getUse(0);
                v = v.getReceiverUseOrDef(visited);
                continue;

            } else if (instr instanceof SSAAbstractInvokeInstruction && instr.getNumberOfUses() > 0
                    && instr.getUse(0) == self) {
                // receiver use
                if (uses != null) {
                    MethodReference mref = ((SSAAbstractInvokeInstruction) instr).getDeclaredTarget();
                    if (mref.getName() == Constants.setInt || mref.getName() == Constants.setString
                            || mref.getName() == Constants.setBigDecimal || mref.getName() == Constants.getFloat
                            || mref.getName() == Constants.getDouble) {
                        Trace.Val d = v.getDef(instr.getUse(2));
                        if (d != null) {
                            uses.add(d);
                        }
                    }
                }
                v = v.getReceiverUseOrDef(visited);
                continue;

            } else if (instr instanceof SSAAbstractInvokeInstruction) {
                // def
                SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) instr;
                MethodReference mref = invoke.getDeclaredTarget();
                if (mref.getDeclaringClass().getName() == Constants.LJavaSqlConnection
                        && (mref.getName() == Constants.prepareStatement || mref.getName() == Constants.prepareCall)) {
                    sql = v.getDef(instr.getUse(1));
                    break;

                }
            }
            break;
        }
        return sql;
    }

    public static void analyzeSqlStatement(Framework fw, Trace trace, Trace.Val v) {
        analyzeSqlStatement(fw, trace, v, null);
    }

    public static void analyzeSqlStatement(Framework fw, Trace trace, Trace.Val v, IntSet uses) {
        if (v.isConstant()) {
            fw.reportSqlStatement(trace, (String) v.constant(), uses);
        } else {
            fw.reportSqlStatement(trace, calculateReachingString(fw, v, new HashSet<>()), uses);
        }
    }

    public static SSAAbstractInvokeInstruction getConstructorForNew(IR ir, SSANewInstruction alloc) {
        for (int i = alloc.iIndex() + 1; i < ir.getInstructions().length; i++) {
            SSAInstruction instr = ir.getInstructions()[i];
            if (instr == null || !(instr instanceof SSAAbstractInvokeInstruction) || instr.getNumberOfUses() == 0
                    || instr.getUse(0) != alloc.getDef())
                continue;
            SSAAbstractInvokeInstruction constr = (SSAAbstractInvokeInstruction) instr;
            if (constr.getDeclaredTarget().getName() != Constants.theInit)
                return null;
            return constr;
        }
        return null;
    }

    public static String calculateReachingString(Framework fw, Trace.Val value, Set<IntPair> visited) {

        if (value == null || value.isParam()) {
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
            int bbid = lhs.trace().node().getIR().getBasicBlockForInstruction(lhs.instr()).getNumber();
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
                    Trace.Val lastVal = value.getReceiverUseOrDef(visited);
                    return calculateReachingString(fw, lastVal, visited);
                } else if (mref.getName() == Constants.append) {
                    Trace.Val lastVal = value.getReceiverUseOrDef(visited);
                    return calculateReachingString(fw, lastVal, visited)
                            + calculateReachingString(fw, value.getDef(instr.getUse(1)), new HashSet<>());
                } else if (mref.getName() == Constants.theInit) {
                    if (mref.getNumberOfParameters() == 0) {
                        return "";
                    } else if (mref.getParameterType(0).isPrimitiveType()) {
                        return "";
                    }
                    return calculateReachingString(fw, value.getDef(instr.getUse(1)), visited);
                }
            }

        } else if (instr instanceof SSANewInstruction) {
            SSANewInstruction alloc = (SSANewInstruction) instr;
            if (alloc.getConcreteType().getName() == Constants.LJavaLangString) {
                SSAAbstractInvokeInstruction constr = getConstructorForNew(value.trace().node().getIR(), alloc);
                if (constr.getNumberOfUses() == 2) {
                    return calculateReachingString(fw, value.trace().getDef(constr.getUse(1)), visited);
                }
            }

        } else if (instr instanceof SSAReturnInstruction) {
            Trace.Val lastVal = value.getReceiverUseOrDef(visited);
            return calculateReachingString(fw, lastVal, visited);
        }

        return "??";
    }

    public static IntSet getUsingOps(Framework fw, List<Trace.Val> seeds) {
        MutableIntSet ops = new BitVectorIntSet();
        getDataflowSources(fw, seeds, (v, h) -> {
            if (!v.isInstr())
                return;
            SSAInstruction instr = v.instr();
            if (instr instanceof SSAAbstractInvokeInstruction) {
                MethodReference mref = ((SSAAbstractInvokeInstruction) instr).getDeclaredTarget();
                if (mref.getDeclaringClass().getName() == Constants.LJavaSqlResultSet
                        && (mref.getName() == Constants.getInt || mref.getName() == Constants.getString
                                || mref.getName() == Constants.getFloat || mref.getName() == Constants.getDouble
                                || mref.getName() == Constants.getBigDecimal)) {
                    Trace.Val query = v.getDef(instr.getUse(0));
                    if (query.isInstr() && query.instr() instanceof SSAAbstractInvokeInstruction) {
                        CallSiteReference site = ((SSAAbstractInvokeInstruction) query.instr()).getCallSite();
                        int op = fw.callSiteToOp.getOrDefault(query.trace().updateSite(site), -1);
                        if (op >= 0) {
                            ops.add(op);
                        }
                    }
                }
            }
        });
        return ops;
    }

    public static void getDataflowSources(Framework fw, List<Trace.Val> seeds,
            BiConsumer<Trace.Val, Consumer<Trace.Val>> cont) {

        Set<IntPair> visited = new HashSet<>();
        Stack<Trace.Val> todo = new Stack<>();
        todo.addAll(seeds);
        final Consumer<Trace.Val> handler = v -> {
            if (v != null && v.isInstr()) {
                IntPair key = IntPair.make(v.trace().node().getGraphNodeId(), v.instr().iIndex());
                if (!visited.contains(key)) {
                    visited.add(key);
                    todo.push(v);
                }
            }
        };

        while (!todo.isEmpty()) {

            Trace.Val v = todo.pop();
            if (v.isConstant()) {
                cont.accept(v, handler);
                continue;
            }

            SSAInstruction instr = v.instr();
            if (instr instanceof SSAGetInstruction) {
                v = PointerAnalysis.fromInits(fw, v.trace(), (SSAGetInstruction) instr);
                handler.accept(v);

            } else if (instr instanceof SSAPhiInstruction) {
                SSAPhiInstruction phi = (SSAPhiInstruction) instr;
                handler.accept(v.getDef(phi.getUse(0)));
                handler.accept(v.getDef(phi.getUse(1)));

            } else if (instr instanceof SSABinaryOpInstruction) {
                handler.accept(v.getDef(instr.getUse(0)));
                handler.accept(v.getDef(instr.getUse(1)));

            } else if (instr instanceof SSACheckCastInstruction) {
                handler.accept(v.getDef(instr.getUse(0)));

            } else if (instr instanceof SSANewInstruction) {
                SSANewInstruction alloc = (SSANewInstruction) instr;

                if (alloc.getConcreteType().getName() == Constants.LJavaLangString
                        || alloc.getConcreteType().getName() == Constants.LJavaLangInteger) {
                    SSAAbstractInvokeInstruction constr = getConstructorForNew(v.trace().node().getIR(), alloc);
                    if (constr.getNumberOfUses() == 2) {
                        handler.accept(v.trace().getDef(constr.getUse(1)));
                    }
                }

            } else if (instr instanceof SSAAbstractInvokeInstruction) {
                MethodReference mref = ((SSAAbstractInvokeInstruction) instr).getDeclaredTarget();

                if (instr.getNumberOfUses() == 1 && (mref.getName() == Constants.toString
                        || mref.getName() == Constants.intValue || mref.getName() == Constants.longValue
                        || mref.getName() == Constants.floatValue || mref.getName() == Constants.doubleValue)) {
                    handler.accept(v.getDef(instr.getUse(0)));
                } else {
                    cont.accept(v, handler);
                }

            } else {
                cont.accept(v, handler);
            }
        }

    }

}
