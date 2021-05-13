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

import java.util.logging.Logger;
import java.util.regex.Pattern;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.types.MethodReference;

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
            fw.reportSqlStatement(trace, "??");
        }
    }

//
//    public static void analyzeMethod(Framework fw, CGNode n, Function<MethodReference, Integer> filter) {
//        IMethod m = n.getMethod();
//        String className = m.getDeclaringClass().getName().toString();
//        String label = className + "." + m.getName().toString();
//
//        for (CallSiteReference site : (Iterable<CallSiteReference>) () -> n.iterateCallSites()) {
//            int pos = filter.apply(site.getDeclaredTarget());
//            if (pos < 0)
//                continue;
//            SSAAbstractInvokeInstruction instr = (SSAAbstractInvokeInstruction) n.getIR().getInstructions()[site
//                    .getProgramCounter()];
//
//            Value v = n.getIR().getSymbolTable().getValue(instr.getUse(pos + 1));
//
//
//
//            // System.out.println(m.getName() + "(" + site.getProgramCounter() + ")" + "->"
//            // + v);
//        }
//
//    }
//        SimpleLocalDefs udChain = null;
//        List<Unit> origUnits = new ArrayList<>(m.retrieveActiveBody().getUnits());
//        for (Unit u : origUnits) {
//            // String us = u.toString();
//            // System.out.println("------------------------");
//            // System.out.println(us);
//            // System.out.println(u.getUseBoxes());
//            // for (ValueBox box : u.getUseBoxes()) {
//            // System.out.println(box.getValue() + "***" + box.getValue().getType() + "***"
//            // + box.getClass());
//            // }
//
//            InvokeExpr expr = Util.getUnitExpr(u);
//            if (expr == null)
//                continue;
//            int pos = filter.apply(expr.getMethodRef());
//            if (pos >= 0) {
//                Value value = expr.getArg(pos);
//                List<String> sqls = null;
//                if (value instanceof StringConstant) {
//                    sqls = Arrays.asList(((StringConstant) value).value.toUpperCase());
//                } else if (value instanceof FieldRef) {
//                    if (pointsToClass != m.getDeclaringClass()) {
//                        pointsToClass = m.getDeclaringClass();
//                        pointsToCache = null;
//                        pointsToCache = pointsToAnalysis(m.getDeclaringClass());
//                    }
//                    if (pointsToCache != null && pointsToCache.containsKey(((FieldRef) value).getField())) {
//                        sqls = pointsToCache.get(((FieldRef) value).getField());
//                    }
//                } else if (value instanceof Local || value instanceof InvokeExpr) {
//                    if (udChain == null) {
//                        udChain = adaptUdChainForStringAppends(m, origUnits);
//                    }
//                    sqls = calculateReachingStrings(u, value, m, udChain, new Stack<Unit>());
//                }
//                if (sqls != null) {
//                    String[] errMsg = new String[] { null };
//                    int[] success = new int[] { 0 };
//                    for (String sql : sqls) {
//                        extractCrudFromSql(sql.toUpperCase(), m, u, e -> {
//                            errMsg[0] = e;
//                            success[0] = success[0] > 0 ? 1 : -1;
//                        });
//                        success[0] = success[0] >= 0 ? 1 : 0;
//                    }
//                    if (success[0] <= 0 && errMsg[0] != null) {
//                        logger.config(errMsg[0]);
//                    }
//                }
//            }
//        }
//    }
//
//    static SimpleLocalDefs adaptUdChainForStringAppends(SootMethod m, List<Unit> origUnits) {
//        UnitPatchingChain units = m.getActiveBody().getUnits();
//        for (Unit u : origUnits) {
//            if (u instanceof InvokeStmt) {
//                InvokeExpr expr = Util.getUnitExpr(u);
//                if ((expr.getMethod().getDeclaringClass().getName().equals("java.lang.StringBuffer")
//                        || expr.getMethod().getDeclaringClass().getName().equals("java.lang.StringBuilder"))
//                        && expr.getMethod().getName().equals("append")) {
//                    Unit v = new JAssignStmt(((VirtualInvokeExpr) expr).getBase(), expr);
//                    units.swapWith(u, v);
//                    // System.out.println(v.getDefBoxes());
//                }
//            }
//        }
//        return new SimpleLocalDefs(new BriefUnitGraph(m.getActiveBody()));
//    }
//
//    static List<String> calculateReachingStrings(Unit unit, Value value, SootMethod m, SimpleLocalDefs udChain,
//            Stack<Unit> visited) {
//        List<String> res = new ArrayList<>();
//        if (value instanceof StringConstant) {
//            res.add(((StringConstant) value).value);
//            return res;
//        }
//
//        if (value instanceof FieldRef) {
//            if (pointsToClass != m.getDeclaringClass()) {
//                pointsToClass = m.getDeclaringClass();
//                pointsToCache = null;
//                pointsToCache = pointsToAnalysis(m.getDeclaringClass());
//            }
//            if (pointsToCache != null && pointsToCache.containsKey(((FieldRef) value).getField())) {
//                res.addAll(pointsToCache.get(((FieldRef) value).getField()));
//                return res;
//            }
//        }
//
//        if (value instanceof InstanceInvokeExpr) {
//            if (visited.contains(unit)) {
//                return res;
//            }
//            InstanceInvokeExpr expr = (InstanceInvokeExpr) value;
//            if (expr.getMethod().getName().equals("toString")) {
//                visited.push(unit);
//                res.addAll(calculateReachingStrings(unit, expr.getBase(), m, udChain, visited));
//                visited.pop();
//                return res;
//            }
//            if ((expr.getMethod().getDeclaringClass().getName().equals("java.lang.StringBuffer")
//                    || expr.getMethod().getDeclaringClass().getName().equals("java.lang.StringBuilder"))
//                    && expr.getMethod().getName().equals("append")) {
//                visited.push(unit);
//                for (String s : calculateReachingStrings(unit, expr.getArg(0), m, udChain, visited)) {
//                    for (String t : calculateReachingStrings(unit, expr.getBase(), m, udChain, visited)) {
//                        res.add(t + s);
//                    }
//                }
//                visited.pop();
//                return res;
//            }
//        }
//
//        if (value instanceof NewExpr) {
//            if (((NewExpr) value).getType().toString().equals("java.lang.StringBuffer")
//                    || ((NewExpr) value).getType().toString().equals("java.lang.StringBuilder")) {
//                InvokeExpr expr;
//                Value lvalue = Util.getUnitLValue(unit);
//                while (true) {
//                    unit = m.getActiveBody().getUnits().getSuccOf(unit);
//                    expr = Util.getUnitExpr(unit);
//                    if (expr != null && expr.getMethod().getName().equals("<init>")
//                            && ((SpecialInvokeExpr) expr).getBase().equals(lvalue))
//                        break;
//                }
//                if (expr.getArgCount() == 0) {
//                    res.add("");
//                    return res;
//                } else {
//                    res.addAll(calculateReachingStrings(unit, expr.getArg(0), m, udChain, visited));
//                    return res;
//                }
//            }
//        }
//
//        if (value instanceof Local) {
//            List<Unit> defs = udChain.getDefsOfAt((Local) value, unit);
//            for (Unit u : defs) {
//                res.addAll(calculateReachingStrings(u, Util.getUnitValue(u), m, udChain, visited));
//            }
//            return res;
//        }
//
//        res.add(" ? ");
//        return res;
//    }
//
//    static void extractCrudFromSql(String sql, SootMethod m, Unit unit, Consumer<String> errorLog) {
//
//        Matcher mc = p_braces.matcher(sql);
//        if (mc.find()) {
//            sql = mc.group(1);
//        }
//
//        if (Code2CRUD.usePegParserForSQL) {
//
//            sql = sql.toLowerCase();
//
//            if (Code2CRUD.skipSQLCrudAnalysis) {
//                Code2CRUD.updateSqlElements(m, unit, sql);
//                return;
//            }
//
//            if (SqlStringAnalysis.p_call.matcher(sql).find()) {
//                Code2CRUD.updateSqlElements(m, unit, sql);
//                return;
//            }
//
//            Result stmt = SqlParse.sqlexp.eval(sql, 0);
//            if (stmt == null) {
//                errorLog.accept(sql + "@" + m.getDeclaringClass() + "." + m.getName() + "=> fail");
//                return;
//            } else if (SqlParse.token(sql, stmt.cursor) != null) {
//                errorLog.accept(
//                        sql + "@" + m.getDeclaringClass() + "." + m.getName() + "=>" + sql.substring(stmt.cursor));
//                return;
//            }
//
//            Stack<List<Object>> todo = new Stack<>();
//            todo.add(stmt);
//
//            while (!todo.isEmpty()) {
//                List<Object> next = todo.pop();
//                List<String> tableNames = new ArrayList<>();
//                String op = "R";
//                for (Object t : next) {
//                    if (t instanceof String) {
//                        String op0 = t.equals("select") ? "R"
//                                : t.equals("update") ? "U" : t.equals("insert") ? "C" : t.equals("delete") ? "D" : null;
//                        if (op0 != null) {
//                            op = op0;
//                        } else {
//                            tableNames.add((String) t);
//                        }
//                    } else if (t instanceof List) {
//                        todo.add((List<Object>) t);
//                    }
//                    for (String tableName : tableNames) {
//                        Code2CRUD.updateCrudElements(m, unit, Code2CRUD.DBTABLE, tableName.toUpperCase(), op);
//                        // System.out.println(" " + tableName.toUpperCase() + "(" + op + ")");
//                    }
//                }
//
//            }
//
//        } else {
//
//            sql = sql.replace("*=", " = ");
//            sql = sql.replace("=*", " = ");
//            Statement stmt = null;
//            try {
//                stmt = CCJSqlParserUtil.parse(sql);
//            } catch (JSQLParserException e) {
//                errorLog.accept(sql + "@" + m.getDeclaringClass() + "." + m.getName() + "=>" + e.getCause());
//                return;
//            }
//
//            if (SqlStringAnalysis.p_call.matcher(sql).find()) {
//
//                Code2CRUD.updateSqlElements(m, unit, sql);
//
//            } else {
//
//                if (SqlStringAnalysis.p_insert.matcher(sql).find()) {
//                    Table table = ((Insert) stmt).getTable();
//                    Code2CRUD.updateCrudElements(m, unit, Code2CRUD.DBTABLE, table.toString(), "C");
//                    // System.out.println(" " + table + "(C)");
//                } else if (SqlStringAnalysis.p_update.matcher(sql).find()) {
//                    Table table = ((Update) stmt).getTable();
//                    Code2CRUD.updateCrudElements(m, unit, Code2CRUD.DBTABLE, table.toString(), "U");
//                    // System.out.println(" " + table + "(U)");
//                } else if (SqlStringAnalysis.p_delete.matcher(sql).find()) {
//                    Table table = ((Delete) stmt).getTable();
//                    Code2CRUD.updateCrudElements(m, unit, Code2CRUD.DBTABLE, table.toString(), "D");
//                    // System.out.println(" " + table + "(D)");
//                }
//
//                Map<Unit, Integer> ordinals = Util.getOrdinals(m.retrieveActiveBody().getUnits());
//                TablesNamesFinderExt tablesNamesFinder = new TablesNamesFinderExt();
//                tablesNamesFinder.getTableList(stmt);
//                List<String> tableList = tablesNamesFinder.getSelectTableList();
//                for (String tableName : tableList) {
//                    Code2CRUD.updateCrudElements(m, unit, Code2CRUD.DBTABLE, tableName, "R");
//                    // System.out.println(" " + tableName + "(R)");
//                }
//            }
//        }
//    }
//
//    static Map<SootField, List<String>> pointsToCache = null;
//    static SootClass pointsToClass = null;
//
//    static Map<SootField, List<String>> pointsToAnalysis(SootClass c) {
//        Map<SootField, List<String>> res = new HashMap<>();
//        for (SootMethod m : c.getMethods()) {
//            if (!m.getName().equals("<init>") && !m.getName().equals("<clinit>"))
//                continue;
//            SimpleLocalDefs[] udChain = new SimpleLocalDefs[] { null };
//            List<Unit> units = new ArrayList<>(m.retrieveActiveBody().getUnits());
//            for (Unit u : units) {
//                if (u instanceof AssignStmt) {
//                    Value lvalue = ((AssignStmt) u).getLeftOp();
//                    Value rvalue = ((AssignStmt) u).getRightOp();
//                    if (lvalue instanceof FieldRef) {
//                        res.compute(((FieldRef) lvalue).getField(), (__, v) -> {
//                            if (v == null)
//                                v = new ArrayList<>();
//                            if (rvalue instanceof StringConstant) {
//                                v.add(((StringConstant) rvalue).value);
//                            } else if (rvalue instanceof Local) {
//                                if (udChain[0] == null) {
//                                    udChain[0] = adaptUdChainForStringAppends(m, units);
//                                }
//                                v.addAll(calculateReachingStrings(u, rvalue, m, udChain[0], new Stack<Unit>()));
//                            }
//                            return v;
//                        });
//                    }
//                }
//            }
//        }
//        return res;
//    }

    static Pattern p_insert = Pattern.compile("^\\s*INSERT");
    static Pattern p_update = Pattern.compile("^\\s*UPDATE");
    static Pattern p_delete = Pattern.compile("^\\s*DELETE");
    static Pattern p_call = Pattern.compile("^\\s*(CALL|call)");
    static Pattern p_braces = Pattern.compile("\\{\\s*\\??\\s*=?(.*)\\}");

}
