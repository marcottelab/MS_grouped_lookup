from __future__ import print_function
import pandas as pd
import sys
import argparse

def format_peptides(peptides_file):
    '''
    Read in a ProteinID Peptide mapping file, and format
    '''   
    peps = pd.DataFrame(pd.read_csv(peptides_file)) 
    #print("Peptide file loaded")
    peps = peps[['ProteinID', 'Peptide']]
    #Replace mass undistinguishable isoleucine/leucine with J
    peps['Peptide'] = peps['Peptide'].str.replace('I', 'J')
    peps['Peptide'] = peps['Peptide'].str.replace('L', 'J')
    peps = peps.drop_duplicates()
    peps = peps.set_index(['ProteinID'])
     
    return peps

# Is this ever called?
def protein_uniq_peptides(peps, output_basename):
    
    #print("Get group unique peptides")   
    peps = peps.reset_index()

    #Need to reset the index before doing this
    uniq_pep = peps.drop_duplicates()
    #this seems like it's only dropping the second duplicate not both. 
    final_pep = uniq_pep.drop_duplicates(subset=['Peptide'], keep=False) #current Docs/version have subset
    #final_pep = uniq_pep.groupby(["Peptide"]).filter(lambda df:df.shape[0] == 1)
    ident_group = output_dir + "protein_unique_peptides.csv"
    final_pep=final_pep.reset_index()
    final_pep.to_csv(ident_group, index=False)
    #final_pep = final_pep.set_index(['Peptide'])

    return final_pep


   
def define_grouping(peps, output_basename, level = 'group', grouping_file=None):   
    '''
    Take a file that tells how to group proteins. 
    Each row should contain one group ID and one protein ID

    '''
    #print("define grouping")
    if grouping_file:

        #print("grouping file provided")
        grouping = pd.DataFrame(pd.read_csv(grouping_file, sep="\t", index_col=False))
        #print(prot)
    
        #Grouping file need columns 'ProteinID' and 'ID'
        grouping = grouping.set_index(['ProteinID']) 
        
        #Join the proteins to their list of peptides
        group_pep = grouping.join(peps, how = "outer")
    
        group_pep = group_pep.reset_index()
  
        #This accounts for if the protein doesn't have an entry in the mapping
        #Then the groupID becomes the proteinID
        group_pep['ID'] = group_pep['ID'].fillna(group_pep['ProteinID'])
       
        group_pep_cols = ['ID', 'ProteinID', 'Peptide']
        
        group_pep = group_pep[group_pep_cols]
    
        group_pep = group_pep.sort_values(['ID']).drop_duplicates()

        #Mapping of groups to peptides with proteins. No uniqueness criteria
        group_prot_pep_filename = output_basename + "_" + level + "_protein_peps.csv"     
        group_pep.to_csv(group_prot_pep_filename, index=False)
        

        
        #These are the only columns we need for the next step
        #print(group_pep)
        group_pep = group_pep[['ID', 'Peptide']]

    else:
        group_pep = peps
        group_pep = group_pep.reset_index()
      
    #Get unique Rows, as one peptide can occur multiple times in one group
    #print("get unique rows so no duplicate peptides in a group")
    uniq_group_pep = group_pep.drop_duplicates()

    #Get Peptides which only occur in one group
    #print("groupby peptide")
    final_group_pep = uniq_group_pep.groupby(["Peptide"]).filter(lambda df:df.shape[0] == 1)
    #final_group_pep = final_group_pep.reset_index()

    if grouping_file:
       ident_group = output_basename + "_" + level + "_unique_peptides.csv"
    else:
       ident_group = output_basename + "_protein_unique_peptides.csv"
    final_group_pep.to_csv(ident_group, index=False)

        
    return final_group_pep
     
if __name__ == "__main__":
    
           
    parser = argparse.ArgumentParser(description='Interpret mass spec experiments using orthologous groups of proteins to make identifications')
    parser.add_argument('--peptides' ,dest='peptides_file', action="store", required = True,  type=str, help="artificially digested proteome with ProteinID Peptide columns")
    parser.add_argument('--output_basename', action="store", type = str, required = True, help = 'Start of output filenames')
    parser.add_argument('--grouping', dest='grouping_file', action="store", required=False, type=str, help="tab separated with ID ProteinID columns")
    parser.add_argument('--level', dest='level', action="store", required=False, type=str, help="Identifier to tie output filename to type of goroups, ex. virNOG")
  
    inputs = parser.parse_args()
    
    #Output of trypsin.py
    #Just J replaces I and L 
    peps  = format_peptides(inputs.peptides_file)
    #returns peps, contam_list, frac
    
    final_grouped_peps = define_grouping(peps, inputs.output_basename, inputs.level, inputs.grouping_file)  
   
    
    #print(final_grouped_peps)
    
    
    
    
    
        
