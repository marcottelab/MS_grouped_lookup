
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import argparse
import pickle
import pandas as pd
import itertools as it

from collections import Counter #for averaging dictionary values
import pandas as pd #for averaging dictionary values

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve
from sklearn.metrics import average_precision_score


from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
#rcParams.update({'grid': False}) # KeyError: u'grid is not a valid rc parameter.See rcParams.keys() for a list of valid parameters.'
mpl.rc('pdf', fonttype=42)
import seaborn as sns
sns.set_style("white")

def main():

    parser = argparse.ArgumentParser(description="Generate Precision Recall Curve")
    parser.add_argument("--results_wprob", action="store", dest="results_wprob", nargs='+', required=True, 
                                    help="Filename of pair results with probability")
    parser.add_argument("--input_positives", action="store", dest="positives", nargs='+', required=True, 
                                    help="Filename of positive pairs")
    parser.add_argument("--input_negatives", action="store", dest="negatives", nargs='+',
                                    help="Filename of negative pairs, default = None (generated from processing positives)")
    parser.add_argument("--output_file", action="store", dest="output_file", required=True, 
                                    help="Filename of output file")
    parser.add_argument("--labels", action="store", dest="labels", nargs='+', required=False, default=None,
                                    help="Labels for input results in order of sets of pairs")
    parser.add_argument("--threshold", action="store", type=float, dest="threshold", required=False, 
                                    help="Only tally predictions above probability threshold")
    parser.add_argument("--plot_thresholds", action="store_true", dest="plot_thresholds", required=False, default=False,
                                    help="Add probability threshold markers to plot")
    parser.add_argument("--average_probs", action="store_true", dest="avg_probs", required=False, default=False,
                                    help="Average a set of result_wprob instead of plotting individually")

    parser.add_argument("--header", action="store_true", dest="header", required=False, default=False,
                                    help="Set true in results_wprob has a header")

    args = parser.parse_args()

    output_pr_table = pd.DataFrame()
    output_roc_table = pd.DataFrame()


    results_dict_list = []
    for filename in args.results_wprob:
        print(filename)
        results_dict = dict()
        results_file = open(filename,"rb")
        for line in results_file.readlines():
            try: 
                if len(line.split()) == 3:
                    id1 = line.split()[0]
                    id2 = line.split()[1]
                    ppi_str = str(sorted(list(frozenset([id1,id2]))))
                    results_dict[ppi_str] = float(line.split()[2])
            except:
                print "WARNING: did not read line: %s" % (line,)

        print "results size: %s" % (len(results_dict))
        results_dict_list.append(results_dict)

    if args.avg_probs:
        df = pd.DataFrame(results_dict_list)
        print(df)
        results_dict = dict(df.mean())
        print(results_dict)
        results_dict_list = []
        results_dict_list.append(results_dict)
         
    #assert len(args.positives) == len(args.labels)

   
    for evalset in range(0, len(args.positives)):
        all_proteins = set()
        ppis = set()
        positive_file = open(args.positives[evalset],"rb")
        print(args.positives[evalset])
        for line in positive_file.readlines():
                if len(line.split()) >= 2:
                    id1 = line.split()[0]
                    id2 = line.split()[1]
                    all_proteins.add(id1)
                    all_proteins.add(id2)
        
                    ppi_str = str(sorted(list(frozenset([id1,id2]))))
                    ppis.add(ppi_str)
 

        for evalset2 in range(0,len(args.negatives)):

            negative_file = open(args.negatives[evalset2],"rb")
            neg_ppis = set()

            for line in negative_file.readlines():
                    if len(line.split()) >= 2:
                        id1 = line.split()[0]
                        id2 = line.split()[1]
                        ppi_str = str(sorted(list(frozenset([id1,id2]))))
                        neg_ppis.add(ppi_str)
 

  
       
        
            print(args.negatives[evalset2])        
            for i, results_dict in enumerate(results_dict_list):
                print(i)
                try:
                    true_array = []
                    prob_array = []
                    neg_list = []
                    pos_list = []
                    for result_pair in results_dict.keys():
                        if args.threshold == None or args.threshold <= results_dict[result_pair]:
                            if result_pair in ppis:
                                true_array.append(1)
                                prob_array.append(results_dict[result_pair])
                                pos_list.append((result_pair, results_dict[result_pair]))
                            elif result_pair in neg_ppis:
                                true_array.append(-1)
                                prob_array.append(results_dict[result_pair])
                                neg_list.append((result_pair, results_dict[result_pair]))
            
            
                    sorted_neg_list = sorted(neg_list, key=lambda k: k[1])
                    sorted_pos_list = sorted(pos_list, key=lambda k: k[1])

                    #print "FoundNegs: %s" % (len([i for i in true_array if i == -1]))
                    #print "FoundPos: %s" % (len([i for i in true_array if i == 1]))


                    print "#ofNegs: %s" % (len(sorted_neg_list))
                    print "#ofPos: %s" % (len(sorted_pos_list))
                    print "FDR: %s" % (1.0*len(sorted_neg_list)/(len(sorted_pos_list)+len(sorted_neg_list)))
            
                    print "#ofNegs: %s, #ofPos: %s, FDR: %s" % (len(sorted_neg_list),len(sorted_pos_list),1.0*len(sorted_neg_list)/(len(sorted_pos_list)+len(sorted_neg_list)))
                    #for k in sorted_neg_list[-100:]:
                    #    print "neg: %s:%s" % (k[0], k[1])
                    #for k in sorted_pos_list[-100:]:
                    #    print "pos: %s:%s" % (k[0], k[1])
                    print len(true_array)
                    print len(prob_array)
                                
                    precision, recall, thresholds = precision_recall_curve(true_array, prob_array) 
                    print("pr dims")
                    print len(recall)
                    print len(precision)
                    FPR, TPR, roc_thresholds = roc_curve(true_array, prob_array)
                    print("roc dims")
                    print len(FPR)
                    print len(TPR) 
                    print len(roc_thresholds)
                    #average_precision = average_precision_score(true_array, prob_array)
            
                    #print "precision: %s" % (list(precision),)
                    #print "recall: %s" % (list(recall),)
                    print len(precision)
                    print len(recall)
                    print len(thresholds)
            
            
                    if args.plot_thresholds:
                        print("plot thresholds")
                        #kdrew: set the index of the entry >= to threshold
                        #kdrew: if there is no entry >= to threshold, set the index to the previous index
                        try:
                            indexOf1 = next(x[0] for x in enumerate(thresholds) if x[1] >= 0.1) 
                        except StopIteration:
                            pass
                        try:
                            indexOf2 = next(x[0] for x in enumerate(thresholds) if x[1] >= 0.2) 
                        except StopIteration:
                            indexOf2 = index01
                        try:
                            indexOf3 = next(x[0] for x in enumerate(thresholds) if x[1] >= 0.3) 
                        except StopIteration:
                            indexOf3 = indexOf2
                        try:
                            indexOf4 = next(x[0] for x in enumerate(thresholds) if x[1] >= 0.4) 
                        except StopIteration:
                            indexOf4 = indexOf3
                        try:
                            indexOf5 = next(x[0] for x in enumerate(thresholds) if x[1] >= 0.5) 
                        except StopIteration:
                            indexOf5 = indexOf4
                        try:
                            indexOf6 = next(x[0] for x in enumerate(thresholds) if x[1] >= 0.6) 
                        except StopIteration:
                            indexOf6 = indexOf5
                        try:
                            indexOf7 = next(x[0] for x in enumerate(thresholds) if x[1] >= 0.7) 
                        except StopIteration:
                            indexOf7 = indexOf6
                        try:
                            indexOf8 = next(x[0] for x in enumerate(thresholds) if x[1] >= 0.8) 
                        except StopIteration:
                            indexOf8 = indexOf7
                        try:
                            indexOf9 = next(x[0] for x in enumerate(thresholds) if x[1] >= 0.9) 
                        except StopIteration:
                            indexOf9 = indexOf8
                        try:
                            indexOf10 = next(x[0] for x in enumerate(thresholds) if x[1] >= 1.0) 
                        except StopIteration:
                            indexOf10 = indexOf9
            
                        print thresholds[indexOf1]
                        print indexOf1
                        print thresholds[indexOf2]
                        print indexOf2
                        print thresholds[indexOf3]
                        print indexOf3
                        print thresholds[indexOf4]
                        print indexOf4
                        print thresholds[indexOf10]
                        print indexOf10
            
                        #print thresholds[indexOf1-1]
                        #print thresholds[indexOf10-1]
            
                        threshold_precisions = []
                        threshold_recalls = []
                        threshold_labels = []
                        print "threshold 0.1"
                        print "precision: %s" % precision[indexOf1]
                        print "recall: %s" % recall[indexOf1]
                        threshold_precisions.append(precision[indexOf1])
                        threshold_recalls.append(recall[indexOf1])
                        threshold_labels.append('0.1')
                        
                        print "threshold 0.2"
                        print "precision: %s" % precision[indexOf2]
                        print "recall: %s" % recall[indexOf2]
                        threshold_precisions.append(precision[indexOf2])
                        threshold_recalls.append(recall[indexOf2])
                        threshold_labels.append('0.2')
                        
                        print "threshold 0.3"
                        print "precision: %s" % precision[indexOf3]
                        print "recall: %s" % recall[indexOf3]
                        threshold_precisions.append(precision[indexOf3])
                        threshold_recalls.append(recall[indexOf3])
                        threshold_labels.append('0.3')
                        
                        print "threshold 0.4"
                        print "precision: %s" % precision[indexOf4]
                        print "recall: %s" % recall[indexOf4]
                        threshold_precisions.append(precision[indexOf4])
                        threshold_recalls.append(recall[indexOf4])
                        threshold_labels.append('0.4')
                        
                        print "threshold 0.5"
                        print "precision: %s" % precision[indexOf5]
                        print "recall: %s" % recall[indexOf5]
                        threshold_precisions.append(precision[indexOf5])
                        threshold_recalls.append(recall[indexOf5])
                        threshold_labels.append('0.5')
                        
                        print "threshold 0.6"
                        print "precision: %s" % precision[indexOf6]
                        print "recall: %s" % recall[indexOf6]
                        threshold_precisions.append(precision[indexOf6])
                        threshold_recalls.append(recall[indexOf6])
                        threshold_labels.append('0.6')
                        
                        print "threshold 0.7"
                        print "precision: %s" % precision[indexOf7]
                        print "recall: %s" % recall[indexOf7]
                        threshold_precisions.append(precision[indexOf7])
                        threshold_recalls.append(recall[indexOf7])
                        threshold_labels.append('0.7')
            
                        print "threshold 0.8"
                        print "precision: %s" % precision[indexOf8]
                        print "recall: %s" % recall[indexOf8]
                        threshold_precisions.append(precision[indexOf8])
                        threshold_recalls.append(recall[indexOf8])
                        threshold_labels.append('0.8')
                        
                        print "threshold 0.9"
                        print "precision: %s" % precision[indexOf9]
                        print "recall: %s" % recall[indexOf9]
                        threshold_precisions.append(precision[indexOf9])
                        threshold_recalls.append(recall[indexOf9])
                        threshold_labels.append('0.9')
            
                        print "threshold 1.0"
                        print "precision: %s" % precision[indexOf10]
                        print "recall: %s" % recall[indexOf10]
                        threshold_precisions.append(precision[indexOf10])
                        threshold_recalls.append(recall[indexOf10])
                        threshold_labels.append('1.0')
            
            
                    label = args.results_wprob[i]
                    
                    if args.labels != None:
                        #label = args.labels[evalset]
                        label = args.labels[i] + "_" + str(evalset) + "_" + str(evalset2)

                    if i == 0 and evalset == 0 and evalset2 ==0:
                          label = args.labels[0]

                    elif i == 0 and evalset == 1 and evalset2 ==1:
                          label = args.labels[1]
                          print(precision)
                          print(recall)
                    #elif i == 1 and evalset == 0 and evalset2 ==0:
                    #      label = 'cross_val'
                    else:
                         print("is this happening?", i, evalset, evalset2) 
                         continue
                    print("recall")
                    print(recall)
                    print("precision")
                    print(precision)
                    print("label")
                    print(label) 

                    label_pr_table = pd.DataFrame({'Recall':recall, 'Precision':precision,'label':label})
                    print(label_pr_table)
                    output_pr_table = output_pr_table.append(label_pr_table, ignore_index=True)
                    
                    label_roc_table = pd.DataFrame({'TPR':TPR, 'FPR':FPR,'Thresholds':roc_thresholds, 'label':label})
                    print(label_roc_table)
                    output_roc_table = output_roc_table.append(label_roc_table, ignore_index=True)

                    line, = plt.plot(recall, precision, label=label)
                    if args.plot_thresholds:
                        plt.scatter(threshold_recalls, threshold_precisions, color=line.get_color())
                        for i, label in enumerate(threshold_labels):
                            plt.annotate(label, xy=(threshold_recalls[i],threshold_precisions[i]))
                except Exception as E:
                 print(E) 
        
    #plt.clf()
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    #plt.title('Precision-Recall example: AUC={0:0.2f}'.format(average_precision))
    plt.title('Precision-Recall')
    plt.legend(loc="upper right",fontsize=8)

    plt.savefig(args.output_file)
 
    output_csv = args.output_file + ".csv"
    output_pr_table.to_csv(output_csv, index = False)

 
    output_roc_csv = args.output_file + "_roc.csv"
    output_roc_table.to_csv(output_roc_csv, index = False)

if __name__ == "__main__":
    main()


