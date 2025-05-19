import json
import argparse
from seqeval.metrics import classification_report

def get_user_choice_dataset():
    options = ["Climate Change NER", "BiodivNER"]
    
    print("Please choose one of the following options:")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    
    while True:
        choice = input("Enter the number of your choice: ").strip().lower()
        
        # Check if input is a valid number
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(options):
                choice = options[index]

                if choice == "Climate Change NER":
                    return [choice, "ccner"]
                elif choice == "BiodivNER":
                    return [choice, "biodivner"]
        else:
            print("Invalid choice. Please try again.")

def get_user_choice_model():

    options = ["gpt-4o-2024-05-13", "gpt-4o-mini", "Meta-Llama-3.1-70B-Instruct", "Meta-Llama-3.1-405B-Instruct"]
    print("Please choose one of the following options:")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    
    while True:
        choice = input("Enter the number of your choice: ").strip().lower()
        
        # Check if input is a valid number
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(options):
                choice = options[index]
                return choice
                
        else: 
        
            print("Invalid choice. Please try again.")

def get_user_choice_prompt(dataset):

    if dataset == "ccner":

        options = ["similar 3 shots", "similar 4 shots", "similar 5 shots",
                "random 3 shots", "random 4 shots", "random 5 shots",
                "cluster 1, 4 shots", "cluster 2, 4 shots", "cluster 3, 4 shots", "cluster 4, 4 shots"]
        
    elif dataset == "biodivner":
        options = ["similar 3 shots", "similar 4 shots", "similar 5 shots",
                "random 3 shots", "random 4 shots", "random 5 shots",
                "cluster 1, 4 shots", "cluster 2, 4 shots", "cluster 3, 4 shots"]
        
    print("Please choose one of the following options:")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    
    while True:
        choice = input("Enter the number of your choice: ").strip().lower()
        
        # Check if input is a valid number
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(options):
                choice = options[index]
                
                if choice == "similar 3 shots":
                    return "similarity_3"
                elif choice == "similar 4 shots":
                    return "similarity_4"
                elif choice == "similar 5 shots":
                    return "similarity_5"
                elif choice == "random 3 shots":
                    return "random_3"
                elif choice == "random 4 shots":
                    return "random_4"
                elif choice == "random 5 shots":
                    return "random_5"
                elif choice == "cluster 1, 4 shots":
                    return "combination_1_4"
                elif choice == "cluster 2, 4 shots":
                    return "combination_2_4"
                elif choice == "cluster 3, 4 shots":
                    return "combination_3_4"
                elif choice == "cluster 4, 4 shots":
                    return "combination_4_4"
        
        else: 
        
            print("Invalid choice. Please try again.")


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
    
    dataset = get_user_choice_dataset()
    model = get_user_choice_model()
    prompt = get_user_choice_prompt(dataset[1])

    print(f"Dataset: {dataset[0]}")
    print(f"Model: {model}")
    print(f"Prompt: {prompt}")

    path = f"{dataset[1]}_tokens_{model}/parsed/{prompt}_parsed_output.json"
    main(path)
