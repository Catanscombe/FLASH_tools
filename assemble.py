import os
import argparse
import sys
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
reference = 'references/NC_000962.3.fasta'
targets = 'references/TB_FLASH_v2_genes.fasta'
def main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument ('in_file_R1',  help = 'forward read')
	parser.add_argument ('in_file_R2',  help = 'reverse read')
	parser.add_argument ('sample_ID' , help = 'how you want out files to be named')

	args = parser.parse_args()
	#assembly_whole_genome(args)
	assembly_targets(args)


def assembly_whole_genome(args):
	os.system ('bwa mem %s/%s %s %s > %s.sam '% (script_dir , reference , args.in_file_R1 , args.in_file_R2, args.sample_ID))
	os.system ('samtools view -h -b -S %s.sam > %s.bam' % (args.sample_ID , args.sample_ID))
	os.system ('samtools sort %s.bam > %s_S.bam' % (args.sample_ID, args.sample_ID))
	# coverage at > Q30
	os.system ('samtools depth -Q 30 %s_S.bam | wc -l > %s_Q30.depth.txt' % (args.sample_ID , args.sample_ID))
	# number of mapped reads
	os.system ('samtools view -F 0x904 -c %s_S.bam > %s_mapped_reads.txt'% (args.sample_ID , args.sample_ID))
	# total number of reads
	os.system ('samtools view -c %s_S.bam > %s_all_reads.txt'% (args.sample_ID , args.sample_ID))

def assembly_targets(args):
#	os.system ('bwa mem %s/%s %s %s > %s_targets.sam '% (script_dir , targets , args.in_file_R1 , args.in_file_R2, args.sample_ID))
#	os.system ('samtools sort %s_targets.bam > %s_targets_S.bam' % (args.sample_ID, args.sample_ID))
	# coverage at > Q30
	os.system ('samtools depth -Q 30 %s_targets_S.bam | wc -l > %s_targets_Q30.depth.txt' % (args.sample_ID , args.sample_ID))
	# number of mapped reads
	os.system ('samtools view -F 0x904 -c %s_targets_S.bam > %s_targets_mapped_reads.txt'% (args.sample_ID , args.sample_ID))
	


main()