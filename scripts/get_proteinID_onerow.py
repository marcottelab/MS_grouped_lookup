from __future__ import print_function
import pandas as pd
import argparse

def combine_rows(eggnog):


   #Consolidate proteins from a group into one row
   egg = pd.DataFrame(pd.read_csv(eggnog, sep="\t"))
   all_prots = egg.groupby(['GroupID'])['ProteinID'].apply(lambda x: ' '.join(x)).reset_index()
   all_prots.columns= ['GroupID', 'AllMembers']
   return all_prots

def main():

    parser = argparse.ArgumentParser(description='Get Protein IDs on one row for groups')

    parser.add_argument('eggnog', action="store", type=str)
    parser.add_argument('outfile', action="store", type=str)
    inputs = parser.parse_args()


    final = combine_rows(inputs.eggnog)

    final.to_csv(inputs.outfile, index=False)


main()






