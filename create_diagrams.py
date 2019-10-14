from os import listdir
from os.path import isfile, join

def fun(s):
	splitted = s.split("_")
	res = ""
	two = False
	for x in splitted:
		if x == "2":
			two = True
		if x == "rlb" and two:
			res += "rlb2 "
		if x == "rlb" and not two:
			res += "rlb1 "
		if x == "tts":
			res += "tts "
		if x == "ptk":
			res += "ptk "
		if x == "5" or x == "10" or x == "15" or x == "20":
			res += x + " "
	if res == "":
		res = "all other"
	return res

mypath = "res"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

pmcfg5files = []
pmcfg10files = []
pmcfg15files = []
pmcfg20files = []

for file in onlyfiles:
	if file.startswith("pmcfg-5"):
		pmcfg5files.append(file)
	elif file.startswith("pmcfg-10"):
		pmcfg10files.append(file)
	elif file.startswith("pmcfg-15"):
		pmcfg15files.append(file)
	elif file.startswith("pmcfg-20"):
		pmcfg20files.append(file)

pmcfg5wordtimes = [[],[],[],[],[]]

bench_mcfg = "bench_mcfg"

l = ["bench_mcfg_tts",
		"bench_mcfg_rlb",
		"2_bench_mcfg_rlb",
		"bench_mcfg_tts_rlb",
		"2_bench_mcfg_tts_rlb",
		"bench_mcfg_rlb_tts",
		"2_bench_mcfg_rlb_tts",
		"bench_mcfg_tts_ptk_20",
		"bench_mcfg_tts_ptk_15",
		"bench_mcfg_rlb_tts_ptk_20",
		"2_bench_mcfg_rlb_tts_ptk_20",
		"bench_mcfg_rlb_tts_ptk_15",
		"2_bench_mcfg_rlb_tts_ptk_15",
		"bench_mcfg_tts_rlb_ptk_20",
		"2_bench_mcfg_tts_rlb_ptk_20",
		"bench_mcfg_tts_rlb_ptk_15",
		"2_bench_mcfg_tts_rlb_ptk_15",
		"bench_mcfg_tts_ptk_20_rlb",
		"2_bench_mcfg_tts_ptk_20_rlb",
		"bench_mcfg_tts_ptk_15_rlb",
		"2_bench_mcfg_tts_ptk_15_rlb"]

abstand = 0.4

times = {}

times[bench_mcfg] = {}
for x in [5, 10, 15, 20]:
	times[bench_mcfg][x] = []
	f = open("res/pmcfg-" + str(x) + "_" + bench_mcfg + ".txt")
	lines = f.readlines()
	for y in xrange(0,5):
		line = lines[1 + y*3]
		linevec = line.split(" ")
		times[bench_mcfg][x].append(float(linevec[1]))

file_aufrufe = open("diagrams/aufrufe.tex", "w+")


for ctf in l:
	if ctf not in times:
		times[ctf] = {}
	for x in [5, 10, 15, 20]:
		times[ctf][x] = []
		f = open("res/pmcfg-" + str(x) + "_" + ctf + ".txt")
		lines = f.readlines()
		for y in xrange(0,5):
			line = lines[1 + y*3]
			linevec = line.split(" ")
			times[ctf][x].append(float(linevec[1]))

	f = open("diagrams/dia" + "".join(fun(ctf).split(" ")) + ".tex", "w+")
	f.write("\\begin{figure}\n")
	f.write("\\centering\n")
	f.write("\\begin{tikzpicture}\n")

	f.write("\\draw [->] (0,0) to (" + str(abstand * 25) + ",0);\n")
	f.write("\\draw [->] (0,0) to (0,6.5);\n")

	f.write("\\draw (0,2) to (" + str(abstand * 25) + ",2);\n")

	f.write("\\draw (-0.1,2) to (0.1,2);\n")
	f.write("\\node [anchor=east] at (-0.2,2) {1};\n")
	f.write("\\draw (-0.1,4) to (0.1,4);\n")
	f.write("\\node [anchor=east] at (-0.2,4) {2};\n")
	f.write("\\draw (-0.1,6) to (0.1,6);\n")
	f.write("\\node [anchor=east] at (-0.2,6) {$\\geq$ 3};\n")

	f.write("\\node [rotate=90,anchor=east] at (-0.85,5.5) {multiple of original runtime};\n")
	f.write("\\node at (" + str(abstand*13) + ", -0.8) {size of corpus};\n")

	currentpos = 0.1

	for x in [5, 10, 15, 20]:
		for y in xrange(0,5):
			if y == 2:
				f.write("\\node [anchor = west] at (" + str(currentpos) + ", -0.3) {" + str(x) + "};\n")

			t = times[ctf][x][y]
			normaltime = times[bench_mcfg][x][y]
			p = t / normaltime
			height = 6
			if p < 3:
				height = p * 2

			gray = 75
			if p < 1:
				gray = 35

			f.write("\\node [minimum width=" + str(height) + "cm,"
				+ "anchor=north west,"
				+ "rotate=90,"
				+ "fill=gray!" + str(gray) + "] at (" + str(currentpos) + ", 0) {};\n")

			if p > 3:
				p = round(p, 1)
				f.write("\\node [anchor=north east,rotate=90,inner sep = 0] at (" + str(currentpos) + ", 6) {\\footnotesize" + str(p) + "};\n")

			currentpos += abstand
		currentpos += abstand


	f.write("\\end{tikzpicture}\n")
	f.write("\\caption{approximation sequence: " + fun(ctf) + "}\n")
	f.write("\\label{fig:" + "".join(fun(ctf).split(" ")) + "}\n")
	f.write("\\end{figure}\n")

	file_aufrufe.write("\\input{diagrams/dia" + "".join(fun(ctf).split(" ")) + "}\n")

	