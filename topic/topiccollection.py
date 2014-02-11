from .topic import TopicVert

class TopicCollection(object):
    def __init__(self, prefix, topic_list_file):
        self.prefix = prefix
        self.topic_names_list = [file_name.strip() for file_name in topic_list_file]

    def __iter__(self):
        for file_name in self.topic_names_list:
            yield TopicVert(self.prefix, file_name)

