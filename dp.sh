#!/bin/bash

echo "start commit..."
git pull
git add *
git status
git commit -m "add a article or modify article"
git push origin master
echo "successful commit"
