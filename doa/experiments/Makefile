cm-single:
	@echo "writing single SQL file to ConfigMap manifest..."
	kubectl create cm sql-single --from-file=./trading_ddl/schema.sql \
    	--dry-run=client -o yaml > cm-sql-single.yaml

cm-multi:
	@echo "writing multi SQL files to ConfigMap manifest..."
	kubectl create cm sql-multi --from-file=./trading_ddl \
    	--dry-run=client -o yaml > cm-sql-multi.yaml
