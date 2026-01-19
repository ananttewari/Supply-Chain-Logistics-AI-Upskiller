from duckduckgo_search import DDGS

def test_simple():
    query = "supply chain training"
    print(f"Query: {query}\n")
    
    try:
        with DDGS() as ddgs:
            print("DDGS initialized successfully")
            results = list(ddgs.text(query, max_results=5))
            print(f"Results count: {len(results)}")
            
            if results:
                print("\nFirst result:")
                print(f"Title: {results[0].get('title', 'N/A')}")
                print(f"Link: {results[0].get('href', 'N/A')}")
                print(f"Body: {results[0].get('body', 'N/A')[:100]}...")
            else:
                print("No results returned (empty list)")
                
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
