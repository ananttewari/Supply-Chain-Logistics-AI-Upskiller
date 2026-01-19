from duckduckgo_search import DDGS
import time

def test_comprehensive():
    """Test various configurations to find why search returns 0 results"""
    
    queries = [
        "supply chain",
        "training courses",
        "semiconductor",
        "logistics manager training"
    ]
    
    backends = [None, 'api', 'html', 'lite']
    
    print("=" * 80)
    print("COMPREHENSIVE DUCKDUCKGO SEARCH DIAGNOSTIC")
    print("=" * 80)
    
    for query in queries:
        print(f"\n{'='*80}")
        print(f"QUERY: '{query}'")
        print(f"{'='*80}")
        
        for backend in backends:
            backend_name = backend if backend else "default"
            print(f"\n--- Backend: {backend_name} ---")
            
            try:
                with DDGS() as ddgs:
                    kwargs = {"max_results": 3}
                    if backend:
                        kwargs["backend"] = backend
                    
                    results = list(ddgs.text(query, **kwargs))
                    
                    print(f"✓ Success! Results: {len(results)}")
                    
                    if results:
                        print(f"  First result:")
                        print(f"    Title: {results[0].get('title', 'N/A')[:60]}")
                        print(f"    Link: {results[0].get('href', 'N/A')[:60]}")
                    else:
                        print(f"  ⚠ Empty result list (no error, but 0 results)")
                        
            except Exception as e:
                print(f"✗ Error: {type(e).__name__}: {str(e)[:100]}")
            
            time.sleep(0.5)  # Rate limit protection
    
    # Test with different parameters
    print(f"\n{'='*80}")
    print("TESTING DIFFERENT PARAMETERS")
    print(f"{'='*80}")
    
    test_configs = [
        {"region": "wt-wt", "safesearch": "off"},
        {"region": "us-en", "safesearch": "moderate"},
        {"timelimit": None, "safesearch": "off"},
    ]
    
    query = "supply chain training"
    
    for config in test_configs:
        print(f"\nConfig: {config}")
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3, **config))
                print(f"  Results: {len(results)}")
                if results:
                    print(f"  ✓ Got results!")
                else:
                    print(f"  ⚠ Empty list")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        time.sleep(0.5)

    print(f"\n{'='*80}")
    print("DIAGNOSIS COMPLETE")
    print(f"{'='*80}")

if __name__ == "__main__":
    test_comprehensive()
