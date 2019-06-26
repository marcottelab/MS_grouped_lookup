#!/usr/bin/python
import sys
sys.path.append('../')
sys.path.append('.')
import unittest
import scripts.proteome_utils.trypsin as tr
import scripts.lookup_utils.define_grouping as dg
import scripts.lookup_utils.get_elution_profiles as gep

from Bio import SeqIO

import numpy as np
import pandas as pd

class TestLookup(unittest.TestCase):

        def setUp(self,):
                sample_proteome_filename = "test/test_proteome.fasta"
                sample_proteome = list(SeqIO.parse(sample_proteome_filename, "fasta"))
 
                self.sample_orthology = "test/test_orthology.tab"
                self.sample_peptides = "test/test_peptides.csv"


                self.testprotein = sample_proteome[0].seq 
    
                self.contam_file = "test/contam_benzo_peptides.csv"
                self.sample_elution = "test/test_elution.csv"
                self.peptides = tr.TRYPSIN(self.testprotein, 2)
                self.peps = dg.format_peptides(self.sample_peptides)

                self.prot_uniq_peps = dg.protein_uniq_peptides(self.peps, 'output_test')
                #print("Test define grouping - grouped")
     
                self.group_uniq_peps = dg.define_grouping(self.peps, 'output_test', self.sample_orthology)

 
        def testCorrectProtein(self,):

                #print("Make sure the right test protein is being chopped")
                self.assertEqual(str(self.testprotein),"MALMMKSSASLKAVSAGRSRRAVVVRAGKYDEELIKTAGTVASKGRGILAMDESNATCGKRLDSIGVENTEENRRAYRELLVTAPGLGQYISGAILFEETLYQSTASGKKFVDVMKEQNIVPGIKVDKGLVPLSNTNGESWCMGLDGLDKRCAEYYKAGARFAKWRSVVSIPHGPSIIAARDCAYGLARYAAIAQNAGLVPIVEPEVLLDGEHDIDRCLEVQEAIWAETFKYMADNKVMFEGILLKPAMVTPGADCKNKAGPAKVAEYTLKMLRRRVPPAVPGIMFLSGGQSELESTLNLNAMNQSPNPWHVSFSYARALQNTVLKTWQGKPENVQAAQAALLKRAKANSDAQQGKYDATTEGKEAAQGMYEKGYVY")

        def testPeptideNum(self,):
                #print("Check that the right number of peptides are being made")


                #print(len(self.peptides))
                self.assertEqual(len(self.peptides), 108)

        def testShouldNotBeFoundProtein(self,):      
                #print("Should not be found in any protein")
                testrow1 = self.prot_uniq_peps[self.prot_uniq_peps.Peptide== 'AAAAAAKAJEQQKAEJESAQQQJESAR']
                #print(testrow1)
                self.assertEqual(len(testrow1),0)

        def testShouldNotBeFoundGroup(self,):      
                #print("Should not be found in any group")
                testrow1 = self.group_uniq_peps[self.group_uniq_peps.Peptide== 'AAAAAAKAJEQQKAEJESAQQQJESAR']
                #print(testrow1)
                self.assertEqual(len(testrow1),0)

        def testNonUniqueAtProteinLevel(self,):    
                #In two proteins
                #print("Should not be unique to a single protein, but will be to a group")
                testrow2 = (self.prot_uniq_peps[self.prot_uniq_peps.Peptide== 'MGJJSJJR'])
                self.assertEqual(len(testrow2),0)

        def testNonUniqueAtProteinLevelUniqueAtGroupLevel(self,):    
                #In two proteins
                #print("Should not be unique to a single protein, but will be to a group")
                testrow2 = (self.group_uniq_peps[self.group_uniq_peps.Peptide== 'MGJJSJJR'])
                #print("testrow2", testrow2)
                self.assertEqual(len(testrow2),1)

        def testUniqueAtProteinLevel(self,):
                #print("Should get one unique protein")
                testrow3 = self.prot_uniq_peps[self.prot_uniq_peps.Peptide== 'MAJMMKSSASJKAVSAGR']
                #print("testrow3", testrow3)
                self.assertEqual(len(testrow3),1)

        def testUniqueAtProteinAndGroupLevel(self,):
                #print("Should get one unique protein")
                testrow3 = self.group_uniq_peps[self.group_uniq_peps.Peptide== 'MAJMMKSSASJKAVSAGR']
                #print("testrow3", testrow3)
                self.assertEqual(len(testrow3),1)
                #self.assertEqual(testrow3['ProteinID'].values[0], 'sp|Q42690|ALFC_CHLRE') 

 
        #def testElution(self,):

        #        gep.create_tables('test', 'euNOG', 'testing', self.sample_elution, self.sample_peptides, self.contam_file)




if __name__ == "__main__":
	#unittest.main()
        suite = unittest.TestLoader().loadTestsFromTestCase(TestLookup)
        unittest.TextTestRunner(verbosity=2).run(suite)

