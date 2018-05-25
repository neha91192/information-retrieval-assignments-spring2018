
Crawler.py is the driver class for this assignment. 

It is built on python version 3.5 and leverages the following libraries:
  * pyenchant version 2.0.0 for focused crawling part
  * BeautifulSoup 4 for parsing HTML pages 

Steps for installation:

-- Please have the appropriate python version installed in the system
-- To install BeautifulSoup 4, run pip install beautifulsoup4 or python setup.py install  
-- To install Pyenchant, run pip3 install pyenchant

To run Crawler.py, use python Crawler.py <seed> <keyword1> <keyword2> .. <keyword n>

The output files can be found in the location - <source>/downloaded_files

To the run the command again, please delete the folder - <source>/downloaded_files manually

Max_Depth reached for DFS Crawl -> 6
Max_Depth reached for BFS Crawl -> 2

Referenced links:

1. http://pythonhosted.org/pyenchant/
2. https://www.crummy.com/software/BeautifulSoup/
3. https://regex101.com/
4. https://docs.python.org/3/library/urllib.html
