from __future__ import division
from Bio.Seq import Seq
from Bio import SeqIO
import os
import argparse
import sys

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
targets = 'probe_target'
reference = 'references/NC_000962.3.fasta'

# with open (reference ) as genome: 
genome = SeqIO.read('%s/%s' % (script_dir, reference) , 'fasta')
# for genome in genome_record:
genome = str(genome.seq)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('depth_file' , help = 'depth file, sample.depth')
	parser.add_argument('sample_ID' , help = 'file naming')
	args = parser.parse_args()

	find_probes(args)

def find_probes(args):

#find the target position of the probes from the H37Rv genome, add to dictionary per gene
	probe_pos = {}
	for line in open('%s/%s' % (script_dir , targets)):
		
		line = line.strip().split('\t')
		ID = line[0]
		gene = ID.strip().split("_")
		gene = gene[0]
		target = line[1]
		#print target
		found = genome.find(target)
		if found!= -1:
	#		print gene, ID , target, found , 'F'
			if gene in probe_pos:
				probe_pos[gene].append(found)
			else:
				probe_pos[gene] =[]
				probe_pos[gene].append(found)

			
		else:
			target = Seq(target)
			target_rc  = target.reverse_complement()
			target_rc = str(target_rc)
			#print target
			#print target_rc
			found_rc = genome.find(target_rc)
			if found_rc != -1:
	#			print gene, ID, target, found_rc , 'RC'
				if gene in probe_pos:
					probe_pos[gene].append(found_rc)
				else:
					probe_pos[gene] =[]
					probe_pos[gene].append(found_rc)
			else: 
	#			print gene, ID, target, 'not found'
				pass
	

	for gene in probe_pos:
		probe_pos[gene] = list(set(probe_pos[gene]))
	print probe_pos
	return probe_pos

main()