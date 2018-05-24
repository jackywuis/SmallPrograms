import argparse
import os

parser = argparse.ArgumentParser(description='A small program to summarize result from FatQC '
                                             'Usage: python table_list_fastqc.py -i path/ '
                                             'Output: fastqc_summary.csv '
                                             'Copyleft: Jacky Woo from ZHK Research team, iSynBio, SIAT.')
parser.add_argument('-i', '--input', type=str, help='Folder that contain all FastQC results in .zip format')
args = parser.parse_args()
fastqc = args.input
if fastqc.split('/')[-1] != '':
    fastqc += '/'

output = fastqc + 'fastqc_summary.csv'
log = fastqc + 'log.txt'
outfh = open(output, 'w')
strain_info = []
strain_file = os.listdir(fastqc)
for strain in strain_file:
    if strain.split('.')[-1] == 'zip':
        strain_info += [fastqc + strain]
head = []
for strain in strain_info:
    result = [strain.rstrip('.zip').split('/')[-1]]
    os.system('unzip -d %s -o %s 1>>%s' % (fastqc, strain, log))
    infile = strain.rstrip('.zip') + '/summary.txt'
    infh = open(infile, 'r')
    if not head:
        for line in infh:
            row = line.split('\t')
            head = head + [row[1]]
        outfh.write('Sample ID\t' + '\t'.join(head) + '\n')
        infh.close()
        infh = open(infile, 'r')
    for line in infh:
        row = line.split('\t')
        result += [row[0].capitalize()]
    outfh.write('\t'.join(result) + '\n')
    infh.close()
    os.system('rm -r %s' % (strain.rstrip('.zip')))
outfh.close()
