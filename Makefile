define compile=
	mkdir -p ./out
	python ./quiz-generator.py -t $1 -o ./out/$2.tex -r $3
	(cd ./out; pdflatex $2)
endef

all: cumulative exam02

cumulative:
	$(call compile,"Cumulative Review",cumulative-review,./in/math-151/*)

# Exam 2: Sections 8.1 to 8.8, Quizes 3 and 4
exam02:
	$(eval files=./in/math-151/{section-08-{01,02,03,04,05,06,08},quiz{03,04},exam02-studyguide}.qs)
	$(call compile,"Exam 2 Review",exam02-review,$(files))

.PHONY: h help clean

help:
	@echo -e "targets:\n"\
	         "  h,help   show this message\n"\
	         "  all      generate LaTeX quiz\n"\
	         "  readme   update project README.md"

h: help

clean:
	rm ./out/*

