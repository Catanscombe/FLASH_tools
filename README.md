# FLASH_tools
Analysis tools for samples process using FLASH for Mtb.

1. mapping.py
2. all_but.py
3. find_folds.py
4. get_mykrobe.py


1) mapping.py

	This script will reference map the reads (using bwa mem) to NC_000962.3 Mycobacterium tuberculosis H37Rv, complete genome. It will also map the reads to the 50 genes which are targetted for enrichment

        usage: mapping.py [-h] in_file_R1 in_file_R2 sample_ID

		positional arguments:
	  		in_file_R1  forward read
	  		in_file_R2  reverse read
	 	 	sample_ID   how you want out files to be named

		optional arguments:
	  		-h, --help  show this help message and exit

    Outputs:

	1)`sample_ID_assembly_stsats.csv` which contains read and mapping information.
	2)`sample_ID_targets.csv` contains mapping results for each of the 50 targets
	3)`sample_ID_S.bam` a sorted bam file from the whole genome mapping
	4)`sample_ID_targets_S.bam` sorted bam file from reference mapping ot target genes
	5)`sample_ID.depth` a file containing the depth at all points in the whole genome

2) all_but.py

    This scripts finds the genome position of the probes and the average depth of the enriched and not enriched genome regions

		usage: all_but.py [-h] depth_file sample_ID

		positional arguments:
	  		depth_file  depth file, sample.depth
	  		sample_ID   file naming

		optional arguments:
	 		 -h, --help  show this help message and exit

    Outputs:

	1) `sample_ID_probe_positions.csv` a file containing the genome points of the probes
	(gene, probe_name , probe_Sequence . genome_point , direction_of_probe)
	2) `sample_ID_all_but` contains average depth of the enriched and not enriched genome regions


3) find_folds.py

    This script describes the fold increase across the whole genome and for all genes in enriched

		usage: find_folds.py [-h] depth_file all_but sample_ID

		positional arguments:
		depth_file  depth file, sample.depth
		all_but     csv file contianing the all_but_av
		sample_ID   file naming

		optional arguments:
		-h, --help  show this help message and exit

    Outputs:

	1)'sample_ID_gene_fold.csv' for each gene there are all the fold enrichemnt values between the first and last probe targetting that region
	2)'sample_ID_gene_fold_stats' per gene stats about the enrichent including max and min fold. Also the number of points with less than one fold enrichment, 1-5 fold enrichment and > 5 fold enrichment
	3)'sample_ID_probe_pairs.csv' for each probes pair it outputs the probe positions, minumum fold enrichment, maximum fold enrichements and the number of times there is <1, 1-5 and >5 fold enrichemnt. It also outputs the distance bwetween the probe pairs


4) get_mykrobe.py

    This script finds the position of the SNPs used by Mykrobe (https://www.mykrobe.com) for mTB resistance testing


		usage: get_mykrobe_targets.py [-h] depth_file_fold sample_ID

		positional arguments:
		depth_file_fold  depth fold file, sample_fold.depth
		sample_ID        file naming

		optional arguments:
		-h, --help       show this help message and exit

Outputs:

	1)'sample_ID_mykrobe_fold.csv' for each gene it outputs the genome position of the SNP used by Mykrobe and the depth at that point in the genome
