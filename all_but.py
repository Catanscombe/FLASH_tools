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

# with open (reference ) as genome: 
genome = SeqIO.read('%s/%s' % (script_dir, reference) , 'fasta')
# for genome in genome_record:
genome = str(genome.seq)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('depth_file' , help = 'depth file, sample.depth')
	parser.add_argument('sample_ID' , help = 'file naming')
	args = parser.parse_args()

	probe_pos = find_probes(args)
	depth_list = coverage_depth(args)
	probe_pair_depth(args, probe_pos, depth_list)



def find_probes(args):

#find the target position of the probes from the H37Rv genome, add to dictionary per gene
	with open ('%s_probe_positions.csv' % (args.sample_ID), 'a' ) as f:
		writer = csv.writer(f , delimiter = ',')
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
				writer.writerow ([gene, ID , target, found , 'F'])
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
					writer.writerow ([ gene, ID, target, found_rc , 'RC'])
					if gene in probe_pos:
						probe_pos[gene].append(found_rc)
					else:
						probe_pos[gene] =[]
						probe_pos[gene].append(found_rc)
				else: 
					writer.writerow ([ gene, ID, target, 'not found' ])

					pass
		

		for gene in probe_pos:
			probe_pos[gene] = list(set(probe_pos[gene]))
		#print probe_pos
		return probe_pos

def coverage_depth (args):
	with open ('%s' % (args.depth_file) , 'rb') as df:
		depth_list = list()
		for line in df:
			line = line.strip().split('\t')
			depth = int(line[2])
			depth_list.append(depth)
	return depth_list

def probe_pair_depth(args, probe_pos, depth_list):
	with open ('%s_all_but_av.csv' % (args.sample_ID), 'w') as f:

		probe_depth_list = list()
		for gene in probe_pos:

			probe_pos_list = probe_pos[gene]
			#print probe_pos_list
			sorted_pos = sorted(probe_pos_list)
			for i in range (0, len(sorted_pos)-1):
				probe_1 = sorted_pos[i]
				probe_2 = sorted_pos[i +1]
				our_list = depth_list[probe_1:probe_2]
				#print gene , our_list
				#print our_list
					

				#length = len(our_list)
				probe_depth_list.append(our_list)
				#print len(probe_depth_list)
				flat_list = []
				for sublist in probe_depth_list:
					for val in sublist:
						flat_list.append(val)

				

		len_enriched = len(flat_list)
	#	print len_enriched
		sum_enriched = sum(flat_list)
	#	print sum_enriched
		average_enriched =  sum_enriched/len_enriched

	#	print average_enriched

		whole_length = len(depth_list)
		whole_depth = sum(depth_list)
		wg_av = whole_depth / whole_length
		all_but_length = whole_length - len_enriched
		all_but_depth = whole_depth - sum_enriched
		all_but_av = all_but_depth / all_but_length
	#	print wg_av
	#	print all_but_av
		writer=csv.writer(f, delimiter  =',')
		writer.writerow([all_but_av, average_enriched])	

	for line in fileinput.input(files = ['%s_all_but_av.csv' % (args.sample_ID)], inplace = True ):
		if fileinput.isfirstline():
			print 'all_but_av, enriched_av'
		print line















main()