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

import static io.tackle.diva.Util.LOGGER;

import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.shrikeBT.IConditionalBranchInstruction;
import com.ibm.wala.shrikeCT.AnnotationsReader.ArrayElementValue;
import com.ibm.wala.shrikeCT.AnnotationsReader.ConstantElementValue;
import com.ibm.wala.shrikeCT.AnnotationsReader.ElementValue;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.ssa.ISSABasicBlock;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSAConditionalBranchInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.types.annotations.Annotation;
import com.ibm.wala.util.intset.BitVectorIntSet;
import com.ibm.wala.util.intset.IntPair;
import com.ibm.wala.util.intset.MutableIntSet;

import io.tackle.diva.Constants;
import io.tackle.diva.Context;
import io.tackle.diva.Framework;
import io.tackle.diva.Trace;
import io.tackle.diva.Util;

public class ServletAnalysis {

    public static List<IMethod> getEntries(IClassHierarchy cha) throws IOException {

        List<IMethod> entries = new ArrayList<>();

        for (IClass c : cha) {
            boolean isServlet = false;
            String urlPattern = null;

            for (Annotation a : Util.getAnnotations(c)) {
                if (a.getType().getName() != Constants.LJavaxWebServlet
                        && a.getType().getName() != Constants.LJavaxWebFilter)
                    continue;
                isServlet = true;
                for (Entry<String, ElementValue> e : a.getNamedArguments().entrySet()) {
                    if ("urlPatterns".equals(e.getKey()) || "value".equals(e.getKey())) {
                        ElementValue v = e.getValue();
                        if (v instanceof ArrayElementValue) {
                            v = ((ArrayElementValue) v).vals[0];
                        }
                        urlPattern = ((ConstantElementValue) v).val.toString();
                    }
                }
            }

            if (!isServlet) {
                for (IClass p : Util.superChain(c)) {
                    if (p.getName() == Constants.LJavaxHttpServlet) {
                        isServlet = true;
                        break;
                    }
                }
            }
            if (isServlet) {
                processServletClass(c, urlPattern, entries);
            }
        }
        return entries;
    }

    static void processServletClass(IClass c, String urlPattern, List<IMethod> entries) {

        List<IMethod> servletEntries = new ArrayList<>();
        boolean parentImpl = false;
        for (IClass p : Util.superChain(c)) {
            for (IMethod m : p.getDeclaredMethods()) {
                if (m.getName() == Constants.doGet || m.getName() == Constants.doPost
                        || m.getName() == Constants.doDelete || m.getName() == Constants.doFilter
                        || m.getName() == Constants.doPut || m.getName() == Constants.service
                        || m.getName() == Constants.init) {
                    boolean dup = false;
                    for (IMethod n : servletEntries)
                        dup |= n.getName().equals(m.getName());
                    if (!dup) {
                        entries.add(m);
                        if (!p.equals(c)) {
                            // if implemented in super class, dispatch is likely done by subclassing??
                            parentImpl = true;
                        }
                    }
                }
            }
        }
    }

