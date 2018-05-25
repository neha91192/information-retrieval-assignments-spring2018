Task1(Lucene):

Lucene.java is the source program for Task 1 of this assignment. To run this program, import the source package 'Task1_Lucene'
present in the assignment folder to any of the Java IDE.

--It is built on Lucene version 4.7.2

Steps to run Lucene.java on Eclipse(Juno and above):
1. Import project:
Go to File --> Import --> General --> Existing projects into workspace --> Browse source directory and select 'Task1_Lucene'
folder of the assignment folder
2. Add classpath variable:
Go to Project --> Properties --> Java Build Path --> Libraries --> choose Add Variable --> click on Configure variable button
--> click 'New' button and enter following details --> Name: LUCENE Folder Path as: <source>/Task1_Lucene/lucene_jars
Click on 'Ok', 'Apply and Close' and when it asks for Apply full build, choose 'yes'
3. Now using eclipse console, select 'Run' option and select 'Lucene' class to run. It will ask for the following details:
  a. Full path for index location:
		 Enter 'Index' to create Index folder. You can locate this folder created inside the Task1_Lucene folder
	b. Path to Corpus location:
		 Enter '../corpus'. It will index all the documents present in the corpus folder outside the Task1_Lucene folder
	c. The program will automatically load queries from the queries.txt file present in the assignment folder. The output
	   for this program can be found in 'Lucene-results.txt' file in Task1_Lucene folder


Task2(BM25 Model):

RetrievalModelTest.py is the driver class for this assignment. The other classes are 'RetrievalModel.py' and 'BM25Model.py' containing main implementation code for this assignment.

--It is built on Python version 3.5

--Steps to run:
1. Input list of queries in the file 'queries.txt'. It already contains 10 queries given in the assignment. However, if you wish to add more in the list,
please enter each query in a new line in the format: '<query_id>. <query>'
2. Once the query is updated, please run the following command:
			python RetrievalModelTest.py
3. Search results can be found at the location <source>/Search_Results_<model_name> file. For this assignment, model_name will be 'BM25Model'


Referenced links for this assignment:

1.https://lucene.apache.org/core/3_5_0/scoring.html
2.https://www.tutorialspoint.com/lucene/lucene_search_operation.htm
3.https://en.wikipedia.org/wiki/Okapi_BM25
