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

for entity in ${entities[@]}; do
	python  ./py/capsule_reduce_pickle.py entity=$entity

done

