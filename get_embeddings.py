import sys
import json
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == "__main__":
    # Read JSON from STDIN
    data = json.load(sys.stdin)

    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        medical_condition = document.get("medical_condition","")
        description = document.get("description","")
        medical_condition_description = document.get("medical_condition_description","")
        side_effects = document.get("side_effects","")
        pregnancy_category = document.get("pregnancy_category","")
        rx_otc = document.get("rx_otc","")


        combined_text = medical_condition + " " + description
        document["vector"] = get_embedding(combined_text)

    # Output updated JSON to STDOUT
    json.dump(data, sys.stdout, indent=4, ensure_ascii=False)
