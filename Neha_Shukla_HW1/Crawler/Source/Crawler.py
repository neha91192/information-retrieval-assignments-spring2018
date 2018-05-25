'''

Created on Jan 30, 2018

@author: nehashukla

'''

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urlparse
import enchant
import os

'''
Performs crawling of any Website.  For a given seed URL, it parses all the desired links of the page and traverses using 2 popular Algorithms - 
1. Breadth First Search and 2. Depth First Search. If a keyword is provided in the argument, it also performs Focused crawling ( i.e visiting only those links
which contains keywords) 
'''
class Crawler:
    
    '''
    Initializes frontier list with the seed url and keyword if it's given in the argument 
    '''
    def __init__(self, seed, keyword):
        self.frontier = [seed]
        self.keyword = keyword
    
    '''    
    Contains regular expression to filter out unwanted urls in the crawl
    '''
    urlFilterRegex = '(^/wiki)/(((?!:|Main_Page).)*$)[a-zA-Z0-9\-/^:]*'
    
    '''
    List containing all the urls to be visited
    '''
    frontier = []
    '''
    Prefix to be added in case only relative url was discovered in the parsing of web pages
    '''
    urlPrefix = ''
    '''
    Variable for storing keywords passed in focused crawling
    '''
    keyword = []
    '''
    Stores maximum crawling size 
    '''
    crawl_size = 1000
    '''
    Stores maximum crawling depth 
    '''
    max_depth = 6
    '''
    Variable to keep a track of current DFS depth
    '''
    dfs_depth = 1
    '''
    Variable to keep a track of current BFS depth
    '''
    bfs_depth = 0
    '''
    Time in seconds for maintaining politeness policy
    '''
    timeout = 1
    '''
    List to store all the links crawled through DFS
    '''
    dfs_visited = []
    '''
    List to store all the links crawled through BFS
    '''
    bfs_visited = []
    '''
    Says whether current crawl is BFS or not
    '''
    is_bfs = False
    '''
    Says whether current crawl is DFS or not
    '''
    is_dfs = False
    '''
    Boolean variable to keep a track of focused crawling
    '''
    is_focused_crawl = False
    
    '''
    Index variable to keep a track of file name 
    '''
    file_index_count = 1
    '''
    Relative path to store crawled links
    '''
    crawled_links_location = '/downloaded_files/crawled_links'
    '''
    Relative path to store BFS crawled content files
    '''
    bfs_content_location = '/downloaded_files/bfs_content_files'
    
    '''
    Finds the domain name of the seed url and creates a prefix to form a complete url for the crawled links
    '''
    def setUrlPrefix(self):
        urlobject = urlparse(self.frontier[0])
        self.urlPrefix = urlobject.scheme + "://" + urlobject.netloc

    '''

    Fetches all the URLs present in seed URL content page

    '''

    def getURLs(self, url):
        
        response = urlopen(url)
        #Check for redirection
   
        html = response.read()
        time.sleep(self.timeout)  # takes care of politeness policy

        soup = BeautifulSoup(html.decode('utf-8'), 'html.parser')
        content = soup.find('html')

        pattern = re.compile(self.urlFilterRegex)
        
        filteredLinks = soup.find_all('a', attrs={'href' : pattern}) 

        url_list = []
        for link in filteredLinks:
            path = link['href']
            completeURL = self.urlPrefix + path
            if(self.is_bfs and self.is_visited(completeURL, self.bfs_visited)):
                continue
            elif(self.is_dfs and completeURL.strip() in self.dfs_visited):
                continue
            if(not(self.is_visited(completeURL, url_list))):  
                if(self.is_focused_crawl and not self.is_link_relevant(path)):
                    continue
                url_list.append(completeURL)
    

        if(self.is_bfs and not self.is_focused_crawl and self.file_index_count <= self.crawl_size):
            self.downloadContent(content.prettify())

        return url_list
    
    def is_visited(self,link, list_to_check):
        is_visited = link.lower() in (n.lower() for n in list_to_check)
        return is_visited
      

    '''

    Performs DFS crawling. 

    '''     

    def crawl_dfs(self, frontier):

        while(len(frontier) > 0 and len(self.dfs_visited) < self.crawl_size):
            seed = frontier.pop(0)
            exit_flag = True
            
            # checks whether seed has been already visited. If found to be visited, it finds the next appropriate seed from the frontier
            if(seed in self.dfs_visited):
                while(seed in self.dfs_visited and len(frontier) > 0):
                    seed = frontier.pop(0)
                    
                if(len(frontier) == 0):
                    exit_flag = False

            if(len(self.dfs_visited) < self.crawl_size):
                self.dfs_visited.append(seed)
            else:
                return

            if(self.dfs_depth < self.max_depth and exit_flag is True):
                frontier_child = self.getURLs(seed)
                self.dfs_depth = self.dfs_depth + 1
                # crawl further
                self.crawl_dfs(frontier_child)

        if(len(frontier) == 0):  # When all the siblings have been visited, go back to step n-1
            self.dfs_depth = self.dfs_depth - 1

    '''
    Performs BFS crawling. 

    '''        
    def crawl_bfs(self, frontier):
        
        while(len(frontier) > 0 and len(self.bfs_visited) < self.crawl_size):
            bfs_children_list = []
            seed = frontier[0]
            
            exit_flag = False
            # Checks if link has been already visited or not
            if(seed in self.bfs_visited):
                while(seed in self.bfs_visited and len(frontier) > 0):
                    seed = frontier.pop(0)
                if(len(frontier) == 0):
                    exit_flag = True

            if(exit_flag is False):
                for i in range(0, len(frontier)):
                    if(frontier[i] not in self.bfs_visited):
                        frontier_child = self.getURLs(frontier[i])
                        if(len(self.bfs_visited) < self.crawl_size ):
                            self.bfs_visited.append(frontier[i])
                        else:
                            return
                    else:
                        continue
                    bfs_children_list.append(frontier_child)
                self.bfs_depth = self.bfs_depth + 1
                print(self.bfs_depth)
                del frontier[:]

            while(len(bfs_children_list) > 0 and self.bfs_depth < self.max_depth):
                self.crawl_bfs(bfs_children_list.pop(0))  
            
   
    
    '''
    Checks if the given link is relevant to the keyword. 
    
    Steps:  
    1. Split the link using '/' delimiter and store in a list. This ensures that all the words in the link are tokenized and ready to be considered for the 
    next step
    2. For n keywords, check if the keyword is present in the list of tokenized url obtained from step 1. If found, save the particular token in a list. Let's call it as a 
    candidate token 
    3. Remove extra special characters from the candidate token and replace it with ' '. If the candidate token is same as keyword, return True, otherwise go 
    to the next step
    4. Split the candidate token using ' ' delimiter and store it in a processed_word_list. ' ' in candidate token is generated because of the previous step.
    This step ensures decompounding of the candidate token. 
    5. Now remove keyword from the processed_word_list to consider those only elements in the processed_word_list which do not match with the keyword.
    6. Using enchant Dictionary for English language, check if the decompounded words in the processed_word_list is found in dictionary. If all of them fails to,
    return false, otherwise true
    7. Repeat the same step for the next keyword in the list
    '''
    def is_link_relevant(self, link):
        tokenized_url_list = link.split('/')  # Splits link using '/' and stores all the word in a list
        candidate_list = []
         
        for keyword in self.keyword:
            match_count = True
            for each_word in tokenized_url_list:  # Compares if each word in the list matches with the keyword and saves in a list for future processing
                if(keyword.lower() in each_word.lower()):   
                    candidate_list.append(each_word)
                
            if(candidate_list != []):
                for word in candidate_list:
                    if(keyword == word):
                        return True
                    else:
                        processed_word = re.sub('[^A-Za-z0-9]+', ' ', word.lower())
                        if(keyword in processed_word):
                            decompounded_word = processed_word.split(keyword)
                        
                if(decompounded_word != []):
                    enchant_checker = enchant.Dict("en_US")
                    for each in decompounded_word:
                        found = False
                        if enchant_checker.check(each):
                            found = True
                    if(not found):
                        match_count = False
            else: 
                match_count = False
        return match_count 
    '''
    Print function to copy crawled links and BFS html content data to a desired location. 
    Files containing the links of bfs, dfs and focused_bfs can be found at '<source_path>/downloaded_files/crawled_links'
    '''
    def printData(self, visited_links):
        rel_path = os.path.dirname(os.path.abspath(__file__))
        directory_path = rel_path + self.crawled_links_location
        directory_path2 = rel_path + self.bfs_content_location
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, 0o777)
        
        if(self.is_bfs):
            if(self.is_focused_crawl):
                file = ''
                file = open(directory_path + '/focused_bfs.txt', 'w+')
            else:
                file = open(directory_path + '/bfs.txt', 'w+')
                file2 = open(directory_path2 + '/file_keys.txt', 'w+')
        else:
            file = open(directory_path + '/dfs.txt', 'w+')
        
        for i in range(0, len(visited_links)):
            print(visited_links[i])
            #file.write(visited_links[i]+'\n')
            if(self.is_bfs and not self.is_focused_crawl):
                file2.write(str(i + 1) + ": " + "%s\n" % self.fetch_doc_id(visited_links[i]))
        file.close()
    
    '''
    Stores the content of visited pages in a folder. It can found at '<source_path>/downloaded_files/bfs_content_files'
    folder and the file names are indexes starting from 1 to the crawl_size of the program. The corresponding key values can be found in 'file_keys.txt' file.
    '''
    def downloadContent(self, data):
        rel_path = os.path.dirname(os.path.abspath(__file__))
        directory_path = rel_path + '/downloaded_files/bfs_content_files'
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, 0o777)
        file = open(directory_path + '/' + str(self.file_index_count) + ".txt", "w", encoding='utf-8')
        
        file.write(str(data))
        file.close()  
        self.file_index_count = self.file_index_count + 1
        
    '''
    Retrieves the Id format of the url. 
    '''
    def fetch_doc_id(self,url):
        link = url
        from_index = link.find('wiki/') + 5
        to_index = len(link) 
        doc_id = link[from_index:to_index]
        return doc_id
        
