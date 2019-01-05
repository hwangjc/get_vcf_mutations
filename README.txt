#################

get_mutations documentation

author:	Jae Chan Hwang (hwangjc@umich.edu)
date:	10-16-2018

#################

usage: get_mutations.py [-h] -i INPUT [-s] [-g] [-a] [-t] [-T]

Scans vcf files and returns lines with somatic/germline mutations. Also cleans
up the data a little bit.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The name of the (parsed) input vcf file.
  -s, --somatic         If -s is specified, will output somatic mutations.
  -g, --germline        If -g is specified, will output germline mutations.
  -a, --all             If -a is specified, will output every line.
  -t, --tcgaid_append   If -t is specified, will append the TCGA ID to the end
                        of every line (if the program can find it).
  -T, --tcgaid_only     If -T is specified, will attempt to search for a TCGA
                        ID within the file and output it. This will be the
                        only output.

examples:

	* If we want to print ONLY the TCGA ID, then run like:
		
		$ python get_mutations.py -i input.vcf -T

	* If we want to print every line, then run like:

	  	$ python get_mutations.py -i input.vcf -a
	
	* If we want to print every line AND append the TCGA ID to the end of every
	  line, then run like:
	
	  	$ python get_mutations.py -i input.vcf -a -t

	* If we want to print ONLY the lines with somatic mutations, then run like:

		$ python get_mutations.py -i input.vcf -s

other:

	The input file will always be valid if you use my other 
	python script, "parse_vcf.py", to parse the raw vcf file first :)

	The input vcf file should not have metadata/header.
