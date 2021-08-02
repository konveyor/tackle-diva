package io.tackle.diva.analysis;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Stack;
import java.util.logging.Logger;

import com.ibm.wala.classLoader.CallSiteReference;
import com.ibm.wala.classLoader.IClass;
import com.ibm.wala.classLoader.IField;
import com.ibm.wala.classLoader.IMethod;
import com.ibm.wala.classLoader.IMethod.SourcePosition;
import com.ibm.wala.ipa.callgraph.CGNode;
import com.ibm.wala.ipa.cha.IClassHierarchy;
import com.ibm.wala.shrikeCT.AnnotationsReader.ConstantElementValue;
import com.ibm.wala.shrikeCT.InvalidClassFileException;
import com.ibm.wala.ssa.SSAAbstractInvokeInstruction;
import com.ibm.wala.ssa.SSANewInstruction;
import com.ibm.wala.ssa.SSAPhiInstruction;
import com.ibm.wala.types.FieldReference;
import com.ibm.wala.types.MethodReference;
import com.ibm.wala.types.Selector;
import com.ibm.wala.types.TypeName;
import com.ibm.wala.types.TypeReference;
import com.ibm.wala.types.annotations.Annotation;

import io.tackle.diva.Constants;
import io.tackle.diva.Context;
import io.tackle.diva.DivaIRGen;
import io.tackle.diva.Framework;
import io.tackle.diva.Trace;
import io.tackle.diva.Util;

public class JPAAnalysis {
    static Logger logger = Logger.getLogger(JDBCAnalysis.class.getName());

    public static class TableColumn {

        public TableColumn(String tableName, String colName, List<TypeName> tags, TypeReference type) {
            super();
            this.tableName = tableName;
            this.colName = colName;
            this.tags = tags;
            this.type = type;
        }

        public String tableName;
        public String colName;
        public List<TypeName> tags;
        public TypeReference type;

    }

    public static Map<FieldReference, TableColumn> columnDefinitions = new LinkedHashMap<>();
    public static Map<MethodReference, String> queryDefinitions = new LinkedHashMap<>();

    public static Set<IClass> customIfaces = new LinkedHashSet<>();

    public static void getEntities(IClassHierarchy cha) throws IOException {

        Set<IClass> repositoryIfaces = new LinkedHashSet<>();
        Map<IClass, IClass> nonRepositoryIfaces = new LinkedHashMap<>();

        for (IClass c : cha) {
            for (Annotation a : Util.getAnnotations(c)) {
                if (a.getType().getName() != Constants.LJavaxPersistenceTable)
                    continue;
                if (!a.getNamedArguments().containsKey("name"))
                    continue;
                String tableName = ((ConstantElementValue) a.getNamedArguments().get("name")).val.toString();
                List<TypeName> tags = new ArrayList<>();
                String colName = null;
                for (IField f : c.getDeclaredInstanceFields()) {
                    for (Annotation a2 : Util.getAnnotations(f)) {
                        if (a2.getType().getName() == Constants.LJavaxPersistenceColumn
                                || a2.getType().getName() == Constants.LJavaxPersistenceId
                                || a2.getType().getName() == Constants.LJavaxPersistenceJoinColumn
                                || a2.getType().getName() == Constants.LJavaxPersistenceManyToOne
                                || a2.getType().getName() == Constants.LJavaxPersistenceOneToMany) {
                            tags.add(a2.getType().getName());
                        }
                        if (a2.getType().getName() == Constants.LJavaxPersistenceColumn
                                || a2.getType().getName() == Constants.LJavaxPersistenceJoinColumn) {
                            ConstantElementValue v = (ConstantElementValue) a2.getNamedArguments().get("name");
                            if (v != null) {
                                colName = v.val.toString();
                            } else {
                                System.out.println(a2);
                            }
                        }
                    }
                    if (colName == null)
                        continue;
                    columnDefinitions.put(f.getReference(), new TableColumn(tableName, colName, tags, null));
                    System.out.println(f + "->" + Util.getAnnotations(f));
                }
            }
            if (Util.any(c.getAllImplementedInterfaces(), c2 -> c2.getName() == Constants.LSpringJPARepository)) {
                repositoryIfaces.add(c);
                for (IMethod m : c.getDeclaredMethods()) {
                    for (Annotation a : Util.getAnnotations(m)) {
                        if (a.getType().getName() != Constants.LSpringJPAQuery)
                            continue;
                        String query = ((ConstantElementValue) a.getNamedArguments().get("value")).val.toString();
                        queryDefinitions.put(m.getReference(), query);
                    }
                }
                // handling custom repositories
            } else if (!c.isInterface()) {
                for (IClass i : c.getAllImplementedInterfaces()) {
                    nonRepositoryIfaces.put(i, c);
                }
            }
        }
        for (IClass c : repositoryIfaces) {
            if (c.getName() == Constants.LSpringJPARepository) {
                continue;
            }
            Util.LOGGER.info(c.toString());
            IClass p = null;
            for (IClass i : c.getAllImplementedInterfaces()) {
                if (nonRepositoryIfaces.containsKey(i)) {
                    p = nonRepositoryIfaces.get(i);
                    customIfaces.add(i);
                }
            }
            IClass impl = p;
            TypeReference tref = TypeReference.findOrCreate(c.getReference().getClassLoader(),
                    TypeName.findOrCreate(c.getName().toString() + "$DivaImpl"));
            Util.LOGGER.info("Adding " + tref);
            cha.addClass(new DivaIRGen.DivaPhantomClass(tref, cha) {

                @Override
                public Collection<IClass> getAllImplementedInterfaces() {
                    Collection<IClass> ifaces = new LinkedHashSet<>();
                    ifaces.add(c);
                    if (impl != null) {
                        ifaces.addAll(impl.getAllImplementedInterfaces());
                    }
                    return ifaces;
                }

                @Override
                public IClass getSuperclass() {
                    if (impl != null) {
                        return impl;
                    }
                    return super.getSuperclass();
                }

                @Override
                public IMethod getMethod(Selector selector) {
                    if (impl != null) {
                        IMethod m = impl.getMethod(selector);
                        if (m != null) {
                            return m;
                        }
                    }
                    return super.getMethod(selector);
                }
            });
        }
    }

