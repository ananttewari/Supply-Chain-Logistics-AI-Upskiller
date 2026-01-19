from duckduckgo_search import DDGS

def test_new_filter():
    print("Testing NEW CJK filter (should keep English results)")
    print("=" * 70)
    
    with DDGS(timeout=10) as ddgs:
        results_raw = list(ddgs.text("supply chain training", max_results=10))
        
        print(f"Raw results from DDGS: {len(results_raw)}\n")
        
        # Apply the NEW filter
        filtered_results = []
        for r in results_raw:
            title = r.get('title', '')
            if not title:
                continue
            
            # Smart filter: Block Chinese/Japanese/Korean but allow English with special chars
            has_cjk = any('\u4e00' <= char <= '\u9fff' or  # Chinese
                          '\u3040' <= char <= '\u309f' or  # Hiragana
                          '\u30a0' <= char <= '\u30ff' or  # Katakana
                          '\uac00' <= char <= '\ud7af'     # Korean
                          for char in title)
            
            if not has_cjk:
                filtered_results.append(r)
                print(f"KEEP: {title[:65]}")
            else:
                print(f"BLOCK: {title[:65]}")
        
        print("\n" + "=" * 70)
        print(f"RESULTS:")
        print(f"  Raw from DDGS: {len(results_raw)}")
        print(f"  After CJK filter: {len(filtered_results)}")
        print(f"\nSUCCESS! Filter should keep English results with special chars.")

if __name__ == "__main__":
    test_new_filter()
