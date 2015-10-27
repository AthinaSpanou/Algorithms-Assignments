#IMPLEMENTATION OF THE ALGORITHM OF AGRAWAL AND SRIKANT (A Priori)
import csv
import itertools
import argparse
import sys

# ARGPARSE
parser = argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--numeric", help="items are numeric",
                    action="store_true", default=False)
parser.add_argument("support", help="support threshold")
parser.add_argument("-p", "--percentage",
                    action="store_true", default=False,
                    help="treat support threshold as percentage value")
parser.add_argument("filename", help="input filename")
parser.add_argument("-o", "--output", type=str, help="output file")

args = parser.parse_args()

input_file = open(args.filename, 'r') # OPEN FILE -- args.filename
csv_reader = csv.reader(input_file, delimiter=',')
count = 0 # counter for the rows of the file
for row in csv_reader:
        unique_row_items = list(set([field.lower().strip() for field in row]))
        count = count + 1 
input_file.close()

s = 0 # SUPPORT
if args.support:
    s = int(args.support)
if args.percentage: # if the percentage is given
    s = (int(args.support) / 100) * count

# METHOD OF FIRST PASS
def APrioriFirstPass(csv_reader,s):
    counts = {} # a dictionary that shows in how many baskets the item is
    freq = {} # a dictionary that has the items with frequency above the support,s
    for row in csv_reader:
        unique_row_items = list(set([field.lower().strip() for field in row]))
        for item in unique_row_items:
            counts[item] = counts.get(item,0) + 1
    for item in counts:
        if counts[item] >= int(s):
            if args.numeric: # if the items are numerics
                freq[(int(item),)] = counts[item]
            else:
                freq[(item),] = counts[item]
    return freq

# METHOD OF K + 1 PASSES
def APrioriPass(csv_reader,freqk,k,s):
    counts = {}
    freq = {} # a dictionary containg the frequencies of itemsets of size k + 1 with threshold s
    for row in csv_reader:
        unique_row_items = list(set([field.lower().strip() for field in row]))
        if args.numeric: # if the items are numerics
            unique_row_items=[int(i) for i in unique_row_items] 
        itemset_pairs = itertools.combinations(freqk, 2) # get all the possible pairs of the set
        candidates=[] # a list whick checks that every itemset is used only once
        for pair in itemset_pairs:
            fp, sp = pair
            candidate = tuple(sorted(set((fp) + (sp))))
            if candidate not in candidates:
                candidates.append(candidate)
                if len(candidate) == k + 1 and set(candidate) <= set(unique_row_items):
                    counts[candidate] = counts.get(candidate,0) + 1
    for itemset in counts:
        if counts[itemset] >= int(s):
            freq[itemset] = counts[itemset]
    return freq

all_freq = [] # a list containing the frequencies of all itemsets with threshold s
k = 1 # the size of itemsets in freqk
freq = {}
freqk = {} # a dictionary containg the frequencies of itemsets of size k in baskets above the support,s

input_file = open(args.filename, 'r') # OPEN FILE -- args.filename
csv_reader = csv.reader(input_file, delimiter=',')

freqk = APrioriFirstPass(csv_reader,s)

input_file.close() # CLOSE INPUT FILE

while freqk:
    all_freq.append(freqk)
    input_file = open(args.filename, 'r') # OPEN FILE -- args.filename
    csv_reader = csv.reader(input_file, delimiter=',')
    freq = APrioriPass(csv_reader,freqk,k,s)
    input_file.close() # CLOSE INPUT FILE
    freqk = freq
    k = k + 1

if args.output: # WRITE THE RESULTS IN A FILE -- args.output
    output_file = open(args.output, 'w')
    csv_writer = csv.writer(output_file, delimiter=';')
else:
    csv_writer = csv.writer(sys.stdout, delimiter=';') # PRINT THE RESULTS
    
for item in all_freq:
    row=[]
    for key,value in item.items():
        row.append(str(key)+':'+str(value)) # (key):value
    csv_writer.writerow(row)

if args.output:
        output_file.close()

