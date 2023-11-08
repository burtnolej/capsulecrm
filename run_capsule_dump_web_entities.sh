#!/bin/bash


export DIRCAPSULE=$HOME/sambashare/veloxmon/capsulecrm
export DIRCAPSULEPY=$DIRCAPSULE/py
export DIRCAPSULECSV=$DIRCAPSULE/csv
export DIRCAPSULETXT=$DIRCAPSULE/txt
export DIRCAPSULEPICKLE=$DIRCAPSULE/pickle
export DIRCAPSULEPICKLEINDEX=$DIRCAPSULE/pickle_indexes
export DIRWEB=/var/www/html
export DIRDATAFILES=$DIRWEB/datafiles

python $DIRCAPSULEPY/capsule_dump_web_entity.py multipage=1000 entity="entries" persistfile="$DIRCAPSULEPICKLE/entries.pickle" start_page=0 pickle_dir="$DIRCAPSULEPICKLE"
#python $DIRCAPSULEPY/capsule_dump_web_entity.py multipage=40 entity="entries" persistfile="$DIRCAPSULEPICKLE/entries_2.pickle" start_page=40 pickle_dir="$DIRCAPSULEPICKLE"

python $DIRCAPSULEPY/capsule_dump_web_entity.py multipage=1000 entity=parties persistfile="$DIRCAPSULEPICKLE/organisation.pickle" start_page=0 filter=organisation_filter pickle_dir=$DIRCAPSULEPICKLE
#python $DIRCAPSULEPY/capsule_dump_web_entity.py multipage=40 entity=parties persistfile="$DIRCAPSULEPICKLE/organisation_2.pickle" start_page=40 filter=organisation_filter pickle_dir=$DIRCAPSULEPICKLE

python $DIRCAPSULEPY/capsule_dump_web_entity.py multipage=1000 entity=opportunities persistfile="$DIRCAPSULEPICKLE/opportunities.pickle" start_page=0 pickle_dir=$DIRCAPSULEPICKLE
#python $DIRCAPSULEPY/capsule_dump_web_entity.py multipage=40 entity=opportunities persistfile="$DIRCAPSULEPICKLE/opportunities_2.pickle" start_page=40 pickle_dir=$DIRCAPSULEPICKLE

exit

python $DIRCAPSULEPY/capsule_dump_web_entity.py filter=person_filter multipage=200 entity=parties persistfile="$DIRCAPSULEPICKLE/person_1.pickle" start_page=0 pickle_dir=$DIRCAPSULEPICKLE

python $DIRCAPSULEPY/capsule_dump_web_entity.py filter=person_filter multipage=200 entity=parties persistfile="$DIRCAPSULEPICKLE/person_2.pickle" start_page=200 pickle_dir=$DIRCAPSULEPICKLE

python $DIRCAPSULEPY/capsule_dump_web_entity.py filter=person_filter multipage=200 entity=parties persistfile="$DIRCAPSULEPICKLE/person_3.pickle" start_page=400 pickle_dir=$DIRCAPSULEPICKLE

python $DIRCAPSULEPY/capsule_dump_web_entity.py filter=person_filter multipage=100000 entity=parties persistfile="$DIRCAPSULEPICKLE/person_4.pickle" start_page=600 pickle_dir=$DIRCAPSULEPICKLE
