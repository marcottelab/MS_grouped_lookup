import argparse
import pandas as pd

def apply_length_factor(pepcount, tryptic_correction, groups = ['ExperimentID', 'ID']):
   ''' Calculating protein length correction for PPM metric from
   https://onlinelibrary.wiley.com/doi/full/10.1002/pmic.200900414'''

   #make a column of peptide lengths
   pepcount['peptidelength'] = pepcount['Peptide'].apply(len)
   
   #make a column of pepcounts * lengths
   pepcount['pepcount_length_prod'] = pepcount['PeptideCount'] * pepcount['peptidelength']
   print(groups)
   #Total for each group (either ['ID'] or ['ID', 'FractionID']
   peptotal = pepcount.groupby(groups)[['pepcount_length_prod']].sum()   
   peptotal = peptotal.rename(columns = {'pepcount_length_prod':'sum_pepcount_length_prod'})
   print(peptotal.head)
   #Add in the tryptic peptide length correction (denominator)
   tryptic_correction = tryptic_correction.set_index(['ID'])
   peptotal = peptotal.join(tryptic_correction, how = "left")

   #Calculate abundance
   peptotal['abundance'] = peptotal['sum_pepcount_length_prod'] / peptotal['corrected_tryptic_peplength'] 
   peptotal = peptotal.reset_index()
   print("groups", groups)
   #Get total abundance
   print(len(groups), groups)
   if len(groups) > 1: 
       #group by fraction ID to get fraction total
       print(groups)
       groups.remove('ID')
       print(groups)
       total_abundance = peptotal.groupby(groups)[['abundance']].sum()
       total_abundance = total_abundance.rename(columns = {'abundance':'total_abundance'})
       print(total_abundance)
       peptotal = peptotal.join(total_abundance, how = "left", on = groups)
       print(total_abundance)

   else:
      #Don't group by anything to get experiment total
      total_abundance = peptotal['abundance'].sum()
      peptotal['total_abundance'] = total_abundance

   #calculate abundance frequency in ppm
   peptotal['abundance_ppm'] = 1000000 * peptotal['abundance']/peptotal['total_abundance']

   return peptotal


def parse_args():

   parser=argparse.ArgumentParser(description = 'Takes peptide counts and applies peptide length correction factor')
   parser.add_argument('--idcorrectionfile', dest='idcorrectionfile', type=str, help = 'Two column csv filename ID,corrected_tryptic_peplength')
   parser.add_argument('--pepcountfile', dest='pepcountfile', type=str, help = 'Table of ID Peptide PeptideCount (and FractionID if needed)')
   return parser.parse_args()


def main():
     
    args=parse_args()
 

    tryptic_correction = pd.read_csv(args.idcorrectionfile)

    pepcount = pd.read_csv(args.pepcountfile) 

    pepabundance_experiment = apply_length_factor(pepcount, tryptic_correction)
    newoutexperiment =  args.pepcountfile +  "_byexperiment_PPM.csv"
    pepabundance_experiment.to_csv(newoutexperiment, index = False)

    pepabundance_fraction = apply_length_factor(pepcount, tryptic_correction, groups = ['ExperimentID', 'FractionID', 'ID'])

    newoutfraction = args.pepcountfile + "_byfraction_PPM.csv"
    pepabundance_fraction.to_csv(newoutfraction, index = False)




main()
