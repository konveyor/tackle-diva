package io.tackle.diva.sql;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.TreeMap;
import java.util.function.BiFunction;

public class SqlParse {

    public static class Env extends TreeMap<String, Object> {

    }

    public static class Name implements CharSequence, Comparable<Name> {

        final String s;

        public Name(String s) {
            this.s = s;
        }

        @Override
        public String toString() {
            return s;
        }

        @Override
        public int length() {
            return s.length();
        }

        @Override
        public char charAt(int index) {
            return s.charAt(index);
        }

        @Override
        public CharSequence subSequence(int start, int end) {
            return s.subSequence(start, end);
        }

        @Override
        public int compareTo(Name o) {
            return s.compareTo(o.s);
        }
    }

    public static class Alias extends Name {
        public Alias(String s) {
            super(s);
        }
    }

    public static class Field extends Name {
        public Field(String s) {
            super(s);
        }
        public String prefix() {
            int dot = s.lastIndexOf('.');
            if (dot == -1)
                return "";
            return s.substring(0, dot);
        }
        public String field() {
            int dot = s.lastIndexOf('.');
            if (dot == -1)
                return s;
            return s.substring(dot + 1);
        }
    }

    public static class From extends ArrayList<Object> {
        public From(List<Object> r) {
            addAll(r);
        }
    }

    @SuppressWarnings("serial")
    public static class Result extends ArrayList<Object> {
        public int cursor = -1;
    }

    public static enum Token {
        SELECT, UPDATE, DELETE, INSERT, VALUES;
    }

    static Object[] getEnv(List<Object> r) {
        String key;
        if (r.size() == 2 && r.get(1) instanceof Alias) {
            key = ((Alias) r.remove(1)).toString();
        } else if (r.size() == 1 && r.get(0) instanceof Field) {
            String[] names = ((Field) r.get(0)).toString().split("\\.");
            key = names[names.length - 1];
        } else {
            return r.toArray(new Object[] {});
        }
        Env e = new Env();
        e.put(key, r.get(0));
        return new Object[] { e };
    }

    static Object getToken(String s) {
        try {
            return Token.valueOf(s.toUpperCase());
        } catch (IllegalArgumentException e) {
            return new Name(s);
        }
    }

    @FunctionalInterface
    public interface PegOp {
        Result eval(String text, int s);
    }

    public static Result parse(String text, PegOp op) {
        Result r = op.eval(text, 0);
        if (r == null) {
            r = op.eval(text, 0);
            System.err.println("Parse failed: " + text);
            return null;
        } else if (r.cursor != text.length()) {
            System.err.println("Parse failed: " + text.substring(r.cursor));
            return null;
        }
        return r;
    }

    public static PegOp seq(PegOp... ops) {
        return (text, s) -> {
            Result r = new Result();
            for (PegOp op : ops) {
                if (op == null) {
                    System.out.println("HERE");
                }
                Result r0 = op.eval(text, s);
                if (r0 == null)
                    return null;
                s = r0.cursor;
                r.addAll(r0);
            }
            r.cursor = s;
            return r;
        };
    }

    public static PegOp choice(PegOp... ops) {
        return (text, s) -> {
            Result r = new Result();
            for (PegOp op : ops) {
                Result r0 = op.eval(text, s);
                if (r0 != null)
                    return r0;
            }
            return null;
        };
    }

    public static PegOp val(String val) {
        return (text, s) -> {
            if (!text.regionMatches(s, val, 0, val.length()))
                return null;
            Result r = new Result();
            r.cursor = s + val.length();
            return r;
        };
    }

    public static PegOp match(PegOp op) {
        return (text, s) -> {
            Result r0 = op.eval(text, s);
            if (r0 == null) {
                return null;
            }
            Result r = new Result();
            r.addAll(r0);
            r.cursor = r0.cursor;
            r.add(text.substring(s, r0.cursor));
            return r;
        };
    }

