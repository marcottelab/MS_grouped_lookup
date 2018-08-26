import pandas as pd
import sys
import argparse
import logging

def make_wide(identified_elution):


   #output from get_elution_ids.py
   elut=pd.read_csv(identified_elution, index_col=False)
   
   elut= elut[['FractionID', 'ID', 'Total_SpecCounts']]

   #changing from long to wide format for elution profiles
   wide = elut.pivot(index='ID', columns = 'FractionID', values='Total_SpecCounts')  
   #print wide

   wide = wide.fillna(0)


def make_annotated_wide(wide, grouping_file):


   #Pull annotations from orthology file (eggnog_output)

   groups = pd.read_csv(grouping_file, sep="\t")

   #Consolidate proteins from a group into one row
   alt_wide_labels = groups.groupby(['ID'])['ProteinID'].apply(lambda x: ' '.join(x)).reset_index()


   alt_wide_labels = alt_wide_labels.set_index(["ID"])
   alt_wide = annot_wide.join(alt_wide_labels, how = "inner")
   return(annot_wide) 


def make_protein_annotated_wide(wide, grouping_file):
   annot = pd.read_csv(annotation_file, sep=",")
   annot = annot[['ID', 'Annotation']]

   annot = annot.set_index(['ID'])
   annot_wide = wide.join(annot, how="left")
   return(annot_wide)

    
parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('identified_elution', action="store", type=str)
parser.add_argument('output_basename', action="store", type=str)
parser.add_argument('grouping_file', action="store", type=str, required=False, "csv two columns called ID,ProteinID))"
parser.add_argument('annotation_file', action="store", type=str, required = False, help = "csv two columns called ID,Annotation)")
args = parser.parse_args()

   wide = make_wide(args.identified_elution)
   raw_outfile = args.basename + "_plain_wide.csv")
   wide.to_csv(raw_outfile)

   #Need to get this set up for future users
   if args.grouping_file:
     wide = make_annotated_wide(wide, args.grouping_file)

   if args.annotation_file:
     wide = make_annotated_wide(wide, args.annotation_file)

   if args.grouping_file or args.annotation_file
      annot_outfile = args.basename + "_annot_wide.csv")
      wide.to_csv(annot_outfile)






    
