# DailyNews

## Table of Contents
* [About](#about)
* [Ollama Setup](#set-up-ollama)
* [Running the Application](#running-the-application)

## About
This application is made to pull news articles from common websites and rate the news articles based on bias, political leaning, categories, etc.

## Getting Started
### Create Conda environment and install packages
```bash
conda create -n DailyNews python=3.14
conda activate DailyNews
pip install -r requirements.txt
```
## Set Up Ollama
This project uses Ollama locally for LLM.
app/services/llmService.py contains the code for the LLM querying.
If api is preferred to LLM, the classify_article method, init method for the class, and app/config/settings.py env variable fetch need to be modified to make a fetch with the api key using the query.

### Ollama Install
Mac/Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
Windows users and those that prefer the installer: [Download Here](https://ollama.com/download)

### Ollama model setup:
To check to VRAM:
```bash
# Windows can also view in Task Manager -> Performance -> GPU
nvidia-smi
```

### Quantization
| Model | Full VRAM | Q4_K_M VRAM |
| :--- | :---: | ---: |
| Llama 3.1 8B | ~16GB | ~5GB |
| Qwen 2.5 14B | ~28GB | ~9GB | 
| Qwen 2.5 32B | ~64GB | ~20GB | 
| Llama 3.3 70B | ~140GB | ~43GB |

### Ollama Usage
To use a model you must first pull it and for it to be reachable by the program, you must make sure it is serving.
The default model is llama 3.1 8B, but can be managed along with the hosting url in the settings.py file.
```bash
# Pull Ollama model
ollama pull <model>:<parameters>

# Examples with K-Quant models
ollama pull llama3.1:8b
ollama pull llama3.1:8b-instruct-q4_K_M

# Run the Ollama model
ollama run <model>:<parameters>

# Serve Ollama model
ollama serve

# Verify (This gives a list of downloaded models)
curl http://localhost:11434/api/tags
```

## Running the Application
The main modules to run are in `app/scraper.py` and `app/main.py`.
The scraper scrapes the given sources (`app/sources/sources.py`), gets a bias rating from allsides.com, and saves the output as a .json file in the same folder. The application runs through all the sources.json values, which should be an RSS or XML, and fetches the most recent articles from the feed. The required environment variables are for the scraper, so make sure to create a .env file with the missing values before running the application. `sample.env` gives more information about what the .env needs and how to get the values.

```bash
# Run the scraper
python -m app.scraper

# Run the app
python -m app.main
```