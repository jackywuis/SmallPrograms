import argparse
import csv
import os
import re

parser = argparse.ArgumentParser(description='A small program to summarize result from MetaPhlAn2 '
                                             'Usage: python table_list_metaphlan.py -i path/ '
                                             'Output: metaphlan_output.csv '
                                             'Copyleft: Jacky Woo from ZHK Research team, iSynBio, SIAT.')
parser.add_argument('-i', '--input', type=str, help='Folder that contain all FastQC results in .zip format')
args = parser.parse_args()
path = args.input
if path.split('/')[-1] != '':
    path += '/'
infh = open(path + 'merged_table')
reader = csv.DictReader(infh)

# get information of genomes
row0 = reader.next()
row = [r.split("\t") for r in row0]
row = row[0]
row_down = []

# get information of species possibility
for rows in reader:
    for r in rows.values():
        k = r.split("\t")
        for species_name in k:
            if len(species_name.split("|")) == 8:
                row_down += [k]
        break

# get information for each strain
species_dic_s = {}
species_dic_d = {}
for row_species in row_down:
    counter = 0
    for strain in row:
        if counter == 0:
            species = row_species[0]
        else:
            if strain in species_dic_d and species_dic_s[strain] > float(row_species[counter]):
                pass
            else:
                species_dic_s[strain] = float(row_species[counter])
                species_dic_d[strain] = species
        counter += 1
    infh.close()
sorted(species_dic_d.keys())

# output collected information
outfh = open(path + 'metaphlan_output.csv', 'w')
outfh.write('Genome\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\tType\tPossibility\n')
for strain in row[1:]:
    outfh.write(strain + '\t' + '\t'.join([re.sub('_', ' ', x[3:]) for x in species_dic_d[strain].split(
        "|")]) + '\t' + str(species_dic_s[strain]) + '\n')
outfh.close()
