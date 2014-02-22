# Std library imports
import argparse
import sys

# Custom imports
from preprocessing import caser_factory, termclassifier_factory, stopwords_factory 
from documentweighting import document_weighting_pattern, document_weighting_factory

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
            type=argparse.FileType('w'),
            dest="output_file")

    #
    # Custom options
    #
    parser.add_argument("-c", "--lowercase",
            help="lowercasing",
            default="no",
            type=caser_factory,
            dest="case",
            metavar=caser_factory.metavar())

    parser.add_argument("-t", "--termclasses",
            help="turning text into bag of words/terms",
            default="forms",
            type=termclassifier_factory,
            dest="classifier",
            metavar=termclassifier_factory.metavar())


    parser.add_argument("-s","--stopwords",
            help="removing stopwords",
            default="none",
            type=stopwords_factory,
            dest="stopwords",
            metavar=stopwords_factory.metavar())

    parser.add_argument("-w", "--weighting",
            help="document weighting scheme given in the following pattern: " + document_weighting_pattern,
            default="lnc",
            type=document_weighting_factory,
            dest="weighting",
            metavar="ddd")
    
    parser.add_argument("-z","--zones",
            help="zones and their weights",
            default="title:1,heading:1,text:1",
            type=zone_weight_factory,
            dest="zones",
            metavar="zone1:weight1[,zone2:weight2[...]")
    
    parser.add_argument("-n","--subprocess",
            help="number of paralell subprocesses (default 30)",
            default="30",
            type=int,
            dest="workers",
            metavar="N")
    
    return parser.parse_args()

def zone_weight_factory(str_weights):
    zones = []
    for str_zone_weight in str_weights.split(','):
        zone, str_weight = str_zone_weight.split(':',2)
        weight = int(str_weight)
        zones.append((zone,weight))
    return zones


config = parse_args()
