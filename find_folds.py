from __future__ import division
from Bio.Seq import Seq
from Bio import SeqIO
import os
import argparse
import sys
import csv
import fileinput

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
targets = 'probe_target'
reference = 'references/NC_000962.3.fasta'



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('depth_file' , help = 'depth file, sample.depth')
	parser.add_argument('sample_ID' , help = 'file naming')
	args = parser.parse_args()

	all_but_av = all_but(args)
	probe_pos = get_probe_pos(args)
	genome_fold (probe_pos, args, all_but_av)


	
def all_but(args):
	with open ('%s_all_but_av.csv' % (args.sample_ID), 'r') as f:
		next(f)
		for line in f:
			line = line.strip().split(',')
			all_but_av = line[0]
			return all_but_av
		

def get_probe_pos(args):
	probe_pos = {}
	with open ('%s_probe_positions.csv' % (args.sample_ID) , 'r') as fi:
		for line in fi:
			line = line.strip().split(',')
			gene = line[0]
			position = line[3]
#			print gene, position
			if gene in probe_pos:
				probe_pos[gene].append(position)
			else:
				probe_pos[gene] = []
				probe_pos[gene].append(position)
		for gene in probe_pos:
			probe_pos[gene] = list(set(probe_pos[gene]))
		print probe_pos['tlyA']
		return probe_pos

def genome_fold (probe_pos, args, all_but_av):
# create a list of the relative fold depth acrosless the whole genome
	with open('%s' %(args.sample_ID), 'rb') as f:
		fold_list = list()
		for line in f:
			line = line.strip().split('\t')

			depth = float(line[2])
			#print depth
			fold = depth/all_but_av
			#print fold
			fold_list.append(fold)
	print fold_list
	return fold_list

main()