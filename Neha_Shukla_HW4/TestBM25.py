'''
Created on Apr 6, 2018

@author: nehashukla
'''

import math

class TestBM25:
    
    doc_length = {}
    bm25scores=[] 
    average_doc_length=  0
    k1=1.2
    k2=100
    b=0.75
    ri = 0;
    R = 0;
    N= 500000
    
    def computeBM25(self, query_list): 
            for query_word in query_list:
                
               
                
                if query_word is 'president':
                    ni = 40000
                    fi= 15
                elif query_word is 'lincoln':
                    ni = 300
                    fi = 25
                    
                qfi = query_list.count(query_word)
                
                K = self.k1 * ((1-self.b) + self.b*0.9)
                print(str(K))
                #fi = doc_tf_dictionary[doc_id]
                
                score = math.log(((self.ri+0.5)/(self.R-self.ri+0.5))/((ni-self.ri+0.5)/(self.N-ni-self.R+self.ri+0.5)))*(((self.k1+1)*fi)/(K+fi))*(((self.k2+1)*qfi)/(self.k2+qfi))
                if(self.bm25scores!=[]):
                    score = self.bm25scores.pop() + score
                self.bm25scores.append(score)
                print(str(score))
                    
def main(): 
    
    test = TestBM25()
    
    query_list = []
    query_list.append("president")
    query_list.append("lincoln")
    
    test.computeBM25(query_list)
    
if __name__ == '__main__':
    main()