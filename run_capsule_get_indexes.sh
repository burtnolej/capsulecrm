#!/bin/bash

cd /home/burtnolej/sambashare/veloxmon/capsulecrm
. ../.bashrc

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

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="person" entity_key="firstName|lastName" pickle_dir=$DIRCAPSULEPICKLEINDEX

exit

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="person" entity_key="organisation" subentity_
key="id" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="opportunities" entity_key="party" subentity_
key="id" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="entries" entity_key="parties|party" subentit
y_key="id" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="organisation" entity_key="Company__Type" sub
entity_key="None" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="person" entity_key="Job__Type" subentity_key
="None" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="person" entity_key="lastName" subentity_key=
"None" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="entries" entity_key="activityType" subentity
_key="name" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="person" entity_key="Department" subentity_ke
y="None" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_indexes.py entity="person" entity_key="Sub__Department" subenti
ty_key="None" pickle_dir=$DIRCAPSULEPICKLEINDEX

python $DIRCAPSULEPY/capsule_get_entity_in
exit
