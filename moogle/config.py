# Std library imports
import argparse
import sys

# Custom imports
from preprocessing.casing import caser_factory 
from preprocessing.termclassing import termclassifier_factory
from preprocessing.stopwords import stopwords_factory

def parse_args():
    
    parser = argparse.ArgumentParser(
            description="Creates index from given list of documents and performs documents retrieval for given list of topics",
            epilog="Author: Matous Machacek <machacekmatous@gmail.com>")

    #
    # Obligatory options
    #
    parser.add_argument("-q",
            help="a file with a list of topic filenames",
            required=True,
            type=argparse.FileType('r'),
            dest="topics_list") 
    
    parser.add_argument("-d",
            help="a file with a list of document filenames",
            required=True,
            type=argparse.FileType('r'),
            dest="documents_list")

    parser.add_argument("-p", "--pathprefix",
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
            type=argparse.FileType('r'),
            dest="documents_list")

    #
    # Custom options
    #
    parser.add_argument("-c", "--lowercase",
            help="lowercasing",
            default="no",
            type=caser_factory,
            dest="case",
            choices=caser_factory.choices())

    parser.add_argument("-t", "--termclasses",
            help="turning text into bag of words/terms (forms, stems, lemmas, classes)",
            default="wordforms",
            type=termclassifier_factory,
            dest="classifier",
            choices=termclassifier_factory.choices())

    parser.add_argument("-s","--stopwords",
            help="removing stopwords",
            default="none",
            type=stopwords_factory,
            dest="stopwords")

    return parser.parse_args()

config = parse_args()
