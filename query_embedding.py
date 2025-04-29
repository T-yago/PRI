import requests
from sentence_transformers import SentenceTransformer

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_combined_query(endpoint, collection, embedding, keyword):
    url = f"{endpoint}/{collection}/select"
    
    data = {
        "q": keyword, 
        "fq": f"{{!knn f=vector topK=50}}{embedding}",  
        "defType": "edismax",  
        "qf": "medical_condition^4.0 description^3.0 side_effects^1.0 Reviews 0.5",  
        "bq": f"medical_condition:{keyword}^5 description:{keyword}^3",  
        "fl": "medical_condition,medical_condition_description,description,score,id,pregnancy_category", 
        "ps": 2,
        "qs": 3,
        "stopwords": "true",
        "lowercaseOperators": "true",
        "rows": 50,
        "wt": "json",
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()


def display_results(results, query_id="0", run_id="run0"):
    docs = results.get("response", {}).get("docs", [])
    if not docs:
        print("No results found.")
        return

    for rank, doc in enumerate(docs, start=1):
        doc_id = doc.get("id")
        score = doc.get("score", 0.0)
        print(f"{query_id} Q0 {doc_id} {rank} {score:.6f} {run_id}")


def main():
    solr_endpoint = "http://localhost:8983/solr"
    collection = "semantic_drugs"
    
    query_text = input("Enter your query: ")
    embedding = text_to_embedding(query_text)
    
    try:
        results = solr_combined_query(solr_endpoint, collection, embedding, query_text)
        display_results(results)
    except requests.HTTPError as e:
        print(f"Error {e.response.status_code}: {e.response.text}")

if __name__ == "__main__":
    main()
