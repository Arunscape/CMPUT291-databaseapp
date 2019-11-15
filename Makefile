SOURCE_CODE = phase1.py phase2.py phase3.py

.RECIPEPREFIX = >
.PHONY: format compress clean

format:
> black .

compress:
> tar -czf prj2.tgz $(SOURCE_CODE) README.txt Report.pdf

clean:
> rm -f terms.txt emails.txt dates.txt recs.txt *.idx
