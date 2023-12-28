#!/bin/bash

hn=`hostname`

if [ $hn == "ip-172-31-77-229" ]; then
        HOME=/home/ubuntu
        export DIRWEB=/var/www/veloxfintech.com/html
else
        export DIRWEB=/var/www/html
fi

cd $HOME/sambashare/veloxmon/capsulecrm
. $HOME/.bashrc
. $HOME/.bashrc.jb

TODAY=`date +%Y%m%d`
NOW=`date +%Y%m%d`

export DIRCAPSULE=$HOME/sambashare/veloxmon/capsulecrm
export DIRCAPSULEPY=$DIRCAPSULE/py
export DIRCAPSULECSV=$DIRCAPSULE/csv
export DIRCAPSULETXT=$DIRCAPSULE/txt
export DIRCAPSULEPICKLE=$DIRCAPSULE/pickle
export DIRCAPSULEPICKLEINDEX=$DIRCAPSULE/pickle_indexes
export DIRWEB=/var/www/html
export DIRDATAFILES=$DIRWEB/datafiles

logname=/tmp/${0##*/}.$NOW.log
outputpath=/var/www/html/datafiles

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_join" entity_key="Seniority" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_person" entity_key="Seniority" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_person" entity_key="firstName|lastName" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_person" entity_key="organisation" subentity_key="id" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_opportunities" entity_key="party" subentity_key="id" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_entries" entity_key="parties|party" subentity_key="id" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_organisation" entity_key="Company__Type" subentity_key="None" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_person" entity_key="Job__Type" subentity_key="None" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_person" entity_key="lastName" subentity_key="None" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_entries" entity_key="activityType" subentity_key="name" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_person" entity_key="Department" subentity_key="None" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="reduced_person" entity_key="Sub__Department" subentity_key="None" pickle_dir=$DIRCAPSULEPICKLEINDEX
