.PHONY: parser grun-tokens

# Run just after the container starts.
# check installation of ANTLR: show usage
test:
	java org.antlr.v4.Tool

# delete intermediate and generated files
clean:
	rm -rf plsql in/.antlr examples/gen examples/out

#
# Generate Python binding of PL/SQL parser.
#
gen: clean
	mkdir -p plsql
	cp in/* plsql
	java org.antlr.v4.Tool -Dlanguage=Python3 -listener -visitor plsql/PlSqlLexer.g4
	java org.antlr.v4.Tool -Dlanguage=Python3 -listener -visitor plsql/PlSqlParser.g4



#
# Some example using a toy grammar.
#

# generate parser and other artifacts source.
examples/gen/HelloParser.java: examples/in/Hello.g4
	java org.antlr.v4.Tool -listener -visitor -Xexact-output-dir -o examples/gen $^

# alias
parser-src: examples/gen/HelloParser.java

# complie parser
examples/out/HelloParser.class: parser-src
	javac -d examples/out examples/gen/*.java

# alias
parser: examples/out/HelloParser.class

#
# Use of TestRig
# Dockerfile defines CLASSPATH as /usr/local/lib/antlr-4.10-complete.jar.
#

# show token sequences
grun-tokens: examples/out/HelloParser.class
	CLASSPATH=./examples/out:$(CLASSPATH) bash -c "echo \"hello test\" | java org.antlr.v4.gui.TestRig Hello r -tokens"

# show parse tree S-exp.
grun-tree: examples/out/HelloParser.class
	CLASSPATH=./examples/out:$(CLASSPATH) bash -c "echo \"hello test\" | java org.antlr.v4.gui.TestRig Hello r -tree"

# show parse tree S-exp, for another grammar rule (expr).
grun-tree2: examples/out/HelloParser.class
	CLASSPATH=./examples/out:$(CLASSPATH) bash -c "echo 1+2*3 | java org.antlr.v4.gui.TestRig Hello expr -tree"
	CLASSPATH=./examples/out:$(CLASSPATH) bash -c "echo 1*2+3 | java org.antlr.v4.gui.TestRig Hello expr -tree"
