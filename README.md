# Supplementary data and code  
### This repository contains supplementari data and code for two papers:
(1) "Large Language Models as Annotators of Named Entities in Climate Change and Biodiversity: A Preliminary Study", presented at the workshop NLP4Ecology in Tallinn, Estonia, and available at: https://aclanthology.org/2025.nlp4ecology-1.7/.
(2) "A Study of Errors in the Output of Large Language Models for Domain-Specific Few-Shot Named Entity Recognition", which was presented at the workshop "LLM Fails: Failed Experiments with Generative AI and what we can learn from them", organised by IDS Mannheim in April, 2025. 

Paper **(1)** explains the **methodology** underpinning the experiments, while paper **(2)** proposes a systematic **error taxonomy** that supplements existing error analyses for few-shot NER in a way that addresses challenges specific to using LLMs for domain-specific NER.

The LLMs used in these experiments include:

- gpt-4o-mini (OpenAI, proprietary);
- gpt-4o-2024-05-13 (OpenAI, proprietary);
- Meta-Llama-3.1-70B-Instruct (Meta, open-source);
- Meta-Llama-3.1-405B-Instruct (Meta, open-source).

## Datasets

Two NER datasets containing scientific texts are used in the experiments: **BiodivNER** with 6 domain-specific NE categories (ORGANISM, PHENOMENA, MATTER, ENVIRONMENT, QUALITY, LOCATION) and **Climate-Change-NER** with 13 domain-specific NE categories (CLIMATE-HAZARDS, CLIMATE-MITIGATIONS, CLIMATE-PROPERTIES, CLIMATE-NATURE, CLIMATE-MODELS, CLIMATE-PROBLEM-ORIGINS, CLIMATE-OBSERVATIONS, CLIMATE-ASSETS, CLIMATE-IMPACTS, CLIMATE-GREENHOUSE-GASES, CLIMATE-ORGANIZATIONS, CLIMATE-ORGANISMS, CLIMATE-DATASETS). 

In this repository, the PDF files **biodivner_dataset_info** and **ccner_dataset_info** contain comprehensive statistical information about each dataset.

See **Dataset holders** at the end of this README file for links to the datasets. 

**Climate-Change-NER**

## Methodology

A detailed description of the methodology is provided in paper (1).  

For prompts from the dataset **Climate-Change-NER**, the system message is: *You are a helpful climate change expert, specialized in annotating named entities in texts on climate change.*

For prompts from the dataset **BiodivNER**, the system message is: *You are a helpful biodiversity expert, specialized in annotating named entities in texts on biodiversity.*

 
### Terms and explanations

**output_files**: Files in json formats containing the prompt and the model output.

**output directories**: Directories where the model output is saved.

**biodivner**: BiodivNER

**ccner**: Climate-Change-NER

**string-based**: refers to prompts where an LLM is expected to extract NERs from a sentence - a Python string. Example in file **Prompt_example_string_ccner_nodalida**.

**token-based**: refers to prompts where an LLM is expected to extract NERs from a Python list containing as nested list a token index and a word-based token. (Example: [[0, "The"], [2, "quick"], [3, "brown"], [4, "fox"], [5, "jumps"], [6, "over"], [7, "the"], [8, "lazy"], [9, "dog"]]). Example in file **Prompt_example_tokens_biodivner_nodalida.pdf**.

**parsed**: refers to output directories / JSON files containing post-processed model output. See section **Structure of output files** for information about the JSON files.

**raw**: refers to output directories / JSON files containing the raw model output i.e. output that has not been post-processed. See section **Structure of output files** for information about the JSON files. 

**full prompts**: refers to prompts where the LLM should extract NEs from all NE categories.

**combination** or **cluster prompts**: refers to prompts where the LLM should recognise entities from 2 to 4 NE categories only.

**task example(s)** or **TE(s)**: question-answer pairs that the model is given as an example of what task it is expected to process.


### Saving LLM output

The output of each LLM and prompt type is stored in dedicated directories. The naming convention for each directory is: name of dataset + _ + input/output format + _ + name of model. For example, for the dataset Climate-Change-NER (ccner), token-based prompt and output format, and gpt-4o-mini model, the name of the dedicated folder is: ccner_tokens_gpt-4o-mini. 

There are *two* subdirectories within each dedicated directory, which contain the models' results in two different forms: **parsed**, where the generated text from the model has been postprocessed in a format allowing the calculation of F1 score, and **raw**, which contain the original output from each model. 

The subdirectories contain the following json files:

- **combination prompts**: combination + _ + number of combination* + _ + number of task examples (always 4) + parsed_output OR raw_output. For example, for NE cluster 3, the file containing the prompt and the parsed output of the LLM's answer is: combination_3_4_parsed_output.json.
- **random** or **similar**: **random** refers to prompts with randomly selected prompt examples, while **similar** refers to prompts where the example sentences are semantically similar to the task sentence. The file naming convention is: random OR similar + _ + number of task examples (3, 4 or 5) + parsed_output OR raw_output. For example, the file containing a prompt with 3 similar task examples and the parsed output of the LLM's answer is: similarity_3_parsed_output.json.

