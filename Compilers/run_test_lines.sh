while IFS='' read -r line || [[ -n "$line" ]]; do
	echo $line
	echo $line | python3 $2/main.py
done < "$1"