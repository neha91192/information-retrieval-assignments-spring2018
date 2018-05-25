
CorpusBuilder.py and IndexBuilder.py are the driver class for this assignment.

--Built on Python version 3.5

--Steps to run:
1. CorpusBuilder.py: Generates corpus from the crawled BFS html files 
To run this file, enter command:  
python CorpusBuilder.py 

2. IndexBuilder.py: Generates n-gram Indexer and corresponding Term and Document Frequency Tables.  It takes 2 arguments, first is the n-gram value for the inverted index and second is a Boolean variable denoting True for storing positions and False for not storing positions. Also, for this assignment, if you are giving arguments for storing position, please restrict the value of n to 1. 

      To run IndexBuilder.py, type command: 
      python IndexBuilder.py <n> <True/False>  

--Location of the Output files: 
1. Corpus: <source>/corpus (generated from 1st step)
2. Output Files from Task 2 and 3: <source>/indexer_output.(generated from 2nd step)

Note: The output files naming convention is as follows:
Task 1: 1. All files can be found in the location : <source>/corpus
Task2:	2. doc_terms_table_n (3 files)
	3. indexer_n (3 files) 
	4. indexer_n_position (1 file)
Task 3:
	1. tf_table_n (3 files)
	2. df_table_n (3 files)
	(where n stands for the unigram (n=1), bigram(n=2), trigram(n=3) values)


Referenced links for this assignment:

1. https://www.crummy.com/software/BeautifulSoup/bs4/doc/


