import os
import argparse

def main():
	script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
	reference = 'references/NC_000962.3.fasta'
	parser = argparse.ArgumentParser()
	parser.add_argument ('in_file_R1',  help = 'forward read')
	parser.add_argument ('in_file_R2',  help = 'reverse read')
	parser.add_argument ('sample_ID' , help = 'how you want out files to be named')

	args = parser.parse_args()
	assembly(args)


def assembly(args):
	os.system ('bwa mem %s %s %s > %s.sam ')


os.system	