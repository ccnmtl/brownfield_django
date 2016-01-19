APP=brownfield_django
#JS_FILES=media/js/ccnmtljs
# most of the JS isn't close to jshint/jscs clean, but we need to target
# something for now
JS_FILES=media/js/ccnmtljs/bb_models.js
MAX_COMPLEXITY=8

all: jenkins

include *.mk
