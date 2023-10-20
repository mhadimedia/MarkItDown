# MarkItDown

Convert your text into beautifully formatted Markdown, HTML, or Plain Text using the power of AI.

## Features
- Convert plain text into three formats: Markdown, HTML, and Plain Text.
- View the processed text in both raw and rendered forms.
- Copy or Download the converted text as `.md`, `.html`, or `.txt` file.
- Configurable to use different versions of GPT models from OpenAI (higher models = higher accuracy)

## Cool Features to Add in the Future
[ ] Better UI
[ ] Option to Select Multiple Output Formats
[ ] Ability to Upload Text Files and PDFs
[ ] Ability to Upload Images and Use OCR for Text Extraction

---
# Installation

## Prerequisites
- Python 3.7+
- An API key from OpenAI

## Installation & Setup

1. **Clone the Repository**
   
   ```bash
   git clone https://github.com/mhadimedia/MarkItDown.git
   cd MarkItDown
   ```

2. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**

   Before running the app, make sure you set up the `config.yaml`:

   ```yaml
   openai_api_key: YOUR_OPENAI_API_KEY
   gpt_version: # Choose between gpt-3.5-turbo or gpt-4
   ```

   Replace `YOUR_OPENAI_API_KEY` with your actual OpenAI API key.

4. **Run the Application**

   ```bash
   python app.py
   ```

   Visit `http://127.0.0.1:5000/` in your browser to use the app.

## Usage

1. Enter or paste the text you'd like to convert.
2. Choose the desired output format: Markdown, HTML, or Plain Text.
3. Click `Submit` to get the processed text.
4. Toggle between the raw and rendered views.
5. You can copy or download the processed text as needed.

## License

This project is licensed under the terms of the Apache 2.0 license. See [LICENSE](LICENSE) for more details.