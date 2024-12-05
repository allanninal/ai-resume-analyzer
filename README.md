
# AI Resume Analyzer

This project is an AI-powered Resume Analyzer that uses Hugging Face’s **Named Entity Recognition (NER)** pipeline to extract and categorize key information from resumes. It simplifies the recruitment process by identifying skills, certifications, experiences, and more from uploaded documents.

---

## Features

- **Key Information Extraction**: Identifies entities such as skills, organizations, locations, and certifications.
- **Multiple File Formats**: Supports PDF and plain text resumes.
- **Organized Results**: Categorizes extracted data for a clean and structured display.

---

## Tech Stack

### **Backend**
- Python with Flask for serving the API.
- Hugging Face Transformers for Named Entity Recognition.

### **AI Model**
- Hugging Face’s `dslim/bert-base-NER` for entity extraction.

---

## Installation and Setup

### Clone the Repository
Start by cloning the repository from GitHub:
```bash
git clone https://github.com/allanninal/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### Backend Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Install the dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```

---

## Usage

1. **Upload Resume**: Upload resumes in PDF or plain text format.
2. **Analyze Results**: View categorized and extracted information such as skills, organizations, and certifications.
3. **Streamline Processes**: Use the structured data for recruitment or resume optimization.

---

## How It Works

1. The uploaded resume text is extracted (if PDF) or processed directly (if plain text).
2. Hugging Face’s **dslim/bert-base-NER** model identifies and categorizes key entities in the text.
3. Results are displayed in a structured and clean format.

---

## What’s Next?

1. **Custom Models**: Fine-tune NER models for resume-specific data.
2. **Job Description Matching**: Analyze resumes against job descriptions to identify gaps.
3. **Summarization**: Generate concise summaries of resumes focusing on achievements.
4. **Multi-Language Support**: Extend functionality to support multilingual resumes.
5. **Export Options**: Allow users to export analysis results in JSON, PDF, or Excel.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Support

If you find this project helpful, consider supporting me on Ko-fi:  
[ko-fi.com/allanninal](https://ko-fi.com/allanninal)
