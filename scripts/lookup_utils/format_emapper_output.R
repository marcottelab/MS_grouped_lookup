#!/usr/bin/env Rscript

suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(tidyr))
suppressPackageStartupMessages(library(readr))
suppressPackageStartupMessages(library("argparse"))


#Should rewrite in python

# create parser object
parser <- ArgumentParser()
# specify our desired options
# by default ArgumentParser will add an help option
parser$add_argument("-f", "--filename", dest="filename", required=TRUE,
                        help="Input eggnog_mapper output, .annotations file output by emapper.py")
parser$add_argument("-f_diamond", "--filenamediamond", dest="filename_diamond",
                        help="Input eggnog_mapper output from diamond to supplement hmmer output")
parser$add_argument("-o", "--output_filename", action="store",
                        dest="output_filename", help="Output filename for ProteinID - groupID mapping tsv", default="outfile.txt")

parser$add_argument("-s", "--search_type", action="store", required=TRUE,
                        dest="search_type", choices=c('diamond', 'hmmer', 'maxrecall'), help="hmmer, diamond, or bestmatch (hmmer), or maxrecall (hmmer + diamond). ")

parser$add_argument("-l", "--level", action="store",
                        dest="level_sel", default=NULL, help="Output a specific phylogenetic level for diamond search")
parser$add_argument("-v", "--version", action = "store", default=1, help = "emapper version, 1 or 2")


args <- parser$parse_args()
df <- read_delim(args$filename, delim="\t", col_names=FALSE)

if(args$version == 1){
    names(df) <- c("ProteinID", "best_prot_match", "prot_match_evalue", "prot_match_bitscore", "predicted_gene_name", "GO_terms", "KEGG_pathways", "Annotation_tax_scope", "Matching_OGs", "hmmer_best", "COG_funcats", "eggNOG_HMM_model_annotation")
}

if(args$version == 2){
 
    names(df) <- c("ProteinID", "seed_eggNOG_ortholog", "seed_ortholog_evalue", "seed_ortholog_score", "Predicted_taxonomic_group", "Predicted_protein_name", "Gene_Ontology_terms", "EC_number", "KEGG_ko", "KEGG_Pathway", "KEGG_Module", "KEGG_Reaction", "KEGG_rclass", "BRITE", "KEGG_TC", "CAZy_", "BiGG_Reaction", "tax_scope", "Matching_OGs", "bestOG", "COG_Functional_Category", "free_text")
}


print(args$output_filename)

if(args$search_type == "diamond"){
    df_sel <- df %>% select(ProteinID, Matching_OGs)
    
    
    df_unnest <- df_sel %>% 
        mutate(Matching_OGs = strsplit(as.character(Matching_OGs), ",")) %>% 
        unnest(Matching_OGs) %>%
        separate(Matching_OGs, into=c('ID', 'level'), sep="@")
    
    
    if(!is.null(args$level_sel)){
        df_final <- df_unnest %>% filter(level==args$level_sel)
 
       
    }
}

if(args$search_type == "hmmer"){

    #Break column into three columns
    df_best <- df %>% select(ProteinID, hmmer_best) %>%
              separate(hmmer_best, into=c('ID', 'evalue', 'score'), sep="[|]")

    #Get one match per row
    df_sel <- df %>% select(ProteinID, Matching_OGs) %>% 
                     mutate(Matching_OGs = strsplit(as.character(Matching_OGs), ",")) %>% 
                     unnest(Matching_OGs) %>%
                     separate(Matching_OGs, into=c('ID', 'level'), sep="@") 
    
    if(!is.null(args$level_sel)){
        df_sel <- df_sel %>% filter(level==args$level_sel)


    df_join <- left_join(df_sel, df_best, by = c("ID", "ProteinID"))   
    df_join[is.na(df_join)] <- 0

    df_final <- df_join %>%
                arrange(desc(score)) %>%
                group_by(ProteinID) %>%  
                filter(row_number() == 1)
 
       
    }
}

if(args$search_type == "maxrecall"){


    # Get best hit hmmer score
    df_best <- df %>% select(ProteinID, hmmer_best) %>%
              separate(hmmer_best, into=c('ID', 'evalue', 'score'), sep="[|]") %>%
              select(ProteinID, ID, score)
              

    # Read supplementary diamond search
    df_diamond <- read_delim(args$filename_diamond, delim="\t", col_names=FALSE, skip=3) 
    names(df_diamond) <- c("ProteinID", "best_prot_match", "prot_match_evalue", "prot_match_bitscore", "predicted_gene_name", "GO_terms", "KEGG_pathways", "Annotation_tax_scope", "Matching_OGs", "hmmer_best", "COG_funcats", "eggNOG_HMM_model_annotation")

    # Organize diamond output
    df_diamond <- df_diamond %>% 
                     select(ProteinID, Matching_OGs) %>% 
                     mutate(Matching_OGs = strsplit(as.character(Matching_OGs), ",")) %>% 
                     unnest(Matching_OGs) %>%
                     separate(Matching_OGs, into=c('ID', 'level'), sep="@")
    # Organize hmmer output
    df_sel <- df %>% select(ProteinID, Matching_OGs) %>% 
                     mutate(Matching_OGs = strsplit(as.character(Matching_OGs), ",")) %>% 
                     unnest(Matching_OGs) %>%
                     separate(Matching_OGs, into=c('ID', 'level'), sep="@")
    

    #Filter to level
    if(!is.null(args$level_sel)){
        df_sel <- df_sel %>% filter(level==args$level_sel)
        df_diamond <- df_diamond %>% filter(level==args$level_sel)

       
    #Get every ProteinID from the diamond search that isn't in the hmmer set using anti_join
    df_diamond_filt <- df_diamond %>% anti_join(df_sel, by = "ProteinID")  
    df_diamond_filt$score <- NA 
    

    #Annotate hmmer search with best match hmmer score
    df_join <- left_join(df_sel, df_best, by = c("ID", "ProteinID")) 


    print(dim(df_diamond_filt))
    print(dim(df_join))
      
    # Combine both data frames
    df_concat <- rbind(df_diamond_filt, df_join)
    print(dim(df_concat))

    #Get the top ID for each proteinID
    #Prioritize IDs with matching hmmer score
    #Otherwise take first ID listed
    df_final <- df_concat %>%
                arrange(desc(score)) %>%
                group_by(ProteinID) %>%  
                filter(row_number() == 1)
       
    }
}


  
if(args$search_type == "bestmatch"){

    print(dim(df))
    df_final <- df %>% select(ProteinID, hmmer_best) 
   
       
}

df_final <- df_final %>% select(ProteinID, ID)

#If the ID starts with a number, assume it needs the ENOG41 prefix. 
#Add ENOG41 prefix
df_final <- df_final %>% mutate(ID = gsub(".*(?=^[0-9])", "ENOG41", ID, perl=TRUE))

print(head(df_final))

df_final %>% write.table(args$output_file, row.names=FALSE, quote=FALSE, sep="\t")


