import argparse
import pandas as pd

def calc_length_factor(peptable):
   ''' Calculating protein length correction for PPM metric from
   https://onlinelibrary.wiley.com/doi/full/10.1002/pmic.200900414'''

   peptable['peptidelength'] = peptable['Peptide'].apply(len)
    
   peptable_filt = peptable.query('peptidelength >= 7 & peptidelength <= 40')

   corrected = peptable_filt.groupby('ID')[['peptidelength']].sum()   

   print(corrected)
   return corrected


def parse_args():

   parser=argparse.ArgumentParser(description = 'Takes a protein-peptide mapping (csv) and calculates peptide length correction factor')
   parser.add_argument('inputfile', metavar='inputfile', type=str, help = 'Two column ID pepsequences')
   parser.add_argument('outputfile', metavar='outputfile', type=str, help = 'An output file name')
   return parser.parse_args()


def main():
     
    args=parse_args()
 
    peptable = pd.read_csv(args.inputfile)

    corrected = calc_length_factor(peptable)

    corrected.to_csv(args.outputfile, header = ["corrected_tryptic_peplength"])

main()
