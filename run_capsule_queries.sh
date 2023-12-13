

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

python -m pdb $DIRCAPSULEPY/capsule_get_query.py entity="person" query='[("SENIORITY","SENIOR"),("SUBDEPTTYPE"," LISTED_DERIVS")]'  query2='[("SENIORITY","SENIOR"),("SUBDEPTTYPE","FUTURES")]'
