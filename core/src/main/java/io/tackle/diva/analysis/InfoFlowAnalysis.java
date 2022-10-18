package io.tackle.diva.analysis;

import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Stack;
import java.util.function.BiConsumer;
import java.util.function.Consumer;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IField;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSABinaryOpInstruction;
import com.ibm.wala.ssa.SSACheckCastInstruction;
import com.ibm.wala.ssa.SSAGetInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSANewInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.types.ClassLoaderReference;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.util.intset.IntPair;

import io.tackle.diva.Constants;
import io.tackle.diva.Context;
import io.tackle.diva.Framework;
import io.tackle.diva.Report;
import io.tackle.diva.Trace;

public class InfoFlowAnalysis {

    public static Context.CallSiteVisitor getTransactionAnalysis(Framework fw, Context context) {

        Map<String, Set<String>> flow = new LinkedHashMap<>();

        return context.new CallSiteVisitor() {

            @Override
            public void visitCallSite(Trace trace) {

                CGNode node = trace.node();
                CallSiteReference site = trace.site();
                MethodReference ref = site.getDeclaredTarget();
                Trace.Val sql = null;
                if ((ref.getDeclaringClass().getName() == Constants.LJavaxRequestDispatcher
                        || ref.getDeclaringClass().getName() == Constants.LUnknown)
                        && (ref.getName() == Constants.include || ref.getName() == Constants.forward)) {
                    SSAAbstractInvokeInstruction instr = trace.instrFromSite(site);

                    for (Trace.Val use : trace.receiverUseChain(instr, instr.getUse(1))) {

                        if (!(use.instr() instanceof SSAAbstractInvokeInstruction))
                            continue;
                        MethodReference ref1 = ((SSAAbstractInvokeInstruction) use.instr()).getDeclaredTarget();
                        if (ref1.getName() != Constants.setAttribute)
                            continue;
                        String attr = StringAnalysis.calculateReachingString(fw, use.getDef(use.instr().getUse(1)));

                        TypeReference tref = use.trace().inferType(use.instr().getUse(2));
                        IClass c = tref == null ? null : fw.classHierarchy().lookupClass(tref);
                        if (c != null && !c.getReference().getClassLoader().equals(ClassLoaderReference.Primordial)) {

                            for (IField f : c.getAllFields()) {
                                SSAGetInstruction get = c.getClassLoader().getInstructionFactory().GetInstruction(
                                        use.instr().iIndex(), -1, use.instr().getUse(2), f.getReference());

                                String key = "req:" + attr + "." + f.getName();

                                handleReachingValues(fw, Collections.singletonList(use.trace().new Val(get)),
                                        resultSetHandler(fw, key, flow).andThen(requestParamHandler(fw, key, flow)));
                            }
                        }
                    }
                    if (!flow.isEmpty()) {

                        fw.reportOperation(trace, (map) -> {
                            map.put("site", ref.toString());
                            map.put("infoflow", (Report.Named info) -> {
                                for (Map.Entry<String, Set<String>> e : flow.entrySet()) {
                                    info.put(e.getKey(), (Report vs) -> {
                                        for (String v : e.getValue()) {
                                            vs.add(v);
                                        }
                                    });
                                }
                            });
                        });
                    }
                }
            }

        };
    }

    public static BiConsumer<Trace.Val, Consumer<Trace.Val>> resultSetHandler(Framework fw, String key,
            Map<String, Set<String>> flow) {
        return (Trace.Val v0, Consumer<Trace.Val> h) -> {

            if (!v0.isInstr() || !(v0.instr() instanceof SSAAbstractInvokeInstruction))
                return;

            MethodReference mref = ((SSAAbstractInvokeInstruction) v0.instr()).getDeclaredTarget();
            if (mref.getDeclaringClass().getName() != Constants.LJavaSqlResultSet)
                return;
            if (!(mref.getName() == Constants.getInt || mref.getName() == Constants.getString
                    || mref.getName() == Constants.getFloat || mref.getName() == Constants.getDouble
                    || mref.getName() == Constants.getBigDecimal))
                return;

            Trace.Val query = v0.getDef(v0.instr().getUse(0));
            if (!query.isInstr() || !(query.instr() instanceof SSAAbstractInvokeInstruction))
                return;
            CallSiteReference site = ((SSAAbstractInvokeInstruction) query.instr()).getCallSite();
            int op = fw.callSiteToOp.getOrDefault(query.trace().updateSite(site), -1);
            if (op < 0)
                return;
            String col = StringAnalysis.calculateReachingString(fw, v0.getDef(v0.instr().getUse(1)));
            if (col == null || col.contains("?"))
                return;

            String val = "sqlop:" + op + "." + col;
            if (!flow.containsKey(key))
                flow.put(key, new LinkedHashSet<>());
            flow.get(key).add(val);
        };
    }

    public static BiConsumer<Trace.Val, Consumer<Trace.Val>> requestParamHandler(Framework fw, String key,
            Map<String, Set<String>> flow) {
        return (Trace.Val v0, Consumer<Trace.Val> h) -> {

            if (!v0.isInstr() || !(v0.instr() instanceof SSAAbstractInvokeInstruction))
                return;

            MethodReference mref = ((SSAAbstractInvokeInstruction) v0.instr()).getDeclaredTarget();
            if (mref.getDeclaringClass().getName() != Constants.LJavaxHttpServletRequest)
                return;
            if (mref.getName() != Constants.getParameter)
                return;

            String name = StringAnalysis.calculateReachingString(fw, v0.getDef(v0.instr().getUse(1)));
            if (name == null || name.contains("?"))
                return;

            String val = "http-param:" + name;
            if (!flow.containsKey(key))
                flow.put(key, new LinkedHashSet<>());
            flow.get(key).add(val);
        };
    }

    public static void handleReachingValues(Framework fw, List<Trace.Val> seeds,
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

            } else if (instr instanceof SSAPhiInstruction || instr instanceof SSACheckCastInstruction
                    || instr instanceof SSABinaryOpInstruction) {
                for (int j = 0; j < instr.getNumberOfUses(); j++) {
                    handler.accept(v.getDef(instr.getUse(j)));
                }

            } else if (instr instanceof SSANewInstruction) {
                SSANewInstruction alloc = (SSANewInstruction) instr;

                if (alloc.getConcreteType().getName() == Constants.LJavaLangString
                        || alloc.getConcreteType().getName() == Constants.LJavaLangInteger) {
                    SSAAbstractInvokeInstruction constr = StringAnalysis.getConstructorForNew(v.trace().node().getIR(),
                            alloc);
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
