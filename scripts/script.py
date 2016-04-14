import glob
for st in glob.iglob("*.csv"):
	if st[0:-4] not in glob.iglob("*"):
		f=open(st,"r")
		k=f.readline()
		with open(st[0:-4],"w") as fo:
			pass
		while k!="":
			with open(st[0:-4],"a") as fo:
				if k.split(",")[1][1:-1]!="NULL":
					fo.write(k.split(",")[1][1:-1]+"\n")
			k=f.readline()
