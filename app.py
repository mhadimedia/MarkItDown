from flask import Flask, render_template, request, redirect, url_for
import openai
import yaml

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

OPENAI_API_KEY = config['openai_api_key']
openai.api_key = OPENAI_API_KEY
GPT_VERSION = config['gpt_version']

app = Flask(__name__)

def process_with_gpt(input_text, output_format):
    # Determine the prompt based on the desired output format
    if output_format == "md":
        prompt_text = f"Convert the following text from a user into Markdown format. Utilize proper Markdown formatting to beautifully display the users input text with correct Markdown formatting. Use Heading 1, 2, and 3 to seperate sections. Frequently bold, underline, and italicize as needed to emphasize. Use lists when needed, and tables if needed. NEVER EMBED IMAGES. Refrain from embedding images UNLESS the URL to the image was provided in the users input text. Don't add any additional text unless needed (as in if a user gives proper text already don't add to it, but if there's text that makes no sense or needs clarification you can add stuff.) Make sure the Markdown that you output makes sense, using markdown WISELY. Here's the text:\n\n{input_text}"
    elif output_format == "html":
        prompt_text = f"Convert the following text into HTML format. Make sure to use a modern font, with proper headings and formatting. It should look as if it were a Markdown document but in HTML:\n\n{input_text}"
    else:  # plain text
        prompt_text = f"Reformat the following text into well-structured plain text. Remove any unnecessary characters such as those used for HTML or Markdown:\n\n{input_text}"
    
    response = get_completion(prompt_text)
    return response

def get_completion(prompt, model=GPT_VERSION):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_text = request.form['input_text']
    output_format = request.form['output_format']

    # Process the input_text with GPT
    processed_text = process_with_gpt(input_text, output_format)
    
    return render_template('index.html', processed_text=processed_text, output_format=output_format)

if __name__ == '__main__':
    app.run(debug=True)