    public static Context.CallSiteVisitor getTransactionAnalysis(Framework fw, Context context) {
        return context.new CallSiteVisitor() {

            @SuppressWarnings("unused")
            @Override
            public void visitCallSite(Trace trace) {

                CGNode node = trace.node();
                CallSiteReference site = trace.site();
                MethodReference ref = site.getDeclaredTarget();
                TypeReference tref = ref.getDeclaringClass();
                IClass c = null;

                if (tref.getName() == Constants.LSpringJPARepository
                        || (c = fw.classHierarchy().lookupClass(tref)) != null
                                && Util.any(c.getAllImplementedInterfaces(),
                                        c2 -> c2.getName() == Constants.LSpringJPARepository)) {
                    if (ref.getName() == Constants.save || ref.getName() == Constants.saveAndFlush) {
                        SSAAbstractInvokeInstruction instr = trace.instrFromSite(site);
                        populateInsertOrUpdate(fw, trace, instr);
                    } else if (queryDefinitions.containsKey(ref)) {
                        fw.reportSqlStatement(trace, queryDefinitions.get(ref));
                    } else {
                        Util.LOGGER.info("=>" + ref);
                    }
                }

                if (tref.getName() == Constants.LJavaxPersistenceEntityManager) {
                    if (ref.getName() == Constants.createQuery) {
                        SSAAbstractInvokeInstruction instr = trace.instrFromSite(site);
                        Trace.Val v = trace.getDef(instr.getUse(1));
                        if (v.isConstant()) {
                            fw.reportSqlStatement(trace, (String) v.constant());
                        } else {
                            fw.reportSqlStatement(trace, JDBCAnalysis.calculateReachingString(fw, v, new HashSet<>()));

                        }
                    }
                }
            }
        };
    }

    public static void populateInsertOrUpdate(Framework fw, Trace trace, SSAAbstractInvokeInstruction instr) {
        Trace.Val v = trace.getDef(instr.getUse(1));
        SourcePosition p = null;
        try {
            p = trace.node().getMethod().getSourcePosition(instr.getProgramCounter());
        } catch (InvalidClassFileException e) {
        }

        Stack<Trace.Val> todo = new Stack<>();
        todo.add(v);
        while (!todo.isEmpty()) {
            v = todo.pop();
            if (v == null || v.isConstant()) {
                v = null;
                continue;
            }
            if (v.instr() instanceof SSAPhiInstruction) {
                todo.add(v.getDef(v.instr().getUse(0)));
                todo.add(v.getDef(v.instr().getUse(1)));
                v = null;
                continue;
            }
            break;
        }
        if (v == null)
            return;
        System.out.println(p + ": " + instr + ": " + v);
        if (v.instr() instanceof SSANewInstruction) {
            populateInsert(fw, trace, v);
        } else if (v.instr() instanceof SSAAbstractInvokeInstruction) {
            populateUpdate(fw, trace, v);
        }
    }

    public static void populateInsert(Framework fw, Trace trace, Trace.Val v) {
        TypeReference tref = ((SSANewInstruction) v.instr()).getConcreteType();
        IClass c = fw.classHierarchy().lookupClass(tref);

        String table = null;
        String s = null;
        String t = null;
        for (IField f : c.getAllFields()) {
            FieldReference ref = f.getReference();
            if (columnDefinitions.containsKey(ref)) {
                TableColumn col = columnDefinitions.get(ref);
                table = col.tableName;
                s = s == null ? col.colName : s + ", " + col.colName;
                t = t == null ? "?" : t + ", ?";
            }
        }
        String sql = "insert into " + table + " (" + s + ") values (" + t + ")";
        fw.reportSqlStatement(trace, sql);
    }

    public static void populateUpdate(Framework fw, Trace trace, Trace.Val v) {
        MethodReference mref = ((SSAAbstractInvokeInstruction) v.instr()).getDeclaredTarget();
        TypeReference tref = mref.getReturnType();
        IClass c = fw.classHierarchy().lookupClass(tref);

        String table = null;
        String s = null;
        for (IField f : c.getAllFields()) {
            FieldReference ref = f.getReference();
            if (columnDefinitions.containsKey(ref)) {
                TableColumn col = columnDefinitions.get(ref);
                table = col.tableName;
                s = (s == null ? "" : s + ", ") + col.colName + " = ?";
            }
        }
        String sql = "update " + table + " set " + s;
        fw.reportSqlStatement(trace, sql);
    }
}
