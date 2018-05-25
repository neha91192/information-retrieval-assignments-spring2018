package Lucene;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class Lucene {
	private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);
	private static String resultsFile = "Lucene-results-cacm.txt";
	private static String queryFile = "cacm_query.txt";
	private static String updatedFile = "cacm_query_updated.txt";

	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();

	/**
	 * Constructor
	 * 
	 * @param indexDir
	 *            the name of the folder in which the index should be created
	 * @throws java.io.IOException
	 *             when exception creating index.
	 */
	Lucene(String indexDir) throws IOException {

		FSDirectory dir = FSDirectory.open(new File(indexDir));

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, sAnalyzer);

		writer = new IndexWriter(dir, config);
	}

	/**
	 * Main class to run Analyzer
	 * 
	 * @param args
	 * @throws IOException
	 */
	public static void main(String[] args) throws IOException {
		System.out.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

		String indexLocation = null;
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		String s = br.readLine();

		Lucene indexer = null;
		try {
			indexLocation = s;
			indexer = new Lucene(s);
		} catch (Exception ex) {
			System.out.println("Cannot create index..." + ex.getMessage());
			System.exit(-1);
		}

		indexer(s, indexer);
		retriever(indexLocation);
	}

	/**
	 * Reads the location of the corpus and adds all the documents to form an
	 * indexer. Quits the method if userInput at anytime is 'q'
	 * 
	 * @param userInput
	 * @param indexer
	 */
	public static void indexer(String userInput, Lucene indexer) {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		// read input from user until he enters q for quit
		try {

			System.out.println(
					"Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
			System.out.println("[Acceptable file types: .xml, .html, .html, .txt]");
			userInput = br.readLine();

			// try to add file into the index
			indexer.indexFileOrDirectory(userInput);

			indexer.closeIndex();
		}

		catch (Exception e) {
			System.out.println("Error indexing " + userInput + " : " + e.getMessage());
		}

	}

	/**
	 * Takes location to the index and retrieves search results for given queries
	 * 
	 * @param indexLocation
	 */
	public static void retriever(String indexLocation) {

		// Now search
		BufferedReader br = null;
		try {
			updateQueryFile(queryFile);
			br = new BufferedReader(new FileReader(updatedFile));
			IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(indexLocation)));
			IndexSearcher searcher = new IndexSearcher(reader);
			TopScoreDocCollector collector = null;
			System.out.println("Reading the queryfile..");

			for (String line = br.readLine(); line != null; line = br.readLine()) {
				if (line.trim().isEmpty()) {
					continue;
				}
				String queryid = line.substring(0, line.indexOf('.'));
				line = line.substring(line.indexOf('.') + 1, line.length());
				collector = TopScoreDocCollector.create(100, true);
				Query q = new QueryParser(Version.LUCENE_47, "contents", sAnalyzer).parse(QueryParser.escape(line));
				searcher.search(q, collector);
				ScoreDoc[] hits = collector.topDocs().scoreDocs;

				// 4. save results in a text file
				saveResults(hits, searcher, line, queryid);

			}

			System.out.println(
					"Successfully found documents for the given queries. To check search results, please visit "
							+ resultsFile + " file in Task1_Lucene folder");

			br.close();
		} catch (FileNotFoundException f) {
			System.out.println("File Not found: " + queryFile + " : " + f.getMessage());
			f.printStackTrace();
		} catch (Exception e) {
			System.out.println("Error searching the query" + " : " + e.getMessage());
			e.printStackTrace();
		}

	}

	public static void updateQueryFile(String filename) {
		BufferedReader breader = null;
		BufferedWriter bwriter = null;
		FileWriter fwriter = null;
		FileReader freader = null;
		try {
			freader = new FileReader(filename);
			breader = new BufferedReader(freader);
			fwriter = new FileWriter(updatedFile);
			bwriter = new BufferedWriter(fwriter);

			String line;

			while ((line = breader.readLine()) != null) {
				String lineToWrite = "";
				if (line.contains("<DOCNO>")) {
					String queryid = line.substring(line.indexOf("<DOCNO>") + 7, line.indexOf("</DOCNO>"));
					lineToWrite = "\n" + (queryid.trim() + ". ").trim();
					bwriter.write(lineToWrite);
				} else if (!line.trim().isEmpty() && !line.contains("<DOC>") && !line.contains("</DOC>")) {

					lineToWrite = line + ' ';
					bwriter.write(lineToWrite);
				}

			}
			breader.close();

			bwriter.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	// after adding, we always have to call the closeIndex, otherwise the index is
	// not created

	/**
	 * Indexes a file or directory
	 * 
	 * @param fileName
	 *            the name of a text file or a folder we wish to add to the index
	 * @throws java.io.IOException
	 *             when exception
	 */
	public void indexFileOrDirectory(String fileName) throws IOException {
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		addFiles(new File(fileName));

		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
			FileReader fr = null;
			try {
				Document doc = new Document();

				// add contents of file
				fr = new FileReader(f);
				doc.add(new TextField("contents", fr));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(), Field.Store.YES));

				writer.addDocument(doc);
				System.out.println("Added: " + f);
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				fr.close();
			}
		}

		int newNumDocs = writer.numDocs();
		System.out.println("");
		System.out.println("************************");
		System.out.println((newNumDocs - originalNumDocs) + " documents added.");
		System.out.println("************************");

		queue.clear();
	}

	/**
	 * Reads file from the directory and add it in the queue used by indexer
	 * 
	 * @param file
	 */
	private void addFiles(File file) {

		if (!file.exists()) {
			System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
			for (File f : file.listFiles()) {
				addFiles(f);
			}
		} else {
			queue.add(file);
		}
	}

	/**
	 * Reads top hits of the query as input and stores it as result in a file.
	 * 
	 * @param hits
	 * @param searcher
	 * @param s
	 */
	private static void saveResults(ScoreDoc[] hits, IndexSearcher searcher, String s, String queryid) {
		PrintWriter out = null;
		try {
			FileWriter fw = new FileWriter(resultsFile, true);
			BufferedWriter bw = new BufferedWriter(fw);
			out = new PrintWriter(bw);
			out.println("Query " + queryid.trim() + s);
			for (int i = 0; i < hits.length; ++i) {
				int docId = hits[i].doc;
				Document d = searcher.doc(docId);
				String filename = d.get("filename");
				out.println(queryid.trim() + " Q0 " + filename.substring(0, filename.length() - 5) + " " + hits[i].score
						+ " Lucene");

			}

		} catch (IOException e) {
			System.out.println("File not found. More details are as followed:");
			e.printStackTrace();
		} finally {
			out.close();
		}

	}

	/**
	 * Closes the index.
	 * 
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	public void closeIndex() throws IOException {
		writer.close();
	}
}