# 
# def main(seed, keyword):
# 
#         crawler = Crawler(seed, keyword)
#         crawler.setUrlPrefix()
# 
#         if(crawler.keyword!=[]):
#             crawler.is_focused_crawl = True
#             print("Starting focused crawl..")
#             crawler.is_bfs = True
#             crawler.crawl_bfs(crawler.frontier)
#             print("Printing visited crawls..")
#             crawler.printData(crawler.bfs_visited)
#             crawler.is_bfs = False
#             crawler.is_focused_crawl = False
#             print("Focused crawl completed!")
#         else:
#             print("Starting BFS crawl..")
#             crawler.is_bfs = True
#             crawler.crawl_bfs(crawler.frontier)
#             print("Printing bfs visited crawls..")
#             crawler.printData(crawler.bfs_visited)
#             crawler.is_bfs = False
#             print("BFS crawl completed!")
#             
#             print("Starting DFS crawl")
#             crawler.is_dfs = True
#             crawler.frontier = [seed]
#             crawler.crawl_dfs(crawler.frontier)
#             print("Printing dfs visited crawls..")
#             crawler.printData(crawler.dfs_visited)
#             crawler.is_dfs = False
#             print("DFS crawl completed!")
#         
#  
# if __name__ == '__main__':
#     
#     if(len(sys.argv) ==1):
#         raise Exception("Please pass the argument(s)\nTo perform Task 1 for BFS and DFS crawling, please provide seed url\nTo perform Task2 for Focused Crawling in BFS, please provide seed url and keyword\n")
#     
#     elif(len(sys.argv)>=2):
#         keyword = []
#         seed = sys.argv[1]
#         for i in range(2,len(sys.argv)):
#             keyword.append(sys.argv[i])
#         
#         if(len(sys.argv)==1):
#             keyword = ''
#         main(seed,keyword)


def main():

  

        seed = "https://en.wikipedia.org/wiki/Solar_eclipse"

        crawler = Crawler(seed, '')

        crawler.setUrlPrefix()        

        crawler.is_bfs = True
 
        crawler.crawl_bfs(crawler.frontier)
 
        crawler.printData(crawler.bfs_visited)
 
        crawler.is_bfs = False  
 
#         crawler.is_dfs = True
#  
#         crawler.frontier = [seed]
#  
#         crawler.crawl_dfs(crawler.frontier)
#            
#         crawler.printData(crawler.dfs_visited)
#  
#         crawler.is_dfs = False

if __name__ == '__main__':

    main()
    
    
       
   
        
