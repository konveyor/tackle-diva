package io.tackle.diva.analysis;

import java.util.Collection;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.ipa.callgraph.CGNode;
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
}
