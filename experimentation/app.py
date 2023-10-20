from flask import Flask, render_template, request, flash
import openai
import yaml
from werkzeug.utils import secure_filename
import os
import pytesseract
from PIL import Image

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

OPENAI_API_KEY = config['openai_api_key']
openai.api_key = OPENAI_API_KEY
GPT_VERSION = config['gpt_version']

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'md', 'html', 'pdf', 'jpg', 'jpeg', 'png', 'gif'}

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flash messages
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_with_gpt(input_text, output_formats):
    results = {}
    for output_format in output_formats:
        if output_format == "md":
            prompt_text = f"Convert the following text from a user into Markdown format. Utilize proper Markdown formatting to beautifully display the users input text with correct Markdown formatting. Use Heading 1, 2, and 3 to separate sections. Frequently bold, underline, and italicize as needed to emphasize. Use lists when needed, and tables if needed. NEVER EMBED IMAGES. Refrain from embedding images UNLESS the URL to the image was provided in the users input text. Here's the text:\n\n{input_text}"
        elif output_format == "html":
            prompt_text = f"Convert the following text into HTML format. Make sure to use a modern font, with proper headings and formatting. It should look as if it were a Markdown document but in HTML:\n\n{input_text}"
        else:  # plain text
            prompt_text = f"Reformat the following text into well-structured plain text. Remove any unnecessary characters such as those used for HTML or Markdown:\n\n{input_text}"

        response = get_completion(prompt_text)
        results[output_format] = response
    return results

def get_completion(prompt, model=GPT_VERSION):
    messages = [{"role": "You are a converter of texts from one format to another.", "content": prompt}]
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
    input_text = request.form.get('input_text', "")

    # Handle uploaded files
    uploaded_files = request.files.getlist('uploaded_files')
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            with open(filepath, 'r') as f:
                input_text += f.read()
            os.remove(filepath)

    # Handle OCR for images
    uploaded_images = request.files.getlist('uploaded_images')
    for image in uploaded_images:
        if image:
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename))
            image.save(img_path)
            text_from_image = pytesseract.image_to_string(Image.open(img_path))
            input_text += text_from_image
            os.remove(img_path)

    if len(input_text) > 3200:
        flash("Text limit exceeded. Truncating to first 3200 characters.")
        input_text = input_text[:3200]

    output_formats = request.form.getlist('output_format')
    processed_texts = process_with_gpt(input_text, output_formats)
    
    return render_template('index.html', processed_texts=processed_texts, output_formats=output_formats)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)