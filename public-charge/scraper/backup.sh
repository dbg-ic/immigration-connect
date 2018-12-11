#!/bin/bash

n=`./count.sh`

sqlite3 comments.sqlite ".backup old/comments-${n}.sqlite"
