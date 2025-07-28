# Challenge_1b - Persona-Based Section Extraction

This repository contains the solution for Round 1B of the Adobe India Hackathon - "Connecting the Dots" Challenge.

# Objective

Given a collection of PDF documents and a specific persona with a job-to-be-done, the task is to:

- Identify and rank the most relevant sections from the documents
- Extract meaningful sub-sections
- Output a structured JSON with relevance-based ranking

This system enables persona-driven document summarization for intelligent reading.

# Approach

We use a semantic, MiniLM-based model to understand document content and match it with the persona's task. The pipeline includes:

- Text extraction using `pdfplumber`
- Sentence segmentation and cleanup
- Semantic similarity scoring with pre-downloaded MiniLM
- Ranking based on cosine similarity
- Extraction of top-matching sections and refined sub-sections

All processing is done offline and on CPU.

# Folder Structure

├── input/ # Folder containing input PDFs

├── output/ # Folder where output JSONs will be saved

├── local_minilm/ # Offline MiniLM model directory

├── main.py # Main processing script

├── requirements.txt # Python dependencies

├── Dockerfile # Docker configuration

└── README.md # Project documentation

# Download Minilm locally

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
model.save('./local_minilm')

# Output Format

The generated output will follow this structure:

```json
{
  "metadata": {
    "documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "PhD Researcher in Computational Biology",
    "job": "Prepare a literature review on GNNs for Drug Discovery",
    "timestamp": "2025-07-28T13:00:00"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page": 4,
      "section_title": "Graph Neural Networks in Drug Interaction",
      "importance_rank": 1
    },
    ...
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "page": 4,
      "refined_text": "GNNs are used to model molecular interactions..."
    }
  ]
}



