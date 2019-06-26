from __future__ import print_function
import pandas as pd
import sys
import argparse
import logging

def load_peptide_key(peptide_file):

    peptide_lookup = pd.DataFrame(pd.read_csv(peptide_file)) 
    peptide_lookup.columns = ['ID', 'Peptide']

    #Remove undistinguishable isoleucine/leucine with J 
    peptide_lookup['Peptide'] = peptide_lookup['Peptide'].str.replace('I', 'J')
    peptide_lookup['Peptide'] = peptide_lookup['Peptide'].str.replace('L', 'J')
    peptide_lookup = peptide_lookup.drop_duplicates()

    return(peptide_lookup)

def load_elution(elution_file):
 
    #The elution profile from msblender consolidate
    elution_peptides = pd.DataFrame(pd.read_csv(elution_file))

    #Replace undistinguishable isoleucine/leucine with J
    elution_peptides['Peptide'] = elution_peptides['Peptide'].str.replace('I', 'J')
    elution_peptides['Peptide'] = elution_peptides['Peptide'].str.replace('L', 'J')
    elution_peptides['Peptide'] = elution_peptides['Peptide'].str.replace('*', '')

    #Consolidate I and L peptides into one row
    elution_peptides = elution_peptides.groupby(['Peptide', 'ExperimentID', 'FractionID']).sum()     
    elution_peptides = elution_peptides.reset_index()
    return(elution_peptides)

def load_contaminants(contam_file):
    #Contaminants
    contam = pd.DataFrame(pd.read_csv(contam_file))
    contam['Peptide'] = contam['Peptide'].str.replace('I', 'J')
    contam['Peptide'] = contam['Peptide'].str.replace('L', 'J')
    contam_list = contam['Peptide'].tolist()
    return(contam_list)

def remove_contaminants(elution_peptides, contam_list): 

    elution_peptides = elution_peptides[~elution_peptides.isin(contam_list)]
    #print("find pep")

    elution_peptides = elution_peptides.dropna(axis=0, how = 'any')
    return(elution_peptides)
 
def create_tables(elution_peptides, peptide_lookup, output_basename):
    '''
    Match identified peptides. Creates a table of peptide and protein counts
    '''

    elution_peptides = elution_peptides.set_index(['Peptide'])
    peptide_lookup = peptide_lookup.set_index(['Peptide'])
     
    #Join peptides in experiment to peptide lookup
    elution_peptides_labeled = elution_peptides.join(peptide_lookup, how='inner')      
    elution_peptides_labeled = elution_peptides_labeled.reset_index()

    #This is for the peptide splitting project
    elut_pep_filename =  output_basename  +"_peps.tidy"
    peptide_protein_fraction = elution_peptides_labeled.to_csv(elut_pep_filename, index=False)

    elution_peptides_labeled = elution_peptides_labeled[['ExperimentID', 'FractionID', 'ID', 'PeptideCount']]
    
    #Add up peptides for each group to get protein totals
    elution_peptides_labeled = elution_peptides_labeled.groupby(by=['ExperimentID', 'FractionID', 'ID'])['PeptideCount'].sum()
    
    final_elution =  elution_peptides_labeled.reset_index(name='Total_PeptideCount')
   
    elut_group = output_basename +"_elut.tidy"
    final_elution.to_csv(elut_group, index=False) 
    
if __name__ == "__main__":
        
        
    parser = argparse.ArgumentParser(description='Interpret mass spec experiments using orthologous groups of proteins to make identifications')
    parser.add_argument('--elution_file', action="store", type=str, required = True, help= 'consolideMSBlender output')
    parser.add_argument('--peptides_file', action="store", type=str, required = True, help= 'csv, two columns, ID, Peptide')
    parser.add_argument('--output_basename', action="store", type = str, required = True,  help = 'Start of output filenames')
    parser.add_argument('--contam_file', action="store", type=str, required = False, help= 'csv, two columns containing peptides to be removed')
    
    args = parser.parse_args()

    peptide_lookup = load_peptide_key(args.peptides_file) 
    elution_peptides = load_elution(args.elution_file)

    if args.contam_file:
        contam_list = load_contaminants(args.contam_file)
        elution_peptides = remove_contaminants(elution_peptides, contam_list)
    

    create_tables(elution_peptides, peptide_lookup, args.output_basename)

    
   
    
    
    
    
        
