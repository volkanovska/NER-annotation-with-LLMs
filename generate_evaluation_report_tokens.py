import json
import argparse
from seqeval.metrics import classification_report


def load_file(path_to_bio_file):

    try:

        with open(path_to_bio_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    
        return data 
    
    except Exception as e:
        print("Error: problem opening the file.")



def extract_labels(data):

    gold = [sent["gold_token_labels"] for sent in data]
    predicted = [sent["predicted_token_labels"] for sent in data]


    gold_labels = []

    for sent in gold:
        labels = [label for token, label in sent]
        gold_labels.append(labels)

    predicted_labels = []

    for sent in predicted:
        labels = [label for token, label in sent]
        predicted_labels.append(labels)

    return gold_labels, predicted_labels 

def main(path_to_bio_file):
    data = load_file(path_to_bio_file)
    gold_labels, predicted_labels = extract_labels(data)

    report = classification_report(gold_labels, predicted_labels, digits=4)

    print(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate classification report from BIO data")
    parser.add_argument("path", type=str, help="Path to the BIO JSON file")
    
    args = parser.parse_args()

    main(args.path)