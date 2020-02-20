from __future__ import division
from Bio.Seq import Seq
from Bio import SeqIO
targets = 'probe_target'
reference = '../Mycobacterium_tuberculosis_H37Rv.fasta'
depth_file = 'Cas9-Rv.depth'
all_but_av = 105



# with open (reference ) as genome: 
genome = SeqIO.read(reference, 'fasta')
# for genome in genome_record:
genome = str(genome.seq)

def main():
	probe_pos = find_probe_pos(targets, reference)
	fold_list = genome_fold(probe_pos, depth_file, all_but_av)
	fold_per_gene (fold_list, probe_pos)
	get_probe_fold (fold_list , probe_pos)
#	get_min_between_probes(fold_list, probe_pos)


# genome = genome.read()
#print genome
def find_probe_pos(targets, reference):
#find the target position of the probes from the H37Rv genome, add to dictionary per gene
	probe_pos = {}
	for line in open(targets):
		
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
#	print probe_pos
	return probe_pos

def genome_fold (probe_pos, depth_file, all_but_av):
# create a list of the relative fold depth acrosless the whole genome
	with open(depth_file, 'rb') as f:
		fold_list = list()
		for line in f:
			line = line.strip().split('\t')

			depth = float(line[2])
			#print depth
			fold = depth/all_but_av
			#print fold
			fold_list.append(fold)
	#print fold_list
	return fold_list



def fold_per_gene (fold_list, probe_pos):
# for each gene find the fold depth, including +300 and -300 from the last and first probe
	print 'gene' , 'min_fold' , 'max_fold' , '<1fold' , '<1-5fold', '>5fold' , 'total_len'
	for gene in probe_pos:
		#print probe_pos[gene]
		last_probe = max(probe_pos[gene])
		first_probe = min(probe_pos[gene])
#		print gene, first_probe , last_probe
		start = first_probe - 300
		end = last_probe + 300

#		print gene , start , end 
		fold_points = fold_list[start:end]
#		print gene ,fold_points
		min_fold = min (fold_list[start:end])
		max_fold = max (fold_list[start:end])
		vlow_fold = sum (i < 1 for i in fold_list[start:end] )
		five_fold = sum (i < 5 for i in fold_list[start:end] )
		low_fold = five_fold - vlow_fold
		total_len = len(fold_points)
		high_fold = total_len - five_fold
		

		print gene ,min_fold , max_fold , vlow_fold , low_fold , high_fold , total_len


def get_probe_fold (fold_list , probe_pos):
# find the fold at the probe points
	for gene in probe_pos:
		for position in probe_pos[gene]:
			# print gene , position
			pf = fold_list[position]
			p_n20 = position-20
			p_p20 = position+20

			f_n20 = fold_list[p_n20]
			f_p20 = fold_list[p_p20]

			start = min(probe_pos[gene])   - 300 
			end = max(probe_pos[gene]) + 300
			#print gene, p_n20 , f_n20 , position , pf, p_p20 , f_p20

def get_min_between_probes(fold_list, probe_pos):
	print 'gene' , 'probe_1' , 'probe_2' ,'low_fold' , 'high_fold' ,'<1_probe' , '1-5_probe' , '>5_probe' , 'probe_pair_len'
	for gene in probe_pos:
		#print probe_pos[gene]
		probe_pos_list = probe_pos[gene]
		sorted_pos = sorted(probe_pos_list)
		#print sorted_pos
		#list_len = len(sorted_pos)
		#print gene , list_len
		for i in range(0, len(sorted_pos) - 1):
			probe_1 = sorted_pos[i]
			probe_2 = sorted_pos[i + 1]
			our_list = fold_list[probe_1:probe_2]
			low_probe =min(our_list)
			low_probe_pos = our_list.index(min(our_list))
			high_probe = max(our_list)
			high_probe_pos = our_list.index(max(our_list))


			vlow_probe_fold =sum (i < 1 for i in our_list)
			five_probe_fold =sum (i < 5 for i in our_list)
			low_probe_fold = five_probe_fold - vlow_probe_fold
			probe_len = len(our_list)
			high_probe_fold = probe_len - five_probe_fold
			print gene, probe_1 , probe_2 ,low_probe, high_probe , vlow_probe_fold, low_probe_fold , high_probe_fold , probe_len  



main ()
















