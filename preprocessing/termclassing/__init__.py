from utils import Factory

from .termclassifier import WordFormClassifier
from .termclassifier import LemmasClassifier

termclassifier_factory = Factory({
    'wordforms' : WordFormClassifier,
    'lemmas'    : LemmasClassifier,
    })
