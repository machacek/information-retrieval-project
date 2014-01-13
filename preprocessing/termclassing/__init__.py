from utils import Factory

from .wordformclassifier import WordFormClassifier

termclassifier_factory = Factory({
    'wordforms' : WordFormClassifier,
    })
