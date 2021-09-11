The scripts in this folder are for extracting and cleaning article webpages for the NJ News Ecosystem project.

*getsamp.py*

This script is for extracting entries from the 12706-fulltext.txt file and any other text file with the same formatting. To use it, you need to enter the number of samples you want, the sourcefile, the outputcsv, and provide it a formatted domainsfile and formatted datesfile which contain the domains and dates to filter on. If you provide it a sample size bigger than the number of entries available with the given domains/dates then it will return all of the entries. Therefore, if you want all of the entries with given dates/domains, just enter a really large sample size (> 3,000,000). 

Ex: python getsamp.py --n 25 --datesfile datesChosen.txt --domainsfile domainsChosen.txt

(default sourcefile is 12706-fulltext.txt, default outputcsv is randsamp.csv)

Ex. python getsamp.py --n 3000000 --datesfile datesChosen.txt --domainsfile domainsChosen.txt --sourcefile 12706-fulltext.txt --outputcsv allChosen.csv

*dates.txt* and *domains.txt*

Both of these files are just lists of dates or domains that you can filter on. Dates should fit the format YYYYMMDD. **Make sure there are no trailing whitespaces on each line otherwise it won't filter correctly.**

*cleanFE.py*

This script is for cleaning the extracted articles' text by scraping the front end of the Internet Archive and using the newspaper3k package to parse and identify the text that belongs to the article. To use it, you simply need to provide the sourcecsv and outputcsv. The outputcsv will have new columns: title, date (publish date), clean_text, and author. 

Ex. python cleanFE.py

(default sourcecsv is randsamp.csv, default outputcsv is cleansamp.csv)

Ex. python cleanFE.py --sourcecsv chosensamp.csv --outputcsv cleanedChosen.csv

**For both scripts, you can enter --help (e.g. python cleanFE.py --help) to see the parameters, their data types, and their defaults**

