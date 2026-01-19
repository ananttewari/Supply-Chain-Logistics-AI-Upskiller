import requests

print("Testing basic internet connectivity...")
print("-" * 60)

# Test 1: Can we reach DuckDuckGo?
print("\n1. Testing connection to duckduckgo.com")
try:
    response = requests.get("https://duckduckgo.com", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   SUCCESS - Can reach DuckDuckGo")
except Exception as e:
    print(f"   FAILED - {e}")

# Test 2: Can we reach Google?
print("\n2. Testing connection to google.com")
try:
    response = requests.get("https://www.google.com", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   SUCCESS - Can reach Google")
except Exception as e:
    print(f"   FAILED - {e}")

# Test 3: Test DDGS with timeout
print("\n3. Testing DDGS with explicit timeout")
try:
    from duckduckgo_search import DDGS
    import time
    
    start = time.time()
    with DDGS(timeout=10) as ddgs:
        results = []
        for r in ddgs.text("test", max_results=2):
            results.append(r)
            break  # Just get first result
    elapsed = time.time() - start
    
    print(f"   Time: {elapsed:.2f}s")
    print(f"   Results: {len(results)}")
    if results:
        print(f"   SUCCESS - Got result: {results[0].get('title', 'N/A')[:50]}")
    else:
        print(f"   EMPTY - No results returned")
        
except Exception as e:
    print(f"   ERROR - {type(e).__name__}: {e}")

print("\n" + "-" * 60)
print("Diagnostic complete")
