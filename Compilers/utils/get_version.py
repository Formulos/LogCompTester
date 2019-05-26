import sys
version = sys.argv[1]
version = version.strip("v").split(".")
latest = ""

for v in sys.stdin:
	v_list = v.strip("v").strip("\n").split(".")
	is_version = True
	for i in range(len(version)):
		if v_list[i] != version[i]:
			is_version = False
			break
	if is_version:
		latest = v

print(latest)



