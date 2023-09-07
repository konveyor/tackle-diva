#
# Commands for test of semantic verification and other toolchain pipeline.
#
# Note: "cd" this directory and run targets!
#
ORACLE_DIR=./tests/0.in-oracle
CASE_A_DIR=/tmp/a.results
LOCAL_OUT_DIR=./output

clean:
	rm -rf $(CASE_A_DIR) $(LOCAL_OUT_DIR)

distclean:
	find doa -name __pycache__ | xargs rm -rf 
	find doa -name .pytest_cache | xargs rm -rf 
	find tests -name __pycache__ | xargs rm -rf 
	find tests -name .pytest_cache | xargs rm -rf 

test-install:
	python -m doa.cli --help

# normal test
test: clean
	python -m doa.cli -n northwind -i $(ORACLE_DIR) -o $(CASE_A_DIR)

# if you need verbose mode (w/ INFO level logs)
test-v: clean
	python -m doa.cli -n northwind -i $(ORACLE_DIR) -o $(CASE_A_DIR) -v

# if you need more verbose mode (w/ DEBUG level logs)
test-vv: clean
	python -m doa.cli -n northwind -i $(ORACLE_DIR) -o $(CASE_A_DIR) -vv


# if you want generated files be in this directory

clean-local:
	rm -rf $(LOCAL_OUT_DIR)

test-local: clean-local
	python -m doa.cli -n northwind -i $(ORACLE_DIR) -o $(LOCAL_OUT_DIR)

# if you need verbose mode (w/ INFO level logs)
test-local-v: clean-local
	python -m doa.cli -n northwind -i $(ORACLE_DIR) -o $(LOCAL_OUT_DIR) -v

# if you need more verbose mode (w/ DEBUG level logs)
test-local-vv: clean-local
	python -m doa.cli -n northwind -i $(ORACLE_DIR) -o $(LOCAL_OUT_DIR) -vv
