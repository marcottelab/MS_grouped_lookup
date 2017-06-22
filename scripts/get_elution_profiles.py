from __future__ import print_function
import pandas as pd
import sys
import argparse
import logging

def  setup_logger(species, level, log_dir):


    LOG_FILENAME = log_dir + species + "_" + level + '.log'
    print("LOGFILENAME", LOG_FILENAME)
    #print("SPECIES", species)
    #print("LEVE:", level)

    logger = logging.getLogger()
    filehandler = logging.FileHandler(LOG_FILENAME, mode="w")
    formatter = logging.Formatter('%(message)s')
    filehandler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(filehandler)


    logger.setLevel(logging.INFO)

def create_tables(species, level, experiment, elution_file, peptide_file, contam_file):
    '''
    Break this  into multiple functions
    Break into 
    '''
    LOG_FILENAME = species + "_" + level + '.log'
    logger =  logging.getLogger(LOG_FILENAME)


    peptide_lookup = pd.DataFrame(pd.read_csv(peptide_file)) 
    print("Peptide file loaded")
    msg = species + "\t"  + "\t" + level + "\t" + "unique_peptides" + "\t" + str(peptide_lookup.shape[0])
    logger.info(msg)

    #Remove undistinguishable isoleucine/leucine with 
    peptide_lookup.columns = ['ID', 'Peptide']
    peptide_lookup = peptide_lookup.set_index(['Peptide'])
    #print(peptide_lookup.head)


    #Contaminants
    contam = pd.DataFrame(pd.read_csv(contam_file))
    contam['Peptide'] = contam['Peptide'].str.replace('I', 'J')
    contam['Peptide'] = contam['Peptide'].str.replace('L', 'J')
    contam_list = contam['Peptide'].tolist()
  
    
    #The elution profile from msblender consolidate
    elution_peptides = pd.DataFrame(pd.read_csv(elution_file))
    #Remove undistinguishable isoleucine/leucine
    elution_peptides['Peptide'] = elution_peptides['Peptide'].str.replace('I', 'J')
    elution_peptides['Peptide'] = elution_peptides['Peptide'].str.replace('L', 'J')
    elution_peptides['Peptide'] = elution_peptides['Peptide'].str.replace('*', '')
    contam=contam.set_index(['Peptide'])
    #Get rid of peptides that occur in the contaminants list
   
    print("pre removing contaminants", elution_peptides.shape)

    elution_peptides = elution_peptides[~elution_peptides.isin(contam_list)]
    print("find pep")

    elution_peptides = elution_peptides.dropna(axis=0, how = 'any')
    print("post removing contamints", elution_peptides.shape)
 
    elution_peptides = elution_peptides.set_index(['Peptide'])

     
    #Join peptides in experiment to peptide lookup
    elution_peptides_labeled = elution_peptides.join(peptide_lookup, how='inner')
    print(elution_peptides_labeled.head)
    msg = species + "\t" + experiment + "\t" + level + "\t" + "identified_peptides" + "\t" + str(elution_peptides_labeled.shape[0])
    logger.info(msg)

      
    elution_peptides_labeled = elution_peptides_labeled.reset_index()
    identified_peptides = elution_peptides_labeled[['Peptide']].drop_duplicates()

    #formerly identifiedpeps
    identified_filename = "proteomes/" + species + "/identified_peptides" + "_" + experiment + "_" + species + "_" + level + ".csv"
    identified_peptides.to_csv(identified_filename)

    #This is for the peptide splitting project
    elut_pep = "identified_elutions/" + species + "/" + experiment +"_peptide_elution_" + species + "_" + level + ".csv"
    peptide_protein_fraction = elution_peptides_labeled.to_csv(elut_pep, index=False)

    
    #print(elution_peptides_labeled.head) 
    elution_peptides_labeled = elution_peptides_labeled[['ExperimentID', 'FractionID', 'ID', 'PeptideCount']]
    
    #Add up peptides for each group
    elution_peptides_labeled = elution_peptides_labeled.groupby(by=['ExperimentID', 'FractionID', 'ID'])['PeptideCount'].sum()
    
    final_elution =  elution_peptides_labeled.reset_index(name='Total_SpecCounts')
   
    msg = species + "\t" + experiment + "\t" + level + "\t" +"spectral_counts" + "\t" + str(final_elution['Total_SpecCounts'].sum())
    logger.info(msg)



    elut_group = "identified_elutions/" + species + "/" + experiment +"_elution_" + species + "_" + level + ".csv"
    final_elution.to_csv(elut_group, index=False) 
    
if __name__ == "__main__":
        
        
    parser = argparse.ArgumentParser(description='Interpret mass spec experiments using orthologous groups of proteins to make identifications')
    parser.add_argument('species_code', action="store", type=str, help= 'for logging, filenaming')
    parser.add_argument('phylogenetic_level', action="store", type=str, help= 'for logging, filenaming')
    parser.add_argument('experimentID', action="store", type=str, help= 'for logging, filenaming')
    parser.add_argument('elution_file', action="store", type=str, help= 'consolideMSBlender output')
    parser.add_argument('peptides_file', action="store", type=str, help= 'csv, two columns, ID, Peptide')
    parser.add_argument('contam_file', action="store", type=str, help= 'csv, two columns')
    parser.add_argument('--log_dir' , action="store", type=str, required=False, default="logs/")
    
    inputs = parser.parse_args()
    
    print(inputs.species_code)
    print(inputs.phylogenetic_level)
    print("experiment", inputs.experimentID)
    print(inputs.peptides_file)
    setup_logger(inputs.species_code, inputs.phylogenetic_level, inputs.log_dir)
    
    create_tables(inputs.species_code, inputs.phylogenetic_level, inputs.experimentID,inputs.elution_file, inputs.peptides_file, inputs.contam_file)
    
    
    
    
    
    
        
