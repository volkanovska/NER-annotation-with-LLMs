# Supplementary data and code for a submission to the NLP4Ecology2025 workshop of the NoDaLiDA2025 conference. 
Submission title: "Large Language Models as Annotators of Named Entities in Climate Change and Biodiversity: A Preliminary Study". 

This repository contains the complete set of prompts tested in the experiments and the results obtained from each large language model (LLM).

Four LLMs are tested: two proprietary - gpt-4o-mini and gpt-4o-2024-05-13, developed and owned by OpenAI, and two open-source: Meta-Llama-3.1-70B-Instruct (hereinafter: Llama-70B) and Meta-Llama-3.1-405B-Instruct (hereinafter: Llama-405B), both developed and owned by Meta and made available both through Hugging Face and API providers.  

For prompts from the dataset Climate-Change-NER, the system message is: "You are a helpful climate change expert, specialized in annotating named entities in texts on climate change."

For prompts from the dataset BiodivNER, the system message is: "You are a helpful biodiversity expert, specialized in annotating named entities in texts on biodiversity."

# Generating classification reports

Classification reports for each type of prompt can be recreated by running the script "generate_evaluation_report_tokens.py" for promts with token-based input, or the script "generate_evaluation_report_strings.py" for prompts with string-based input. 

For example, to obtain the results for the dataset BiodivNER, model gpt-4o-mini, and a prompt type containing similar 5 task examples (TEs), open a terminal and run:

```python
python3 generate_evaluation_report_tokens.py biodivner_gpt-4o-mini/parsed/similarity_5_parsed_output.json 
```

These files contain only valid model output i.e. output that can be processed as a Python list.

The script can be run from terminal with the command: python3 generate_evaluation_report.py corpus_name/model_name/json file with prompts (example: biodivner_bio/gpt-4o-2024-05-13/prompts_combination_1_4_valid_output.json)

# Inspecting raw output

The raw output per dataset and per model, is saved in json files under the directories "ccner_raw_output" and "biodivner_raw_output".
Each file is a list of dictionaries storing the prompt and the respective response. 

Structure of directory:

-biodivner_raw_output OR ccner_raw_output
    -gpt-4o-224-05-13
        - prompt + raw model output, saved as json files per prompt
    -gpt-4o-mini
        - prompt + raw model output, saved as json files per prompt
    - mistralV03
        - prompt + raw model output, saved as json files per prompt

# Citing the data holders

Climate-Change-NER (https://huggingface.co/datasets/ibm/Climate-Change-NER):

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

BiodivNER (https://zenodo.org/records/6458503):

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
