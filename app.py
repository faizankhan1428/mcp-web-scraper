from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import sqlite3
import os
from core.search_engine import smart_search, delete_document_from_search

app = Flask(__name__)

SAVE_FOLDER = r"D:\Faizan Data\mcp-web-scraper\scraped_outputs"
DB_PATH = os.path.join(SAVE_FOLDER, "scraped_database.db")

def get_records(file_filter="ALL"):
    """Fetches scrapes from SQLite database with optional file type filtering."""
    if not os.path.exists(DB_PATH):
        return [], 0, 0, 0
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get stats
    cursor.execute("SELECT COUNT(*) FROM scrapes")
    total_scrapes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM scrapes WHERE file_type = 'PDF'")
    pdf_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM scrapes WHERE file_type = 'Word'")
    word_count = cursor.fetchone()[0]

    # Get records based on filter
    if file_filter and file_filter != "ALL":
        cursor.execute("SELECT id, timestamp, url, title, file_path, file_type FROM scrapes WHERE file_type = ? ORDER BY id DESC", (file_filter,))
    else:
        cursor.execute("SELECT id, timestamp, url, title, file_path, file_type FROM scrapes ORDER BY id DESC")
        
    rows = cursor.fetchall()
    conn.close()
    
    return rows, total_scrapes, pdf_count, word_count

@app.route('/')
def index():
    file_filter = request.args.get('filter', 'ALL')
    records, total_scrapes, pdf_count, word_count = get_records(file_filter)
    return render_template('index.html', records=records, search_results=None, total_scrapes=total_scrapes, pdf_count=pdf_count, word_count=word_count, selected_filter=file_filter)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = smart_search(DB_PATH, query)
    records, total_scrapes, pdf_count, word_count = get_records("ALL")
    return render_template('index.html', records=records, search_results=results, query=query, total_scrapes=total_scrapes, pdf_count=pdf_count, word_count=word_count, selected_filter="ALL")

@app.route('/delete/<int:record_id>')
def delete_record(record_id):
    """Deletes a scrape record from SQLite, FTS index, and removes the physical file."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Fetch title and file path before deletion
        cursor.execute("SELECT title, file_path FROM scrapes WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        
        if row:
            title, file_path = row
            
            # 1. Remove physical file from disk if it exists
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as ex:
                    print(f"Physical file removal error: {ex}")
            
            # 2. Remove from FTS search index
            delete_document_from_search(DB_PATH, title)
            
        # 3. Remove from main logs table
        cursor.execute("DELETE FROM scrapes WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Delete Route Error: {e}")
        
    return redirect(url_for('index'))

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(SAVE_FOLDER, filename, as_attachment=False)

if __name__ == '__main__':
    print("Starting Advanced Flask Web Dashboard on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)