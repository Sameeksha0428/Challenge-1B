import os
import json
from datetime import datetime
import pdfplumber
from sentence_transformers import SentenceTransformer, util

# Load persona + job
with open("persona_input.json", "r", encoding="utf-8") as f:
    persona_data = json.load(f)

persona = persona_data["persona"]["role"]
task = persona_data["job_to_be_done"]["task"]
input_documents = [doc["filename"] for doc in persona_data["documents"]]
query = f"{persona}. {task}"

# Load local MiniLM model
model = SentenceTransformer("local_model")  # saved earlier

# Function to extract paragraphs from a PDF
def extract_paragraphs(pdf_path):
    paragraphs = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                for para in text.split('\n\n'):
                    para = para.strip().replace('\n', ' ')
                    if len(para) > 50:
                        paragraphs.append({
                            "text": para,
                            "page": page_num + 1
                        })
    return paragraphs

# Function to rank paragraphs by semantic similarity
def rank_paragraphs_semantic(paragraphs, query):
    para_texts = [p["text"] for p in paragraphs]
    if not para_texts:
        return []

    para_embeddings = model.encode(para_texts, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, para_embeddings)[0]

    for i, para in enumerate(paragraphs):
        para["score"] = float(scores[i])

    return sorted(paragraphs, key=lambda x: x["score"], reverse=True)

# Process each PDF and build output
extracted_sections = []
subsection_analysis = []

for file in input_documents:
    pdf_path = os.path.join("input", file)
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {file}")
        continue

    paragraphs = extract_paragraphs(pdf_path)
    if not paragraphs:
        print(f"⚠️ No paragraphs in {file}")
        continue

    ranked = rank_paragraphs_semantic(paragraphs, query)
    top_para = ranked[0]

    extracted_sections.append({
        "document": file,
        "section_title": top_para["text"][:80] + "...",
        "importance_rank": len(extracted_sections) + 1,
        "page_number": top_para["page"]
    })

    subsection_analysis.append({
        "document": file,
        "refined_text": top_para["text"],
        "page_number": top_para["page"]
    })

# Final output JSON
output = {
    "metadata": {
        "input_documents": input_documents,
        "persona": persona,
        "job_to_be_done": task,
        "processing_timestamp": datetime.now().isoformat()
    },
    "extracted_sections": extracted_sections,
    "subsection_analysis": subsection_analysis
}

os.makedirs("output", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
safe_name = persona.lower().replace(" ", "_")
output_file = f"output/output_{safe_name}_{timestamp}.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print("\n✅ Done! Output saved to output/output.json")