from config import config

def output(result)
    for rank, (docid, score) in enumerate(result.most_common()):
        print(topic.num, 0, docid, rank, score, config.run_id, sep='\t', file=config.output_file)
