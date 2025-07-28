🔍 Adobe Hackathon – Round 1A: Document Structure Extraction (Offline with MiniLM)
🎯 Problem Statement
You are given a PDF document and are tasked with extracting a structured outline that includes:

The document title

Hierarchical headings: H1, H2, H3

Their page numbers

This structured output will enable semantic understanding for further intelligent processing.

📂 Folder Structure
graphql
Copy
Edit
├── input/                   # Folder containing input PDFs
├── output/                  # Folder where output JSONs will be saved
├── local_minilm/            # Pre-downloaded MiniLM model (offline)
├── main.py                  # Main script
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
└── README.md                # You are here!
💡 How It Works
PDF Text Extraction:
We use pdfplumber to extract text from each page of the input PDF.

Sentence Segmentation & Filtering:
Extracted lines are cleaned and filtered to avoid false positives like headers, footers, or repeated phrases (e.g., “Opportunity”).

Semantic Heading Detection (MiniLM):
Each line is passed through a local MiniLM model to calculate similarity with heading templates like:

css
Copy
Edit
["introduction", "chapter", "contents", "overview", "references", "conclusion", ...]
Based on semantic closeness, heading levels H1, H2, H3 are assigned.

Output Generation:
The script produces a structured JSON like:

json
Copy
Edit
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    ...
  ]
}
Saved Output:
Saved in /output/filename_timestamp.json to ensure no overwriting.

📥 Setup Instructions
1. ✅ Environment Setup
bash
Copy
Edit
pip install -r requirements.txt
2. ✅ Download MiniLM Locally
Use the following in a separate Python script:

python
Copy
Edit
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
model.save('./local_minilm')
Move local_minilm/ into your project root.

🚫 This model is < 100MB and runs entirely offline on CPU.

▶️ Running the Code
bash
Copy
Edit
python main.py
It will process all PDFs in /input/ and save results in /output/.

🐳 Docker Usage
dockerfile
Copy
Edit
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
Run:

bash
Copy
Edit
docker build -t adobe-1a .
docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" adobe-1a
🧠 Model & Constraints
Constraint	Status
Runs Offline	✅ Yes
CPU-only	✅ Yes
< 200MB model	✅ MiniLM
Exec time	✅ < 10 sec for 50-page PDF

📌 Sample Output
json
Copy
Edit
{
  "title": "Overview Foundation Level Extensions",
  "outline": [
    { "level": "H1", "text": "Revision History", "page": 2 },
    { "level": "H1", "text": "Table of Contents", "page": 3 },
    { "level": "H2", "text": "2.1 Intended Audience", "page": 6 }
  ]
}
👨‍💻 Team Notes
Uses semantic embedding matching instead of just font size heuristics.

Prevents repetition of generic text (like "Opportunity").

Fully dockerized and production-ready.

