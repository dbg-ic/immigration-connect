#!/bin/bash

# Label for new batch
batch=${1:?Specify batch label}

# Label of unreported records
unreported="A"

# Label all unreported records with the new batch label
update="UPDATE comments SET phase = \"${batch}\" WHERE phase = \"${unreported}\""
sqlite3 comments.sqlite "${update}"

# Report how many records are in this new batch
query="SELECT COUNT(*) FROM comments WHERE phase = \"${batch}\""
sqlite3 comments.sqlite "${query}"