**Example structure of dedicated directory**

```bash
├── ccner_tokens_gpt-4o-mini
│   ├── parsed
│   │   ├── combination_1_4_parsed_output.json    # corresponds to NE class cluster 1
│   │   ├── combination_2_4_parsed_output.json    # corresponds to NE class cluster 2
│   │   ├── combination_3_4_parsed_output.json    # corresponds to NE class cluster 3
│   │   ├── combination_4_4_parsed_output.json    # corresponds to NE class cluster 4
│   │   ├── random_3_parsed_output.json           # a prompt with random k examples, where k == 3
│   │   ├── random_4_parsed_output.json           # a prompt with random k examples, where k == 4
│   │   ├── random_5_parsed_output.json           # a prompt with random k examples, where k == 5
│   │   ├── similarity_3_parsed_output.json       # a prompt with similar k examples, where k == 3
│   │   ├── similarity_4_parsed_output.json       # a prompt with similar k examples, where k == 4
│   │   ├── similarity_4_parsed_output.json       # a prompt with similar k examples, where k == 5
│   ├── raw
│       ├── combination_1_4_raw_output.json       # corresponds to NE class cluster 1
│       ├── combination_2_4_raw_output.json       # corresponds to NE class cluster 2
│       ├── combination_3_4_raw_output.json       # corresponds to NE class cluster 3
│       ├── combination_4_4_raw_output.json       # corresponds to NE class cluster 4
│       ├── random_3_raw_output.json              # a prompt with random k examples, where k == 3
│       ├── random_4_raw_output.json              # a prompt with random k examples, where k == 4
│       ├── random_5_raw_output.json              # a prompt with random k examples, where k == 5
│       ├── similarity_3_raw_output.json          # a prompt with similar k examples, where k == 3
│       ├── similarity_4_raw_output.json          # a prompt with similar k examples, where k == 4
│       ├── similarity_5_raw_output.json          # a prompt with similar k examples, where k == 5

```

### Structure of output files

JSON files designated as **parsed** store a list of dictionaries with identical structure, which is:

```python3
[
    {"gold_sent_str": # Gold sentence presented as a string,
     "gold_spans": [[NE instance 1, NE class, start token index, end token index], [NE instance 2, NE class, start token index, end token index] ...],
     "gold_token_labels": [[token_1, IOB-tag], [token_2, IOB-tag], [token_3, IOB-tag] ...],
     "predicted_spans": [[NE instance 1, NE class, start token index, end token index], [NE instance 2, NE class, start token index, end token index] ...],
     "predicted_token_labels": [[token_1, IOB-tag], [token_2, IOB-tag], [token_3, IOB-tag] ...],   
    },
    {
    ...
    }
]
```
JSON files designated as **raw** store a list of dictionaries with identical structure, which is:

```python3
[
    {"prompt": # Prompt sent to the LLM,
     "raw_output": # The text generated by the LLM before post-processing
    },
    {
    ...
    }
]
```

### Prompt examples

The files *Prompt_example_string_ccner_nodalida.pdf* and *Prompt_example_tokens_biodivner_nodalida.pdf* are examples of string-based and token-based prompts respectively. These files are provided for clearer overview of the prompt structure, the blueprint of which is given in Figure 1 of the paper.

### Generating evaluation reports for F scores

Evaluation reports for each type of prompt can be recreated by running the script *generate_evaluation_report_tokens.py* for promts with token-based input, or the script *generate_evaluation_report_strings.py* for prompts with string-based input. 

For example, to obtain the results for the dataset **BiodivNER**, model **gpt-4o-mini**, and a prompt type containing **similar 5 task examples** (TEs), open a terminal and run:

```python3
python3 generate_evaluation_report_tokens.py biodivner_gpt-4o-mini/parsed/similarity_5_parsed_output.json 
```

## Error taxonomy

A detailed description of the error taxonomy is provided in paper (2). 

The error classes are: missed entities, sources of confusion, possible candidates, new categories, and pure noise.

Two directories contain error-relevant information: *error_counts* and *error_rankings*.

### Error counts

Error counts contain the number of times instances of an error class have been encountered in an LLM's output. It serves as the basis for error rankings.

Error counts are available for each individual model.

In addition to *missed entities* and *perfect matches*, errors of the classes *sources of confusion*, *possible candidates*, *new categories*, and *pure noise* can be obtained by running the scripts count_errors_ccner.py and count_errors_biodivner.py for each dataset respectively. At the moment, the script counts errors in full prompts.

