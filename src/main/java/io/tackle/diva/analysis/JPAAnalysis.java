package io.tackle.diva.analysis;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
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
import com.ibm.wala.ssa.SSACheckCastInstruction;
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
import io.tackle.diva.Framework;
import io.tackle.diva.Trace;
import io.tackle.diva.Util;
import io.tackle.diva.irgen.DivaIRGen;
import io.tackle.diva.irgen.DivaPhantomClass;

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
                    if (tags.isEmpty())
                        continue;
                    if (colName == null)
                        colName = f.getName().toString();
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
            cha.addClass(new DivaPhantomClass(tref, cha) {

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

    public static IClass getRepoParamterType(Framework fw, TypeReference tref) {
        List<TypeName> paramTypes = DivaIRGen.instantiations.getOrDefault(tref, Collections.emptyMap())
                .getOrDefault(Constants.LSpringJPARepository, null);
        if (paramTypes != null) {
            return fw.classHierarchy()
                    .lookupClass(TypeReference.findOrCreate(tref.getClassLoader(), paramTypes.get(0)));
        }
        return null;
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

                    } else if (ref.getName() == Constants.find || ref.getName() == Constants.findAll
                            || ref.getName() == Constants.findById || ref.getName() == Constants.findAllById
                            || ref.getName() == Constants.getOne || ref.getName() == Constants.getById
                            || ref.getName() == Constants.existsById || ref.getName() == Constants.delete
                            || ref.getName() == Constants.deleteAll || ref.getName() == Constants.deleteById) {
                        String table = null;
                        String id = null;
                        IClass typ = getRepoParamterType(fw, tref);
                        if (typ == null) {
                            SSAAbstractInvokeInstruction instr = trace.instrFromSite(site);
                            typ = trace.inferType(fw, instr.getUse(0));
                            if (typ != null) {
                                typ = getRepoParamterType(fw, typ.getReference());
                            }
                        }
                        if (typ != null) {
                            for (IField f : typ.getAllFields()) {
                                FieldReference fref = f.getReference();
                                if (columnDefinitions.containsKey(fref)) {
                                    TableColumn col = columnDefinitions.get(fref);
                                    table = col.tableName;
                                    if (col.tags.contains(Constants.LJavaxPersistenceId)) {
                                        id = col.colName;
                                        break;
                                    }
                                }
                            }
                        }

                        if (table != null) {
                            String exp = "";
                            if (ref.getName() != Constants.findAll && ref.getName() != Constants.deleteAll) {
                                exp = " where " + id + " = ?";
                            }
                            if (ref.getName() == Constants.delete || ref.getName() == Constants.deleteAll
                                    || ref.getName() == Constants.deleteById) {
                                fw.reportSqlStatement(trace, "delete from " + table + exp);
                            } else {
                                fw.reportSqlStatement(trace, "select * from " + table + exp);
                            }
                        } else {
                            Util.LOGGER.info("Couldn't resolve jpa operation: " + ref);
                        }

                    } else if (queryDefinitions.containsKey(ref)) {
                        fw.reportSqlStatement(trace, queryDefinitions.get(ref));

                    } else if (parseQueryCreation(ref, tref, trace, fw)) {
                    } else {
                        Util.LOGGER.info("Couldn't resolve jpa operation: " + ref);
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

    public static String[] CONNECTIVES = new String[] { "And", "Or", "OrderBy" };
    public static String[] OPERATORS = new String[] { "Is", "Equals", "Between", "LessThanEqual", "LessThan",
            "GreaterThanEqual", "GreaterThan", "After", "Before", "IsNull", "IsNotNull", "NotNull", "Like", "NotLike",
            "StartingWith", "EndingWith", "Containing", "NotIn", "Not", "In", "True", "False", "IgnoreCase", "Asc",
            "Desc" };

    public static String[] JPQL_CONNECTIVES = new String[] { "and", "or", "order by" };
    public static String[] JPQL_OPERATORS = new String[] { "= ?", "= ?", "between ? and ?", "<= ?", "< ?", ">= ?",
            "> ?", "> ?", "< ?", "is null", "not null", "not null", "like ?", "not like ?", "like ?", "like ?",
            "like ?", "not in ?", "<> ?", "in ?", "= true", "= false", "<ignorecase>", "asc", "desc" };

    public static boolean parseQueryCreation(MethodReference ref, TypeReference tref, Trace trace, Framework fw) {
        // @See
        // https://docs.spring.io/spring-data/commons/docs/2.3.6.BUILD-SNAPSHOT/reference/html/#repositories.query-methods.query-creation

        String mname = ref.getName().toString();
        if (!mname.contains("By"))
            return false;

        String stmt;
        if (mname.startsWith("find") || mname.startsWith("read") || mname.startsWith("get") || mname.startsWith("query")
                || mname.startsWith("search") || mname.startsWith("stream")) {
            stmt = "select * from";
        } else if (mname.startsWith("exists") || mname.startsWith("count")) {
            stmt = "select count(*) from";
        } else if (mname.startsWith("delete") || mname.startsWith("remove")) {
            stmt = "delete from";
        } else {
            return false;
        }

        String term = mname.substring(mname.indexOf("By") + 2);
        String table = "?";
        String exp = "";

        while (!term.isEmpty()) {
            String field = null;
            int i0 = -1, k0 = -1;
            for (int k = 0; k < CONNECTIVES.length; k++) {
                int i = term.indexOf(CONNECTIVES[k]);
                int i1 = i + CONNECTIVES[k].length();
                if (i1 >= term.length() || !Character.isUpperCase(term.charAt(i1)))
                    continue;
                if (i >= 0 && (i0 < 0 || i < i0)) {
                    i0 = i;
                    k0 = k;
                }
            }
            if (k0 >= 0) {
                field = term.substring(0, i0);
                term = term.substring(i0 + CONNECTIVES[k0].length());
            } else {
                field = term;
                term = "";
            }
            int j0 = -1;
            for (int j = 0; j < OPERATORS.length; j++) {
                if (field.endsWith(OPERATORS[j])) {
                    field = field.substring(0, field.length() - OPERATORS[j].length());
                    j0 = j;
                    break;
                }
            }

            IClass typ = fw.classHierarchy().lookupClass(ref.getReturnType());
            if (typ == null || typ.getName() == Constants.LJavaUtilList) {
                typ = getRepoParamterType(fw, tref);
            }
            TableColumn tcol = null;
            if (typ != null) {
                for (IField f : typ.getDeclaredInstanceFields()) {
                    if (f.getName().toString().equalsIgnoreCase(field)) {
                        if (columnDefinitions.containsKey(f.getReference())) {
                            tcol = columnDefinitions.get(f.getReference());
                            break;
                        }
                    }
                }
            }
            if (tcol != null) {
                if (j0 >= 0) {
                    exp += tcol.colName + " " + JPQL_OPERATORS[j0];
                } else {
                    exp += tcol.colName + " = ?";
                }
                table = tcol.tableName;
            } else if (j0 >= 0) {
                exp += "? " + JPQL_OPERATORS[j0];
            } else {
                exp += "?";
            }
            if (k0 >= 0) {
                exp += " " + JPQL_CONNECTIVES[k0] + " ";
            }
        }

        String sql = stmt + " " + table;
        if (!exp.isEmpty()) {
            sql += " where " + exp;
        }
        fw.reportSqlStatement(trace, sql);
        Util.LOGGER.info("Spring query creation: " + sql);
        return true;
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
            if (v.instr() instanceof SSACheckCastInstruction) {
                v = v.getDef(v.instr().getUse(0));
            }
            break;
        }
        if (v == null)
            return;
        // System.out.println(p + ": " + instr + ": " + v);
        if (v.instr() instanceof SSANewInstruction) {
            TypeReference tref = ((SSANewInstruction) v.instr()).getConcreteType();
            IClass c = fw.classHierarchy().lookupClass(tref);
            populateInsert(fw, trace, c);

        } else if (v.instr() instanceof SSAAbstractInvokeInstruction) {
            IClass repo = trace.inferType(fw, instr.getUse(0));
            if (repo == null) {
                repo = fw.classHierarchy().lookupClass(instr.getDeclaredTarget().getDeclaringClass());
            }
            IClass c = getRepoParamterType(fw, repo.getReference());
            if (c == null) {
                c = trace.inferType(fw, instr.getUse(1));
                if (c == null) {
                    MethodReference mref = ((SSAAbstractInvokeInstruction) v.instr()).getDeclaredTarget();
                    c = fw.classHierarchy().lookupClass(mref.getReturnType());
                }
            }
            if (c != null) {
                populateUpdate(fw, trace, c);
            } else {
                Util.LOGGER.info("Couldn't resolve jpa operation: " + instr.getDeclaredTarget());
            }
        } else {
            Util.LOGGER.info("Couldn't resolve jpa operation: " + instr.getDeclaredTarget());
        }
    }

    public static void populateInsert(Framework fw, Trace trace, IClass c) {
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

    public static void populateUpdate(Framework fw, Trace trace, IClass c) {
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
