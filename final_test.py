from duckduckgo_search import DDGS

print("FINAL DIAGNOSTIC TEST")
print("=" * 70)

queries_to_test = [
    "python programming",
    "machine learning",
    "supply chain",
    "semiconductor logistics training"
]

for i, query in enumerate(queries_to_test, 1):
    print(f"\nTest {i}: '{query}'")
    print("-" * 70)
    
    try:
        with DDGS(timeout=10) as ddgs:
            results_list = []
            
            # Iterate and collect
            for result in ddgs.text(query, max_results=5):
                results_list.append(result)
            
            count = len(results_list)
            print(f"Total results collected: {count}")
            
            if count > 0:
                print(f"\nFirst result:")
                print(f"  Title: {results_list[0].get('title', 'N/A')}")
                print(f"  Link: {results_list[0].get('href', 'N/A')}")
                print(f"  Body: {results_list[0].get('body', 'N/A')[:80]}...")
            else:
                print("NO RESULTS - Iterator returned empty")
                print("This suggests:")
                print("  - DuckDuckGo may be rate-limiting your IP")
                print("  - Query may be blocked/filtered")
                print("  - Regional restrictions")
                
    except StopIteration:
        print("StopIteration - No results in iterator")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}")
        print(f"Message: {e}")

print("\n" + "=" * 70)
print("CONCLUSION:")
print("If all tests show 0 results, DuckDuckGo is blocking/rate-limiting.")
print("The fallback curated resources are the correct solution.")
print("=" * 70)
