from __future__ import print_function
import pandas as pd
import sys
import argparse

def format_peptides(peptides_file, species, output_dir = ''):
    '''
    Read in a ProteinID Peptide mapping file, and format
    '''   
    peps = pd.DataFrame(pd.read_csv(peptides_file)) 
    print("Peptide file loaded")

    #Replace mass undistinguishable isoleucine/leucine with J
    peps['Peptide'] = peps['Peptide'].str.replace('I', 'J')
    peps['Peptide'] = peps['Peptide'].str.replace('L', 'J')
    peps_filename = output_dir + 'Jreplaced_' + species + '_peptides.csv'
    peps.to_csv(peps_filename, index=False)
    peps = peps.set_index(['ProteinID'])
     
    return peps


def protein_uniq_peptides(peps, species, output_dir=''):
    
    print("Get protein unique peptides")   
    peps = peps.reset_index()
    #Need to reset the index before doing this
    uniq_pep = peps.drop_duplicates()
    print(uniq_pep[uniq_pep.Peptide== 'AAAAAAKAJEQQKAEJESAQQQJESAR'])
    #this seems like it's only dropping the second duplicate not both. 
    final_pep = uniq_pep.drop_duplicates(subset=['Peptide'], keep=False) #current Docs/version have subset
    #final_pep = uniq_pep.groupby(["Peptide"]).filter(lambda df:df.shape[0] == 1)
    print(final_pep[final_pep.Peptide== 'AAAAAAKAJEQQKAEJESAQQQJESAR'])
    msg = species + "\t" + "unique_peptides" + "\t" + str(final_pep.shape[0])
    print(msg)
    #formerly identifying_orthogroup
    ident_group = output_dir + "protein_unique_peptides_" + species + ".csv"
    final_pep=final_pep.reset_index()
    final_pep.to_csv(ident_group, index=False)
    #final_pep = final_pep.set_index(['Peptide'])

    return final_pep


   
def define_grouping(peps, species, level, output_dir='', grouping_file=None):   
    '''
    Take a file that tells how to group proteins. 
    Each row should contain one group ID and one protein ID

    '''
    print("define grouping")
    if grouping_file:
        print("grouping file provided")
        prot = pd.DataFrame(pd.read_csv(grouping_file, sep="\t", index_col=False))
        #print(prot)
    
        #Grouping file need columns 'ProteinID' and 'ID'
        prot = prot.set_index(['ProteinID']) 
        
        #Join the grouped proteins to their list of peptides
        #Change to outer
        group_pep = prot.join(peps, how = "outer")
    
        #This will be the same for every experiment
        group_pep = group_pep.reset_index()

        group_pep['ID'] = group_pep['ID'].fillna(group_pep['ProteinID'])
    
        #Mapping of groups to peptides with proteins. No uniqueness criteria
        group_prot_pep_filename = output_dir + "group_prot_pep_" + species + "_" + level + ".csv"
    
        group_pep_cols = ['ID', 'ProteinID', 'Peptide']

        
        group_pep = group_pep[group_pep_cols]
    
        group_pep = group_pep.sort(['ID'])
     
        group_pep.to_csv(group_prot_pep_filename, index=False)
        

        

        #These are the only columns we need for the next step
        #print(group_pep)
        group_pep = group_pep[['ID', 'Peptide']]
    else:
        group_pep = peps
        group_pep = group_pep.reset_index()
      
    #Get unique Rows, as one peptide can occur multiple times in one group
    print("get unique rows so no duplicate peptides in a group")
    uniq_group_pep = group_pep.drop_duplicates()

    #Get Peptides which only occur in one group
    #final_group_pep = uniq_group_pep.drop_duplicates(subset=['Peptide'], keep=False) #current Docs/version have subset

    print("groupby peptide")
    final_group_pep = uniq_group_pep.groupby(["Peptide"]).filter(lambda df:df.shape[0] == 1)
    #final_group_pep = final_group_pep.reset_index()


    msg = species + "\t"  + "\t" + level + "\t" + "unique_peptides" + "\t" + str(final_group_pep.shape[0])
    print(msg)

    ident_group = output_dir + "unique_peptides_" + species + "_" + level + ".csv"

    #final_group_pep = final_group_pep.reset_index()
    final_group_pep.to_csv(ident_group, index=False)
        

    #final_group_pep = final_group_pep.set_index(['Peptide'])

    return final_group_pep
     
if __name__ == "__main__":
    
           
    parser = argparse.ArgumentParser(description='Interpret mass spec experiments using orthologous groups of proteins to make identifications')
    parser.add_argument('--spec', dest='species_code', action="store", type=str, help="species code, ex. human")
    parser.add_argument('--grouping_type', dest='phylogenetic_level', action="store", type=str, required=False, default='', help="Identifier for the type of grouping")
    parser.add_argument('--peptides' ,dest='peptides_file', action="store", type=str, help="artificially digested proteome with ProteinID Peptide columns")
    parser.add_argument('--output_dir' , action="store", type=str, required=False, default="peptide_assignments/")
    parser.add_argument('--log_dir' , action="store", type=str, required=False, default="logs/")
    parser.add_argument('--grouping', dest='grouping_file', action="store", required=False, type=str, help="tab separated with ID ProteinID columns")
   
    inputs = parser.parse_args()
    
    print(inputs.species_code)
    print(inputs.phylogenetic_level)
    print("GROUPING", inputs.grouping_file)
    print("OUTPUTLOC", inputs.output_dir)
    
    
    #setup_logger(inputs.species_code, inputs.phylogenetic_level, inputs.log_dir)
    
    peps  = format_peptides(inputs.peptides_file, inputs.species_code, inputs.output_dir)
    #returns peps, contam_list, frac
    
    final_grouped_peps = define_grouping(peps, inputs.species_code, inputs.phylogenetic_level, inputs.output_dir, inputs.grouping_file)  
   
    
    print(final_grouped_peps)
    
    
    
    
    
        
