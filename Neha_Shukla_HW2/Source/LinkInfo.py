'''
Created on Feb 25, 2018

@author: nehashukla
'''


class LinkInfo:

    
    def __init__(self):
        self.url = ''
        self.page_rank = 0
        self.inlinks = []
        self.outlinks = []
        
    
    def setPageRank(self,score):
        self.page_rank = score
        
    def getPageRank(self):
        return self.page_rank
    
    def getInlinks(self):
        return self.inlinks
    
    def setInlinks(self, links):
        self.inlinks = links
        
    def setInlink(self, link):
        self.inlinks.append(link)

    def getOutlinks(self):
        return self.outlinks
    
    def setOutlinks(self, links):
        self.outlinks = links
    def setOutlink(self,link):
        self.outlinks.append(link)


if __name__ == '__main__':
    pass