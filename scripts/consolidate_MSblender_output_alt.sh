


#BASEDIR=/MS/processed/Fusion_data/OP_3frog_MTbinding_102016
BASEDIR=/project/cmcwhite/frogeggs

#for exp in Hymeno Xtr Xla 
for exp in tropspindles laevisspindles
do
   #rm /project/cmcwhite/protein_complex_maps/protein_complex_maps/orthology_proteomics/elutions/${exp}_elution.csv
   echo "ExperimentID,FractionID,Peptide,PeptideCount" >  $BASEDIR/elutions/${exp}_elution.csv

   cd $BASEDIR/${exp}/msblender
   for pep in *.pep_count_mFDRpsm001
   do

       #echo "you are here"
       #pwd
       echo $exp
   
       frac=${pep%.pep_count_mFDRpsm001}
       #echo $dir
       info=`echo $exp,$frac`
       echo $info
       tail -n +3 $pep | awk -F'\t' -v OFS=',' -v info="$info" '{print info, $1, $2}'  >> $BASEDIR/elutions/${exp}_elution.csv
       #rm msblender.pep_count_mFDRpsm001.tmp 
   done
   cd ../
done

