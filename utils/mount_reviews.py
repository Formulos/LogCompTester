import sys

for p in sys.stdin:
	p = p.strip('\n')
	with open(f"{sys.argv[1]}/{p}.txt", "w+") as f:
		f.write(f"Versão testada: {sys.argv[2]} \n\n")
		f.write("Status:\n\n")
		f.write("Seu programa apresentou defeito(s) com as seguinte(s) entrada(s):\n\n")
		f.write("Comentários:")