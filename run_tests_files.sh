for file in $1/*; do
	echo "$(basename "$file")"
	cat $file
	echo ""
	python3 $2/main.py $1/"$(basename "$file")"
done