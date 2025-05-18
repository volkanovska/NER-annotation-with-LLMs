import os
import pandas as pd 
import argparse

'''
MAKE IT INTERACTIVE, WITH PROMPTING FOR MODEL, ERROR TYPE, AND DATASET
PRINT OUT THE NAME AND PATH OF THE RESULT FILES
'''


dataset = "ccner"
#models_all = ["gpt-4o-2024-05-13", "gpt-4o-mini", "Meta-Llama-3.1-70B-Instruct", "Meta-Llama-3.1-405B-Instruct"]
#model = "gpt-4o-2024-05-13"
input_output_type = "tokens" # can be strings
#error_type = "perfect" # can be confusion, new_categories, possible, pure_noise, missed, perfect  
prompt_type = "full" # or "combination" for cluster prompts
#error_counts_dir = f"error_counts/{dataset}"
#output_dir = "error_rankings"
#os.makedirs(f"{output_dir}/{dataset}", exist_ok=True)


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



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose a model and an error type to rank categories and named entities.")
    
    models = ["gpt-4o-2024-05-13", "gpt-4o-mini", "Meta-Llama-3.1-70B-Instruct", "Meta-Llama-3.1-405B-Instruct"]
    error_types = ["confusion", "new_categories", "possible", "pure_noise", "missed", "perfect"]

    parser.add_argument("model", 
                        type=str,
                        choices=models,
                        #required=True, 
                        help="Choose a model.")
    
    parser.add_argument("error_type",
                        type=str,
                        choices=error_types,
                        #required=True, 
                        help="Choose an error type.")
    
    parser.add_argument("dataset",
                        type=str,
                        choices=["ccner", "biodivner"],
                        help="Choose a dataset.")
    
    args = parser.parse_args()
    
    main(args.model, args.error_type, args.dataset)