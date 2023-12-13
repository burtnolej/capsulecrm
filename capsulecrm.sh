
#!/bin/bash

cd /home/burtnolej/sambashare/veloxmon/capsulecrm
. ../.bashrc
TODAY=`date +%Y%m%d`
NOW=`date +%Y%m%d`
#NOW=`date +%Y%m%d.%H%M%S`

#outputpath=~/gdrive/Capsule

if [[ "$3" == 'today' ]]; then
        FILTER=`date +%Y-%m-%d`
else
        FILTER="nofilter"
fi

logname=/tmp/${0##*/}.$NOW.$1.$2.$FILTER.log
outputpath=/var/www/html/datafiles

echo "entity_type:$1, env:$2, filter:$FILTER"
platform='unknown'
unamestr=`uname`
if [[ "$1" == 'email' ]]; then
        python ./capsulecrm.py entity=entry entity_type=email action=read env=$2 ofile=$outputpath/$2_d
ata_emails_$NOW.$3.txt >> $logname 2>&1
elif [[ "$1" == 'person' ]]; then
        python ./capsulecrm.py entity=party entity_type=person action=read env=$2 col_count=22 filter=$
FILTER ofile=$outputpath/$2_data_persons_$NOW.$3.txt >> $logname 2>&1
elif [[ "$1" == 'opportunity' ]]; then
        python ./capsulecrm.py entity=opportunity action=read env=$2 col_count=29 filter=$FILTER ofile=
$outputpath/$2_data_opportunity_$NOW.$3.txt >> $logname 2>&1
elif [[ "$1" == 'client' ]]; then
        python ./capsulecrm.py entity=party entity_type=organisation action=read env=$2 filter=$FILTER
col_count=15 ofile=$outputpath/$2_data_clients_$NOW.$3.txt >> $logname 2>&1
elif [[ "$1" == 'notes' ]]; then
        python ./capsulecrm.py entity=entry entity_type=tasks env=$2 action=read ofile=$outputpath/$2_d
ata_tasks_$NOW.$3.txt >> $logname 2>&1
fi
