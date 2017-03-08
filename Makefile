APP=brownfield_django
JS_FILES=media/js/ccnmtljs
MAX_COMPLEXITY=5

all: jenkins

include *.mk

eslint: $(JS_SENTINAL)
	$(NODE_MODULES)/.bin/eslint $(JS_FILES)

.PHONY: eslint
