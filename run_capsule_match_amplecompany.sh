#!/bin/bash


export DIRCAPSULE=$HOME/sambashare/veloxmon/capsulecrm
export DIRCAPSULEPY=$DIRCAPSULE/py
export DIRCAPSULECSV=$DIRCAPSULE/csv
export DIRCAPSULETXT=$DIRCAPSULE/txt
export DIRCAPSULEPICKLE=$DIRCAPSULE/pickle
export DIRCAPSULEPICKLEINDEX=$DIRCAPSULE/pickle_indexes
export DIRWEB=/var/www/html
export DIRDATAFILES=$DIRWEB/datafiles

python $DIRCAPSULEPY/capsule_companyname_mapper.py persistfile="$DIRCAPSULEPICKLE/ampleexport.pickle" pickle_dir=$DIRCAPSULEPICKLE outputfile="$DIRCAPSULECSV/matchedampleexport.csv"

