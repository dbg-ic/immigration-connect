#!/bin/bash

batch=$1

if [ -z "$batch" ]
then
	query='SELECT COUNT(*) FROM comments'
else
	query="SELECT COUNT(*) FROM comments WHERE phase = \"${batch}\""
fi

exec sqlite3 comments.sqlite "${query}"
