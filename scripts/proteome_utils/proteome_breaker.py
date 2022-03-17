import argparse
from Bio import SeqIO
#CDM I didn't write this, not sure where it was from

def proteome_breaker(fasta_file, numseq, output_dir):
        print("Breaking proteome into {0} sequences".format(str(numseq)))
        #read in proteome
        proteome = SeqIO.parse(fasta_file, "fasta")
        #get the name of the proteome
        pid = fasta_file.replace(".fasta", "")
        pid = pid.replace(".fa", "")
        pid = pid.split('/')
        pid = pid[len(pid)-1] 
        print(pid)
        
        #build up batches
        n = 0
        entry = True
        while entry:
            print(n)
            batch = []        
            while len(batch) < int(numseq):
                try:
                    entry = next(proteome)
                except StopIteration:
                    entry = None
                if entry is None:
                   #End of file
                    break
                batch.append(entry)
            print(batch)
            if batch:
                #SeqIO.write(batch, sys.argv[3]+pid+".scan"+str(n+1)+".fasta", "fasta")
                SeqIO.write(batch, output_dir + "/" + pid+".seg"+str(n+1)+".fasta", "fasta")
            n+=1	


parser = argparse.ArgumentParser(description='Returns a group of fasta files with specified number of sequences each (except for the last file which will likely be short)')

parser.add_argument('fasta_file', action="store", type=str, help="a fasta file to break up")
parser.add_argument('numseq', action="store", type=int, help="Number of sequences per output")
parser.add_argument('output_dir', action="store", type=str, help = "a directory to store output files")

args = parser.parse_args()

        
proteome_breaker(args.fasta_file, args.numseq, args.output_dir)