    public static Trace.NodeVisitor getContextualAnalysis(Framework fw) {

        Map<String, Map<String, Set<IntPair>>> coveringBranches = new LinkedHashMap<>();

        return (Trace trace) -> {

            CGNode node = trace.node();

            IMethod method = node.getMethod();
            IR ir = node.getIR();
            if (ir == null)
                return;

            MethodReference stringEquals = MethodReference.findOrCreate(
                    TypeReference.findOrCreate(node.getMethod().getDeclaringClass().getClassLoader().getReference(),
                            "Ljava/lang/String"),
                    "equals", "(Ljava/lang/Object;)Z");

            outer: for (SSAInstruction instr : ir.getInstructions()) {
                if (!(instr instanceof SSAConditionalBranchInstruction))
                    continue;
                SSAConditionalBranchInstruction branch = (SSAConditionalBranchInstruction) instr;
                if (branch.getOperator() != IConditionalBranchInstruction.Operator.EQ)
                    continue;
                Trace.Val v1 = trace.getDef(branch.getUse(1));
                if (v1 == null || !v1.isConstant() || !(v1.constant() instanceof Integer)
                        || (Integer) v1.constant() != 0)
                    continue;

                Trace.Val v0 = trace.getDef(branch.getUse(0));
                if (v0 == null || v0.isConstant())
                    continue;

                MutableIntSet phiOrigins = new BitVectorIntSet();

                // System.out.println(ud[branch.getUse(0)]);
                if (v0.instr() instanceof SSAPhiInstruction) {
                    if (v0.trace() != trace)
                        continue outer;
                    /*
                     * Handling param.equals("A") || param.equals("B") This is turned to branch on
                     * phi(true, param.equals("B")) whose originating branch is about
                     * param.equals("A"). Maybe it's easier to rewrite IR?
                     */
                    SSAPhiInstruction phi = (SSAPhiInstruction) v0.instr();
                    ISSABasicBlock bb = ir.getBasicBlockForInstruction(v0.instr());
                    if (bb == null)
                        continue outer;
                    int i = 0;
                    v0 = null;
                    for (ISSABasicBlock pred : (Iterable<ISSABasicBlock>) () -> ir.getControlFlowGraph()
                            .getPredNodes(bb)) {
                        Trace.Val v = trace.getDef(phi.getUse(i++));
                        if (v.isConstant() && v.constant() instanceof Boolean && (Boolean) v.constant()) {
                            for (ISSABasicBlock pred2 : (Iterable<ISSABasicBlock>) () -> ir.getControlFlowGraph()
                                    .getPredNodes(pred)) {
                                if (pred2.getNumber() != pred.getNumber() - 1)
                                    continue outer;
                                SSAInstruction last = pred2.getLastInstruction();
                                if (last == null || !(last instanceof SSAConditionalBranchInstruction))
                                    continue outer;
                                phiOrigins.add(last.iIndex());
                            }
                        } else if (v0 == null) {
                            v0 = v;
                        } else {
                            continue outer;
                        }
                        // System.out.println(pred + "->" + bb);
                    }
                    if (v0 == null)
                        continue outer;
                }

                if (!(v0.instr() instanceof SSAAbstractInvokeInstruction))
                    continue;
                SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) v0.instr();

                if (invoke.getDeclaredTarget() != stringEquals)
                    continue;

                Trace.Val v2 = v0.getDef(invoke.getUse(0));
                Trace.Val v3 = v0.getDef(invoke.getUse(1));

                // System.out.println("stringeq(" + v2 + ", " + v3 + ")");

                if (v2 == null || v3 == null)
                    continue;
                if (v2.isConstant()) {
                    Trace.Val tmp = v2;
                    v2 = v3;
                    v3 = tmp;
                }
                if (!v3.isConstant() || !(v3.constant() instanceof String) || v2.isConstant()
                        || !(v2.instr() instanceof SSAAbstractInvokeInstruction))
                    continue;

                SSAAbstractInvokeInstruction invoke2 = (SSAAbstractInvokeInstruction) v2.instr();
                if (invoke2.getDeclaredTarget().getName() != Constants.getParameter)
                    continue;

                Trace.Val v4 = v2.getDef(invoke2.getUse(1));
                if (!v4.isConstant() && !(v4.constant() instanceof String))
                    continue;

                String key = v4.toString();

                if (!phiOrigins.isEmpty()) {
                    MutableIntSet copy = new BitVectorIntSet();
                    copy.copySet(phiOrigins);

                    for (Map.Entry<String, Map<String, Set<IntPair>>> e : coveringBranches.entrySet()) {
                        if (!e.getKey().equals(key))
                            continue;
                        for (Set<IntPair> s : e.getValue().values()) {
                            for (IntPair p : s) {
                                if (p.getX() == node.getGraphNodeId() && phiOrigins.contains(p.getY())) {
                                    s.add(IntPair.make(node.getGraphNodeId(), branch.iIndex()));
                                    copy.remove(p.getY());
                                    break;
                                }
                            }
                        }
                    }

                    if (!copy.isEmpty()) {
                        LOGGER.info("TODO");
                    }
                }

                String val = v3.toString();
                IntPair branchId = IntPair.make(node.getGraphNodeId(), branch.iIndex());

                if (!coveringBranches.containsKey(key)) {
                    coveringBranches.put(key, new LinkedHashMap<>());
                }
                if (!coveringBranches.get(key).containsKey(val)) {
                    coveringBranches.get(key).put(val, new LinkedHashSet<>());
                }
                coveringBranches.get(key).get(val).add(branchId);

                fw.recordContraint(new HttpParameterConstraint(key, val) {

                    @Override
                    public Iterable<IntPair> fallenThruBranches() {
                        return coveringBranches.get(key).get(val);
                    }

                    @Override
                    public Iterable<IntPair> takenBranches() {
                        Set<IntPair> res = new LinkedHashSet<>();
                        for (Entry<String, Set<IntPair>> e : coveringBranches.get(key).entrySet()) {
                            res.addAll(e.getValue());
                        }
                        res.removeAll(coveringBranches.get(key).get(val));
                        return res;
                    }

                });

                LOGGER.info(v4 + "=" + v3);
            }

        };
    }

    public static abstract class HttpParameterConstraint implements Context.BranchingConstraint {
        @Override
        public String category() {
            return "http-param";
        }

        @Override
        public String type() {
            return key;
        }

        @Override
        public String value() {
            return val;
        }

        String key;
        String val;

        public HttpParameterConstraint(String key, String val) {
            super();
            this.key = key;
            this.val = val;
        }

    }

}
