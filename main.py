import argparse
import json
import sys
from fun.summarizer import summarize
from fun.semantic_search import semantic_search


def parse_all(urls):
    print(f"Parsing {len(urls)} URLs and storing summaries...")
    for url in urls:
        try:
            print(f"\nParsing: {url}")
            result = summarize(url)
            print(
                "Title:", result["title"] if isinstance(result, dict) else result.title
            )
            print(
                "Summary:",
                result["summary"] if isinstance(result, dict) else result.summary,
            )
        except Exception as e:
            print(f"Failed to process {url}: {e}")
    print("Parsing complete.\n")


def interactive_search():
    print("--- Interactive Semantic Search ---")
    print(
        "Type your search query /max-results N to adjust result count, /thresh X to adjust threshold (or /exit to quit):"
    )
    max_results = 3
    distance_threshold = 0.5
    while True:
        query = input(
            f"[max-results={max_results} thresh={distance_threshold}] > "
        ).strip()
        if query == "/exit":
            print("Goodbye!")
            break
        elif query.startswith("/max-results "):
            try:
                max_results = int(query.split()[1])
                print(f"Max results set to {max_results}")
            except Exception:
                print("Usage: /max-results 5")
            continue
        elif query.startswith("/thresh "):
            try:
                distance_threshold = float(query.split()[1])
                print(f"Distance threshold set to {distance_threshold}")
            except Exception:
                print("Usage: /thresh 0.3")
            continue
        else:
            results = semantic_search(
                query, max_results=max_results, distance_threshold=distance_threshold
            )
            if not results:
                print("No results found.")
            else:
                for art in results:
                    print(art.as_str())
                    print("=" * 30)


def main():
    parser = argparse.ArgumentParser(
        description="News Semantic Search Command Line Tool"
    )
    parser.add_argument(
        "--parse", action="store_true", help="Parse URLs and enter search mode"
    )
    parser.add_argument(
        "--search", action="store_true", help="Only semantic search (skip parsing)"
    )
    parser.add_argument(
        "--urls", nargs="*", help="Provide URLs to parse (overrides data.json)"
    )
    args = parser.parse_args()

    if not args.parse and not args.search:
        parser.print_help()
        sys.exit(0)

    if args.parse:
        if args.urls:
            urls = args.urls
        else:
            with open("data.json") as f:
                data = json.load(f)
                urls = data.get("urls", [])
        if not urls:
            print("No URLs to parse.")
            sys.exit(1)
        parse_all(urls)
        interactive_search()
    elif args.search:
        interactive_search()


if __name__ == "__main__":
    main()
