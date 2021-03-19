from scg.candidate_generator import candidate_dui_generator, batcher
from tqdm import tqdm

if __name__ == '__main__':
    mentions = list()
    with open('./data/bc5cdr_mentions.txt', 'r') as f:
        for line in f:
            mention = line.strip()
            mentions.append(mention)
    entire_candidates = list()
    for batch in tqdm(batcher(mentions, 64)):
        batch_candidates = candidate_dui_generator(batch)
        entire_candidates += batch_candidates