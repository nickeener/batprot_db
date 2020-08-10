import pandas as pd
import math
import pdb


data = pd.read_csv('proto_batprot_db.tab', sep='\t')

# Remove low quality proteins and proteins that don't have a species in species_geo.tab
new_data = pd.DataFrame()
geo_data = pd.read_csv('species_geo.tab', sep='\t')
species = geo_data['Species'].to_list()
for i in range(len(data)):
	try:
		if data.iloc[i]['Protein'][:19] != 'LOW QUALITY PROTEIN' and data.iloc[i]['Species'] in species:
			new_data = new_data.append(data.iloc[i])
	except:
		if math.isnan(data.iloc[i]['Protein']):
			pass


new_data.to_csv('post-filter.tab', sep='\t', index=None)
# Fix protein names and create lists that will be added as new columns
new_data = pd.read_csv('post-filter.tab', sep='\t')
type_ = []
with open('cov_species.txt', 'r') as file:
	lines = file.readlines()
cov_species = [line.rstrip() for line in lines]
resovoir = []
geo_dict = {}
new_geo = []
for i in range(len(geo_data)):
	geo_dict[geo_data.iloc[i]['Species']] = geo_data.iloc[i]['Geographic Origin']
for i in range(len(new_data)):
	# Create list that will become 'Sequence Type' column
	if new_data.iloc[i]['NCBI Accession'][2] == '_':
		if new_data.iloc[i]['NCBI Accession'][:2] == 'YP':
			type_.append('Model (no transcript)')
		elif new_data.iloc[i]['NCBI Accession'][:2] == 'NP':
			type_.append('Direct Derived')
		elif new_data.iloc[i]['NCBI Accession'][:2] == 'XP':
			type_.append('Model')
	else:
		type_.append('Direct')
	# Remove '(mitochondrion)' from protein names
	if '(mitochondrion)' in str(new_data.iloc[i]['Protein']):
		new_data.iloc[i]['Protein'] = new_data.iloc[i]['Protein'].replace(' (mitochondrion) ', '')
	# Create list that will become "Known CoV Resovoir" column from species list
	if new_data.iloc[i]['Species'] in cov_species:
		resovoir.append('Yes')
	else:
		resovoir.append('No')
	# Create list that will become 'Geographical Origin' column
	new_geo.append(geo_dict[new_data.iloc[i]['Species']])


# Add lists to dataframe as new columns
new_data['Sequence Type'] = type_
new_data['Known CoV Resovoir'] = resovoir
new_data['Geographic Origin'] = new_geo


# Add column 'Suspected SARS-CoV-2 Vector', Rhinolophus genus and endemic to Asia
cov2 = []
for i in range(len(new_data)):
	if i%10000 == 0 :
		print(i)
	if 'Rhinolophus' in new_data.iloc[i]['Species'] and 'Asia' in new_data.iloc[i]['Geographic Origin']:
		cov2.append('Yes')
	else:
		cov2.append('No')
new_data['Potential SARS-CoV-2 Vector'] = cov2


# Rearrange columns and save to file
new_data = new_data[['Protein', 'Species', 'NCBI Accession', 'Sequence Type', 'Known CoV Resovoir', 'Potential SARS-CoV-2 Vector', 'Geographic Origin', 'Sequence']]
new_data.to_csv('batprot_db.tab', sep='\t', index=None)


