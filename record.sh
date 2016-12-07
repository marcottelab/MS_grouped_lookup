#This needs to be changed to take into account the calculations directory

echo "Peptide lookup"
echo "euNOG"
#bash scripts/run_all.sh xentr euNOG Xtr proteomes/xentr/XENTR_JGIv90pV2_prot_final_peptides.csv proteomes/contam/contam_benzo_peptides.csv

#bash scripts/run_all.sh hymbo euNOG Hymeno proteomes/hymbo/Hym_PEP_peptides.csv proteomes/contam/contam_benzo_peptides.csv

#bash scripts/run_all.sh xenla euNOG Xla proteomes/xenla/XENLA_JGIv18pV4_prot_peptides.csv proteomes/contam/contam_benzo_peptides.csv



#bash scripts/run_all.sh xentr euNOG tropspindles proteomes/xentr/XENTR_JGIv90pV2_prot_final_peptides.csv proteomes/contam/contam_benzo_peptides.csv


#bash scripts/run_all.sh xenla euNOG laevisspindles proteomes/xenla/XENLA_JGIv18pV4_prot_peptides.csv proteomes/contam/contam_benzo_peptides.csv






echo "veNOG"
#bash scripts/run_all.sh xentr veNOG Xtr proteomes/xentr/XENTR_JGIv90pV2_prot_final_peptides.csv proteomes/contam/contam_benzo_peptides.csv

#bash scripts/run_all.sh hymbo veNOG Hymeno proteomes/hymbo/Hym_PEP_peptides.csv proteomes/contam/contam_benzo_peptides.csv

#bash scripts/run_all.sh hymbo_xentr veNOG Hymeno proteomes/hymbo_xentr/hymbo_xentr_supplemented_peptides.csv proteomes/contam/contam_benzo_peptides.csv

#bash scripts/run_all.sh xenla veNOG Xla proteomes/xenla/XENLA_JGIv18pV4_prot_peptides.csv proteomes/contam/contam_benzo_peptides.csv

#bash scripts/run_all.sh xentr veNOG tropspindles proteomes/xentr/XENTR_JGIv90pV2_prot_final_peptides.csv proteomes/contam/contam_benzo_peptides.csv


#bash scripts/run_all.sh xenla veNOG laevisspindles proteomes/xenla/XENLA_JGIv18pV4_prot_peptides.csv proteomes/contam/contam_benzo_peptides.csv

echo "combine elutions"
#bash scripts/run_concat.sh

echo "run quantification"



#python scripts/quantify_threefrog.py threefrogs_euNOG_concat.csv threefrogs_calculations
#python scripts/annotate_tables.py annotations/all_annotations.csv threefrogs_calculations threefrogs_calculations_annot GroupID , , bla ,
#python scripts/get_proteinID_onerow.py eggnog_output/xentr.euNOG_orthology.tab annotations/xentr.euNOG_annotations.txt
#python scripts/annotate_tables.py annotations/xentr.euNOG_annotations.txt threefrogs_calculations_annot threefrogs_calculations_annot_xentr GroupID ',' ',' bla ','



#python scripts/quantify_twofrog.py twofrogs_euNOG_concat.csv twofrogs_calculations
#python scripts/annotate_tables.py annotations/all_annotations.csv twofrogs_calculations twofrogs_calculations_annot GroupID , , bla ,
#python scripts/annotate_tables.py annotations/xentr.euNOG_annotations.txt twofrogs_calculations_annot twofrogs_calculations_annot_xentr GroupID ',' ',' bla ','




#python scripts/quantify_threefrog.py threefrogs_veNOG_concat.csv threefrogs_calculations_veNOG 
#python scripts/annotate_tables.py annotations/all_annotations.csv threefrogs_calculations_veNOG threefrogs_calculations_veNOG_annot GroupID , , bla ,
#python scripts/get_proteinID_onerow.py eggnog_output/xentr.veNOG_orthology.tab annotations/xentr.veNOG_annotations.txt
#python scripts/annotate_tables.py annotations/xentr.veNOG_annotations.txt threefrogs_calculations_veNOG_annot threefrogs_calculations_veNOG_annot_xentr GroupID ',' ',' bla ','


#python scripts/quantify_threefrog.py threefrog_hymxtr_veNOG_concat.csv threefrogs_calculations_hymxtr_veNOG
#python scripts/annotate_tables.py annotations/all_annotations.csv threefrogs_calculations_hymxtr_veNOG threefrogs_calculations_hymxtr_veNOG_annot GroupID , , bla ,
#python scripts/get_proteinID_onerow.py eggnog_output/xentr.veNOG_orthology.tab annotations/xentr.veNOG_annotations.txt
#python scripts/annotate_tables.py annotations/xentr.veNOG_annotations.txt threefrogs_calculations_hymxtr_veNOG_annot threefrogs_calculations_hymxtr_veNOG_annot_xentr GroupID ',' ',' bla ','



#python scripts/quantify_twofrog.py twofrogs_veNOG_concat.csv twofrogs_calculations_veNOG

#python scripts/annotate_tables.py annotations/all_annotations.csv twofrogs_calculations_veNOG twofrogs_calculations_veNOG_annot GroupID , , bla ,
#python scripts/annotate_tables.py annotations/xentr.veNOG_annotations.txt twofrogs_calculations_veNOG_annot twofrogs_calculations_veNOG_annot_xentr GroupID ',' ',' bla ','





