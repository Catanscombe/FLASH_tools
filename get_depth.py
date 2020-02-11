from __future__ import division
import csv

in_file = 'Cas9-Rv.depth'
genes = 'target_genes_info_clean.txt'
def main():
	depth_list = depth (in_file)
	gene_dic = list_lookup (depth_list , genes)
	gene_depth_list = gene_depth (gene_dic , depth_list)
	all_but (depth_list , gene_depth_list)


def depth (in_file):
	with open (in_file, 'rb') as f:
		depth_list = list()
		for line in f:
		
			#print line
			line = line.strip(). split('\t')
			
			#print line[2]
			depth = int(line[2]) 
	   
			depth_list.append(depth)


		#print depth_list

	return depth_list

def list_lookup (depth_list, genes):
	gene_dic = {}
	for line in open (genes):
		print line
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

def gene_depth (gene_dic, depth_list):
	gene_depth_list = list()
	for gene in gene_dic:
		depth_points = depth_list[ gene_dic[gene][0]:gene_dic[gene][1]]
		gene_depth_list.extend(depth_points)
		print gene
		#print gene_dic[gene]
		#print depth_points
		print sum(depth_points) / len(depth_points)
		print min(depth_points)
		print max(depth_points)
		#print depth_points
	print len(gene_depth_list)

	#print gene_depth_list
	return gene_depth_list
def all_but (depth_list , gene_depth_list):

	all_sum = sum(depth_list)
	gene_sum = sum(gene_depth_list)
	all_len = len(depth_list)
	gene_len = len(gene_depth_list)

	all_but_sum = all_sum - gene_sum
	all_but_len = all_len - gene_len

	all_but_av = all_but_sum/all_but_len
	print all_but_av



		
main()