    public static PegOp match(PegOp op, BiFunction<List<Object>, String, Object[]> cons) {
        return (text, s) -> {
            Result r0 = op.eval(text, s);
            if (r0 == null) {
                return null;
            }
            Result r = new Result();
            r.cursor = r0.cursor;
            if (cons == null) {
                r.addAll(r0);
            } else {
                r.addAll(Arrays.asList(cons.apply(r0, text.substring(s, r0.cursor).trim())));
            }
            return r;
        };
    }

    public static PegOp star(PegOp op) {
        return (text, s) -> {
            Result r = new Result();
            while (true) {
                Result r0 = op.eval(text, s);
                if (r0 == null) {
                    r.cursor = s;
                    return r;
                }
                r.addAll(r0);
                s = r0.cursor;
            }
        };
    }

    public static Result nil(String text, int s) {
        Result r = new Result();
        r.cursor = s;
        return r;
    };

    public static Result token0(String text, int k0) {
        for (; k0 < text.length(); k0++) {
            if (!Character.isWhitespace(text.charAt(k0)))
                break;
        }
        if (k0 == text.length())
            return null;
        Result r = new Result();
        String s = null;
        if (k0 + 2 <= text.length() && operator_tokens.contains(s = text.substring(k0, k0 + 2))) {
            r.add(s);
            r.cursor = k0 + 2;
            return r;
        }
        if (k0 + 3 <= text.length() && operator_tokens.contains(s = text.substring(k0, k0 + 3))) {
            r.add(s);
            r.cursor = k0 + 3;
            return r;
        }
        int k = k0 + 1;
        if (Character.isLetter(text.charAt(k0)) || text.charAt(k0) == '_' || text.charAt(k0) == ':'
                || text.charAt(k0) == '?') {
            for (; k < text.length(); k++)
                if (!Character.isLetterOrDigit(text.charAt(k)) && text.charAt(k) != '_'
                        && (text.charAt(k) != '-' || text.charAt(k0) != ':'))
                    break;
        } else if (Character.isDigit(text.charAt(k0)) || text.charAt(k0) == '.') {
            boolean p = text.charAt(k0) == '.';
            for (; k < text.length(); k++)
                if (text.charAt(k) == '.' && p) {
                    break;
                } else if (text.charAt(k) == '.') {
                    p = true;
                } else if (!Character.isDigit(text.charAt(k))) {
                    break;
                }
        } else if (text.charAt(k0) == '\'' || text.charAt(k0) == '"') {
            for (; k < text.length(); k++)
                if (text.charAt(k) == text.charAt(k0)) {
                    k++;
                    break;
                }
        }
        if (k > k0) {
            r.cursor = k;
            r.add(text.substring(k0, k));
            return r;
        }
        return null;
    }

    public static Result token(String text, int s) {
        Result r = token0(text, s);
        if (r != null && reserved_that_can_be_names.contains(r.get(0))) {
            Result r2 = token0(text, r.cursor);
            if (r2 == null || what_only_follow_names.contains(r2.get(0))) {
                r.set(0, "\"" + r.get(0) + "\"");
                return r;
            }
        } else if (r != null && reserved.contains(r.get(0)) && r.cursor < text.length()
                && text.charAt(r.cursor) == '.') {
            r.set(0, "\"" + r.get(0) + "\"");
            return r;
        }
        return r;
    }

    public static Result any(String text, int s) {
        Result r = token(text, s);
        if (r != null) {
            r.clear();
        }
        return r;
    }

    public static PegOp until(String... args) {
        List<String> list = Arrays.asList(args);
        int n = list.indexOf(null);
        if (n >= 0) {
            list = new ArrayList<>(list);
            list.remove(n);
        }
        Set<String> set = new LinkedHashSet<>(list);
        return (text, s) -> {
            while (true) {
                Result t = token(text, s);
                if (t == null) {
                    if (n >= 0) {
                        Result r = new Result();
                        r.cursor = s;
                        return r;
                    } else {
                        return null;
                    }
                }
                if (set.contains(t.get(0))) {
                    Result r = new Result();
                    r.cursor = s;
                    return r;
                }
                s = t.cursor;
            }
        };
    }

