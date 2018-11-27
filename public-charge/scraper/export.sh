#!/bin/bash

batch=$1

if [ -z "$batch" ]
then
	batch="all"
	query="SELECT * FROM comments"
else
	query="SELECT * FROM comments WHERE phase = \"${batch}\""
fi

exec sqlite3 -csv -header comments.sqlite "${query}" > ${batch}.csv
