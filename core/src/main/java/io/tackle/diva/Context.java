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

package io.tackle.diva;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.Stack;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.ssa.SSAConditionalBranchInstruction;
import com.ibm.wala.ssa.SSAGotoInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSASwitchInstruction;
import com.ibm.wala.util.collections.Pair;
import com.ibm.wala.util.intset.BitVector;
import com.ibm.wala.util.intset.BitVectorIntSet;
import com.ibm.wala.util.intset.IntSet;

import io.tackle.diva.Constraint.BranchingConstraint;
import io.tackle.diva.Constraint.EntryConstraint;

@SuppressWarnings("serial")
public class Context extends ArrayList<Constraint> {

    public abstract class CallSiteVisitor implements Trace.CallSiteVisitor {
        @Override
        public void visitNode(Trace trace) {
            trace.setContext(Context.this);
        }
    }

    public abstract class NodeVisitor implements Trace.NodeVisitor {
        @Override
        public void visitNode(Trace trace) {
            trace.setContext(Context.this);
            visitNode(trace, Context.this);
        }

        public abstract void visitNode(Trace trace, Context context);
    }

    public abstract class InstructionVisitor implements Trace.InstructionVisitor {
        @Override
        public void visitNode(Trace trace) {
            trace.setContext(Context.this);
        }

        @Override
        public void visitCallSite(Trace trace) {
        }
    }

    public Map<IClass, IClass> dispatch;

    public Map<IClass, IClass> dispatchMap() {
        if (dispatch == null) {
            dispatch = new LinkedHashMap<>();
            for (Constraint con : this) {
                if (!(con instanceof Constraint.DispatchConstraint))
                    continue;
                dispatch.put(((Constraint.DispatchConstraint) con).base, ((Constraint.DispatchConstraint) con).impl);
            }
        }
        return dispatch;
    }

    public Context(Iterable<Constraint> cs) {
        for (Constraint c : cs)
            add(c);
    }

    public Context() {
    }

    public BitVector calculateReachable(Framework fw, CGNode n) {
        BitVector reachable = null;

        Set<Pair<String, String>> knownKeys = new HashSet<>();

        for (Constraint con : this) {
            if (con instanceof BranchingConstraint) {
                Map<Integer, BitVector> reaching = ((BranchingConstraint) con).reachingInstrs();
                if (reaching.containsKey(n.getGraphNodeId())) {
                    if (reachable == null) {
                        reachable = reaching.get(n.getGraphNodeId());
                    } else {
                        reachable = BitVector.and(reachable, reaching.get(n.getGraphNodeId()));
                    }
                }
            }
            knownKeys.add(Pair.make(con.category(), con.type()));
        }

        for (Map.Entry<Pair<String, String>, List<Constraint>> e : fw.constraints.entrySet()) {
            if (!knownKeys.contains(e.getKey()) && e.getValue().get(0) instanceof BranchingConstraint) {
                Map<Integer, BitVector> reaching = ((BranchingConstraint) e.getValue().get(0)).defaultConstraint()
                        .reachingInstrs();
                if (reaching.containsKey(n.getGraphNodeId())) {
                    if (reachable == null) {
                        reachable = reaching.get(n.getGraphNodeId());
                    } else {
                        reachable = BitVector.and(reachable, reaching.get(n.getGraphNodeId()));
                    }
                }
            }

        }

        if (reachable != null)
            return reachable;

        // otherwise select non-exceptional code
        BitVector visited = new BitVector();
        BitVector todo = new BitVector();

        IR ir = n.getIR();
        int i = 0;

        todo.set(i);

        while (!todo.isZero()) {
            i = todo.nextSetBit(0);
            todo.clear(i);
            visited.set(i);
            if (i >= ir.getInstructions().length)
                continue;
            SSAInstruction instr = ir.getInstructions()[i];

            if (instr instanceof SSAConditionalBranchInstruction) {

                SSAConditionalBranchInstruction c = (SSAConditionalBranchInstruction) instr;
                if (c.getTarget() >= 0 && !visited.contains(c.getTarget())) {
                    todo.set(c.getTarget());
                }

            } else if (instr instanceof SSASwitchInstruction) {
                SSASwitchInstruction c = (SSASwitchInstruction) instr;
                for (int l : c.getCasesAndLabels()) {
                    int j = c.getTarget(l);
                    if (!visited.contains(j)) {
                        todo.set(j);
                    }
                }
                if (!visited.contains(c.getDefault())) {
                    todo.set(c.getDefault());
                }
            } else if (instr instanceof SSAGotoInstruction) {
                SSAGotoInstruction c = (SSAGotoInstruction) instr;
                if (c.getTarget() >= 0 && !visited.contains(c.getTarget())) {
                    todo.set(c.getTarget());
                }
            }
            if (instr == null || instr.isFallThrough()) {

                if (!visited.contains(i + 1)) {
                    todo.set(i + 1);
                }
            }
        }
        return visited;
    }

