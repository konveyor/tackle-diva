.PHONY: parser grun-tokens

# Run just after the container starts.
# check installation of ANTLR: show usage
test:
	java org.antlr.v4.Tool

test-testrig:
	java org.antlr.v4.gui.TestRig --help

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
# Generate Java (= default) binding of PL/SQL parser.
# Class files are generated in ${root}/plsql-java/clz.
gen-java:
	rm -rf plsql-java
	mkdir -p plsql-java
	java org.antlr.v4.Tool -Xexact-output-dir -o plsql-java in/PlSqlLexer.g4 in/PlSqlParser.g4
	cp org-java/*.java plsql-java
	javac -d plsql-java/clz plsql-java/*.java

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

#
# Other tests
#
test-color:
	bash -c 'for i in $(seq 0 15); do echo ${i}; done'