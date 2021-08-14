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

package io.tackle.diva;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ssa.IR;
import com.ibm.wala.ssa.SSAConditionalBranchInstruction;
import com.ibm.wala.ssa.SSAGotoInstruction;
import com.ibm.wala.ssa.SSAInstruction;
import com.ibm.wala.ssa.SSASwitchInstruction;
import com.ibm.wala.util.collections.Pair;
import com.ibm.wala.util.intset.BitVector;
import com.ibm.wala.util.intset.IntPair;
import com.ibm.wala.util.strings.StringStuff;

public class Context extends ArrayList<Context.Constraint> {

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

    public static interface Constraint {

        default public void report(Report.Named report) {
            report.put(category(), (Report.Named map) -> {
                map.put(type(), (Report values) -> {
                    values.add(value());
                });
            });
        }

        public String category();

        public String type();

        public String value();

        public boolean forbids(Constraint other);
    }

    public static interface BranchingConstraint extends Constraint {
        public Iterable<IntPair> fallenThruBranches();

        public Iterable<IntPair> takenBranches();
    }

    public static class EntryConstraint implements Constraint {

        public EntryConstraint(CGNode node) {
            super();
            this.node = node;
        }

        CGNode node;

        @Override
        public String category() {
            return "entry";
        }

        @Override
        public String type() {
            return "methods";
        }

        @Override
        public String value() {
            IMethod method = node.getMethod();
            return StringStuff.jvmToBinaryName(method.getDeclaringClass().getName().toString()) + "."
                    + method.getName().toString();
        }

        public CGNode node() {
            return node;
        }

        @Override
        public boolean forbids(Context.Constraint other) {
            return false;
        }
    }

    public Context(Iterable<Constraint> cs) {
        for (Constraint c : cs)
            add(c);
    }

    public Context() {
    }

    public BitVector calculateReachable(CGNode n) {
        BitVector visited = new BitVector();
        BitVector todo = new BitVector();
        BitVector fallenThru = new BitVector();
        BitVector taken = new BitVector();

        for (Constraint con : this) {
            if (con instanceof BranchingConstraint) {
                BranchingConstraint c = (BranchingConstraint) con;
                for (IntPair key : c.fallenThruBranches()) {
                    if (key.getX() != n.getGraphNodeId())
                        continue;
                    fallenThru.set(key.getY());
                }
                for (IntPair key : c.takenBranches()) {
                    if (key.getX() != n.getGraphNodeId())
                        continue;
                    taken.set(key.getY());
                }
            }
        }

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
                if (!fallenThru.get(i)) {
                    SSAConditionalBranchInstruction c = (SSAConditionalBranchInstruction) instr;
                    if (c.getTarget() >= 0 && !visited.contains(c.getTarget())) {
                        todo.set(c.getTarget());
                    }
                }
                if (taken.get(i)) {
                    continue;
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

    public static List<Context> calculateDefaultContexts(Framework fw) throws IOException {
        // calculate cross product of constraint groups
        LinkedHashSet<Context> result = new LinkedHashSet<>();

        int[] counter = new int[fw.constraints.size()];
        List<Constraint>[] cs = new List[fw.constraints.size()];

        int k = 0;
        for (List<Constraint> c : fw.constraints.values()) {
            counter[k] = 0;
            cs[k] = c;
            k++;
        }

        outer: while (true) {
            Context cxt = new Context();

            for (k = 0; k < cs.length; k++) {
                Constraint r = cs[k].get(counter[k]);
                if (!Util.any(cxt, r2 -> r.forbids(r2) || r2.forbids(r))) {
                    cxt.add(r);
                }
            }

            result.add(cxt);

            counter[cs.length - 1] += 1;
            for (k = cs.length - 1; k >= 0; k--) {
                if (counter[k] < cs[k].size()) {
                    break;
                }
                if (k == 0)
                    break outer;
                counter[k] = 0;
                counter[k - 1] += 1;
            }
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
}
