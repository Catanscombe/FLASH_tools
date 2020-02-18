import os
import subprocess
import argparse
import sys
from Bio import SeqIO
import csv
import fileinput

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
reference = 'references/NC_000962.3.fasta'
targets = 'references/TB_FLASH_v2_genes.fasta'
genome_size = 4474555
target_size = 103895
def main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument ('in_file_R1',  help = 'forward read')
	parser.add_argument ('in_file_R2',  help = 'reverse read')
	parser.add_argument ('sample_ID' , help = 'how you want out files to be named')

	args = parser.parse_args()
	assembly_whole_genome(args)
	get_target_tats(args)


def assembly_whole_genome(args):
	with open ('%s_Assembly_statsw.csv' % (args.sample_ID) , 'a' ) as rf:
		
		os.system ('bwa mem %s/%s %s %s > %s.sam '% (script_dir , reference , args.in_file_R1 , args.in_file_R2, args.sample_ID))
		os.system ('samtools view -h -b -S %s.sam > %s.bam' % (args.sample_ID , args.sample_ID))
		os.system ('samtools sort %s.bam > %s_S.bam' % (args.sample_ID, args.sample_ID))
		# coverage at > Q30
		coverage_Q30 = subprocess.check_output('samtools depth -Q 30 %s_S.bam | wc -l '  % (args.sample_ID ) , shell = True)
		# number of mapped reads
		WG_mapped_reads = subprocess.check_output ('samtools view -F 0x904 -c %s_S.bam'% (args.sample_ID ), shell = True)
		#total number of reads
		total_reads = subprocess.check_output ('samtools view -c %s_S.bam '% (args.sample_ID ), shell = True)


		os.system ('bwa mem %s/%s %s %s > %s_targets.sam '% (script_dir , targets , args.in_file_R1 , args.in_file_R2, args.sample_ID))
		os.system ('samtools view -h -b -S %s_targets.sam > %s_targets.bam' % (args.sample_ID , args.sample_ID))
		os.system ('samtools sort %s_targets.bam > %s_targets_S.bam' % (args.sample_ID, args.sample_ID))
		# coverage at > Q30
		target_Q30_coverage =subprocess.check_output('samtools depth -Q 30 %s_targets_S.bam | wc -l ' % (args.sample_ID ) ,shell = True)
		# number of mapped reads
		target_mapped_reads = subprocess.check_output ('samtools view -F 0x904 -c %s_targets_S.bam '% (args.sample_ID ), shell = True)
		os.system ('rm %s_targets.sam' % (args.sample_ID))
		os.system ('rm %s.sam' % (args.sample_ID))


		pec_genome_cov = float(coverage_Q30)/genome_size
		target_pec_genome_cov = float(target_Q30_coverage)/target_size
		pec_mapped_reads = float(WG_mapped_reads)/int(total_reads)
		pec_target_mapped_reads = float(target_mapped_reads)/int(total_reads)

		
		to_print = map(str,[total_reads, WG_mapped_reads, pec_mapped_reads,genome_size,coverage_Q30,pec_genome_cov,target_mapped_reads,pec_target_mapped_reads,target_size,target_Q30_coverage,target_pec_genome_cov])

		to_print = [x.strip() for x in to_print]
		
		
		writer =csv.writer(rf , delimiter = ',')
		writer.writerow (to_print)
	for line in fileinput.input(files = ['%s_Assembly_statsw.csv' % (args.sample_ID)] , inplace = True):
		if fileinput.isfirstline():
			print 'sample_ID,total_reads,WG_mapped_reads,pec_mapped_reads,genome_size,coverage_Q30,pec_genome_cov,target_mapped_reads,pec_target_mapped_reads,target_size,target_Q30_coverage,target_pec_genome_cov'
		print line

def  get_target_tats(args):
	
	os.system ('samtools depth -Q 30 %s_targets_S.bam > %s_targets.depth'% (args.sample_ID , args.sample_ID))
	with open ('%s_targets.csv' % (args.sample_ID) , 'a') as f:
		FastaFile = open('%s/%s' % (script_dir , targets) , 'rU')
		
		for rec in SeqIO.parse(FastaFile, 'fasta'):
		    name = rec.id
		    name = name.split('|')
		    name = name[0] 
		    seq = rec.seq
		    seqLen = len(rec)
		    
		    coverage_target = subprocess.check_output ('grep "%s" %s_targets.depth |wc -l ' % (name, args.sample_ID), shell = True)
		    pec_target_coverage = float(coverage_target)/seqLen
		    out_put = map(str, [name, seqLen , coverage_target , pec_target_coverage])
		    out_put = [x.strip() for x in out_put]
		    writer =csv.writer (f, delimiter = ',')
		    writer.writerow (out_put)

		FastaFile.close()


main()
