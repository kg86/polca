#!/bin/bash
base_url="http://corpus.canterbury.ac.nz/resources/"
files=(cantrbry.tar.gz artificl.tar.gz large.tar.gz misc.tar.gz calgary.tar.gz)

for fname in ${files[@]}
do
  if [ -e $fname ]; then
    echo "skip $fname since it exists"
  else
    echo ${base_url}${fname}
    wget ${base_url}${fname}
  fi
done

for tar in `ls *.tar.gz`
do
  tar xvf $tar
done
