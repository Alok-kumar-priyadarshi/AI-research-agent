def needs_realtime_data(query: str) -> bool:
    keywords = [
        "latest",
        "current",
        "today",
        "now",
        "recent",
        "2025",
        "2026",
        "update",
        "news"
    ]

    query = query.lower()
    return any(k in query for k in keywords)