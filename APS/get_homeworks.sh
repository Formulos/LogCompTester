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
		git clone "https://github.com/${line}" ${version}/${BASH_REMATCH[0]}
	fi

	if [ ! -f "${version}/${BASH_REMATCH[0]}.txt" ]; then
  		touch ${version}/${BASH_REMATCH[0]}.txt
	fi
	
done < "git_paths.txt"