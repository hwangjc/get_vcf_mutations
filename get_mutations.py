import sys
import argparse
import cStringIO

##### parse arguments
parser = argparse.ArgumentParser(description="Scans vcf files and returns lines with somatic/germline mutations. Also cleans up the data a little bit.");
parser.add_argument('-i', '--input', required=True, help="The name of the (parsed) input vcf file.");
parser.add_argument('-s', '--somatic', action='store_true', help="If -s is specified, will output somatic mutations.");
parser.add_argument('-g', '--germline', action='store_true', help="If -g is specified, will output germline mutations.");
parser.add_argument('-a', '--all', action='store_true', help="If -a is specified, will output every line.");
parser.add_argument('-t', '--tcgaid_append', action='store_true', help="If -t is specified, will append the TCGA ID to the end of every line (if the program can find it).");
desc_T = "If -T is specified, will attempt to search for a TCGA ID within the file and output it. This will be the only output.";
parser.add_argument('-T', '--tcgaid_only', action='store_true', help=desc_T);

_args = parser.parse_args();
globals()['args'] = _args;
#####

##### functions #####

# finds the TCGA ID inside the file
# looks at the file name and the first line of the file to see if it can find
# a TCGA ID. If it finds more than one, it uses the longer one.
def findID(file_name,first_line):
    file_name_index = file_name.find("TCGA-");
    first_line_index = first_line.find("TCGA-");
    tcga_id_file = ""
    tcga_id_line = ""
    tcga_id = ""

    if file_name_index != -1:
        tcga_id_file = file_name[file_name_index:]; 
    if first_line_index != -1:
        tcga_id_line = first_line[first_line_index:];

    counter = 0;
    for i in tcga_id_file:
        if i.isalnum() or i == '-':
            counter += 1;
        else:
            break;
    tcga_id_file = tcga_id_file[0:counter];

    counter = 0;
    for i in tcga_id_line:
        if i.isalnum() or i == '-':
            counter += 1;
        else:
            break;
    tcga_id_line = tcga_id_line[0:counter];

    if len(tcga_id_file) < len(tcga_id_line):
        tcga_id = tcga_id_line;
    else:
        tcga_id = tcga_id_file;

    globals()['ID'] = tcga_id;


# finds the columns that contains the information about somatic / germline mutations.
# looks for columns that start with either '0/', '1/', or '.:'
def setColumns(first_line):
    counter = 0;
    col_counter = 0;

    first_line = first_line.split();
    for col in first_line:
        if len(col) > 2 and (((col[0] == '0' or col[0] == '1') and col[1] == '/') or (col[0] == '.' and col[1] == ':')):
            if counter == 0:
                globals()['COL1'] = col_counter;
            elif counter == 1:
                globals()['COL2'] = col_counter;
            counter += 1;
        col_counter += 1;

# removes unecessary information from columns containing somatic/germline info
def cleanCol(col):
    if col[0:2] == ".:":
        col = col[0:2];
    else:
        col = col[0:3];
    
    return col;

# prints the line to stdout and appends TCGA ID if -t is flagged
def printLine(line):
    from cStringIO import StringIO
    oss = StringIO();

    max_col = len(line);
    curr_col = 1;
    for col in line:
        if curr_col == max_col:
            oss.write(col);
        else:
            oss.write(col + '\t');
        curr_col += 1;
    
    if args.tcgaid_append == True:
        oss.write('\t' + ID); 

    print(oss.getvalue());

# parses the line to see whether it contains a somatic or germline mutation.
# if mutation is somatic and -s is flagged, it will print the line to stdout.
# if mutation is germline and -g is flagged, it will print the line to stdout.
# if -a is flagged, it will print every line
# if -t is flagged, it will also append the TCGA ID to the end of every line
def parseLine(line):
    line = line.split();
    
    line[COL1] = cleanCol(line[COL1]);
    line[COL2] = cleanCol(line[COL2]);

    if args.all == True:
        printLine(line); 
    else:
        if args.germline == True:
            if line[COL1] == line[COL2] and line[COL1] != ".:":
                printLine(line);
        if args.somatic == True:
            if line[COL1] != line[COL2] and line[COL1] != ".:" and line[COL2] != ".:":
                printLine(line);

##### #####

##### ___main___ #####

vcf_file_name = args.input;

if vcf_file_name[-4:] != ".vcf":
    print("File is not a .vcf file");
    sys.exit();

vcf_file = open(vcf_file_name);

first_line = vcf_file.readline().strip();

# find TCGA ID if -t or -T was specified
if args.tcgaid_only == True or args.tcgaid_append == True: 
    findID(vcf_file_name,first_line);

# if -T flag was set, print the TCGA ID and exit
if args.tcgaid_only == True:
    print(ID);
    sys.exit();

setColumns(first_line);
parseLine(first_line);

for line in vcf_file:
    parseLine(line);

##### end #####
