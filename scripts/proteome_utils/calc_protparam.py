# Straight from https://biopython.org/wiki/ProtParam
from __future__ import print_function
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import argparse

def get_params(fasta_file, out_file):
    with open(out_file, "w") as out: 
        out.write("UniprotID,MW,pI\n")
        with open(fasta_file, "r") as handle:
            for record in SeqIO.parse(handle, "fasta") :
    
                analysed_seq = ProteinAnalysis(str(record.seq).replace("X", ""))
                outstring = record.id + ","+ str(analysed_seq.molecular_weight()) + "," + str(analysed_seq.isoelectric_point()) + "\n"
                out.write(outstring)


parser = argparse.ArgumentParser("Calcular MW and pI for a proteome")
parser.add_argument("--fasta_file", dest = "fasta_file",  required = True,
                             help  = "A fasta to compute params for")
parser.add_argument("--out_file", dest = "out_file", required = False,
                             help  = "filenametowrite")


args = parser.parse_args()
 

get_params(args.fasta_file, args.out_file)

