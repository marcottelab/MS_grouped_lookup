# MS_grouped_lookup

This is a folder for looking up peptides from fractionation-MS experiments using custom grouping for uniqueness

## Analysis steps


### Define grouping of peptides


1. Run eggnog-mapper to assign proteins to groups




2. Do an artificial trypsin digest on a proteome


3. Get protein-unique peptides
    ```{bash}
    $ python scripts/define_grouping.py --spec human --grouping_type protein  --peptides proteomes/human/working_proteome/uniprot-proteome_human_reviewed_peptides.csv --output_dir proteomes/human/working_proteome/
    ```


4. Get group-unique peptides

    ```
    python scripts/define_grouping.py --spec human --grouping_type euNOG --grouping eggnog_mapper/human_hmmer_euk.mapping  --peptides proteomes/human/working_proteome/uniprot-proteome_human_reviewed_peptides.csv --output_dir proteomes/human/working_proteome/
    ```


### Identify proteins in an experiment

1. Consolidate identified peptides from multiple experiments into a single file
  
   ``` 
   $ bash scripts/consolidate_MSblender_output.sh /MS/processed/Fusion_data/ExperimentA/output ExperimentA elutions/
   ```

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

    
2. Lookup peptides by protein

    for exp in ExperimentA
    do
        python scripts/get_elution_profiles.py human protein $exp elutions/${exp}_elution.csv proteomes/human/protein_unique_peptides_human.csv proteomes/contam/contam_benzo_peptides.csv
        python scripts/get_wideform_prot.py identified_elutions/human/${exp}_elution_human_protein.csv
    done

3. Lookup peptides according to a grouping of proteins

    for exp in ExperimentA
    do

        python scripts/get_elution_profiles.py human euNOG $exp elutions/${exp}_elution.csv proteomes/human/orthogroup_unique_peptides_human_euNOG.csv proteomes/contam/contam_benzo_peptides.csv
        python scripts/get_wideform_group.py identified_elutions/human/${exp}_elution_human_euNOG.csv eggnog_output/human.euNOG_orthology.tab
    done
    
    
    
    
    
    