    public static PegOp before(String... args) {
        // TODO Auto-generated method stub
        return null;
    }

    public static Result name(String text, int s) {
        Result r = token(text, s);
        if (r == null || reserved.contains(r.get(0)))
            return null;
        char c = ((String) r.get(0)).charAt(0);
        if (c == '_' || Character.isLetter(c) || c == '"') {
            r.clear();
            return r;
        }
        return null;
    }

    public static Result variable0(String text, int s) {
        Result r = token(text, s);
        if (r == null)
            return null;
        char c = ((String) r.get(0)).charAt(0);
        if (c == ':' || c == '?') {
            r.clear();
            return r;
        }
        return null;
    }

    public static Result literal(String text, int s) {
        Result r = token(text, s);
        if (r == null)
            return null;
        char c = ((String) r.get(0)).charAt(0);
        if (c == '\'' || r.get(0).equals("null") || Character.isDigit(c)
                || c == '.' && ((String) r.get(0)).length() > 1) {
            r.clear();
            return r;
        }
        return null;
    }

    public static PegOp op(String val) {
        return (text, s) -> {
            Result r = token(text, s);
            if (r == null)
                return null;
            if (r.get(0).equals(val)) {
                r.clear();
                return r;
            }
            return null;
        };
    }

    // -- auto-generated code starts --
    public static final Set<String> reserved = new LinkedHashSet<>(Arrays.asList(new String[] { "as", "by", "in", "on",
            "asc", "all", "end", "set", "from", "left", "join", "full", "desc", "case", "when", "then", "else", "into",
            "where", "group", "inner", "outer", "order", "right", "union", "except", "select", "update", "delete",
            "insert", "null", "having", "listagg", "within", "current", "fetch", "concat", "nextval", "for", "and",
            "or", "is", "not", "like", "escape", "partition", "exists", "top", "using", ":_where_in", ":_where_and",
            ":_where_or", ":_in", ":_or", ":_and" }));
    public static final Set<String> reserved_that_can_be_names = new LinkedHashSet<>(
            Arrays.asList(new String[] { "as", "by", "in", "on", "all", "set", "from", "left", "join", "full", "when",
                    "then", "else", "where", "group", "inner", "outer", "order", "right", "union", "except", "select",
                    "delete", "insert", "listagg", "within", "current", "fetch", "concat", "for", "partition" }));
    public static final Set<String> what_only_follow_names = new LinkedHashSet<>(
            Arrays.asList(new String[] { ")", ",", "as", "in", "on", "where", "then", "else", "inner" }));
    public static final Set<String> operator_tokens = new LinkedHashSet<>(
            Arrays.asList(new String[] { "||", "<=", ">=", "<>", "!=", "(+)", "=*", "*=" }));
    public static final PegOp qname = seq(SqlParse::name, star(seq(op("."), SqlParse::name)),
            choice(seq(op("@"), SqlParse::name), SqlParse::nil));
    public static final PegOp paren = seq(op("("), star(seq(until("(", ")"), (t, s) -> SqlParse.paren.eval(t, s))),
            until("(", ")"), op(")"));
    public static final PegOp variable = choice(
            SqlParse::variable0, seq(
                    op("#"), op("{"), qname, choice(
                            seq(op(","),
                                    seq(seq(SqlParse::name, op("="), SqlParse::name),
                                            star(seq(op(","), seq(SqlParse::name, op("="), SqlParse::name))))),
                            SqlParse::nil),
                    op("}")));
    public static final PegOp func = choice(qname, variable, op("left"), op("right"), op("concat"));
    public static final PegOp callargs = choice(
            seq(seq(choice(choice(op("distinct"), op("all")), SqlParse::nil), choice(
                    (t, s) -> SqlParse.colexp.eval(t, s), match(op("*"), (r, v) -> new Object[] { new Field(v) }))),
                    star(seq(op(","),
                            seq(choice(choice(op("distinct"), op("all")), SqlParse::nil),
                                    choice((t, s) -> SqlParse.colexp.eval(t, s),
                                            match(op("*"), (r, v) -> new Object[] { new Field(v) })))))),
            SqlParse::nil);
    public static final PegOp callexp = choice(
            seq(op("listagg"), op("("), callargs, op(")"),
                    choice(seq(op("within"), op("group"), paren), SqlParse::nil)),
            seq(op("cast"), op("("), (t, s) -> SqlParse.colexp.eval(t, s), op("as"),
                    seq(star(seq(until("(", ")", ")"), paren)), until("(", ")", ")"), until(")")), op(")")),
            seq(func, op("("), callargs, op(")"), choice(seq(op("over"), paren), SqlParse::nil)));
    public static final PegOp caseexp = seq(
            op("case"), choice((t, s) -> SqlParse.colexp.eval(t, s), SqlParse::nil), seq(
                    seq(op("when"),
                            seq(star(seq(until("(", ")", "then"), paren)), until("(", ")", "then"), until("then")),
                            op("then"), (t, s) -> SqlParse.colexp.eval(t, s)),
                    star(seq(op("when"),
                            seq(star(seq(until("(", ")", "then"), paren)), until("(", ")", "then"), until("then")),
                            op("then"), (t, s) -> SqlParse.colexp.eval(t, s)))),
            choice(seq(op("else"), (t, s) -> SqlParse.colexp.eval(t, s)), SqlParse::nil), op("end"));
    public static final PegOp colexp0 = choice(SqlParse::literal,
            seq(match(variable, (r, v) -> new Object[] { new Field(v) }),
                    choice(seq(op("indicator"), variable), SqlParse::nil)),
            seq(op("current"), SqlParse::name), callexp, caseexp,
            seq(op("("),
                    seq((t, s) -> SqlParse.colexp.eval(t, s), star(seq(op(","), (t, s) -> SqlParse.colexp.eval(t, s)))),
                    op(")")),
            (t, s) -> SqlParse.nestedexp.eval(t, s),
            match(seq(SqlParse::name, op("."), op("*")), (r, v) -> new Object[] { new Field(v) }),
            seq(choice(seq(op("nextval"), op("for")), SqlParse::nil),
                    match(qname, (r, v) -> new Object[] { new Field(v) }),
                    choice(seq(op("."), op("nextval")), SqlParse::nil)),
            seq(op("set"), op("("), (t, s) -> SqlParse.colexp.eval(t, s), op(")")));
    public static final PegOp binaryexp = seq(colexp0,
            choice(op("+"), op("-"), op("*"), op("/"), op("||"), op("concat")), (t, s) -> SqlParse.colexp.eval(t, s));
    public static final PegOp naryexp = choice(seq(op("-"), (t, s) -> SqlParse.colexp.eval(t, s)), binaryexp);
    public static final PegOp colexp = choice(naryexp, colexp0);
    public static final PegOp colexp1 = match(match(
            seq(colexp,
                    choice(seq(choice(op("as"), SqlParse::nil),
                            match(SqlParse::name, (r, v) -> new Object[] { new Alias(v) })), SqlParse::nil)),
            (r, v) -> getEnv(r)), (r, v) -> getEnv(r));
    public static final PegOp colsexp = choice(seq(colexp1, star(seq(op(","), colexp1))),
            match(op("*"), (r, v) -> new Object[] { new Field(v) }));
    public static final PegOp jointype = seq(
            choice(seq(choice(op("left"), op("right"), op("full")), choice(op("outer"), SqlParse::nil)), op("inner"),
                    SqlParse::nil),
            op("join"), choice(op("fetch"), SqlParse::nil));
    public static final PegOp joincond = seq(op("on"), (t, s) -> SqlParse.condexp.eval(t, s));
    public static final PegOp tblexp = choice(
            seq(match(qname, (r, v) -> new Object[] { getToken(v) }),
                    choice(seq(op("partition"), op("("), SqlParse::name, op(")")), SqlParse::nil)),
            (t, s) -> SqlParse.nestedexp.eval(t, s), seq(op("("), (t, s) -> SqlParse.tblsexp.eval(t, s), op(")")));
    public static final PegOp tblsexp = match(
            seq(match(
                    seq(tblexp,
                            choice(seq(
                                    choice(op("as"), SqlParse::nil), match(SqlParse::name,
                                            (r, v) -> new Object[] { new Alias(v) })),
                                    SqlParse::nil)),
                    (r, v) -> getEnv(r)),
                    star(choice(
                            seq(op(","),
                                    match(seq(
                                            tblexp, choice(
                                                    seq(choice(op("as"), SqlParse::nil),
                                                            match(SqlParse::name,
                                                                    (r, v) -> new Object[] { new Alias(v) })),
                                                    SqlParse::nil)),
                                            (r, v) -> getEnv(r))),
                            seq(jointype,
                                    match(seq(
                                            tblexp, choice(
                                                    seq(choice(op("as"), SqlParse::nil),
                                                            match(SqlParse::name,
                                                                    (r, v) -> new Object[] { new Alias(v) })),
                                                    SqlParse::nil)),
                                            (r, v) -> getEnv(r)),
                                    choice(joincond, SqlParse::nil))))),
            (r, v) -> new Object[] { new From(r) });
    public static final PegOp nestedexp = seq(op("("),
            choice(match((t, s) -> SqlParse.selexp.eval(t, s), (r, v) -> new Object[] { r }),
                    match((t, s) -> SqlParse.valuesexp.eval(t, s), (r, v) -> new Object[] { r }),
                    (t, s) -> SqlParse.nestedexp.eval(t, s)),
            op(")"));
    public static final PegOp colexp2 = choice(seq(qname, op("(+)")), colexp);
    public static final PegOp condexp = seq(
            choice(seq(op("("), (t, s) -> SqlParse.condexp.eval(t, s), op(")")),
                    seq(op("not"), (t, s) -> SqlParse.condexp.eval(t, s)), seq(op("exists"), choice(colexp, nestedexp)),
                    seq(colexp2, choice(
                            seq(choice(op("="), op("<"), op(">"), op("<="), op(">="), op("<>"), op("!="), op("*="),
                                    op("=*"), seq(op("is"), choice(op("not"), SqlParse::nil))), colexp2),
                            seq(choice(op("not"), SqlParse::nil),
                                    choice(seq(op("in"), choice(colexp, nestedexp)),
                                            seq(op("like"), colexp, choice(seq(op("escape"), colexp), SqlParse::nil)),
                                            seq(op("between"), colexp, op("and"), colexp))),
                            variable)),
                    seq(choice(op(":_where_and"), op(":_or"), op(":_and")), op("("),
                            seq((t, s) -> SqlParse.condexp.eval(t, s),
                                    star(seq(op(","), (t, s) -> SqlParse.condexp.eval(t, s)))),
                            op(")")),
                    seq(op(":_in"), op("("), qname, choice(op("="), SqlParse::nil), variable, op(")")),
                    seq(op("current"), op("of"), choice(colexp, nestedexp)), callexp),
            choice(seq(choice(op("and"), op("or")), (t, s) -> SqlParse.condexp.eval(t, s)), SqlParse::nil));
    public static final PegOp whrexp = choice(seq(op("where"), condexp), seq(
            choice(seq(op(":_where_in"), colexp),
                    seq(choice(op(":_where_and"), op(":_where_or")), op("("), choice(condexp, SqlParse::nil),
                            star(seq(choice(op(","), SqlParse::nil), choice(condexp, variable))), op(")"))),
            choice(seq(choice(op("and"), op("or")), condexp), SqlParse::nil)));
    public static final PegOp havingexp = seq(op("having"), condexp);
    public static final PegOp grpexp = seq(op("group"), op("by"),
            seq(choice(qname, variable), star(seq(op(","), colexp))));
    public static final PegOp orderexp = seq(op("order"), op("by"),
            seq(seq(colexp, choice(choice(op("asc"), op("desc")), SqlParse::nil)),
                    star(seq(op(","), seq(colexp, choice(choice(op("asc"), op("desc")), SqlParse::nil))))));
    public static final PegOp assignexp = match(seq(
            choice(match(qname, (r, v) -> new Object[] { new Field(v) }), seq(op("("),
                    seq(match(qname, (r, v) -> new Object[] { new Field(v) }),
                            star(seq(op(","), match(qname, (r, v) -> new Object[] { new Field(v) })))),
                    op(")"))),
            op("="), colexp), (r, v) -> new Object[] { r });
    public static final PegOp assignsexp = seq(assignexp, star(seq(op(","), assignexp)));
    public static final PegOp frmspec = seq(tblsexp, choice(whrexp, SqlParse::nil), choice(grpexp, SqlParse::nil),
            choice(havingexp, SqlParse::nil), choice(orderexp, SqlParse::nil), choice(variable, SqlParse::nil),
            choice(seq(op("fetch"), op("first"), choice(SqlParse::literal, variable, SqlParse::nil), op("rows"),
                    op("only")), SqlParse::nil),
            choice(seq(op("for"), op("update"),
                    choice(op("nowait"), seq(op("wait"), SqlParse::literal), seq(op("with"), op("rs")), SqlParse::nil)),
                    SqlParse::nil),
            choice(seq(op("with"), op("ur")), SqlParse::nil));
    public static final PegOp selexp = withcxt(unioncxt(seq(match(op("select"), (r, v) -> new Object[] { getToken(v) }),
            choice(op("distinct"), SqlParse::nil), choice(seq(op("top"), SqlParse::literal), SqlParse::nil), colsexp,
            choice(op(","), SqlParse::nil), choice(seq(op("into"), colsexp), SqlParse::nil), op("from"), frmspec)));
    public static final PegOp updexp = withcxt(seq(match(op("update"), (r, v) -> new Object[] { getToken(v) }),
            match(seq(match(
                    seq(match(qname, (r, v) -> new Object[] { getToken(v) }),
                            choice(seq(choice(op("as"), SqlParse::nil),
                                    match(SqlParse::name, (r, v) -> new Object[] { new Alias(v) })), SqlParse::nil)),
                    (r, v) -> getEnv(r)), op("set"), assignsexp), (r, v) -> new Object[] { new From(r) }),
            choice(whrexp, SqlParse::nil)));
    public static final PegOp valuesexp = seq(match(op("values"), (r, v) -> new Object[] { getToken(v) }), op("("),
            seq(match(colexp, (r, v) -> new Object[] { r }),
                    star(seq(op(","), match(colexp, (r, v) -> new Object[] { r })))),
            op(")"));
    public static final PegOp insexp = withcxt(seq(match(op("insert"), (r, v) -> new Object[] { getToken(v) }),
            op("into"),
            match(seq(
                    match(seq(match(qname, (r, v) -> new Object[] { getToken(v) }),
                            choice(seq(choice(op("as"), SqlParse::nil),
                                    match(SqlParse::name, (r, v) -> new Object[] { new Alias(v) })), SqlParse::nil)),
                            (r, v) -> getEnv(r)),
                    choice(seq(op("("),
                            seq(match(qname, (r, v) -> new Object[] { new Field(v) }),
                                    star(seq(op(","), match(qname, (r, v) -> new Object[] { new Field(v) })))),
                            op(")")), SqlParse::nil)),
                    (r, v) -> new Object[] { new From(r) }),
            choice(valuesexp, selexp)));
    public static final PegOp delexp = withcxt(seq(match(op("delete"), (r, v) -> new Object[] { getToken(v) }),
            choice(op("from"), SqlParse::nil),
            match(match(
                    seq(match(qname, (r, v) -> new Object[] { getToken(v) }),
                            choice(seq(choice(op("as"), SqlParse::nil),
                                    match(SqlParse::name, (r, v) -> new Object[] { new Alias(v) })), SqlParse::nil)),
                    (r, v) -> getEnv(r)), (r, v) -> new Object[] { new From(r) }),
            choice(whrexp, SqlParse::nil)));
    public static final PegOp mergeexp = seq(match(op("merge"), (r, v) -> new Object[] { getToken(v) }), op("into"),
            match(seq(match(
                    seq(match(qname, (r, v) -> new Object[] { getToken(v) }),
                            choice(seq(choice(op("as"), SqlParse::nil),
                                    match(SqlParse::name, (r, v) -> new Object[] { new Alias(v) })), SqlParse::nil)),
                    (r, v) -> getEnv(r))), (r, v) -> new Object[] { new From(r) }),
            op("using"), star(SqlParse::any));
    public static final PegOp sqlexp = seq(choice(selexp, updexp, insexp, delexp, valuesexp, mergeexp),
            choice(op(";"), SqlParse::nil));

