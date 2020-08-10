# Bat Protein Database

This repository contains a tabular database file of bat proteins, as well as the scripts and other data files needed to create it.

## Database Creation

GenPept files for all bat proteins on NCBI were downloaded by using the search term: "bats"[porgn:\__txid9397], in the NCBI Protein database and downloading the resulting set of GenPept files. The script genpept_reader.py was then used to extract protein name, species of origin, NCBI accession ID, and amino acid sequence information from the GenPept text file and convert it into a tabular dataset. The db.py script was then run on this proto-dataset to remove proteins marked as low quality as well as any duplicates (proteins from the same species with the same sequence but different accession IDs). A number of additional columns are added in this step as well such as geographic origin of the species and whether that species is known coronavirus resovoir (see below for full column descriptions). The resulting database contains 144,717 data entries across 446 species (current as of 08/04).

## Coronavirus

Bats have long been known as resovoirs of coronavirus so a thorough search of the published literature was done to identify all species that have been found to capable of infection by coronaviruses, resulting in a list of 47 bat species (listed in cov_species.txt), 30 of which appear in the set of proteins downloaded from NCBI. Proteins that originate from one of these species are marked.

Bats are currently suspected as the most likely vector for the transmission of the SARS-CoV-2 virus to humans, specifically asian Horseshoe Bats (genus *Rhinolophus*). Proteins from *Rhinolophus* species that are endemic to Asia have been marked in the database.

## Column Descriptions

The main datafile (batprot_db.zip) is a tabular file with a total of nine columns:

**Protein** - Protein name

**Species** - Species of origin

**NCBI Accession** - NCBI accession ID

**Sequence Type** - How the protein sequence was obtained. Three possible values: 'Direct Derived' (directly sequenced), 'Model' (predicted sequence derived from a larger genome assembly), and 'Model (no transcript)' (same as 'Model' but without a known associated transcript).

**Known CoV Resovoir** - Known coronavirus resovoir or not (criteria described above). Two possible values: Yes or No.

**Potential SARS-CoV-2 Vector** - Suspected SARS-CoV-2 transmission vector (criteria described above). Two possible values: Yes of No.

**Geographic Origin** - Continent/region the protein's species is endemic to. Has the possible values: Africa, Asia, Australia, Caribbean, Europe, Middle East, North America, South America, Unknown, or any combination of these separated by a '/'.

**Sequence** - Amino acid sequence
