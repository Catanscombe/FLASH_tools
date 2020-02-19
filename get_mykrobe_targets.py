from __future__ import division
import csv
import re
import os
import sys
import argparse
import csv

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
target_file = 'panel.final.mykrobe.txt'

genes = 'target_genes_info_clean.txt'
all_genes = 'all_genes'


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('depth_file_fold' , help = 'depth fold file, sample_fold.depth')
	parser.add_argument('sample_ID' , help = 'file naming')
	args = parser.parse_args()


	mykrobe_gene = get_DNA(target_file)	
	mykrobe_prot = get_prot (target_file, mykrobe_gene)
	fold_list = fold (in_file)
	gene_dic = list_lookup ()
	mykrobe_genome_pos = mykrobe_positions (gene_dic, mykrobe_gene)
	mykrobe_fold (mykrobe_positions , fold_list)
	

def get_DNA(target_file):
	#create dictionary for gene[position]
	mykrobe_gene = {}
	#gene gene list from mykorbe targets
	for line in open ('%s/%s' %(script_dir , target_file)):
		line = line.strip().split('\t')
		gene = line[0]
		DNA = line[2]
		#if they are DNA targets, get the position from the change information eg 'CTG607CTT'
		if DNA == 'DNA':
			pos = line[1]
			#print pos
			temp = re.findall(r'\d+', pos)
			assert len(temp) == 1
			position = int(temp[0])
			# position = list(map(int , temp))
			#print gene
			#print position
		#see if the gene is in the dictionary, if so check if the value is, if not add it

			if gene in mykrobe_gene:
				
				mykrobe_gene[gene].append(position)

			else: 
				mykrobe_gene[gene] = []
				mykrobe_gene[gene].append(position)

	for gene in mykrobe_gene:
		mykrobe_gene[gene] = list(set(mykrobe_gene[gene]))
	#print mykrobe_gene['rpoB']
	return mykrobe_gene
	


def get_prot (target_file, mykrobe_gene):
	#create dictionary of gene [position] for proteins 
 	for line in open ('%s/%s' %(script_dir , target_file)):
		line = line.strip().split('\t')
		gene = line[0]
		DNA = line[2]
		if DNA == 'PROT':
			#print line
			pos = line[1]
			#print pos
			temp = re.findall(r'\d+', pos)
			#print temp
			position = int(temp[0])
			
			#print position
			position_1 = (position * 3)
			position_2 = (position_1 + 1)
			position_3 = (position_1 + 2)

			#print position_1
			#print position_1, position_2, position_3
		else:
			pass

		if gene in mykrobe_gene:
			
				mykrobe_gene[gene].extend([position_1, position_2, position_3])
			
		else:
			mykrobe_gene[gene] = []
			mykrobe_gene[gene].extend([position_1, position_2, position_3])
	for gene in mykrobe_gene:
		mykrobe_gene[gene] = list (set(mykrobe_gene[gene]))
	#print mykrobe_gene['rpoB']
	
	for gene in mykrobe_gene:
		snps = mykrobe_gene[gene]
		#print gene , snps 

	return mykrobe_gene
	

def fold (args):
	with open ('%s' % (args.depth_file_fold) , 'rb') as f:
		fold_list = list()
		for line in f:
		
			#print line
			line = line.strip(). split('\t')
			
			#print line[2]
			depth = int(line[2]) 
	   
			depth_list.append(depth)


		#print depth_list

	return fold_list



def list_lookup ():

	gene_dic = {}
	for line in open ('%s/%s' % (script_dir , genes)):
		#print line
		line = line.strip().split(' ')
		gene = line[0]
		#print gene
		start = int(line[1])
		start = start -1 
		stop = int(line[2])
		stop = stop -1 
		#print stop
		gene_dic [gene] = start, stop
	gene_dic ['eis'] = 2715371 , 2715596
	#print gene_dic
	return gene_dic

def mykrobe_positions (gene_dic, mykrobe_gene):
	mykrobe_genome_pos = {}
	for gene in mykrobe_gene:
		if gene in gene_dic:
			gene_start = gene_dic[gene][0]
			#print gene, gene_start
		else: 
			pass
			#print gene , 'gene missing'	
		

		for entry in open('%s/%s' % (script_dir , all_genes)):
			#print entry
			entry = entry.split('\t')
			#print entry[0]
			ID = entry[0]
			start = entry[1]
			end = entry[2]
			reverse = entry[3]
			if gene == ID:
				print ID, start, end
				if reverse == 'c' :
					print 'reverse'
					start = int(start)
					end = int(end)
					genome_pos_list = mykrobe_gene[gene]
					genome_pos_list = [end - x for x in genome_pos_list]
					mykrobe_genome_pos[gene] = genome_pos_list
					
					

				else:
					print 'forward'
					start = int(start)
					end = int(end)
					genome_pos_list = mykrobe_gene[gene]
					genome_pos_list = [  x + start for x in genome_pos_list]
					mykrobe_genome_pos[gene] = genome_pos_list

	#print mykrobe_gene['inhA']
	#print mykrobe_genome_pos['inhA']
	#print mykrobe_gene['gid']
	#print mykrobe_genome_pos['gid']
	
	for gene in mykrobe_genome_pos:
		snps = mykrobe_genome_pos[gene]
		print gene, snps
	#print mykrobe_genome_pos
	return mykrobe_genome_pos
		
def mykrobe_fold (mykrobe_positions , fold_list)
	
	for gene in mykrobe_positions:
		print gene 



main()