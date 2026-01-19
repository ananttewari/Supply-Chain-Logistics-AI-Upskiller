from duckduckgo_search import DDGS
import json

results_data = {
    "tests": []
}

queries = ["python", "supply chain training"]

for query in queries:
    test_result = {
        "query": query,
        "status": "unknown",
        "count": 0,
        "error": None,
        "sample": None
    }
    
    try:
        with DDGS(timeout=10) as ddgs:
            results = list(ddgs.text(query, max_results=3))
            test_result["count"] = len(results)
            test_result["status"] = "success" if results else "empty"
            
            if results:
                test_result["sample"] = {
                    "title": results[0].get("title", ""),
                    "href": results[0].get("href", "")
                }
    except Exception as e:
        test_result["status"] = "error"
        test_result["error"] = str(e)
    
    results_data["tests"].append(test_result)

# Write to file
with open("search_results.json", "w", encoding="utf-8") as f:
    json.dump(results_data, f, indent=2, ensure_ascii=False)

print("Results written to search_results.json")
print(json.dumps(results_data, indent=2, ensure_ascii=False))
