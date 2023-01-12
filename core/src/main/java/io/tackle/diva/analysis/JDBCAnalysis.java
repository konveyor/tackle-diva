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

import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.logging.Logger;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSACheckCastInstruction;
import com.ibm.wala.ssa.SSAGetInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.util.intset.BitVectorIntSet;
import com.ibm.wala.util.intset.IntPair;
import com.ibm.wala.util.intset.IntSet;
import com.ibm.wala.util.intset.MutableIntSet;

import io.tackle.diva.Constants;
import io.tackle.diva.Context;
import io.tackle.diva.Framework;
import io.tackle.diva.Report;
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
                Map<String, Set<String>> flow = null;
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
                        flow = new LinkedHashMap<>();
                    }
                    sql = analyzeJdbc(fw, trace, site, flow);

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
                    // IntSet uses = null;
                    // if (seeds != null && !seeds.isEmpty()) {
                    // uses = getUsingOps(fw, seeds);
                    // }

                    analyzeSqlStatement(fw, trace, sql, flow);
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

    public static Trace.Val analyzeJdbc(Framework fw, Trace trace, CallSiteReference site,
            Map<String, Set<String>> flow) {
        Trace.Val sql = trace.new Val("??");

        SSAInstruction instr = trace.instrFromSite(site);

        Set<IntPair> visited = new HashSet<>();
        boolean isDef = false;
        Trace.Val v = trace.getReceiverUse(instr, visited);
        if (v == null) {
            isDef = true;
            v = trace.getDef(instr.getUse(0));
        }
        outer: while (true) {
            if (v == null || !v.isInstr())
                break;
            instr = v.instr();

            if (!isDef && instr instanceof SSAAbstractInvokeInstruction) {
                // receiver use
                if (flow != null) {
                    MethodReference mref = ((SSAAbstractInvokeInstruction) instr).getDeclaredTarget();
                    if (mref.getName() == Constants.setInt || mref.getName() == Constants.setString
                            || mref.getName() == Constants.setBigDecimal || mref.getName() == Constants.setFloat
                            || mref.getName() == Constants.setDouble) {
                        Trace.Val d = v.getDef(instr.getUse(2));
                        if (d != null) {
                            Trace.Val k = v.getDef(instr.getUse(1));

                            String key = "arg:" + StringAnalysis.calculateReachingString(fw, k);

                            InfoFlowAnalysis.handleReachingValues(fw, Collections.singletonList(d),
                                    InfoFlowAnalysis.resultSetHandler(fw, key, flow)
                                            .andThen(InfoFlowAnalysis.requestParamHandler(fw, key, flow)));
                        }
                    }
                }
                v = v.getReceiverUse(visited);
                if (v == null) {
                    isDef = true;
                    v = trace.getDef(instr.getUse(0));
                }
                continue;

            } else if (instr instanceof SSAPhiInstruction) {
                IntPair key = null;
                for (int k = 0; k < instr.getNumberOfUses(); k++) {
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

            } else if (instr instanceof SSAAbstractInvokeInstruction) {
                // def
                SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) instr;
                MethodReference mref = invoke.getDeclaredTarget();
                if (mref.getDeclaringClass().getName() == Constants.LJavaSqlConnection
                        && (mref.getName() == Constants.prepareStatement || mref.getName() == Constants.prepareCall)) {
                    sql = v.getDef(instr.getUse(1));
                    break;

                }

                if (!fw.stringDictionary.isEmpty() && instr.getNumberOfUses() == 2
                        && (mref.getDeclaringClass().getName() == Constants.LJavaUtilHashtable
                                || mref.getDeclaringClass().getName() == Constants.LJavaUtilHashMap)
                        && mref.getName() == Constants.get) {

                    // Some framework is doing key-based prepared statement lookup ...
                    String key = StringAnalysis.calculateReachingString(fw, v.getDef(instr.getUse(1)), visited);
                    if (fw.stringDictionary.containsKey(key)) {
                        sql = trace.new Val(fw.stringDictionary.get(key));
                        break;
                    }
                }

            } else if (instr instanceof SSAGetInstruction) {
                // todo: what about uses before setfield?
                v = PointerAnalysis.fromInits(fw, v.trace(), (SSAGetInstruction) instr);
                continue;

            } else if (instr instanceof SSACheckCastInstruction) {
                // todo: what about uses before checkcast?
                isDef = true;
                v = v.getDef(instr.getUse(0));
                continue;

            }
            break;
        }
        return sql;
    }

    public static void analyzeSqlStatement(Framework fw, Trace trace, Trace.Val v) {
        analyzeSqlStatement(fw, trace, v, null);
    }

    public static void analyzeSqlStatement(Framework fw, Trace trace, Trace.Val v, Map<String, Set<String>> flow) {
        String sql = v.isConstant() ? (String) v.constant() : StringAnalysis.calculateReachingString(fw, v);
        if (flow == null) {
            fw.reportSqlStatement(trace, sql);
        } else {
            fw.reportSqlStatement(trace, sql, (map) -> {
                map.put("infoflow", (Report.Named info) -> {
                    for (Map.Entry<String, Set<String>> e : flow.entrySet()) {
                        info.put(e.getKey(), (Report vs) -> {
                            for (String s : e.getValue()) {
                                vs.add(s);
                            }
                        });
                    }
                });
            });
        }
    }

    public static IntSet getUsingOps(Framework fw, List<Trace.Val> seeds) {
        MutableIntSet ops = new BitVectorIntSet();
        InfoFlowAnalysis.handleReachingValues(fw, seeds, (v, h) -> {
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

}
