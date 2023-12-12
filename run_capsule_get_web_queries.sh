

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

python $DIRCAPSULEPY/capsule_query_entity_indexes.py query_terms='[[("person","Sub Department","EQUITIES"),("person","Seniority","CSUITE|SENIOR")], [("person","Sub Department","CASH_EQUITIES"),("person","Seniority","CSUITE|SENIOR")]]' outputfile="/var/www/html/datafiles/equities_csuite_senior_midlevel.csv" pickle_dir=$DIRCAPSULEPICKLEINDEX outputfields='["firstName","lastName","jobTitle","Seniority","id","LinkedInURL","emailAddresses","phoneNumbers"]'

#python $DIRCAPSULEPY/capsule_query_entity_indexes.py query_terms='[("entries","activityType","Meeting")]' outputfile="/var/www/html/datafiles/entries_meetings.csv" pickle_dir=$DIRCAPSULEPICKLEINDEX outputfields='["activityType","id","creator","subject","content","party","createdAt"]'
python $DIRCAPSULEPY/capsule_query_entity_indexes.py query_terms='[[("person","Sub Department","CLEARED_DERIVS"),("person","Seniority","CSUITE|SENIOR|MID_LEVEL")]]' outputfile="/var/www/html/datafiles/cleared_derivs_csuite_senior_midlevel.csv" pickle_dir=$DIRCAPSULEPICKLEINDEX outputfields='["firstName","lastName","jobTitle","Seniority","id","LinkedInURL","emailAddresses","phoneNumbers"]'


