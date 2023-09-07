package io.tackle.diva.sql;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.function.Consumer;

import com.ibm.wala.util.collections.Pair;

import io.tackle.diva.sql.SqlParse.Env;
import io.tackle.diva.sql.SqlParse.Field;
import io.tackle.diva.sql.SqlParse.From;
import io.tackle.diva.sql.SqlParse.Name;
import io.tackle.diva.sql.SqlParse.Result;

public class SqlProc {

    /*
     * NOTE: SQL has two types of aliases, table aliases, and column aliases.
     *
     * Context c maps table-alias to a pair (fst, snd), where fst is a set of
     * concrete tables to which the table-alias may be mapped, and snd is a mapping
     * from column-alias to resolved column.
     */

    public static interface AliasContext extends Map<String, Pair<Set<Name>, Map<String, Field>>> {
        public default void update(String k, Consumer<Pair<Set<Name>, Map<String, Field>>> upd) {
            this.compute(k, (__, p) -> {
                if (p == null)
                    p = Pair.make(new TreeSet<>(), new TreeMap<>());
                upd.accept(p);
                return p;
            });
        }
    };

    public static class AliasContextImpl extends TreeMap<String, Pair<Set<Name>, Map<String, Field>>>
            implements AliasContext {
        public AliasContextImpl() {
            update("", p -> {
            });
        }
    }

    public static AliasContext cxt(List<Object> a, AliasContext c0) {

        AliasContext c = new AliasContextImpl();

        for (Object w : a) {
            if (!(w instanceof From))
                continue;

            for (Object v : (From) w) {
                if (v instanceof Name && !(v instanceof Field)) {
                    c.update(v.toString(), p -> {
                        p.fst.add((Name) v);
                    });

                } else if (v instanceof Env) {
                    // aliased table reference
                    Map.Entry<String, Object> e = ((Env) v).entrySet().iterator().next();
                    if (e.getValue() instanceof Name && !(e.getValue() instanceof Field)) {
                        c.update(e.getKey(), p -> {
                            p.fst.add((Name) e.getValue());
                        });

                    } else if (e.getValue() instanceof Result) {
                        // nested select ..
                        Map<String, Pair<Set<Name>, Map<String, Field>>> c2 = cxt((Result) e.getValue(), null);
                        c.update(e.getKey(), p -> {
                            p.fst.addAll(c2.get("").fst);
                            p.snd.putAll(c2.get("").snd);
                        });
                    }

                } else if (v instanceof Result) {

                }
            }
        }

        for (String k : c.keySet()) {
            c.update("", p -> {
                p.fst.addAll(c.get(k).fst);
                p.snd.putAll(c.get(k).snd);
            });
        }

        // TODO: handle mapping

        // handle column aliases
        for (Object v : a) {
            if (!(v instanceof Env))
                continue;
            Map.Entry<String, Object> e = ((Env) v).entrySet().iterator().next();
            if (e.getValue() instanceof Field) {
                Field f = (Field) e.getValue();
                if (f.field().equals("?"))
                    continue;
                if (c.containsKey(f.prefix()) && c.get(f.prefix()).snd.containsKey(f.field())) {
                    c.get("").snd.put(e.getKey(), c.get(f.prefix()).snd.get(f.field()));

                } else if (c.containsKey(f.prefix()) && c.get(f.prefix()).fst.size() == 1) {
                    c.get("").snd.put(e.getKey(), new Field(c.get(f.prefix()).fst.iterator().next() + "." + f.field()));
                } else {
                    c.get("").snd.put(e.getKey(), new Field("???." + f.field()));
                }
            }
        }

        // handle outer context c0
        if (c0 != null) {
            for (String k : c0.keySet()) {
                if (/* !k.equals("") && */ c.containsKey(k))
                    continue;
                c.update(k, p -> {
                    p.fst.addAll(c0.get(k).fst);
                    p.snd.putAll(c0.get(k).snd);
                });
            }
        }
        return c;
    }

    public static boolean isVariable(String s) {
        if (s.startsWith(":"))
            return true;
        if (s.startsWith("?"))
            return true;
        return false;
    }

    public static List<Object> resolve(List<Object> a, AliasContext c) {
        c = cxt(a, c);

        List<Object> r = new ArrayList<>();
        for (Object v : a) {
            if (v instanceof Env) {
                v = ((Env) v).values().iterator().next();
            }

            if (v instanceof List) {
                r.add(resolve((List<Object>) v, c));

            } else if (v instanceof Field) {
                Field f = (Field) v;
                if (isVariable(f.field()))
                    continue;
                if (c.containsKey(f.prefix())) {
                    Pair<Set<Name>, Map<String, Field>> x = c.get(f.prefix());
                    if (x.snd.containsKey(f.field())) {
                        r.add(x.snd.get(f.field()));

                    } else if (x.fst.size() == 1) {
                        r.add(new Field(x.fst.iterator().next() + "." + f.field()));

                    } else if (f.field().equals("*")) {
                        for (Name n : x.fst) {
                            r.add(new Field(n + ".*"));
                        }

                    } else {
                        r.add(new Field("???." + f.field()));
                    }

                } else {
                    r.add(new Field("???." + f.field()));
                }
            } else {
                r.add(v);
            }

        }
        return r;

    }

    public static void main(String[] args) {
        Result r = SqlParse.parse("select a as x from b t left outer join ( select * from d ) u on t.i = u.i, e w",
                SqlParse.sqlexp);
        System.out.println(r);
        System.out.println(resolve(r, null));
    }

}
