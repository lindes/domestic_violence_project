corpus/%.txt : reddit/%.json Makefile
	jq -r .title,.selftext $< > $@

default: $(patsubst reddit/%.json,corpus/%.txt,$(wildcard reddit/*.json))
