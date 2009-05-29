# compress js files, generate docs

all: docs

docs: webnote.js objects.js
	mkdir -p docs/jsdoc
	jsdoc -d docs/jsdoc --project-name Webnote --project-summary docs/summary.txt *.js
