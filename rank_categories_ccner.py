import os
import pandas as pd 

dataset = "ccner"
models_all = ["gpt-4o-2024-05-13", "gpt-4o-mini", "Meta-Llama-3.1-70B-Instruct", "Meta-Llama-3.1-405B-Instruct"]
models_large = ["gpt-4o-2024-05-13", "Meta-Llama-3.1-405B-Instruct"]
models_small = ["gpt-4o-mini", "Meta-Llama-3.1-70B-Instruct"]
input_output_type = "tokens" # can be strings
error_type = "pure_noise" # can be confusion, new_categories, potential, pure_noise 
prompt_type = "full" # or "combination" for cluster prompts
error_counts_dir = f"error_counts/{dataset}"
output_dir = "error_rankings"
os.makedirs(f"{output_dir}/{dataset}", exist_ok=True)


large_models_results = []
small_models_results = []

for model in models_all:

    model_dir = f"{error_counts_dir}/{model}/"
    for prompt_dir in os.listdir(model_dir): 
        if prompt_dir.startswith("combination"):
            continue 
        else:
            error_counts_path = f"{model_dir}/{prompt_dir}/{input_output_type}_{error_type}.xlsx"            
            df = pd.read_excel(error_counts_path)
            if model in models_small:
                small_models_results.append(df)
            elif model in models_large:
                large_models_results.append(df)


large_combined_dfs = pd.concat(large_models_results, ignore_index=True)
large_combined_counts = large_combined_dfs.groupby(["predicted_entity", "predicted_category"], as_index=False)["predicted_count"].sum()
large_combined_counts["predicted_count_normalized"] = (large_combined_counts["predicted_count"]/12).round(2)
large_combined_counts_sorted = large_combined_counts.sort_values(by="predicted_count_normalized", ascending=False).reset_index(drop=True)
large_combined_counts_sorted.to_excel(f"{output_dir}/{dataset}/{error_type}_full_prompts_large_models_error_counts.xlsx", index=False)

large_category_ranking = large_combined_counts_sorted.groupby("predicted_category", as_index=False)["predicted_count_normalized"].sum()
large_category_ranking["rank"] = large_category_ranking["predicted_count_normalized"].rank(method="dense", ascending=False).astype(int)
large_category_ranking = large_category_ranking.sort_values("rank").reset_index(drop=True)
large_category_ranking.to_excel(f"{output_dir}/{dataset}/{error_type}_full_prompts_large_models_error_category_ranking.xlsx", index=False)

small_combined_dfs = pd.concat(small_models_results, ignore_index=True)
small_combined_counts = small_combined_dfs.groupby(["predicted_entity", "predicted_category"], as_index=False)["predicted_count"].sum()
small_combined_counts["predicted_count_normalized"] = (small_combined_counts["predicted_count"]/12).round(2)
small_combined_counts_sorted = small_combined_counts.sort_values(by="predicted_count_normalized", ascending=False).reset_index(drop=True)
small_combined_counts_sorted.to_excel(f"{output_dir}/{dataset}/{error_type}_full_prompts_small_models_error_counts.xlsx", index=False)

small_category_ranking = small_combined_counts_sorted.groupby("predicted_category", as_index=False)["predicted_count_normalized"].sum()
small_category_ranking["rank"] = small_category_ranking["predicted_count_normalized"].rank(method="dense", ascending=False).astype(int)
small_category_ranking = small_category_ranking.sort_values("rank").reset_index(drop=True)
small_category_ranking.to_excel(f"{output_dir}/{dataset}/{error_type}_full_prompts_small_models_error_category_ranking.xlsx", index=False)