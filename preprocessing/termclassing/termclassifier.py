from document import DocumentTokens
from topic import TopicTokens

class TermClassifier(object):

    def convert_document_collection(self, collection):
        return (DocumentTokens(document, self) for document in collection)

    def convert_topic_collection(self, collection):
        return (TopicTokens(topic, self) for topic in collection)

    def convert_vert_list(self, list):
        return [ self.convert_vert_item(item) for item in list ]

class WordFormClassifier(TermClassifier):
    def convert_vert_item(self, vert_item):
        return vert_item.form

class LemmaClassifier(TermClassifier):
    def convert_vert_item(self, vert_item):
        return vert_item.lemma
