from duckduckgo_search import DDGS
import time

def test_search_simple():
    """Simple test to identify why search returns 0 results"""
    
    print("Testing DuckDuckGo Search")
    print("-" * 60)
    
    # Test 1: Very simple query
    print("\nTest 1: Simple query 'python'")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text("python", max_results=3))
            print(f"Results: {len(results)}")
            if results:
                print(f"SUCCESS - First result: {results[0].get('title', 'N/A')}")
            else:
                print("EMPTY - Got 0 results")
    except Exception as e:
        print(f"ERROR: {e}")
    
    time.sleep(1)
    
    # Test 2: Supply chain query
    print("\nTest 2: Query 'supply chain training'")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text("supply chain training", max_results=3))
            print(f"Results: {len(results)}")
            if results:
                print(f"SUCCESS - First result: {results[0].get('title', 'N/A')}")
            else:
                print("EMPTY - Got 0 results")
    except Exception as e:
        print(f"ERROR: {e}")
    
    time.sleep(1)
    
    # Test 3: With region parameter
    print("\nTest 3: With region='wt-wt'")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text("training", max_results=3, region='wt-wt'))
            print(f"Results: {len(results)}")
            if results:
                print(f"SUCCESS - First result: {results[0].get('title', 'N/A')}")
            else:
                print("EMPTY - Got 0 results")
    except Exception as e:
        print(f"ERROR: {e}")
    
    time.sleep(1)
    
    # Test 4: With safesearch off
    print("\nTest 4: With safesearch='off'")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text("courses", max_results=3, safesearch='off'))
            print(f"Results: {len(results)}")
            if results:
                print(f"SUCCESS - First result: {results[0].get('title', 'N/A')}")
            else:
                print("EMPTY - Got 0 results")
    except Exception as e:
        print(f"ERROR: {e}")
    
    print("\n" + "-" * 60)
    print("Testing complete")

if __name__ == "__main__":
    test_search_simple()
