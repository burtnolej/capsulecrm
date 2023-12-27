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

logname=/tmp/${0##*/}.$NOW.log

hn=`hostname`
if [ $hn == "ip-172-31-77-229" ]; then
	export DIRWEB=/var/www/veloxfintech.com/html
else
	export DIRWEB=/var/www/html
fi

export DIRDATAFILES=$DIRWEB/datafiles
		
entities=("organisation" "entries" "opportunities" "person" "join" )
outputtype="list"
outputfields="model"

#for entity in ${entities[@]}; do
#	python ./py/capsule_get_entity.py entity=$entity outputtype=$outputtype outputfields=$outputfields outputfile="$DIRDATAFILES/$entity.csv" pickle_dir=$DIRDATAFILES csv_dir=$DIRCAPSULECSV
#
#done

cat /dev/null > $DIRDATAFILES/data_manifest.txt
for entity in ${entities[@]}; do
        outfile=$DIRDATAFILES/$entity.csv
        timestamp=$(date -r $outfile +%Y-%m-%d_%H-%M-%S)
        linecount=$(wc -l < $outfile)
        printf "%-50s  %s   %s\n" $entity $timestamp ${linecount[0]} >> "$DIRDATAFILES/data_manifest.txt"
done
