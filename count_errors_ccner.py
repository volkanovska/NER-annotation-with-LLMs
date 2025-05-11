'''
get a count of error types per prompt for Climate Change NER
for each language model
returns: Excel files with error counts
'''


import json
import pandas as pd
import os 

def open_json(path):

    with open(path, "r", encoding="utf-8") as f:
        json_file = json.load(f)
    
    return json_file

def save_df(path, lookup_list, columns):

    df = pd.DataFrame(lookup_list, columns=columns)
    df.to_excel(path, index=False)  

# for combination prompts, we need to filter gold standard sentences  

def get_valid_categories(combination_type=None):

    class_combos_ccner = {
    "combination_1": ["CLIMATE-HAZARDS", "CLIMATE-PROBLEM-ORIGINS", "CLIMATE-GREENHOUSE-GASES",],
    "combination_2": ["CLIMATE-IMPACTS", "CLIMATE-ASSETS", "CLIMATE-NATURE", "CLIMATE-ORGANISMS",],
    "combination_3": ["CLIMATE-DATASETS", "CLIMATE-MODELS", "CLIMATE-OBSERVATIONS", "CLIMATE-PROPERTIES",],
    "combination_4": ["CLIMATE-MITIGATIONS", "CLIMATE-ORGANIZATIONS",],
}
    
    if combination_type:
        return class_combos_ccner[combination_type]

    else:
        all_categories = []
        for k, v in class_combos_ccner.items():
            all_categories.extend(v)

        return all_categories
    

dataset = "ccner"
input_output_type = "tokens" # if interested in string-based tokens, change this to strings
models = ["gpt-4o-2024-05-13", "gpt-4o-mini", "Meta-Llama-3.1-70B-Instruct", "Meta-Llama-3.1-405B-Instruct"]
filetype = "parsed"

for model in models:
    files_dir = f"{dataset}_{input_output_type}_{model}/{filetype}"
    for file in os.listdir(files_dir):
        
        if file.endswith(".json"):

            result = open_json(f"{dataset}_{input_output_type}_{model}/{filetype}/{file}")
            prompt_type = file[:-5]

            gold_lookup_dict = {}
            predicted_lookup_dict = {}

            if file[:13] in ["combination_1", "combination_2", "combination_3", "combination_4"]:
                valid_categories = get_valid_categories(file[:13])
            else:
                valid_categories = get_valid_categories()

            for item in result:
                if item["gold_spans"]:

                    for entity, category, _, _ in item["gold_spans"]:
                        if category in valid_categories:
                            if (entity, category) not in gold_lookup_dict.keys():
                                gold_lookup_dict.update({(entity, category): 1})
                            else:
                                gold_lookup_dict[(entity, category)] += 1

                if item["predicted_spans"]:

                    for entity, category, _, _ in item["predicted_spans"]:
                        try:
                            if (entity, category) not in predicted_lookup_dict.keys():
                                predicted_lookup_dict.update({(entity, category): 1})
                            else:
                                predicted_lookup_dict[(entity, category)] += 1
                        except Exception as e:

                            if isinstance(item["predicted_spans"], list) and len(item)==1 and isinstance(item["predicted_spans"][0], list):
                                if all(isinstance(subitem, list) for subitem in item["predicted_spans"][0]):
                                    flattened_output = item["predicted_spans"][0]

                                    for entity, category, _, _ in flattened_output:
                                        if (entity, category) not in predicted_lookup_dict.keys():
                                            predicted_lookup_dict.update({(entity, category): 1})
                                        else:
                                            predicted_lookup_dict[(entity, category)] += 1

            gold_entities = [k[0] for k in gold_lookup_dict.keys()]
            gold_categories = [k[1] for k in gold_lookup_dict.keys()]

            perfect = []
            perfect_nocounts = []
            missed = []
            confusion = []
            potential = []
            new_categories = []
            pure_noise = []


            for entity_category, count in predicted_lookup_dict.items():

                entity = entity_category[0]
                category = entity_category[1]

                if entity_category in gold_lookup_dict.keys():
                    perfect.append([entity, category, predicted_lookup_dict[entity_category], gold_lookup_dict[entity_category]])
                    perfect_nocounts.append(entity_category)

                elif entity in gold_entities and category in gold_categories:
                    confusion.append([entity, category, predicted_lookup_dict[entity_category]])
                
                elif entity not in gold_entities and category in gold_categories:
                    potential.append([entity, category, predicted_lookup_dict[entity_category]])

                elif entity in gold_entities and category not in gold_categories:
                    new_categories.append([entity, category, predicted_lookup_dict[entity_category]])

                elif entity not in gold_entities and category not in gold_categories:
                    pure_noise.append([entity, category, predicted_lookup_dict[entity_category]])


            for entity_category in gold_lookup_dict.keys():
                if entity_category not in perfect_nocounts:
                    missed.append([entity_category[0], entity_category[1], gold_lookup_dict[entity_category]])    

            output_dir = f"error_counts/{dataset}/{model}/{prompt_type}"
            os.makedirs(output_dir, exist_ok=True)

            df_perfect = pd.DataFrame(perfect, columns=["predicted_entity", "predicted_category", "predicted_count", "gold_count"])
            df_perfect.to_excel(f"{output_dir}/{input_output_type}_perfect.xlsx", index=False)

            df_missed = pd.DataFrame(missed, columns = ["gold_entity", "gold_category", "gold_count"])
            df_missed.to_excel(f"{output_dir}/{input_output_type}_missed.xlsx", index=False)

            df_confusion = pd.DataFrame(confusion, columns = ["predicted_entity", "predicted_category", "predicted_count"])
            df_confusion.to_excel(f"{output_dir}/{input_output_type}_confusion.xlsx", index=False)

            df_potential = pd.DataFrame(potential, columns=["predicted_entity", "predicted_category", "predicted_count"])
            df_potential.to_excel(f"{output_dir}/{input_output_type}_potential.xlsx", index=False) 
            
            df_new_categories = pd.DataFrame(new_categories, columns=["predicted_entity", "predicted_category", "predicted_count"])
            df_new_categories.to_excel(f"{output_dir}/{input_output_type}_new_categories.xlsx", index=False)

            df_pure_noise = pd.DataFrame(pure_noise, columns=["predicted_entity", "predicted_category", "predicted_count"])
            df_pure_noise.to_excel(f"{output_dir}/{input_output_type}_pure_noise.xlsx", index=False)