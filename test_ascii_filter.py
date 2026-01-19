from duckduckgo_search import DDGS

print("Testing ASCII filter issue")
print("=" * 70)

with DDGS(timeout=10) as ddgs:
    results = list(ddgs.text("supply chain training", max_results=10))
    
    print(f"Total results from DDGS: {len(results)}\n")
    
    filtered_count = 0
    kept_count = 0
    
    for i, r in enumerate(results, 1):
        title = r.get('title', '')
        is_ascii = title.isascii()
        
        if is_ascii:
            kept_count += 1
            status = "KEEP"
        else:
            filtered_count += 1
            status = "FILTER"
        
        print(f"{i}. [{status}] {title[:60]}")
        print(f"   is_ascii: {is_ascii}")
        if not is_ascii:
            # Show which characters are non-ASCII
            non_ascii = [c for c in title if ord(c) > 127]
            print(f"   Non-ASCII chars: {non_ascii[:5]}")
        print()

print("=" * 70)
print(f"SUMMARY:")
print(f"  Total results: {len(results)}")
print(f"  Kept (ASCII): {kept_count}")
print(f"  Filtered (non-ASCII): {filtered_count}")
print(f"\nIf filtered_count is high, the .isascii() check is too strict!")
