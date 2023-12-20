#/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    exit
fi

if [ "$1" == "" ]; then
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
num_adds=`git status --short | grep " A " | wc -l`

if [ $num_valid_repo -ne 1 ]; then
        echo "not valid repo"
else
	echo "yes $2 is a valid repo "
fi

echo "number of changes are "$num_changes
echo "number of adds are "$num_adds

if [ "${num_changes}" -eq 0 ] && [ "${num_adds}" -eq 0 ]; then
	echo "no adds or changes to commit"
	exit
fi

if [ $3 != "test" ]; then
	git commit -m "$1"
	git diff HEAD  --name-only
	eval "$(ssh-agent -s)"
	ssh-add ~/.ssh/id_ed25519_jb
	git push $2
else
	echo "in test mode"
fi
