import pandas as pd

# Extracts protein name, species, ncbi accession, and sequence info from a NCBI genpept file
# and creates a tabular file with that information
with open('ncbi_batprots_08042020.gp', 'r') as file:
	lines = file.readlines()
lines = [line.rstrip() for line in lines]
all_rows = []
bad_rows = []
row = []
prot,acc,species,seq = (0,0,0,0)
start = time.time()
for i,line in enumerate(lines):
	if line[:10] == 'DEFINITION':
		prot = line[12:] # Protein name
		if lines[i+1][:5] == '     ':
			prot2 = lines[i+1][12:]
			prot = prot + ' ' + prot2
		if lines[i+2][:5] == '     ':
			prot3 = lines[i+2][12:]
			prot = prot + ' ' + prot3
		prot = prot.split('[')[0]
		if prot[:7] == 'RecName':
			prot = prot.split('=')[1].split(';')[0]
	if line[:9] == 'ACCESSION':
		acc = line[12:]
	if line[:10] == '  ORGANISM':
		species = line[12:] # Species name
	if line[:6] == 'ORIGIN':
		new_lines = lines[i+1:]
		seqparts = ''
		for new_line in new_lines:
			if new_line[:2] == '//':
				break
			else:
				seqparts += new_line
		new_seqparts = seqparts.replace(' ', '')
		seq = ''.join([i for i in new_seqparts if not i.isdigit()]).upper()
	if line[:2] == '//':
		row = [prot, species, acc, seq]
		if 0 not in row:
			all_rows.append(row)
		else:
			bad_rows.append(row)
		prot,acc,species,seq = (0,0,0,0)

prots = [row[0] for row in all_rows]
species = [row[1] for row in all_rows]
acc = [row[2] for row in all_rows]
seqs = [row[3] for row in all_rows]
data = pd.DataFrame({"Protein": prots, "Species": species, 'NCBI Accession': acc, "Sequence": seqs})
data = data.drop_duplicates(subset=['Protein', 'Species', 'Sequence'])
partials = []
for i in range(len(data)):
	if 'partial' in data.iloc[i]["Protein"]:
		partials.append(i)
data = data.drop(data.index[partials])
data.to_csv('proto_batprot_db.tab', sep='\t', index=None)