    public static PegOp unioncxt(PegOp e) {
        PegOp[] fix = new PegOp[] { null };
        fix[0] = seq(choice(e, seq(op("("), choice(e, (t, s) -> fix[0].eval(t, s)), op(")"))),
                star(seq(choice(seq(op("union"), choice(op("all"), SqlParse::nil)), op("except")),
                        match(choice(e, seq(op("("), choice(e, (t, s) -> fix[0].eval(t, s)), op(")"))),
                                (r, v) -> new Object[] { r }))),
                choice(grpexp, SqlParse::nil), choice(orderexp, SqlParse::nil));
        return fix[0];
    }

    public static PegOp withcxt(PegOp e) {
        PegOp[] fix = new PegOp[] { null };
        fix[0] = choice(
                seq(op("with"), seq(
                        seq(SqlParse::name,
                                choice(seq(op("("), seq(SqlParse::name, star(seq(op(","), SqlParse::name))), op(")")),
                                        SqlParse::nil),
                                op("as"), nestedexp),
                        star(seq(op(","),
                                seq(SqlParse::name, choice(
                                        seq(op("("), seq(SqlParse::name, star(seq(op(","), SqlParse::name))), op(")")),
                                        SqlParse::nil), op("as"), nestedexp)))),
                        e),
                e);
        return fix[0];
    }
    // -- auto-generated code ends --

    public static void main(String[] args) {
        System.out.println(parse("abc", seq(val("a"), match(val("b")), val("c"))));
        System.out.println(parse("abc", star(choice(val("a"), val("b"), val("c")))));
        System.out.println(parse("abc", star(val("a"))));

        System.out.println(token(" <=", 0));
        System.out.println(seq(SqlParse::name, op("<="), SqlParse::name).eval("a <= b", 0));
        System.out.println(token(" :abc ", 0));
        System.out.println(tblsexp.eval("a as b", 0));
        System.out.println(parse("select * from s, (select * from t, u) where a >= b", sqlexp));
        System.out.println(parse("select * from s where a = 'a'", sqlexp));
        System.out.println(parse(
                "select dept, listagg(name, ',') within group (order by saraly desc nulls last, a asc) csv_name from listagg_sample group by dept",
                sqlexp));
        System.out.println(
                parse("update accountejb set lastLogin=?, logincount=logincount+1 where profile_userid=?", sqlexp));
        System.out.println(
                parse("select a as x from b t left outer join ( select * from d ) u on t.i = u.i, e w", sqlexp));

    }

}
