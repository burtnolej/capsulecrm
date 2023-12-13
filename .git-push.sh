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
num_changes=`git status --short | grep " A " | wc -l`

if [ $num_valid_repo -ne 1 ]; then
        echo "not valid repo"
else
	echo "yes $2 is a valid repo "
fi

echo "number of changes are "$num_changes

if [ $3 != "test" ]; then
	git status --short | grep " A "
	git commit -m $1
	eval "$(ssh-agent -s)"
	ssh-add ~/.ssh/id_ed25519_j
	b
	git push $2
else
	echo "in test mode"
fi
