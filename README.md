# MS_grouped_lookup

This is a folder for looking up peptides from fractionation-MS experiments using custom grouping for uniqueness


One part of a larger scheme that goes:

1. Convert .RAW thermo files in /MS/submit to mzXML in /MS/processed using local Windows MSConvert
2. Run MSblender on TACC (ls5) $scratch using the https://github.com/marcottelab/run_msblender setup (using branch https://github.com/marcottelab/MSblender/tree/msblender_restructure)
      - Download output ot /MS/processed
3. Format proteome for peptide lookup
4. Lookup peptides

## Analysis steps

### Define grouping of peptides


**1. Run eggnog-mapper to assign proteins to groups and format output**


    Running hmmer straight on a full protein will take several days to process

    $ nohup python /project/eggnog-mapper-0.99.2/emapper.py -i /project/cmcwhite/orthology_proteomics/proteomes/human/uniprot-reviewed%3Ayes+AND+proteome%3Aup000005640.fasta --output human_hmmer_euNOG -d euNOG --override --scratch_dir /project/cmcwhite/orthology_proteomics/proteomes/human/ -m hmmer --output_dir /project/cmcwhite/orthology_proteomics/eggnog_mapper  &> /project/cmcwhite/orthology_proteomics/logs/nohup_human_euNOG.txt &


    Alternatively, break up the proteome into chunks and process in parallel using proteome_breaker.py
    
    The output from the eggnog mapper need to be formatted 
    $ format_emapper_output.R -f human_hmmer_euNOG.emapper.annotations -o human_hmmer_euNOG.mapping -s hmmer -l euNOG

    creates file with format:
    ProteinID	ID



**2. Do an artificial trypsin digest on a proteome**


   $ python scripts/trypsin.py --input proteomes/human/uniprot-proteome%3AUP000005640.fasta  --output  proteomes/human/uniprot-proteome%3AUP000005640_peptides.csv --miss 2




**4. Get group-unique peptides**
    Identify groups of proteins from peptides that are unique to the proteins in a group
    
    $ python scripts/define_grouping.py --spec human --grouping_type euNOG --grouping eggnog_mapper/human_hmmer_euk.mapping  --peptides proteomes/human/working_proteome/uniprot-proteome_human_reviewed_peptides.csv --output_dir proteomes/human/working_proteome/
   


#### Identify proteins in an experiment

**1. Consolidate identified peptides from multiple experiments into a single file**
  
    
   $ bash scripts/consolidate_MSblender_output.sh /MS/processed/Fusion_data/ExperimentA/output ExperimentA elutions/
   

   /MS/processed/Fusion_data/ExperimentA/output

      fraction1_pep_count_FDR001
         ACDER 1
         ETIAJR 2

      fraction2_pep_count_FDR001
         GFEAR 1
         AYTQWER 3

   --->

   ExperimentA_elution.csv
        ExperimentA,fraction1,ACDER,1
        ExperimentA,fraction1,ETIAJR,2
        ExperimentA,fraction2,GFEAR,1
        ExperimentA,fraction2,AYTQWER,3
 

   These formatted files are stored in the elutions/ folder




#Don't do by proteins. Use weighted peptide output instead   
**2. Lookup peptides by protein**


   Do the look up
   $ python scripts/get_elution_profiles.py human protein ExperimentA elutions/ExperimentA_elution.csv proteomes/human/working_proteome/unique_peptides_human_protein.csv proteomes/contam/contam_benzo_peptides.csv

          


   $ python scripts/get_wideform_prot.py identified_elutions/human/ExperimentA_elution_human_protein.csv

   Transform columns to a wide table.
   ex. 
       "tidy elution format"
       ExperimentA,fraction1,protein1,10
       ExperimentA,fraction2,protein1,30
       ExperimentA,fraction1,protein2,3
       ExperimentA,fraction2,protein2,2
       
       --> 
       "wide elution format"

       ID,fraction1,fraction1
       protein1,10,30
       protein2,3,2
 





**3. Lookup peptides according to a grouping of proteins**

**3. Get protein-unique peptides**
    Identify proteins from peptides that are unique to single proteins
    
    $ python scripts/define_grouping.py --spec human --grouping_type protein  --peptides proteomes/human/working_proteome/uniprot-proteome_human_reviewed_peptides.csv --output_dir proteomes/human/working_proteome/

   $ python scripts/get_elution_profiles.py human euNOG ExperimentA elutions/ExperimentA_elution.csv proteomes/human/working_proteome/unique_peptides_human_euNOG.csv proteomes/contam/contam_benzo_peptides.csv


   $ python scripts/get_wideform_group.py identified_elutions/human/ExperimentA_elution_human_euNOG.csv eggnog_mapper/human_hmmer_euNOG.mapping annotation_files/all_annotations.csv

   *Going to be removed, not very useful extra format*
   Similar to get_wideform_prot.py, but also creates an alternate format that shows the proteins in a group 
    
   ID,proteinIDs,fraction1,fraction2
  

    


