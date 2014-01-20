from .document import Document

class DocumentCollection(object):
    def __init__(self, prefix, document_list_file):
        self.prefix = prefix
        self.document_names_list = [file_name.strip() for file_name in document_list_file]

    def __iter__(self):
        for file_name in self.document_names_list:
            yield Document(self.prefix, file_name)

