package io.tackle.diva.analysis;

import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.types.MethodReference;

import io.tackle.diva.Framework;
import io.tackle.diva.Trace;
import io.tackle.diva.Util;

public class DispatchAnalysis {

    public static Trace.CallSiteVisitor getContextualAnalysis(Framework fw) {

        Set<MethodReference> seen = new HashSet<>();

        return (Trace trace) -> {

            CGNode node = trace.node();
            CallSiteReference site = trace.site();

            String klazz = site.getDeclaredTarget().getDeclaringClass().getName().toString();
            if (klazz.startsWith("Ljava/") || klazz.startsWith("Ljavax/"))
                return;

            if (seen.contains(site.getDeclaredTarget()))
                return;
            seen.add(site.getDeclaredTarget());

            Collection<CGNode> nodes = fw.callgraph().getPossibleTargets(node, site);

            if (nodes.size() > 1) {
                if (nodes.size() > 10) {
                    Iterator<CGNode> i = nodes.iterator();
                    nodes = Util.makeList(Util.map(Util.range(10), __ -> i.next()));
                }
                System.out.println(site + " => " + nodes);
            }
        };
    }

    public static Set<CGNode> getFilteredTargets(Framework fw, Trace trace, CallSiteReference site) {
        Set<CGNode> targets = fw.callgraph.getPossibleTargets(trace.node(), site);

        if (targets.isEmpty())
            return targets;

        if (Util.any(targets, n -> n.getIR() == null)) {
            // native methods...
            targets = Util.makeSet(Util.filter(targets, n -> n.getIR() != null));
        }

        if (targets.size() > 1 && trace.context() != null && !trace.context().dispatchMap().isEmpty()) {
            IClass c = fw.classHierarchy().lookupClass(site.getDeclaredTarget().getDeclaringClass());
            outer: for (Map.Entry<IClass, IClass> e : trace.context().dispatchMap().entrySet()) {
                if (e.getKey() == c
                        || Util.any(e.getKey().isInterface() ? c.getAllImplementedInterfaces() : Util.superChain(c),
                                i -> i == e.getKey())) {
                    for (IClass d : Util.superChain(e.getValue())) {
                        Set<CGNode> ts = Util
                                .makeSet(Util.filter(targets, n -> n.getMethod().getDeclaringClass() == d));
                        if (!ts.isEmpty()) {
                            targets = ts;
                            break outer;
                        }
                    }
                }
            }
        }

        if (targets.size() > 1 && trace.node().getGraphNodeId() != 0) {
            SSAAbstractInvokeInstruction instr = trace.instrFromSite(site);
            IClass self = trace.inferType(fw, instr.getUse(0));
            if (self != null) {
                targets = Util.makeSet(Util.filter(targets, n -> {
                    IClass c = n.getMethod().getDeclaringClass();
                    return Util.any(self.isInterface() ? c.getAllImplementedInterfaces() : Util.superChain(c),
                            i -> i == self);
                }));
            }
        }

        if (targets.size() > 1) {
            for (CGNode m : targets) {
                if (site.getDeclaredTarget() == m.getMethod().getReference()) {
                    return Collections.singleton(m);
                }
            }
        }
        return targets;
    }
}
