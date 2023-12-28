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

export DIRDATAFILES=$DIRWEB/datafiles

logname=/tmp/${0##*/}.$NOW.log
outputpath=/var/www/html/datafiles

query_name=('equities_csuite_senior_midlevel' 'entries_meetings' 'cleared_derivs_csuite_senior_midlevel' 'test_organisation' 'test_join')

query_terms=('[[("person","Sub$$Department","EQUITIES"),("person","Seniority","CSUITE|SENIOR")],[("person","Sub$$Department","CASH_EQUITIES"),("person","Seniority","CSUITE|SENIOR")]]' \
       		'[[("entries","activityType","Meeting")]]' \
		'[[("person","Sub$$Department","CLEARED_DERIVS"),("person","Seniority","CSUITE|SENIOR|MID_LEVEL")]]' \
		'[[("organisation","Company$$Type","INVESTMENT_BANK")]]' \
		'[[("join","Seniority","CSUITE")]]')


outputfields=('["firstName","lastName","jobTitle","Seniority","id","LinkedInURL","emailAddresses","phoneNumbers"]' \
		'["activityType","id","creator","subject","content","party","createdAt"]' \
		'["firstName","lastName","jobTitle","Seniority","id","LinkedInURL","emailAddresses","phoneNumbers"]' \
		'["name","Company$$Type"]' \
	       	'["firstName","lastName","jobTitle","name","Company$$Type"]')

#query_name=('test_organisation' 'test_join')
#query_terms=('[[("organisation","Company$$Type","INVESTMENT_BANK")]]' '[[("join","Seniority","CSUITE")]]')
#outputfields=('["name","Company$$Type"]' '["firstName","lastName","jobTitle","name","Company$$Type"]')

count=0

for query_term in ${query_terms[@]}; do
	query_term=$(echo $query_term | sed 's/\$\$/ /g')
	outputfields=$(echo ${outputfields[$count]} | sed 's/\$\$/ /g')

	echo "query_term=$query_term"
	echo "outputfields=$outputfields"
	echo "query_name=${query_name[$count]}"
	outfile=$DIRDATAFILES/${query_name[$count]}.csv
	echo "out_file=$outfile"

	python $DIRCAPSULEPY/capsule_query_entity_indexes.py \
		query_terms="$query_term" \
		outputfile=$outfile \
		pickle_dir=$DIRCAPSULEPICKLEINDEX \
		outputfields="$outputfields" \
		reduced="false"

	count=$count+1
	echo
	echo
	echo
done

cat /dev/null > $DIRDATAFILES/query_manifest.txt
for query_name in ${query_name[@]}; do
        outfile=$DIRDATAFILES/$query_name.csv
        timestamp=$(date -r $outfile +%Y-%m-%d_%H-%M-%S)
        linecount=$(wc -l < $outfile)
        printf "%-50s  %s   %s\n" $query_name $timestamp ${linecount[0]} >> "$DIRDATAFILES/query_manifest.txt"
done
