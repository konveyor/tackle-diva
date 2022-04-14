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

import com.ibm.wala.classLoader.CallSiteReference;
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
import com.ibm.wala.types.annotations.Annotation;
import com.ibm.wala.util.intset.BitVectorIntSet;
import com.ibm.wala.util.intset.IntPair;
import com.ibm.wala.util.intset.IntSet;
import com.ibm.wala.util.intset.MutableIntSet;
import com.ibm.wala.util.intset.MutableSparseIntSet;

import io.tackle.diva.Constants;
import io.tackle.diva.Constraint;
import io.tackle.diva.Framework;
import io.tackle.diva.Report;
import io.tackle.diva.Trace;
import io.tackle.diva.Util;

public class ServletAnalysis {

    public static List<IMethod> getEntries(IClassHierarchy cha) throws IOException {

        List<IMethod> entries = new ArrayList<>();

        for (IClass c : cha) {
            boolean isServlet = false;
            String urlPattern = null;

            if (c.isAbstract())
                continue;

            for (Annotation a : Util.getAnnotations(c)) {
                if (a.getType().getName() != Constants.LJavaxWebServlet
                        && a.getType().getName() != Constants.LJavaxWebFilter)
                    continue;
                isServlet = true;
                for (Entry<String, ElementValue> e : a.getNamedArguments().entrySet()) {
                    if ("urlPatterns".equals(e.getKey()) || "value".equals(e.getKey())) {
                        ElementValue v = e.getValue();
                        if (v != null) {
                            if (v instanceof ArrayElementValue) {
                                v = ((ArrayElementValue) v).vals[0];
                            }
                            urlPattern = "" + ((ConstantElementValue) v).val;
                        }
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
                if (m.isAbstract() || m.isNative())
                    continue;
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

    @FunctionalInterface
    public interface Matcher {
        public String apply(Framework fw, Trace.Val v);

        public default Matcher with(Matcher m) {
            return (fw, v) -> {
                String k = Matcher.this.apply(fw, v);
                if (k != null) {
                    return k;
                }
                return m.apply(fw, v);
            };
        }
    }

    public static Trace.InstructionVisitor getContextualAnalysis(Framework fw) {
        return getContextualAnalysisAux(fw, getHttpParameterMatcher().with(SpringBootAnalysis.getJsonRequestMatcher()));
    }

    public static Matcher getHttpParameterMatcher() {
        return (fw, v) -> {
            if (v.isConstant() || !(v.instr() instanceof SSAAbstractInvokeInstruction))
                return null;
            SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) v.instr();
            if (invoke.getDeclaredTarget().getName() != Constants.getParameter)
                return null;
            Trace.Val v2 = v.getDef(invoke.getUse(1));
            if (!v2.isConstant() && !(v2.constant() instanceof String))
                return null;
            return v2.toString();
        };
    }

    public static Trace.InstructionVisitor getContextualAnalysisAux(Framework fw, Matcher matcher) {
        /*
         * Search for branches corresponding to test expressions in the form of
         * 'value.equals(request.getParameter(key))'.
         *
         * coveringBranches: Mapping (key, value)-constraint to a set of depending
         * branch instructions.
         *
         * reachingNodesCache: Reachability analysis for calculating forbidden (=
         * irrelevant) entry methods
         */
        Map<String, Map<String, Set<IntPair>>> coveringBranches = new LinkedHashMap<>();
        Map<Integer, MutableIntSet> reachingNodesCache = new LinkedHashMap<>();

        return (Trace trace, SSAInstruction instr) -> {

            CGNode node = trace.node();

            IMethod method = node.getMethod();
            IR ir = node.getIR();
            if (ir == null)
                return;

            if (!(instr instanceof SSAConditionalBranchInstruction))
                return;
            SSAConditionalBranchInstruction branch = (SSAConditionalBranchInstruction) instr;
            if (branch.getOperator() != IConditionalBranchInstruction.Operator.EQ)
                return;
            Trace.Val v1 = trace.getDef(branch.getUse(1));
            if (v1 == null || !v1.isConstant() || !(v1.constant() instanceof Integer) || (Integer) v1.constant() != 0)
                return;

            Trace.Val v0 = trace.getDef(branch.getUse(0));
            if (v0 == null || v0.isConstant())
                return;

            MutableIntSet phiOrigins = new BitVectorIntSet();

            // System.out.println(ud[branch.getUse(0)]);
            if (v0.instr() instanceof SSAPhiInstruction) {
                if (v0.trace() != trace)
                    return;
                /*
                 * Handling param.equals("A") || param.equals("B") This is turned to branch on
                 * phi(true, param.equals("B")) whose originating branch is about
                 * param.equals("A"). Maybe it's easier to rewrite IR?
                 */
                SSAPhiInstruction phi = (SSAPhiInstruction) v0.instr();
                ISSABasicBlock bb = ir.getBasicBlockForInstruction(v0.instr());
                if (bb == null)
                    return;
                int i = 0;
                v0 = null;
                for (ISSABasicBlock pred : (Iterable<ISSABasicBlock>) () -> ir.getControlFlowGraph().getPredNodes(bb)) {
                    Trace.Val v = trace.getDef(phi.getUse(i++));
                    if (v == null)
                        return;
                    if (v.isConstant() && v.constant() instanceof Boolean && (Boolean) v.constant()) {
                        for (ISSABasicBlock pred2 : (Iterable<ISSABasicBlock>) () -> ir.getControlFlowGraph()
                                .getPredNodes(pred)) {
                            if (pred2.getNumber() != pred.getNumber() - 1)
                                return;
                            SSAInstruction last = null;
                            try {
                                last = pred2.getLastInstruction();
                            } catch (RuntimeException e) {
                            }
                            if (last == null || !(last instanceof SSAConditionalBranchInstruction))
                                return;
                            phiOrigins.add(last.iIndex());
                        }
                    } else if (v0 == null && v.isInstr()) {
                        v0 = v;
                    } else
                        return;
                    // System.out.println(pred + "->" + bb);
                }
                if (v0 == null)
                    return;
            }

            if (!(v0.instr() instanceof SSAAbstractInvokeInstruction))
                return;
            SSAAbstractInvokeInstruction invoke = (SSAAbstractInvokeInstruction) v0.instr();

            if (invoke.getDeclaredTarget().getName() != Constants.equals
                    && invoke.getDeclaredTarget().getName() != Constants.equalsIgnoreCase
                    && invoke.getDeclaredTarget().getName() != Constants.contains)
                return;

            Trace.Val v2 = v0.getDef(invoke.getUse(0));
            Trace.Val v3 = v0.getDef(invoke.getUse(1));

            // System.out.println("stringeq(" + v2 + ", " + v3 + ")");

            if (v2 == null || v3 == null)
                return;
            if (v2.isConstant()) {
                Trace.Val tmp = v2;
                v2 = v3;
                v3 = tmp;
            }
            if (!v3.isConstant() || !(v3.constant() instanceof String))
                return;

            String key = matcher.apply(fw, v2);

            if (key == null)
                return;

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
                    LOGGER.fine("TODO");
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

            MutableIntSet reached = reachingNodesCache.getOrDefault(node.getGraphNodeId(), null);
            if (reached == null) {
                MutableIntSet rs = MutableSparseIntSet.makeEmpty();
                rs.add(node.getGraphNodeId());
                boolean done = false;
                while (!done) {
                    done = true;
                    for (CGNode n : fw.callgraph()) {
                        if (rs.contains(n.getGraphNodeId()))
                            continue;
                        for (CallSiteReference site : (Iterable<CallSiteReference>) () -> n.iterateCallSites()) {
                            String klazz = site.getDeclaredTarget().getDeclaringClass().getName().toString();
                            if (klazz.startsWith("Ljava/") || klazz.startsWith("Ljavax/"))
                                continue;
                            if (Util.any(fw.callgraph().getPossibleTargets(n, site),
                                    m -> rs.contains(m.getGraphNodeId()))) {
                                rs.add(n.getGraphNodeId());
                                done = false;
                                break;
                            }
                        }

                    }
                }
                reached = rs;
                reachingNodesCache.put(node.getGraphNodeId(), reached);
            }
            IntSet reachingNodes = reached;

            fw.recordContraint(new HttpParameterConstraint(key, val) {

                @Override
                public boolean forbids(Constraint other) {
                    if (other instanceof Constraint.EntryConstraint) {
                        return !reachingNodes.contains(((Constraint.EntryConstraint) other).node().getGraphNodeId());
                    }
                    if (other instanceof HttpParameterConstraint) {
                        return key.equals(((HttpParameterConstraint) other).key);
                    }
                    return false;
                }

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

            LOGGER.fine(key + "=" + val);

        };
    }

    public static abstract class HttpParameterConstraint implements Constraint.BranchingConstraint {
        @Override
        public String category() {
            return Report.HTTP_PARAM;
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
