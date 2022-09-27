package io.tackle.diva.analysis;

import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.function.BiFunction;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IClassLoader;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.callgraph.impl.Everywhere;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSACheckCastInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.types.TypeName;
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.util.strings.StringStuff;

import io.tackle.diva.Constants;
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

    public static Set<CGNode> getFilteredTargets(Framework fw, Trace trace, CallSiteReference site,
            boolean pathSensitive) {
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

        if (pathSensitive && targets.size() > 1 && trace.node().getGraphNodeId() != 0) {
            SSAAbstractInvokeInstruction instr = trace.instrFromSite(site);
            IClass self = calculateReceiverType(fw, trace, instr.getUse(0));
            if (self != null) {
                Set<CGNode> targets0 = Util.makeSet(Util.filter(targets, n0 -> {
                    IClass c = n0.getMethod().getDeclaringClass();
                    return Util.any(self.isInterface() ? c.getAllImplementedInterfaces() : Util.superChain(c),
                            i -> i == self);
                }));
                if (!targets0.isEmpty()) {
                    targets = targets0;

                } else {
                    IMethod m = self.getMethod(site.getDeclaredTarget().getSelector());
                    if (m != null) {
                        CGNode n = fw.callgraph.getNode(m, Everywhere.EVERYWHERE);
                        if (n != null && targets.contains(n)) {
                            targets = Collections.singleton(n);

                        }
                    }
                }

            }
        }

        if (targets.size() > 1) {
            for (CGNode m : targets) {
                if (site.getDeclaredTarget() == m.getMethod().getReference()) {
                    return Collections.singleton(m);
                }
            }
        }

        if (targets.size() > 8) {
            targets = Collections.emptySet();
        }
        return targets;
    }

    public static IClass calculateReceiverType(Framework fw, Trace trace, int number) {
        Trace.Val v = trace.getDefOrParam(number);

        while (true) {
            if (v == null)
                return null;

            if (v.isInstr() && v.instr() instanceof SSAPhiInstruction) {
                v = v.getDef(v.instr().getUse(0));
                continue;

            } else if (v.isInstr() && v.instr() instanceof SSACheckCastInstruction) {
                v = v.getDef(v.instr().getUse(0));
                continue;

            }
            if (v.isInstr() && v.instr() instanceof SSAAbstractInvokeInstruction) {

                MethodReference mref = ((SSAAbstractInvokeInstruction) v.instr()).getCallSite().getDeclaredTarget();

                if (mref.getDeclaringClass().getName() == Constants.LJavaLangClass
                        && mref.getName() == Constants.newInstance) {

                    Trace.Val c = v.getDef(v.instr().getUse(0));

                    if (c.isInstr() && c.instr() instanceof SSAAbstractInvokeInstruction) {

                        MethodReference mref2 = ((SSAAbstractInvokeInstruction) c.instr()).getCallSite()
                                .getDeclaredTarget();

                        if ((mref2.getDeclaringClass().getName() == Constants.LJavaLangClass
                                && mref2.getName() == Constants.forName)
                                || (mref2.getDeclaringClass().getName() == Constants.LJavaLangClassLoader
                                        && mref2.getName() == Constants.loadClass)) {
                            String klazz = classNameAnalysis.apply(fw,
                                    c.getDef(c.instr().getUse(mref2.getName() == Constants.forName ? 0 : 1)));
                            if (klazz != null && !klazz.contains("?")) {
                                TypeName t = TypeName
                                        .string2TypeName(StringStuff.deployment2CanonicalTypeString(klazz));
                                for (IClassLoader cl : fw.classHierarchy().getLoaders()) {
                                    IClass r = cl.lookupClass(t);
                                    if (r != null) {
                                        return r;
                                    }
                                }
                            }
                        }
                    }
                }

            }
            break;
        }

        TypeReference tref = trace.inferType(v);

        return tref == null ? null : fw.classHierarchy().lookupClass(tref);
    }

    public static BiFunction<Framework, Trace.Val, String> classNameAnalysis = (fw, v) -> StringAnalysis
            .calculateReachingString(fw, v, new HashSet<>());

}
