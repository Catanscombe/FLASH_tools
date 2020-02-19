# FLASH_tools
Analysis tools for samples process using FLASH for mTB. 

1)mapping.py
This script will reference map the reads (using bwa mem) to NC_000962.3 Mycobacterium tuberculosis H37Rv, complete genome. It will also map the reads to the 50 genes which are targetted for enrichment
output: 
	1)'sample_ID_assembly_stsats.csv' which contains read and mapping information. 
	2)'sample_ID_S.bam' a sorted bam file from the whole genome mapping
	3)'sample_ID_targets_S.bam' sorted bam file from reference mapping ot target genes
	4)'sample_ID.depth' a file containing the depth at all points in the whole genome





usage: mapping.py [-h] in_file_R1 in_file_R2 sample_ID

positional arguments:
  in_file_R1  forward read
  in_file_R2  reverse read
  sample_ID   how you want out files to be named

optional arguments:
  -h, --help  show this help message and exit



