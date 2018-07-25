import argparse
import screed
parser = argparse.ArgumentParser(description='Trim-assemble - A program to trim assemble data.\n'
                                             'Example: python trim_assemble.py -m 512 -i /mnt/sdb/assemble/file/')
parser.add_argument('-i', '--input', type=str, help='Enter the path with the scaffold.fasta file you want to trim')
parser.add_argument('-m', '--minlen', type=int, default=512, help='Minimum length of contigs for assemble output')
args = parser.parse_args()
out = args.input
if out.split('/')[-1]:
    out += '/'
outfh = open(out + 'cleaned.fasta', 'w')
contig_id = 0
for rec in screed.open(out + 'scaffolds.fasta'):
    seq = rec.sequence
    if len(seq) >= args.minlen:
        contig_id += 1
        outfh.write('> contig' + str(contig_id) + '\n')
        for count, word in enumerate(str(seq)):
            outfh.write(word)
            if count % 60 == 59:
                outfh.write('\n')
        if len(seq) % 60 != 0:
            outfh.write('\n')
outfh.close()