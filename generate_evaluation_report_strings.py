import json
import argparse
from seqeval.metrics import classification_report
from collections import Counter

path = "/home/elena/nlp_social_good/github_paper_december/biodivner/strings/gpt-4o-mini/similarity_3_parsed_output.json"

def load_file(path_to_file):

    try:

        with open(path_to_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    
        return data 
    
    except Exception as e:
        print("Error: problem opening the file.")

def create_entity_counter(entities_list):
    entity_counter = Counter()
    for entity in entities_list:
        key = (entity[0], entity[1])
        entity_counter[key] += 1
    return entity_counter

def extract_information(data):

    true_positives = 0
    total_predicted = 0
    total_gold = 0

    for sent in data:

        gold = sent["gold_spans"]
        predicted = sent["predicted_spans"]

        gold_counter = create_entity_counter(gold)
        predicted_counter = create_entity_counter(predicted)

        exact_matches_counter = gold_counter & predicted_counter 

        true_positives += sum(exact_matches_counter.values())
        total_gold += sum(gold_counter.values())
        total_predicted += sum(predicted_counter.values())

        
    return true_positives, total_predicted, total_gold


def main(path_to_bio_file):
    
    data = load_file(path_to_bio_file)
    true_positives, total_predicted, total_gold = extract_information(data)

    print(f"True positives are: {true_positives}.")
    print(f"Total predicted are: {total_predicted}.")
    print(f"Total gold are: {total_gold}.")


    precision = true_positives / total_predicted if total_predicted > 0 else 0
    recall = true_positives / total_gold if total_gold > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print(f"F score is {round(f1_score, 2)}.")
    print(f"Recall is {round(recall, 2)}.")
    print(f"Precision is {round(precision, 2)}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate classification report from BIO data")
    parser.add_argument("path", type=str, help="Path to the string-type JSON file.")
    
    args = parser.parse_args()

    main(args.path)

