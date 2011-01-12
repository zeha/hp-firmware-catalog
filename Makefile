download: catalog.json
	python download_fw.py

catalog.json: catalog2json_english_rhel.xsl catalog.xml
	xsltproc -o catalog.json catalog2json_english_rhel.xsl catalog.xml

catalog.xml:
	curl -v -f -o catalog.xml -z catalog.xml ftp://ftp.hp.com/pub/softlib/software2/COL3293/catalog.xml

clean: 
	-rm catalog.xml catalog.json

.PHONY: clean catalog.xml

