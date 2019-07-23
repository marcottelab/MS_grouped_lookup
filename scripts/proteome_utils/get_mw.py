import argparse
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis




def MASS(fasta, output_file):

    handle=SeqIO.parse(fasta,'fasta')


    output=open(output_file,'w')
    
    output.write("%s,%s\n" % ("ProteinID","MW"))
    
    for record in handle:
        proseq=str(record.seq)
        proseq = proseq.replace("X", "D") #Replace unknown with median weight amino acid
        mw = round(ProteinAnalysis(proseq).molecular_weight(), 4)

        output.write("%s,%s\n" % (record.id,mw))
    
    handle.close()
    output.close()
 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get wide form')

    parser.add_argument('--fasta', '-f', dest='fasta', action="store", type=str, required=True)
    parser.add_argument('--outfile', '-o', dest='outfile', action="store", type=str, required=False, default ="mw_mapping")

    args = parser.parse_args()

    MASS(args.fasta, args.outfile)
    

    
   
