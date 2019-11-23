SOURCE_CODE = phase1.py phase2.sh break.pl phase3.py

.RECIPEPREFIX = >
.PHONY: format compress clean hugo-upload-data hugo-upload-code

format:
> black .

compress:
> tar -czf prj2.tgz $(SOURCE_CODE) README.txt Report.pdf

clean:
> rm -f terms.txt emails.txt dates.txt recs.txt
> rm -f re.idx te.idx em.idx da.idx

hugo-upload-data:
> rsync -vrzP data10 data1k haiyang3@ug11.cs.ualberta.ca:~/database-app

hugo-upload-code:
> rsync -vrzP $(SOURCE_CODE) haiyang3@ug11.cs.ualberta.ca:~/database-app
> ssh haiyang3@ug11.cs.ualberta.ca
