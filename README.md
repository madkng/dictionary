# Spanish Dictionary CLI

A command-line interface (CLI) tool that helps non-Spanish speakers learn Spanish words and their meanings.
## Disclaimer
This app is not finished yet. The instructions for usage might not be accurate. 

## Description

This tool provides an easy way to look up Spanish words, their translations, and meanings directly from your terminal. It's designed to assist learners of the Spanish language by providing quick access to word definitions and translations.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/dictionary.git
    cd dictionary
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv dictionary_env
    source dictionary_env/bin/activate  # On Windows: .\dictionary_env\Scripts\activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set an environment variable named "api_key" with your gemini token
    ```bash
    export api_key="your_token"
    ```
## Usage

Basic usage:
```bash
python src/dictionary.py -s <word>
```
```bash
python src/dictionary.py -w
```

Add translation to english using AI:
```bash
python src/dictionary.py -s <word> -t
```
```bash
python src/dictionary.py -w -t
```

### Examples

Look up a Spanish word:
```bash
python src/dictionary.py -s perezoso
```
See the word of the day:
```bash
python src/dictionary.py -w
```
Translate the search result:
```bash
python src/dictionary.py -s perezoso -t
```
```bash
python src/dictionary.py -w -t
```

## Features

- Quick word lookups from the command line
- Spanish to English translations
- Word definitions and meanings
- Easy-to-use interface

## Requirements

- Python 3.12 or higher
- Internet connection for online dictionary access

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
