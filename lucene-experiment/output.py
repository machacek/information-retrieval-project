def output(topic, result, run_id, output_file):
    for rank, (docid, score) in enumerate(result.most_common()):
        print(topic.num, 0, docid, rank, score, run_id, sep='\t', file=output_file)
