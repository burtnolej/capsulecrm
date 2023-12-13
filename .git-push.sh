#/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    exit
fi

if [ $1 == "" ]; then
        echo "please provide commit message"
	exit
fi

if [ $2 == "" ]; then
	echo "please provide repo shortname (like capsulecrm)"
	exit
fi

if [ $3 == "" ]; then
        echo "please provide exec flag test|prod"
	exit
fi

tmp="$(git ls-remote | grep $2 2>&1)" 	
num_valid_repo="$(echo $tmp | wc -l)"
num_changes=`git status --short | grep " M " | wc -l`

echo "is $2 a valid repo "$num_valid_repo
echo "number of changes are "$num_changes

if [ $3 != "test" ]; then
	git -m commit $1
	eval "$(ssh-agent -s)"
	ssh-add ~/.ssh/id_ed25519
	git push $2
else
	echo "in test mode"
fi
