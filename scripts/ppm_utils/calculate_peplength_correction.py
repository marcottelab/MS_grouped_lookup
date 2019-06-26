import argparse
import pandas as pd

def calc_length_factor(peptable):
   ''' Calculating protein length correction for PPM metric from
   https://onlinelibrary.wiley.com/doi/full/10.1002/pmic.200900414'''

   peptable['peptidelength'] = peptable['Peptide'].apply(len)
    
   peptable_filt = peptable.query('peptidelength >= 7 & peptidelength <= 40')

   corrected = peptable_filt.groupby('ID')[['peptidelength']].sum()   

   return corrected


if __name__ == "__main__":

    parser=argparse.ArgumentParser(description = 'Takes a protein-peptide mapping of uniquely assigned peptides (csv) and calculates peptide length correction factor')
    parser.add_argument('--inputfile', dest='inputfile', required = True, type=str, help = 'Two columns named (ID, Peptide)')
    parser.add_argument('--outputfile', dest='outputfile', required = True,  type=str, help = 'An output file name')
    args = parser.parse_args()

    peptable = pd.read_csv(args.inputfile)
    corrected = calc_length_factor(peptable)
    corrected.to_csv(args.outputfile, header = ["corrected_tryptic_peplength"])

