import os
import pandas as pd 
import argparse

'''
MAKE IT INTERACTIVE, WITH PROMPTING FOR MODEL, ERROR TYPE, AND DATASET
PRINT OUT THE NAME AND PATH OF THE RESULT FILES
'''


dataset = "ccner"
input_output_type = "tokens" # can be strings
prompt_type = "full" # or "combination" for cluster prompts

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

def get_user_choice_error_type():

    options = ["Sources of confusion", "Possible candidates", "New categories", "Pure noise", "Missed entities", "Perfect matches"]
    
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
                if choice == "Sources of confusion":
                    return [choice, "confusion"]
                elif choice == "Possible candidates":
                    return [choice, "possible"]
                elif choice == "New categories":
                    return [choice, "new_categories"]
                elif choice == "Pure noise":
                    return [choice, "pure_noise"]
                elif choice == "Missed entities":
                    return [choice, "missed"]
                elif choice == "Perfect matches":
                    return [choice, "perfect"]
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


def main(model, error_type, dataset):

    error_counts_dir = f"error_counts/{dataset}"
    output_dir = "error_rankings"
    os.makedirs(f"{output_dir}/{dataset}", exist_ok=True)


    model_dir = f"{error_counts_dir}/{model}/"

    model_results = []

    for prompt_dir in os.listdir(model_dir): 
        if prompt_dir.startswith("combination"):
            continue 
        else:
            error_counts_path = f"{model_dir}/{prompt_dir}/{input_output_type}_{error_type}.xlsx"
            #print(error_counts_path)            

            df = pd.read_excel(error_counts_path)
            model_results.append(df)    


    if error_type == "missed":
        
        combined_dfs = pd.concat(model_results, ignore_index=True)
        combined_counts = combined_dfs.groupby(["gold_entity", "gold_category"], as_index=False)["gold_count"].sum()
        combined_counts["gold_count_normalized"] = (combined_counts["gold_count"]/12).round(2)
        combined_counts_sorted = combined_counts.sort_values(by="gold_count_normalized", ascending=False).reset_index(drop=True)
        combined_counts_sorted.to_excel(f"{output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_counts.xlsx", index=False)

        category_ranking = combined_counts_sorted.groupby("gold_category", as_index=False)["gold_count_normalized"].sum()
        category_ranking["rank"] = category_ranking["gold_count_normalized"].rank(method="dense", ascending=False).astype(int)
        category_ranking = category_ranking.sort_values("rank").reset_index(drop=True)
        category_ranking.to_excel(f"{output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_category_ranking.xlsx", index=False)

        print(f"Named entities of this error type have been ranked and saved to {output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_counts.xlsx")
        print(f"Ranked categories for this error type have been saved to {output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_category_ranking.xlsx")
        exit()  

    elif error_type == "perfect":

        combined_dfs = pd.concat(model_results, ignore_index=True)
        combined_counts = combined_dfs.groupby(["predicted_entity", "predicted_category"], as_index=False).agg({"predicted_count": "sum", "gold_count": "first"})
        combined_counts["predicted_count_normalized"] = (combined_counts["predicted_count"]/12).round(2)
        combined_counts_sorted = combined_counts.sort_values(by="predicted_count_normalized", ascending=False).reset_index(drop=True)
        combined_counts_sorted.to_excel(f"{output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_counts.xlsx", index=False)
        #large_combined_counts_sorted.to_csv(f"{output_dir}/{dataset}/{error_type}_full_prompts_large_models_error_counts_DEBUG.csv", index=False)

        category_ranking = combined_counts_sorted.groupby("predicted_category", as_index=False)["predicted_count_normalized"].sum()
        category_ranking["rank"] = category_ranking["predicted_count_normalized"].rank(method="dense", ascending=False).astype(int)
        category_ranking = category_ranking.sort_values("rank").reset_index(drop=True)
        category_ranking.to_excel(f"{output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_category_ranking.xlsx", index=False)

        print(f"Named entities of theis error type have been ranked and saved to {output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_counts.xlsx")
        print(f"Ranked categories for this error type have been saved to {output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_category_ranking.xlsx")
        
        exit() 

    else:
        combined_dfs = pd.concat(model_results, ignore_index=True)
        combined_counts = combined_dfs.groupby(["predicted_entity", "predicted_category"], as_index=False)["predicted_count"].sum()
        combined_counts["predicted_count_normalized"] = (combined_counts["predicted_count"]/12).round(2)
        combined_counts_sorted = combined_counts.sort_values(by="predicted_count_normalized", ascending=False).reset_index(drop=True)
        combined_counts_sorted.to_excel(f"{output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_counts.xlsx", index=False)

        category_ranking = combined_counts_sorted.groupby("predicted_category", as_index=False)["predicted_count_normalized"].sum()
        category_ranking["rank"] = category_ranking["predicted_count_normalized"].rank(method="dense", ascending=False).astype(int)
        category_ranking = category_ranking.sort_values("rank").reset_index(drop=True)
        category_ranking.to_excel(f"{output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_category_ranking.xlsx", index=False)

        print(f"Named entities of this error type have been ranked and saved to {output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_counts.xlsx")
        print(f"Ranked categories for this error type have been saved to {output_dir}/{dataset}/{error_type}_full_prompts_{model}_error_category_ranking.xlsx")



if __name__ == "__main__":
    
    model = get_user_choice_model()
    error_type_pretty, error_type = get_user_choice_error_type()
    dataset_pretty, dataset = get_user_choice_dataset()

    print(f"Selected LLM: {model}")
    print(f"Selected error type: {error_type_pretty}")
    print(f"Selected dataset: {dataset_pretty}")
    main(model, error_type, dataset)