import argparse
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import pandas as pd

def concatenate_seq(fasta, orthology_grouped, limit = True):
     print("start concat")
     
     #concatseq = orthology_grouped['seq'].transform(lambda x: 'KKK'.join(x)).drop_duplicates()
     if limit == True:
         limitedseq = orthology_grouped.head(3)
         orthology_grouped = limitedseq.groupby(['ID'])
 
     

     concatseq = orthology_grouped['seq'].agg(lambda x: 'KKK'.join(x))
     concatseq = concatseq.reset_index()
     print(concatseq)

     return(concatseq)


def longest_seq(fasta, orthology_grouped):

     longestseq = orthology_grouped.first()
     longestseq = longestseq.reset_index()
     longestseq = longestseq[['ID', 'seq']]
     print(longestseq)
     return(longestseq) 

def random_seq(fasta, orthology_grouped):
     randsamp = orthology_grouped.apply(lambda x: x.sample(n=1))
     randsamp = randsamp[['ID', 'seq']]
     print(randsamp)
     return randsamp



def diploid(fasta_file,  orthology_file, choice):
	#read in proteome
	proteome = SeqIO.parse(fasta_file, "fasta")

        identifiers = []
        lengths = []
        seqs = []
        for seq_record in proteome:
            identifiers.append(seq_record.id)
            lengths.append(len(seq_record.seq))
            seqs.append(''.join(seq_record.seq))

        fasta_table = pd.DataFrame(dict(ProteinID = identifiers, length=lengths, seq = seqs)).set_index(['ProteinID'])

     
        orthology = pd.read_table(orthology_file, index_col=0)
      
        fasta_orthoannot = fasta_table.join(orthology, how = "left")
        

        
        fasta_orthoannot = fasta_orthoannot.reset_index()
        fasta_orthoannot['ID'] = fasta_orthoannot['ID'].fillna(fasta_orthoannot['ProteinID'])
        print(fasta_orthoannot.head)
        orthology_grouped = fasta_orthoannot.sort_values(by=['length'], ascending=False).groupby(['ID'])

        
        
        if choice == 'random':
            newseqs = random_seq(proteome, orthology_grouped)
        elif choice == 'longest':
            newseqs = longest_seq(proteome, orthology_grouped)
        elif choice == 'concat':
            newseqs = concatenate_seq(proteome, orthology_grouped)
       
        newseqs = newseqs.set_index(['ID'])
        newseqs_list = newseqs.to_records()
        outfilename = choice + "_" + fasta_file

        annot_df = pd.read_csv(args.annotation_file, index_col = 0)
        annot_dict = annot_df.to_dict('index')
        seqs = []
        for key, value in newseqs_list:
            #print(key)
            #print(value)
            try:
                print(annot_dict[key])
                              
                key_annot = key + "|" + str(annot_dict[key]['Annotation'])

            except:
                key_annot = key
            record = SeqRecord(Seq(value), key_annot, '', '')

            seqs.append(record)

        SeqIO.write(seqs, outfilename, "fasta")
             

         


parser = argparse.ArgumentParser(description='Returns a group of fasta files with specified number of sequences each (except for the last file which will likely be short)')

parser.add_argument('fasta_file', action="store", type=str, help="a fasta file to break up")
parser.add_argument('orthology_file', action="store", type=str, help="a orthology file with a column of  ProteinID and ID")
parser.add_argument('choice', action="store", type=str, help="random, longest, or concat")
parser.add_argument('annotation_file', action="store", type=str, help="File with ID and Annotations")
args = parser.parse_args()

diploid(args.fasta_file, args.orthology_file, args.choice)
	
