# Adobe Hackathon Round 1B – Persona-Driven Document Intelligence (Offline)

## 📌 Challenge Objective

Build an **intelligent document analyst** that extracts and prioritizes the most relevant sections from a set of PDF documents based on:

- A defined **persona** (e.g., Travel Planner, Analyst)
- A specific **job-to-be-done** (e.g., "Plan a 4-day trip", "Summarize financial reports")

The system outputs a structured JSON containing:
- Metadata
- Top relevant sections
- Subsection analysis

All processing is done **offline**, under **1GB**, on **CPU only**, and within **60 seconds**.

---

## 🔧 How It Works

1. Reads persona, task, and PDF filenames from `persona_input.json`
2. Loads PDFs from `/input2/` folder
3. Extracts paragraphs using `pdfplumber`
4. Ranks content relevance using **MiniLM-based semantic similarity**
5. Outputs `output_<persona>_<timestamp>.json` in `/output/` folder

---

## 🧠 Example Use Case

```json
{
  "persona": { "role": "Travel Planner" },
  "job_to_be_done": { "task": "Plan a trip of 4 days for a group of 10 college friends." },
  "documents": [
    { "filename": "South of France - Cities.pdf" },
    { "filename": "South of France - Cuisine.pdf" }
  ]
}
✅ Output JSON will contain top-ranked sections and refined text per document.

🧾 Folder Structure
graphql
Copy
Edit
project_root/
├── input2/                  # Input PDFs
├── output/                  # Output JSONs
├── persona_input.json       # Persona + Task input
├── local_minilm/            # Local MiniLM model folder
├── main.py                  # Main processing script
├── requirements.txt
└── README.md
📥 Model Download
⚠️ This solution uses a local MiniLM model (under 200MB) stored offline.

📦 Download it here:
👉 MiniLM Model Folder (Google Drive): https://drive.google.com/drive/folders/1KlDc0x7Yh6SpHU9Xbx3QzFvEpCHxOiuH?usp=sharing

After downloading:

Unzip if necessary

Place the folder as local_minilm/ in the project root

▶️ Run the Project
1. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
2. Add PDFs to /input2/ and configure persona_input.json
3. Run the script
bash
Copy
Edit
python main.py
JSON output will be saved to /output/ with a timestamp.

📦 requirements.txt
nginx
Copy
Edit
pdfplumber
sentence-transformers
torch
✅ Constraints Covered
Constraint	✅ Covered
Model size < 1GB	✅ Yes
Runs offline	✅ Yes
CPU-only	✅ Yes
Execution < 60s	✅ Yes

💡 Output Format (Simplified)
json
Copy
Edit
{
  "metadata": {
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip...",
    "processing_timestamp": "2025-07-25T14:00:00"
  },
  "extracted_sections": [
    {
      "document": "South of France - Cuisine.pdf",
      "section_title": "Culinary Experiences",
      "importance_rank": 1,
      "page_number": 6
    }
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Cuisine.pdf",
      "refined_text": "In addition to dining at...",
      "page_number": 6
    }
  ]
}
🙌 Built With
Python 🐍

PDFPlumber 📄

MiniLM (Sentence Transformers) 🤖

JSON 📦
