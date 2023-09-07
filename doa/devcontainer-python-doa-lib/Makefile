#
# Commands for test of semantic verification and other toolchain pipeline.
#
# Note: "cd" this directory and run targets!
#
ORACLE_DIR=./0.in-oracle
PREPROCESSED_DIR=./1.preprocessed
SPLIT_DIR=./2.splitted
ANAL_BEFORE_DIR=./3.analysis-before
POSTGRES_DIR=./4.out-postgres
SYN_VERIFY_DIR=./5.syntax-verification
SEM_VERIFY_DIR=./6.semantics-verification
CASE_A_DIR=./a.results

# toolchain tests
all: case-a

clean:
	rm -rf $(PREPROCESSED_DIR) $(SPLIT_DIR) $(ANAL_BEFORE_DIR) $(POSTGRES_DIR) \
		$(SYN_VERIFY_DIR) $(SEM_VERIFY_DIR) $(CASE_A_DIR)

# run whole toolchain
case-a-clean:
	rm -rf $(CASE_A_DIR)

case-help:
	python -m sqal.cli --help

case-a: case-a-clean
	python -m doa.cli --convert -n northwind -i $(ORACLE_DIR) -o $(CASE_A_DIR)

case-a-wo-rules: case-a-clean
	python -m sqal.cli --convert -n northwind -i $(ORACLE_DIR) -o $(CASE_A_DIR) --no-use-rules

case-a-v: case-a-clean
	python -m sqal.cli --convert -n northwind -i $(ORACLE_DIR) -o $(CASE_A_DIR) -v

case-a-dump:
	python -m sqal.verification.syntax dump -i $(CASE_A_DIR)

# tests for each component

components: split analyze-before convert copy-after-convert syntax-verify semantics-verify

split:
	rm -rf $(SPLIT_DIR)
	python -m sqal.analysis.split \
	-i $(ORACLE_DIR) \
	-o $(SPLIT_DIR)

split-v:
	rm -rf $(SPLIT_DIR)
	python -m sqal.analysis.split \
	-i $(ORACLE_DIR) \
	-o $(SPLIT_DIR) \
	-v 

split-vv:
	rm -rf $(SPLIT_DIR)
	python -m sqal.analysis.split \
	-i $(ORACLE_DIR) \
	-o $(SPLIT_DIR) \
	-vv

analyze-before:
	python -m sqal.analysis.from_source -n northwind \
	-i $(SPLIT_DIR) \
	-o $(ANAL_BEFORE_DIR)

analyze-before-v:
	python -m sqal.analysis.from_source -n northwind \
	-i $(SPLIT_DIR) \
	-o $(ANAL_BEFORE_DIR) \
	-v

analyze-before-vv:
	python -m sqal.analysis.from_source -n northwind \
	-i $(SPLIT_DIR) \
	-o $(ANAL_BEFORE_DIR) \
	-vv

convert:
	python -m sqal.doa -n northwind -i $(SPLIT_DIR) -o $(POSTGRES_DIR)

convert-v:
	python -m sqal.doa -n northwind -i $(SPLIT_DIR) -o $(POSTGRES_DIR) -v 

convert-vv:
	python -m sqal.doa -n northwind -i $(SPLIT_DIR) -o $(POSTGRES_DIR) -vv 

# execute after conversion and before syntax analysis.
copy-after-convert:
	cp $(ANAL_BEFORE_DIR)/schema-info.yaml $(POSTGRES_DIR)

syntax-verify:
	python -m sqal.verification.syntax run -i $(POSTGRES_DIR) -o $(SYN_VERIFY_DIR)

syntax-verify-v:
	python -m sqal.verification.syntax run -i $(POSTGRES_DIR) -o $(SYN_VERIFY_DIR) -v

syntax-verify-vv:
	python -m sqal.verification.syntax run -i $(POSTGRES_DIR) -o $(SYN_VERIFY_DIR) -vv

dump-syntax-result:
	python -m sqal.verification.syntax dump -i $(SYN_VERIFY_DIR)

dump-syntax-result-all:
	python -m sqal.verification.syntax dump -i $(SYN_VERIFY_DIR) --all

# semantic analysis

semantics-verify:
	python -m sqal.verification.semantics -i $(POSTGRES_DIR) -o $(SEM_VERIFY_DIR)

semantics-verify-v:
	python -m sqal.verification.semantics -i $(POSTGRES_DIR) -o $(SEM_VERIFY_DIR) -v

semantics-verify-vv:
	python -m sqal.verification.semantics -i $(POSTGRES_DIR) -o $(SEM_VERIFY_DIR) -vv

# extra: test of preprocess.py
#   actually preprocess is incorporated into another process.
#   so you do not need to run this by yourself.
preprocess:
	rm -rf $(PREPROCESSED_DIR)
	python -m sqal.preprocess -i $(ORACLE_DIR) -o $(PREPROCESSED_DIR) 

preprocess-v:
	python -m sqal.preprocess -i $(ORACLE_DIR) -o $(PREPROCESSED_DIR) -v

preprocess-vv:
	python -m sqal.preprocess -i $(ORACLE_DIR) -o $(PREPROCESSED_DIR) -f Oracle_Northwind_1_CreateObjects.sql -vv

preprocess-s:
	python -m sqal.preprocess -i $(ORACLE_DIR) -o $(PREPROCESSED_DIR) -f Oracle_Northwind_1_CreateObjects.sql -s
