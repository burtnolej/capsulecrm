#!/bin/bash

cd /home/burtnolej/sambashare/veloxmon/capsulecrm
. ~/.bashrc

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

#entities=("person")
entities=("person" "join")

#entities=("organisation" "entries" "opportunities" "person" )
outputtype="list"
outputfields="model"

for entity in ${entities[@]}; do
	python ./py/capsule_get_entity.py entity=$entity outputtype=$outputtype outputfields=$outputfields outputfile="$DIRDATAFILES/$entity.csv" pickle_dir=$DIRDATAFILES csv_dir=$DIRCAPSULECSV

done



#python ./py/capsule_get_entity.py entity=entries outputtype=list outputfields=model outputfile=/var/www/html/datafiles/entries.csv pickle_dir=/home/burtnolej/sambashare/veloxmon/capsulecrm/pickle csv_dir=/home/burtnolej/sambashare/veloxmon/capsulecrm/csv


#python ./py/capsule_get_entity.py entity=opportunities outputtype=list outputfields=model outputfile=/var/www/html/datafiles/opportunities.csv pickle_dir=/home/burtnolej/sambashare/veloxmon/capsulecrm/pickle csv_dir=/home/burtnolej/sambashare/veloxmon/capsulecrm/csv

#python ./py/capsule_get_entity.py entity=person outputtype=list outputfields=model outputfile=/var/www/html/datafiles/person.csv pickle_dir=/home/burtnolej/sambashare/veloxmon/capsulecrm/pickle csv_dir=/home/burtnolej/sambashare/veloxmon/capsulecrm/csv

