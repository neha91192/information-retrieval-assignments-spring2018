'''
Created on Feb 25, 2018

@author: nehashukla
'''
'''

'''

import collections
import io
import math
import os
import sys

from LinkInfo import LinkInfo


class PageRank:
    
   
    '''
    Teleportation Factor
    '''
    d = 0.85
    '''
    True for stopping page rank computation upto 4 iterations
    '''
    test2 = False
    '''
    Stores the input graph value
    '''
    graph_name = ''
    
    '''
    Count for displaying Page Rank values and inlink counts of sorted document ids 
    '''
    result_count = 50
    
    '''
    Constructor
    '''
    def __init__(self):
        
        self.N = 0
        self.perplexity_values = []
        self.document_dictionary = {}
        
    '''
    Computes page rank for the given graph. 
    Converts the graph to a document dictionary {doc id : <LinkInfo> object} 
    Calculates page rank until the page rank converges to a value. 
     
    '''    
    def computePageRank(self, graph_name):
        
        self.graph_name = graph_name
        self.create_dictionary_from_graph()
        
        pages = self.document_dictionary.keys()
        self.N = len(pages)
        sink_nodes = []

        for page in pages:
            if(len(self.document_dictionary[page].getOutlinks())==0):
                sink_nodes.append(page)
            self.document_dictionary[page].setPageRank(1.0/self.N)
        
        i = 1   
        while(not(self.convergence(i))):
            page_rank = {}
            sinkPR = 0
            for node in sink_nodes:
                sinkPR += self.document_dictionary[node].getPageRank()
            
            for each_page in pages:
                newPR = (1-self.d)/self.N
                newPR +=(self.d*sinkPR)/self.N
            
                for inlink in self.document_dictionary[each_page].getInlinks():
                    inlink_info = self.document_dictionary[inlink]
                    no_outlinks = len(inlink_info.getOutlinks())
                    newPR+= (self.d*inlink_info.getPageRank())/no_outlinks
                    page_rank[each_page] = newPR 

            for each_page in pages:
                PR = page_rank[each_page]
                self.document_dictionary[each_page].setPageRank(PR)
           
            i+=1
        
        return self.document_dictionary
  
    
    '''
    Checks if the page rank values have converged or not for at least past 4 iterations
    '''
    def convergence(self, iteration):
        #ends after iteration 4
        if(self.test2 is True and iteration==5):
            return True
        if(iteration>4):
            count = 0
            for i in range(len(self.perplexity_values)-1, len(self.perplexity_values)-4, -1):
                if(abs(self.perplexity_values[i] - self.perplexity_values[i-1]) < 1):
                    count+=1
            if(count==3):
                return True  
            
        self.calculate_perplexity()
            
        return False
    '''
    Finds the perplexity value of the Page Rank distribution
    '''
    def calculate_perplexity(self):
        entropy = 0
        for entry in self.document_dictionary.keys():
            info = self.document_dictionary[entry]
            entropy = entropy + info.getPageRank()*(math.log2(info.getPageRank()))
        entropy = -1*entropy
        
        perplexity = 2**entropy
        self.perplexity_values.append(perplexity)
    
    '''
    Creates dictionary for storing link information. Link information includes --> inlinks list, outlinks list, and the final page rank value.
    '''
    def create_dictionary_from_graph(self):
        dictionary = collections.OrderedDict()
        
        file_name = self.graph_name
        if(os.path.isfile(file_name)):
                with open(file_name, 'r', encoding='utf-8') as file:
                    for line in file:
                        key, values = line.strip('\n').split(':  ')
                   
                        inlinks = values.split('  ')
                        if(key in dictionary.keys()):
                            linkinfo = dictionary.get(key) 
                        else: 
                            linkinfo = LinkInfo()
                        
                        linkinfo.setInlinks(inlinks)
                        dictionary[key] = linkinfo
                        for inlink in inlinks:
                            if(inlink in dictionary.keys()):
                                inlink_info = dictionary.get(inlink) 
                            else: 
                                inlink_info = LinkInfo() 
                            inlink_info.setOutlink(key)
                            dictionary[inlink] = inlink_info
        
        self.document_dictionary = dictionary



    def save_results(self, dictionary):
        print("*****Links as per page rank values******")
        sortedOrderbyPageRank = sorted(dictionary, key=lambda x:dictionary.get(x).getPageRank(),reverse=True)
    
        for key in sortedOrderbyPageRank:
            print(key,':',dictionary[key].getPageRank())
    
        sortedOrderbyInlinks = sorted(dictionary, key=lambda x:len(dictionary.get(x).getInlinks()),reverse=True)

        with io.open(self.graph_name[:2]+"_pagerank_results.txt", 'w+', encoding='utf-8') as file:
            i =1
            for key in sortedOrderbyPageRank:
                if(i==self.result_count+1):
                    break
                value = dictionary[key]
                data_to_write = str(i)+"."+"  "+key+"    "+str(value.getPageRank())
                file.write(data_to_write+'\n')
                i+=1
        
        with io.open(self.graph_name[:2]+"_inlinks_results.txt", 'w+', encoding='utf-8') as file:
            i =1
            for key in sortedOrderbyInlinks:
                if(i==self.result_count+1):
                    break
                value = dictionary[key]
                data_to_write = str(i)+"."+" "+key+"    "+str(len(value.getInlinks()))
                file.write(data_to_write+'\n')
                i+=1
                
        with io.open(self.graph_name[:2]+"_PerplexityValues.txt", 'w+', encoding='utf-8') as file:
            i =1
            for value in self.perplexity_values:
                data_to_write = "Perplexity "+str(i)+": "+str(value)
                file.write(data_to_write+'\n')
                i+=1
                
    
def main(graph_name):
 
    
    pagerank = PageRank()
    
    dictionary = pagerank.computePageRank(graph_name)
    
    pagerank.save_results(dictionary)
    
       
        
if __name__ == '__main__':
    if(len(sys.argv)==1):
        raise Exception("Please pass the argument: Either G1 for BFS graph or G2 for DFS graph")
    else:
        graph_name =sys.argv[1]
        
    main(graph_name)       
        
        
            
        
               
        
        
            
        
        
        
