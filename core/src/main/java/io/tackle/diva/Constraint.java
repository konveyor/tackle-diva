package io.tackle.diva;

import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.util.intset.IntPair;
import com.ibm.wala.util.strings.StringStuff;

public interface Constraint {

    interface BranchingConstraint extends Constraint {
        public Iterable<IntPair> fallenThruBranches();

        public Iterable<IntPair> takenBranches();
    }

    class EntryConstraint implements Constraint {

        public EntryConstraint(CGNode node) {
            super();
            this.node = node;
        }

        CGNode node;

        @Override
        public String category() {
            return Report.ENTRY;
        }

        @Override
        public String type() {
            return Report.METHODS;
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
        public boolean forbids(Constraint other) {
            return false;
        }
    }

    class DispatchConstraint implements Constraint {

        IClass base;
        IClass impl;

        public DispatchConstraint(IClass base, IClass impl) {
            this.base = base;
            this.impl = impl;
        }

        @Override
        public String category() {
            return Report.DISPATCH;
        }

        @Override
        public String type() {
            return base.getName().toString();
        }

        @Override
        public String value() {
            return impl.getName().toString();
        }

        @Override
        public boolean forbids(Constraint other) {
            return false;
        }
    }

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