from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import pdfplumber
import os
import torch
import pytesseract
from PIL import Image

# Initialize the Flask application
app = Flask(__name__)
# Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app)

# Determine the device to use for model inference (0 for GPU, -1 for CPU)
device = 0 if torch.cuda.is_available() else -1

# Load the Named Entity Recognition (NER) pipeline from Hugging Face Transformers
# Specify the model and the device to use
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", device=device)

def save_uploaded_file(uploaded_file):
    """
    Save the uploaded file temporarily and return the file path.

    Parameters:
    uploaded_file (FileStorage): The uploaded file from the request.

    Returns:
    str: The path to the saved temporary file.
    """
    # Define the temporary file path
    temp_file_path = os.path.join("temp", uploaded_file.filename)
    # Create the 'temp' directory if it doesn't exist
    os.makedirs("temp", exist_ok=True)
    # Save the uploaded file to the temporary path
    uploaded_file.save(temp_file_path)
    return temp_file_path

def extract_text_from_file(file_path, file_extension):
    """
    Extract text from the uploaded file based on its extension.

    Parameters:
    file_path (str): The path to the file.
    file_extension (str): The file extension (e.g., '.pdf').

    Returns:
    str: The extracted text from the file.
    """
    if file_extension.lower() == 'pdf':
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page_number, page in enumerate(pdf.pages):
                # Try to extract text
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    # If no text is extracted, use OCR
                    page_image = page.to_image()
                    ocr_text = pytesseract.image_to_string(page_image.original)
                    text += ocr_text
        
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF file.")
        return text
    else:
        # Try reading the text file with different encodings
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze the uploaded resume file to extract named entities.

    Returns:
    Response: A JSON response containing extracted keywords or an error message.
    """
    try:
        # Check if a file is uploaded in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        uploaded_file = request.files['file']
        if not uploaded_file:
            return jsonify({"error": "Empty file"}), 400

        # Save the uploaded file temporarily
        temp_file_path = save_uploaded_file(uploaded_file)

        # Extract text from the file based on its extension
        extracted_text = extract_text_from_file(temp_file_path, uploaded_file.filename.split('.')[-1])

        if not extracted_text.strip():
            return jsonify({"error": "No text extracted from the file"}), 400

        # Process the extracted text with the NER model
        named_entities = ner_pipeline(extracted_text)

        if not named_entities:
            return jsonify({"message": "No named entities found"}), 200

        # Extract keywords from the named entities
        extracted_keywords = [entity['word'] for entity in named_entities]

        # Return the extracted keywords as a JSON response
        return jsonify({"keywords": extracted_keywords})

    except Exception as error:
        # Return an error response
        return jsonify({"error": str(error)}), 500

    finally:
        # Clean up the temporary file after processing
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
