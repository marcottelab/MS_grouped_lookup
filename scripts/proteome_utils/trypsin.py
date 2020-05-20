'''
    this is an in silico trypsin digestion program. The input is a fasta file which contains protein sequence to be digested, the output is a txt file which contains all trypsin digested peptides and corresponding protein accessions.

From https://github.com/yafeng/trypsin/blob/master/trypsin.py
Modified by Claire McWhite 5/13/2016 
'''
from __future__ import print_function
from Bio import SeqIO
import argparse
def TRYPSIN(proseq,miss_cleavage):
    peptides=[]
    cut_sites=[0]

    for i in range(0,len(proseq)-1):
        if proseq[i]=='K' and proseq[i+1]!='P':
            cut_sites.append(i+1)
        elif proseq[i]=='R' and proseq[i+1]!='P':
            cut_sites.append(i+1)
    
    if cut_sites[-1]!=len(proseq):
        cut_sites.append(len(proseq))

    if len(cut_sites)>2:
        if  miss_cleavage==0:
            for j in range(0,len(cut_sites)-1):
                #peptides.append(proseq[cut_sites[j]:cut_sites[j+1]])
                start = cut_sites[j]
                end = cut_sites[j + 1]
                peptides.append([proseq[start:end], start + 1, end])
 

        elif miss_cleavage==1:
            for j in range(0,len(cut_sites)-2):
                start = cut_sites[j]
                end1 = cut_sites[j+1]
                end2 = cut_sites[j+2]
                peptides.append([proseq[start:end1], start + 1, end1])
                peptides.append([proseq[start:end2], start + 1, end2])
            
            startm2 = cut_sites[-2]
            endm1 = cut_sites[-1]
            #peptides.append([proseq[cut_sites[-2]:cut_sites[-1]], )
            peptides.append([proseq[startm2:endm1], startm2 + 1, endm1] )

        elif miss_cleavage==2:
            for j in range(0,len(cut_sites)-3):

                start = cut_sites[j]
                end1 = cut_sites[j+1]
                end2 = cut_sites[j+2]
                end3 = cut_sites[j+3]

                peptides.append([proseq[start:end1], start + 1, end1])
                peptides.append([proseq[start:end2], start + 1, end2])
                peptides.append([proseq[start:end3], start + 1, end3])

            startm3 = cut_sites[-3]
            startm2 = cut_sites[-2]
            endm2 = cut_sites[-2]
            endm1 = cut_sites[-1]
           
            peptides.append([proseq[startm3:endm2],startm3 + 1,endm2])
            peptides.append([proseq[startm3:endm1],startm3 + 1,endm1])
            peptides.append([proseq[startm2:endm1],startm2 + 1,endm1])

    else: #there is no trypsin site in the protein sequence
        peptides.append([proseq, 1, len(proseq)]) #Check this
    final_peptides = [i for i in peptides if len(i[0])>=6 and len(i[0])<=60]
    return final_peptides

def process_fasta(input_file, miss, output_file, positions= False): 
    handle=SeqIO.parse(args.input_file,'fasta')
    output=open(output_file,'w')

    if positions == False:
        output.write("%s,%s\n" % ("ProteinID","Peptide"))
    elif positions == True:
        output.write("%s,%s,%s,%s\n" % ("ProteinID","Peptide", "Start","End"))
    for record in handle:
        proseq = str(record.seq)
        peptide_list = TRYPSIN(proseq, miss)
        for peptide in peptide_list:
            if positions == False:
                output.write("%s,%s\n" % (record.id,peptide[0]))
            elif positions == True:
                output.write("%s,%s,%s,%s\n" % (record.id,peptide[0], peptide[1], peptide[2]))
   

    handle.close()
    output.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Break a fasta into canonical and readthrough DNA/protein/peptides')

    
    parser.add_argument('-i', '--input_file', dest='input_file', action="store", required=True, type=str, help= 'Input fasta')

    parser.add_argument('-m', '--miss', dest='miss', action="store", default = 2, type=int, help= 'Number of missed cleavages. Default 2')

    parser.add_argument('-o', '--output_file', dest= 'output_file', action="store", type=str, help= 'Output file for peptides')

    parser.add_argument('-p', '--positions', dest= 'positions', action="store", type=bool, default = False, help= 'Whether or not to include peptide positions')

    args = parser.parse_args()
    process_fasta(args.input_file, args.miss, args.output_file, args.positions)
   
