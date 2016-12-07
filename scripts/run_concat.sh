BASEDIR=$( pwd )
 
echo 3 Frogs - MT, extract
python $BASEDIR/scripts/combine_elution_group.py threefrogs euNOG identified_elutions/hymbo/Hymeno_raw_wide_elution_hymbo_euNOG.csv identified_elutions/xenla/Xla_raw_wide_elution_xenla_euNOG.csv identified_elutions/xentr/Xtr_raw_wide_elution_xentr_euNOG.csv

echo 2 Frogs - spindles
python $BASEDIR/scripts/combine_elution_group.py twofrogs euNOG identified_elutions/xenla/laevisspindles_raw_wide_elution_xenla_euNOG.csv identified_elutions/xentr/tropspindles_raw_wide_elution_xentr_euNOG.csv


echo 3 Frogs - MT, extract, veNOG
python $BASEDIR/scripts/combine_elution_group.py threefrogs veNOG identified_elutions/hymbo/Hymeno_raw_wide_elution_hymbo_veNOG.csv identified_elutions/xenla/Xla_raw_wide_elution_xenla_veNOG.csv identified_elutions/xentr/Xtr_raw_wide_elution_xentr_veNOG.csv

echo 3 Frogs - MT, extract, veNOG
python $BASEDIR/scripts/combine_elution_group.py threefrogs_hymxtr veNOG identified_elutions/hymbo_xentr/Hymeno_raw_wide_elution_hymbo_xentr_veNOG.csv identified_elutions/xenla/Xla_raw_wide_elution_xenla_veNOG.csv identified_elutions/xentr/Xtr_raw_wide_elution_xentr_veNOG.csv


echo 2 Frogs - spindles, veNOG
python $BASEDIR/scripts/combine_elution_group.py twofrogs veNOG identified_elutions/xenla/laevisspindles_raw_wide_elution_xenla_veNOG.csv identified_elutions/xentr/tropspindles_raw_wide_elution_xentr_veNOG.csv

