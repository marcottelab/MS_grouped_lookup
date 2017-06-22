from __future__ import print_function
import pandas as pd
import argparse


def consolidate_rows(mapping_file, grouping_col, to_consolidate_col, outfile, sep, consolidate_sep):

   '''
   Go from:
   A 1
   A 2
   B 3

   to 
  
   A 1,2
   B 3
   '''
   
   map_df=pd.read_csv(mapping_file, index_col=False, sep=sep)


   print(map_df)   

   #list comprehensing makes sure each element in vector is a string   
   final = map_df.groupby([grouping_col])[to_consolidate_col].apply(lambda x: consolidate_sep.join(str(y) for y in x)).reset_index()

   final.to_csv(outfile, sep=sep, index=False)


parser = argparse.ArgumentParser(description='Take a mapping and consolidate multiple entries into one row')
parser.add_argument('--mapping', '-m', dest='mapping_file', action="store", required=True,  type=str, help="a two column tsv")
parser.add_argument('--sep', '-s', dest='sep', action="store", required=False, type=str, help="Column separator", default=' ')
parser.add_argument('--grouping_col', '-g', dest='grouping_col', action="store", required=True, type=str, help="The column to group by")
parser.add_argument('--consolidate_col', '-c', dest='to_consolidate_col', action="store", required=True, type=str, help="the column to consolidate")
parser.add_argument('--consolidate_sep', '-csep', dest='consolidate_sep', action="store", required=False, default=',', type=str, help="what to separate the value in the column by")
parser.add_argument('--outfile', '-o', dest='outfile', action="store", required=True, type=str)
inputs = parser.parse_args()
consolidate_rows(inputs.mapping_file, inputs.grouping_col, inputs.to_consolidate_col, inputs.outfile, inputs.sep, inputs.consolidate_sep)






    