    public static int MAX_NUM_CONTEXTS = 4096;

    public static List<Context> calculateDefaultContexts(Framework fw) throws IOException {
        // calculate cross product of constraint groups

        LinkedHashSet<Context> result = new LinkedHashSet<>();

        if (fw.constraints.isEmpty())
            return Collections.emptyList();

        List<Constraint> cons = new ArrayList<>();

        for (Constraint c : Util.flatMap(fw.constraints.values(), v -> v)) {
            if (c instanceof EntryConstraint)
                cons.add(c);
        }
        for (Constraint c : Util.flatMap(fw.constraints.values(), v -> v)) {
            if (c instanceof EntryConstraint)
                continue;
            if (c instanceof BranchingConstraint && !((BranchingConstraint) c).isRelevant())
                continue;
            cons.add(c);
        }

        Stack<IntSet> stack = new Stack<>();
        stack.add(new BitVectorIntSet());
        while (result.size() < MAX_NUM_CONTEXTS && !stack.isEmpty()) {
            IntSet v = stack.pop();
            for (int k = v.isEmpty() ? 0 : v.max() + 1; k < cons.size(); k++) {
                Constraint c = cons.get(k);
                if (v.isEmpty() && !(c instanceof EntryConstraint))
                    continue;
                if (Util.any(Util.makeIterable(v), i -> cons.get(i).forbids(c) || c.forbids(cons.get(i))))
                    continue;
                BitVectorIntSet w = new BitVectorIntSet(v);
                w.add(k);
                stack.push(w);
            }
            if (v.isEmpty())
                continue;
            Context cxt = new Context();
            for (Constraint c2 : Util.map(Util.makeIterable(v), cons::get))
                cxt.add(c2);
            result.add(cxt);
        }

        List<Object> json = new ArrayList<>();
        Report report = new Util.JsonReport(json);
        for (Context cxt : result) {
            report.add((Report.Named map) -> {
                for (Constraint c : cxt) {
                    c.report(map);
                }
            });

        }
        try (Writer f = new FileWriter("contexts.yml")) {
            f.write(Util.YAML_SERIALIZER.writeValueAsString(json));
        }

        return new ArrayList<>(result);
    }

    public static List<Context> loadContexts(Framework fw, String file)
            throws JsonParseException, JsonMappingException, IOException {

        @SuppressWarnings("unchecked")
        List<Map<String, Map<String, List<String>>>> data = (List<Map<String, Map<String, List<String>>>>) Util.YAML_SERIALIZER
                .readValue(new File(file), Object.class);

        List<Context> result = new ArrayList<>();

        for (Map<String, Map<String, List<String>>> e : data) {
            Context cxt = new Context();
            for (Entry<String, Map<String, List<String>>> e2 : e.entrySet()) {
                for (Entry<String, List<String>> e3 : e2.getValue().entrySet()) {
                    for (Constraint c : fw.constraints.get(Pair.make(e2.getKey(), e3.getKey()))) {
                        if (e3.getValue().contains(c.value())) {
                            cxt.add(c);
                        }
                    }
                }
            }
            result.add(cxt);
        }

        return result;
    }

    @Override
    public int hashCode() {
        int result = 1;
        for (Constraint element : this) {
            result = 31 * result + System.identityHashCode(element);
        }
        return result;
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || !(o instanceof Context))
            return false;
        Context other = (Context) o;
        if (size() != other.size())
            return false;
        for (int k = 0; k < size(); k++) {
            if (get(k) != other.get(k))
                return false;
        }
        return true;
    }
}
