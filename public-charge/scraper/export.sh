#!/bin/bash

batch=${1:?Specify batch}

query="SELECT * FROM comments WHERE phase = \"${batch}\""

exec sqlite3 -csv -header comments.sqlite "${query}" > ${batch}.csv
