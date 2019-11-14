SOURCE_CODE = main.py

.RECIPEPREFIX = >
.PHONY: format compress

format:
> black .

compress:
> tar -czf prj2.tgz $(SOURCE_CODE) README.txt Report.pdf
