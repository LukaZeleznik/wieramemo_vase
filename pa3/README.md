# Wieramemo_vase
## Webpage Indexing

### Description
This is a simple program that can index webpages into a SQLite database, or can run a sequential search for a certain query.

### Instructions
Firstly, move to the /implementation-indexing directory and check if all the packages are installed on your sistem.

List of all the packages used:\
sqlite3\
bs4\
nltk\
re\
string\
os\
codecs\
time\

To run the program, run:

`python create-database-py` to initialize the database\
`python indexing.py` to index the files in the /webpages-data directory\
`python run-sqlite-search.py {QUERY}` to use sqlite implementation\
`python run-basic-search.py {QUERY}` to use sequential implementation

All the data will be outputted to the standard output.
