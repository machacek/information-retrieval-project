# Std library imports
import argparse
import sys

# Custom imports
from preprocessing import termclassifier_factory, stopwords_factory 
#from query import query_factory

def parse_args(args=None):
    
    parser = argparse.ArgumentParser(
            description="""
create_index creates Lucene index from given list of documents
search_index performs retrieval for given index and list of topics""",
            epilog="Author: Matous Machacek <machacekmatous@gmail.com>")

    #
    # Obligatory options
    #
    parser.add_argument("-l",
            help="a file with a list of documents/topics",
            required=True,
            type=argparse.FileType('r'),
            dest="file_list")
    
    parser.add_argument("-i",
            help="an index location",
            default="index",
            dest="index") 

    parser.add_argument("-p",
            help="path to which filenames are relative to",
            dest="prefix",
            default="")

    parser.add_argument("-r",
            help="a label identifying particular experiment run",
            default="no_id",
            dest="run_id")

    parser.add_argument("-o",
            help="an output file",
            default=sys.stdout,
            type=argparse.FileType('w'),
            dest="output_file")

    #
    # Custom options
    #
    parser.add_argument("-c", "--lowercase",
            help="lowercasing",
            action="store_true",
            dest="lowercase")

    parser.add_argument("-t", "--termclasses",
            help="turning text into bag of words/terms",
            default="forms",
            #type=termclassifier_factory,
            dest="classes",
            metavar=termclassifier_factory.metavar())


#    parser.add_argument("-s","--stopwords",
#            help="removing stopwords",
#            default="none",
#            type=stopwords_factory,
#            dest="stopwords",
#            metavar=stopwords_factory.metavar())
#
#    parser.add_argument("-Q", "--query",
#            help="query construction",
#            default="title",
#            type=query_factory,
#            dest="query",
#            metavar=stopwords_factory.metavar())

    parser.add_argument("-n","--workers",
            help="number of paralell subprocesses (default 10)",
            default="10",
            type=int,
            dest="workers",
            metavar="N")

    return parser.parse_args()

config = parse_args()
