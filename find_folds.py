from __future__ import division
from Bio.Seq import Seq
from Bio import SeqIO
import os
import argparse
import sys
import csv
import fileinput
import subprocess

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
	fold_list = genome_fold (probe_pos, args, all_but_av)
	fold_per_gene(args , fold_list , probe_pos)


def all_but(args):
	with open ('%s_all_but_av.csv' % (args.sample_ID), 'r') as f:
		next(f)
		for line in f:
			line = line.strip().split(',')
			all_but_av = float(line[0])
			return all_but_av
		

def get_probe_pos(args):
	probe_pos = {}
	with open ('%s_probe_positions.csv' % (args.sample_ID) , 'r') as fi:
		for line in fi:
			line = line.strip().split(',')
			gene = line[0]
			position = line[3]
			if position != 'not found':

#			print gene, position
				if gene in probe_pos:
					probe_pos[gene].append(int(position))
				else:
					probe_pos[gene] = []
					probe_pos[gene].append(int(position))

#			else: 
#				print gene, 'not found'
		for gene in probe_pos:
			probe_pos[gene] = list(set(probe_pos[gene]))
#		print probe_pos['tlyA']
		return probe_pos

def genome_fold (probe_pos, args, all_but_av):
# create a list of the relative fold depth acrosless the whole genome
	with open ('%s_fold.depth' % (args.sample_ID) , 'w') as depth_file:
		with open('%s.depth' %(args.sample_ID), 'rb') as f:
			fold_list = list()
			for line in f:
				line = line.strip().split('\t')

				depth = float(line[2])
				#print depth
				fold = depth/all_but_av
				#print fold
				fold_list.append(fold)
	#print len(fold_list)
		writer = csv.writer(depth_file)
		writer.writerow(fold_list)
	return fold_list
 

def fold_per_gene(args , fold_list , probe_pos):
 	with open ('%s_gene_fold.csv' % (args.sample_ID) , 'a') as f:
 		with open ('%s_gene_fold_stats.csv' % (args.sample_ID) , 'a') as f2:

		 	for gene in probe_pos: 

		# 		print gene , probe_pos[gene]
		 		last_probe = max(probe_pos[gene])
		 		first_probe = min(probe_pos[gene])
		#		print gene , first_probe , last_probe
				fold_points = fold_list[first_probe:last_probe]
				writer = csv.writer (f, delimiter = ',')
				writer.writerow([gene , fold_points])
		#		print gene
		#		print fold_points
				length = len(fold_points)
				max_fold = max(fold_points)
				min_fold = min(fold_points)
				less_1 = sum (i<1 for i in fold_points)
				less_5 = sum (i <5 for i in fold_points)
				_1_5 = less_5 - less_1
				greater_5 = length - _1_5
				writer = csv.writer(f2 , delimiter = ',')
				writer.writerow([ gene , length , min_fold , max_fold , less_1 , _1_5 , greater_5] ) 
#
		
		for line in fileinput.input(files = ['%s_gene_fold_stats.csv' % (args.sample_ID)], inplace = True ):
			if fileinput.isfirstline():
				print 'gene, length, min_fold , max_fold , <1 , 1-5 , >5'
			print line


#		print gene , max_fold






main()