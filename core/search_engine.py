import sqlite3
import os

def init_fts_db(db_path: str):
    """Initializes SQLite FTS5 (Full-Text Search) table for advanced smart search."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Using FTS5 virtual table for high-performance relevance-ranked search
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS scrapes_fts USING fts5(
            title,
            url,
            content,
            file_path,
            file_type,
            timestamp
        )
    """)
    conn.commit()
    conn.close()

def index_document_for_search(db_path: str, title: str, url: str, content: str, file_path: str, file_type: str, timestamp: str):
    """Indexes a scraped document into the FTS5 search engine."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scrapes_fts (title, url, content, file_path, file_type, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (title, url, content[:3000], file_path, file_type, timestamp)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"FTS Indexing Error: {e}")

def delete_document_from_search(db_path: str, title: str):
    """Deletes a document from the FTS5 search index matching the title."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scrapes_fts WHERE title = ?", (title,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"FTS Deletion Error: {e}")

def smart_search(db_path: str, query: str) -> str:
    """
    Performs smart full-text search with relevance ranking (BM25) 
    across all past scraped documents.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # FTS5 match query with ranking
        cursor.execute(
            """
            SELECT title, url, file_path, file_type, timestamp, rank 
            FROM scrapes_fts 
            WHERE scrapes_fts MATCH ? 
            ORDER BY rank 
            LIMIT 5
            """,
            (query,)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return f"No intelligent matches found for query: '{query}'."

        result = f"Found {len(rows)} smart match(es) ranked by relevance:\n\n"
        for row in rows:
            result += f"📌 **Title:** {row[0]}\n"
            result += f"🔗 **URL:** {row[1]}\n"
            result += f"📂 **Path:** {row[2]} ({row[3]})\n"
            result += f"🕒 **Date:** {row[4]}\n"
            result += "-" * 40 + "\n"

        return result
    except Exception as e:
        return f"Smart search query failed: {str(e)}"