'''
Created on Apr 3, 2018

@author: nehashukla
'''
import os
import math
import collections

class RetrievalModel:
    '''
    Score = Sum of each(Q,D(i)) [log (((ri+0.5)/(R-ri+0.5))/((ni-ri+0.5)/(N-ni-R+ri+0.5))) * ((k1+1)*fi/(k+fi)) * ((k2+1)*qfi/(k2+qfi))]
    
    K = k1((1-b) + b.dl/avdl)
    
    '''
    index_folder_location = '/indexer_output'
    index_file_name = '/indexer_1'
    doc_terms_file = '/doc_terms_table_1'
    corpus_location = '/corpus'
    search_results_file = '/bm25results'
    query_file_name = '/queries.txt'
    doc_length = {}
    average_doc_length=  0
    k1=1.2
    k2=100
    b=0.75
    ri = 0;
    R = 0;
    hits = 100
    
    
    def __init__(self):
        '''
        Constructor
        '''
        self.index_entries = {}
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        self.bm25scores = {}
        self.N = len(os.listdir(self.rel_path+self.corpus_location))
        self.queries = {}
    
    '''
    Loads queries from the text file.  
    '''    
    def loadQueries(self):
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        filename = self.rel_path+self.query_file_name
        self.queries = collections.OrderedDict()
        
        #file = open(filename, "r", encoding='utf-8')
        with open(filename, 'r', encoding="utf-8") as file:
            lines = file.read().splitlines()
            for query in lines:
                line = query.split('.')
                self.queries[line[0]] = line[1].strip()
    '''
    Reads inverted list entry [term : (doc_id, frequency_of_occurence_in_that_doc) ] for each query term. 
    Stores the same in a dictionary (index_entries), where key is query term and value is the (doc_id, frequency) pairs.
    '''        
    def fetchInvertedList(self):
        #read indexer file
        entries = []
        query_words = []
        for query in self.queries.values():
            query_words = query_words + query.split()
        
        query_words = set(query_words)
        with open(self.rel_path+self.index_folder_location+self.index_file_name, 'r', encoding="utf-8") as file:
            lines = file.read().splitlines()
            for line in lines:
                entries = line.split(':')
    
                if entries[0] in query_words: 
                    doc_list_text = entries[1]
                    doc_list = doc_list_text.split(', ')
                    self.index_entries[entries[0]] = doc_list
                    
    '''
    Uses BM25 retrieval model to calculate scores for related documents. It uses query list (eg 'dark', 'eclipse', 'moon') and calculates document score for every document in the corresponding 
    inverted list entries of these terms.  
    '''
                     
    def computeScore(self, query_list): 
        
        self.bm25scores = {}
        
        for query_word in query_list:
            
            doc_tf_dictionary = {}
            doc_list= []
            
            #processes index entries to find term frequency for each document.
            entry_list = self.index_entries[query_word]
            for entry in entry_list:
                doc_entry = entry.rsplit(',', 1)
                term_frequency_entry = doc_entry[1].strip(')')
                doc_entry =doc_entry[0].strip()
                doc_id = doc_entry[1:]
                doc_list.append(doc_id)
                doc_tf_dictionary[doc_id] = int(term_frequency_entry)
            
            #no of documents with the given query term
            ni = len(doc_list)
            #frequency of query term in the query
            qfi = query_list.count(query_word)
            
            #for each document in the set of documents that this query term has been appeared in 
            for doc_id in doc_list:
                K = self.k1 * ((1-self.b) + self.b*self.doc_length[doc_id]/self.average_doc_length)
                #frequency of the query term in the document
                fi = doc_tf_dictionary[doc_id]
                score = math.log(((self.ri+0.5)/(self.R-self.ri+0.5))/((ni-self.ri+0.5)/(self.N-ni-self.R+self.ri+0.5)))*(((self.k1+1)*fi)/(K+fi))*(((self.k2+1)*qfi)/(self.k2+qfi))
                if(query_word=='2017'):
                    log_value = math.log(((self.ri+0.5)/(self.R-self.ri+0.5))/((ni-self.ri+0.5)/(self.N-ni-self.R+self.ri+0.5)))
                    print('For query: '+str(query_list))
                    print(str(log_value))
                    print(str(ni))
                if(doc_id in self.bm25scores):
                    self.bm25scores[doc_id] = self.bm25scores[doc_id] + score
                else:
                    self.bm25scores[doc_id] = score
        
        
    '''
    Finds number of terms in all the relevant documents. It also calculates the average document length of the corpus
    '''    
    def calculateDocumentLength(self):
        with open(self.rel_path+self.index_folder_location+self.doc_terms_file, 'r', encoding="utf-8") as file:
            for line in file:
                entries = line.split(':')
                self.doc_length[entries[0]] = int(entries[1].strip())
            self.average_doc_length  = sum(self.doc_length.values())/self.N
            print(self.average_doc_length)
                
#     def setCorpusSize(self):
#         self.N  = len(os.listdir(self.rel_path+self.corpus_location)) # dir is your directory path
        
    '''
    Saves top result in the following order:
    query_id Q0 doc_id rank BM25_score system_name
    '''
    def saveResults(self,query_id):
        
        sorted_bm25_scores = sorted(self.bm25scores, key=lambda x:self.bm25scores.get(x) ,reverse=True)
        
        with open(self.rel_path+self.search_results_file, 'a', encoding='utf-8') as file:
            heading = '******Top 100 results for query '+self.queries[query_id]+':******\n'
            file.write(heading)
            for index,key in enumerate(sorted_bm25_scores):
                if(index<self.hits): 
                    line = str(query_id)+' Q0 '+key+' '+str(index+1)+' '+str(self.bm25scores[key])+' bm25Model'+'\n'
                    file.write(line)
                else:
                    break
       
      
def main():  

    bm25 = RetrievalModel();
    
    bm25.loadQueries()
    bm25.fetchInvertedList()
    bm25.calculateDocumentLength()
    
    for query_id, query in bm25.queries.items():
        querylist= query.split()
        bm25.computeScore(querylist)
        bm25.saveResults(query_id)
    
    

if __name__ == '__main__':
    main()