re="[A-Za-z0-9_]+"
version="$1"

while IFS='' read -r line || [[ -n "$line" ]]; do
	[[ $line =~ $re ]]
	echo ""
	echo ${BASH_REMATCH[0]}
	
	if [ ! -d "${version}" ]; then
  		mkdir ${version}
	fi

	if [ ! -d "${version}/${BASH_REMATCH[0]}" ]; then
  		mkdir ${version}/${BASH_REMATCH[0]}
	fi

	if [ ! "$(ls -A ${version}/${BASH_REMATCH[0]})" ]; then
		cd ${version}
		git clone "https://github.com/${line}" ${BASH_REMATCH[0]}
		cd ..
	fi
	cd ${version}
	cd ${BASH_REMATCH[0]}
	git reset --hard
	git fetch --tags
	echo $(git tag -l)
	current=$(git tag -l | python3 ../../utils/get_version.py $version)
	echo $current
	git checkout tags/${current}	
	cd ../..

	if [ ! -d "${version}" ]; then
  		mkdir ${version}
	fi

	if [ ! -f "${version}/${BASH_REMATCH[0]}.txt" ]; then
  		echo ${BASH_REMATCH[0]} | python3 utils/mount_reviews.py $version $current
	fi

done < "git_paths.txt"