import csv
target = 'target_genes'
all_genes = 'all_genes'


for line in open(target):
    line = line.strip()
    #print(line)
    for entry in open(all_genes):
        #print entry
        entry = entry.split('\t')
        #print entry[0]
        ID = entry[0]
        start = entry[1]
        end = entry[2]
        if line == ID:
            print ID, start, end
        

    

