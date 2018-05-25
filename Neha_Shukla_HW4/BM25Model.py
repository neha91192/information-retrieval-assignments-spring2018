'''
Created on Apr 7, 2018

@author: nehashukla
'''
import math
import os
class BM25Model:
    '''
    classdocs
    '''
  


    def __init__(self, index_entries, no_of_documents, queries):
        '''
        Constructor
        '''
        self.index_entries = index_entries
        self.rel_path = os.path.dirname(os.path.abspath(__file__))
        self.bm25scores = {}
        self.N = no_of_documents
        self.queries = queries
        
    def computeScore(self):
        for query_word in self.queries:
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
                qfi = self.queries.count(query_word)
                
                #for each document in the set of documents that this query term has been appeared in 
                for doc_id in doc_list:
                    K = self.k1 * ((1-self.b) + self.b*self.doc_length[doc_id]/self.average_doc_length)
                    #frequency of the query term in the document
                    fi = doc_tf_dictionary[doc_id]
                    score = math.log(((self.ri+0.5)/(self.R-self.ri+0.5))/((ni-self.ri+0.5)/(self.N-ni-self.R+self.ri+0.5)))*(((self.k1+1)*fi)/(K+fi))*(((self.k2+1)*qfi)/(self.k2+qfi))
                    if(doc_id in self.bm25scores):
                        self.bm25scores[doc_id] = self.bm25scores[doc_id] + score
                    else:
                        self.bm25scores[doc_id] = score
            