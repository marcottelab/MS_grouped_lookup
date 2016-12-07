for f in proteomes/?????/*.fasta
do

   echo $f   
   python scripts/trypsin.py --input $f --output ${f%.*}_peptides.csv --miss 2

done

