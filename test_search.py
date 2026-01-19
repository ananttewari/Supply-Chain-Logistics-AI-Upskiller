from duckduckgo_search import DDGS
import json

def test_search():
    query = "semiconductor supply chain training"
    print(f"Testing search with query: '{query}'")
    
    # Test Default Backend
    print("\n--- Testing Default Backend ---")
    try:
        results = []
        with DDGS() as ddgs:
            gen = ddgs.text(query, max_results=3)
            for r in gen:
                results.append(r)
        print(f"Success! Found {len(results)} results.")
        print(json.dumps(results[:1], indent=2))
    except Exception as e:
        print(f"Default Backend Failed: {e}")

    # Test Lite Backend
    print("\n--- Testing Lite Backend ---")
    try:
        results = []
        with DDGS() as ddgs:
            gen = ddgs.text(query, max_results=3, backend='lite')
            for r in gen:
                results.append(r)
        print(f"Success! Found {len(results)} results.")
        print(json.dumps(results[:1], indent=2))
    except Exception as e:
        print(f"Lite Backend Failed: {e}")

    # Test html Backend
    print("\n--- Testing HTML Backend ---")
    try:
        results = []
        with DDGS() as ddgs:
            gen = ddgs.text(query, max_results=3, backend='html')
            for r in gen:
                results.append(r)
        print(f"Success! Found {len(results)} results.")
        print(json.dumps(results[:1], indent=2))
    except Exception as e:
        print(f"HTML Backend Failed: {e}")

if __name__ == "__main__":
    test_search()
