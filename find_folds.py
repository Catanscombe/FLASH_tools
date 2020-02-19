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
	probe_pos(args)

def all_but(args):
	with open ('%s_all_but_av.csv' % (args.sample_ID), 'r') as f:
		next(f)
		for line in f:
			line = line.strip().split(',')
			all_but_av = line[0]
			return all_but_av
		

def probe_pos(args):
	with open ('%s_probe_positions.csv' % (args.sample_ID) , 'r') as fi:
		for line in fi:
			line = line.strip().split(',')
			gene = line[0]
			position = line[3]
			print gene, position

main()