The script counts errors detected in the output of token-based prompts. 

[ADD GUIDELINES FOR COMBINATION PROMPTS]

### Error rankings

The rankings are done by *combining* and *normalizing* the raw counts for full prompts. This is 6 prompts per model (prompts with 3, 4, and 5 *random* examples and prompts with 3, 4, and 5 *similar* examples). 

In paper (2) the rankings are calculated by combining the models' output as follows:

- Large: gpt-4o-2024-05-13 and Meta-Llama-3.1-405B-Instruct;
- Small: gpt-4o-mini and Meta-Llama-3.1-70B-Instruct.

These results can be obtained by running the scripts rank_categories_biodivner.py and rank_categories_ccner.py from the terminal. The output is saved in the directory *error_rankings*.  
From the terminal, run:
python3 rank_categories_biodivner.py small OR python3 rank_categories_biodivner.py large 

This repository also offers a script to run error count on individual models. The results are saved in the same directory (*error rankings*).
To do this, run:
python3 rank_categories_individual_models.py gpt-4o-mini missed biodivner, where:

- the first argument is the name of the model (gpt-4o-mini, gpt-4o-2024-05-13, Meta-Llama-3.1-70B-Instruct, Meta-Llama-3.1-405B-Instruct).
- the second argument is the name of the error ("confusion", "new_categories", "possible", "pure_noise", "missed", "perfect").
- the third argument is the name of the dataset (biodivner, ccner),
  

#### Explanation of counts and ranking calculation (toy example)

Let's imagine that gpt-4o-mini and Llama-70B wrongly annotate *climate change* as CLIMATE-PROBLEM-ORIGIN as follows:

| Type of TE | Number of TEs | gpt-4o-mini error count | Llama-70B error count |
|------------|----------------|--------------------------|------------------------|
| random     | 3              | 6                        | 2                      |
| random     | 4              | 7                        | 6                      |
| random     | 5              | 3                        | 3                      |
| similar    | 3              | 4                        | 2                      |
| similar    | 4              | 6                        | 6                      |
| similar    | 6              | 8                        | 3                      |
|            |                | **34**                   | **22**                 |

The normalized error count for the ENTITY *climate change* is (34 + 22) / 12 = 4.67.

**Ranking**

The models annotated 2 more named entities in the same category, with normalized error counts of 3.23 and 1.56.
The error count for the category CLIMATE-PROBLEM-ORIGIN will then be: 4.67 + 3.23 + 1.56 = 9,46.

This directory contains Excel sheets with error rankings on two levels:

(1) By NE category, where entity categories are ranked by their frequency in a certain error type, and
(2) By entity. 

NE categories that appear most frequently in the error counts can be seen in the directory *error_rankings*. 
In paper (2), rankings are grouped by model size; this repository also contains rankings for individual models.


# Dataset holders

**Climate-Change-NER**

Link to dataset: https://huggingface.co/datasets/ibm/Climate-Change-NER

```bibtex
@misc{bhattacharjee2024indus,
  title={INDUS: Effective and Efficient Language Models for Scientific Applications}, 
  author={Bishwaranjan Bhattacharjee and Aashka Trivedi and Masayasu Muraoka and Muthukumaran Ramasubramanian and Takuma Udagawa and Iksha Gurung and Rong Zhang and Bharath Dandala and Rahul Ramachandran and Manil Maskey and Kayleen Bugbee and Mike Little and Elizabeth Fancher and Lauren Sanders and Sylvain Costes and Sergi Blanco-Cuaresma and Kelly Lockhart and Thomas Allen and Felix Grazes and Megan Ansdel and Alberto Accomazzi and Yousef El-Kurdi and Davis Wertheimer and Birgit Pfitzmann and Cesar Berrospi Ramis and Michele Dolfi and Rafael Teixeira de Lima and Panos Vagenas and S. Karthik Mukkavilli and Peter Staar and Sanaz Vahidinia and Ryan McGranaghan and Armin Mehrabian and Tsendgar Lee},
  year={2024},
  eprint={2405.10725},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2405.10725}
}
```

**BiodivNER** 

Link to dataset: https://zenodo.org/records/6458503

```bibtex
@dataset{nora_abdelmageed_2022_6575865,
  author       = {Nora Abdelmageed and
                  Felicitas Löffler and
                  Leila Feddoul and
                  Alsayed Algergawy and
                  Sheeba Samuel and
                  Jitendra Gaikwad and
                  Anahita Kazem and
                  Birgitta König-Ries},
  title        = {{BiodivNERE: Gold Standard Corpora for Named Entity 
                   Recognition and Relation Extraction in
                   Biodiversity Domain}},
  month        = apr,
  year         = 2022,
  note         = {Added BiodivRE Multi-class corpus},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.6575865},
  url          = {https://doi.org/10.5281/zenodo.6575865}
}
```
