This script scans comment dumps (available from https://files.pushshift.io/reddit/comments) and creates a list of users sorted by the average reply time ascending.

In order for this script to work successfully, you should:

1) Have a lot of RAM for analyzing a large number of comments (This can be optimized)
2) Pipe comment data into the script sequentially from oldest to newest
3) Have a few hours to spare when analyzing millions

The output from this script has the following data (CSV format):

1) The average reply time to parent comments (sorted ascending)
2) The total number of comments made
3) The total number of unique subreddits commented in
4) The total number of unqiue submissions commented in
5) The average length of comments
6) The average Levenshtein ratio
7) The average Ratcliff/Obershelp ratio
8) The author for the comments

