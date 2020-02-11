from Bio.Seq import Seq
from Bio import SeqIO
targets = 'probe_target'
reference = 'Mycobacterium_tuberculosis_H37Rv.fasta'
# with open (reference ) as genome: 
genome = SeqIO.read(reference, 'fasta')
# for genome in genome_record:
genome = str(genome.seq)
# genome = genome.read()
#print genome
for line in open(targets):
	line = line.strip().split('\t')
	ID = line[0]
	target = line[1]
	found = genome.find(target)
	if found!= -1:
		print ID , target, found , 'F'
	else:
		target = Seq(target)
		target_rc  = target.reverse_complement()
		target_rc = str(target_rc)
		#print target
		#print target_rc
		found_rc = genome.find(target_rc)
		if found_rc != -1:
			print ID, target, found_rc , 'RC'
		else: 
			print ID, target, 'not found'
