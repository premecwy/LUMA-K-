from serpapi import GoogleSearch

def search_google(query, api_key, num_results=1):
    try:
        search = GoogleSearch({
            "q": query,
            "api_key": api_key,
            "num": num_results,
            "hl": "th",
            "gl": "th"
        })
        results = search.get_dict()
        organic = results.get("organic_results", [])
        return [r.get("link") for r in organic[:num_results] if "link" in r]
    except Exception as e:
        print(f"❌ Error searching Google: {e}")
        return []
