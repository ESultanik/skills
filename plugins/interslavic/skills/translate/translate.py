#!/usr/bin/env python3
"""
Interslavic dictionary lookup tool.

Downloads and indexes the Interslavic cross-language dictionary from a public
Google Spreadsheet, caches it locally in SQLite, and provides substring search
across all language columns.

Compatible with Python 3.9+ (macOS system Python). No external dependencies.
"""

import argparse
import csv
import io
import json
import sqlite3
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any

# Character normalization for non-standard ISV characters
# Maps diacritics to ASCII equivalents for search matching
NORMALIZATION_MAP = {
    # Nasal/dotted vowels -> base vowel
    'ę': 'e', 'ą': 'a', 'ų': 'u', 'ȯ': 'o', 'ė': 'e', 'å': 'a',
    # Soft consonants -> base consonant
    'ń': 'n', 'ť': 't', 'ľ': 'l', 'ŕ': 'r', 'ď': 'd',
    'ś': 's', 'ź': 'z', 'ć': 'c', 'đ': 'dj',
    # Standard ISV hacek characters -> ASCII (for diacritic-free search)
    'č': 'c', 'š': 's', 'ž': 'z', 'ě': 'e',
    # Uppercase variants
    'Č': 'C', 'Š': 'S', 'Ž': 'Z', 'Ę': 'E', 'Ą': 'A', 'Ų': 'U',
    'Ń': 'N', 'Ť': 'T', 'Ľ': 'L', 'Ŕ': 'R', 'Ď': 'D',
    'Ś': 'S', 'Ź': 'Z', 'Ć': 'C', 'Đ': 'DJ',
}

SCHEMA_VERSION = 2


def normalize_text(text: str) -> str:
    """Normalize diacritical characters to ASCII equivalents.

    Args:
        text: Input text with potential diacritics.

    Returns:
        Text with diacritics replaced by ASCII equivalents.
    """
    return ''.join(NORMALIZATION_MAP.get(c, c) for c in text)


# Google Sheets configuration
SHEET_ID = "1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY"
GID = "1987833874"
EXPORT_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

# Cache configuration
CACHE_DIR = Path.home() / ".cache" / "interslavic"
DB_PATH = CACHE_DIR / "dictionary.db"
META_PATH = CACHE_DIR / "metadata.json"


def download_csv() -> str:
    """Download CSV data from Google Sheets.

    Returns:
        The CSV content as a string.

    Raises:
        urllib.error.URLError: If download fails.
    """
    print(f"Downloading dictionary from Google Sheets...", file=sys.stderr)

    request = urllib.request.Request(
        EXPORT_URL,
        headers={"User-Agent": "Mozilla/5.0 (Interslavic Dictionary Tool)"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read().decode("utf-8")

    return content


def init_database(csv_data: str) -> int:
    """Create and populate SQLite database from CSV data.

    Creates both a regular table for storage and an FTS5 virtual table
    for efficient full-text search.

    Args:
        csv_data: The CSV content as a string.

    Returns:
        The number of rows inserted.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # Remove existing database
    if DB_PATH.exists():
        DB_PATH.unlink()

    # Parse CSV
    reader = csv.DictReader(io.StringIO(csv_data))
    columns = reader.fieldnames

    if not columns:
        raise ValueError("CSV has no columns")

    # Normalize column names (lowercase, strip whitespace)
    columns = [col.strip().lower() for col in columns]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create main table with all columns as TEXT plus normalized ISV column
    col_defs = ", ".join(f'"{col}" TEXT' for col in columns)
    col_defs += ', "isv_normalized" TEXT'
    cursor.execute(f'CREATE TABLE dictionary ({col_defs})')

    # Create index on normalized column for faster LIKE searches
    cursor.execute('CREATE INDEX idx_isv_normalized ON dictionary(isv_normalized)')

    # Create FTS5 virtual table for full-text search (original columns only)
    col_list = ", ".join(f'"{col}"' for col in columns)
    cursor.execute(f'CREATE VIRTUAL TABLE dictionary_fts USING fts5({col_list}, content=dictionary)')

    # Insert data with normalized ISV column
    col_list_with_norm = col_list + ', "isv_normalized"'
    placeholders = ", ".join("?" for _ in columns) + ", ?"
    insert_sql = f'INSERT INTO dictionary ({col_list_with_norm}) VALUES ({placeholders})'

    # Find ISV column index
    isv_idx = columns.index('isv') if 'isv' in columns else None

    row_count = 0
    for row in reader:
        values = [row.get(col, "") or "" for col in reader.fieldnames]
        # Add normalized ISV value
        isv_value = values[isv_idx] if isv_idx is not None else ""
        values.append(normalize_text(isv_value.lower()))
        cursor.execute(insert_sql, values)
        row_count += 1

    # Populate FTS index
    cursor.execute('INSERT INTO dictionary_fts(dictionary_fts) VALUES ("rebuild")')

    conn.commit()
    conn.close()

    # Save metadata
    metadata = {
        "last_download": datetime.now().isoformat(),
        "source_url": EXPORT_URL,
        "row_count": row_count,
        "columns": columns,
        "schema_version": SCHEMA_VERSION,
    }
    META_PATH.write_text(json.dumps(metadata, indent=2))

    print(f"Indexed {row_count} entries with {len(columns)} columns.", file=sys.stderr)
    return row_count


def get_columns() -> List[str]:
    """Get the column names from metadata or database.

    Returns:
        List of column names.
    """
    if META_PATH.exists():
        metadata = json.loads(META_PATH.read_text())
        return metadata.get("columns", [])

    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(dictionary)")
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()
        return columns

    return []


def needs_schema_update() -> bool:
    """Check if database schema needs updating.

    Returns:
        True if schema version is outdated and refresh is needed.
    """
    if not META_PATH.exists():
        return False  # No metadata means no database, will be created fresh
    metadata = json.loads(META_PATH.read_text())
    return metadata.get("schema_version", 1) < SCHEMA_VERSION


def search(terms: List[str], lang: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search the dictionary for terms using substring matching.

    Args:
        terms: List of search terms.
        lang: Optional language code to filter results by.

    Returns:
        List of matching dictionary entries.
    """
    if not DB_PATH.exists():
        raise FileNotFoundError("Dictionary database not found. Run with --refresh first.")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get column names (excluding internal normalized column)
    cursor.execute("PRAGMA table_info(dictionary)")
    all_columns = [row[1] for row in cursor.fetchall()]
    columns = [col for col in all_columns if col != 'isv_normalized']

    results = []
    seen_rowids = set()

    for term in terms:
        # Normalize term for ISV column matching
        normalized_term = normalize_text(term.lower())

        # Build LIKE conditions for substring matching across all columns
        # For ISV, search the normalized column; for others, use original term
        like_conditions = []
        like_values = []

        for col in columns:
            if col == 'isv':
                # Search normalized ISV column with normalized term
                like_conditions.append('"isv_normalized" LIKE ?')
                like_values.append(f"%{normalized_term}%")
            else:
                like_conditions.append(f'"{col}" LIKE ?')
                like_values.append(f"%{term}%")

        query = f'SELECT rowid, * FROM dictionary WHERE {" OR ".join(like_conditions)}'
        cursor.execute(query, like_values)

        for row in cursor.fetchall():
            rowid = row["rowid"]
            if rowid in seen_rowids:
                continue
            seen_rowids.add(rowid)

            entry = {col: row[col] for col in columns}
            entry["_matched_term"] = term

            # Filter by language if specified
            if lang:
                lang_lower = lang.lower()
                if lang_lower in entry and entry[lang_lower]:
                    results.append(entry)
            else:
                results.append(entry)

    conn.close()
    return results


def format_entry(entry: Dict[str, Any], columns: List[str]) -> str:
    """Format a dictionary entry for human-readable output.

    Args:
        entry: The dictionary entry.
        columns: List of column names to display.

    Returns:
        Formatted string representation.
    """
    lines = []

    # Try to find the Interslavic word (common column names)
    isv_cols = ["isv", "interslavic", "slovianto", "medžuslovjansky"]
    isv_value = None
    for col in isv_cols:
        if col in entry and entry[col]:
            isv_value = entry[col]
            break

    if isv_value:
        lines.append(f"[ISV] {isv_value}")

    # Display other columns
    for col in columns:
        if col.startswith("_"):
            continue
        if col in isv_cols:
            continue
        value = entry.get(col, "")
        if value:
            lines.append(f"  {col.upper()}: {value}")

    return "\n".join(lines)


def print_results(results: List[Dict[str, Any]], columns: List[str], as_json: bool = False) -> None:
    """Print search results to stdout.

    Args:
        results: List of matching entries.
        columns: List of column names.
        as_json: If True, output as JSON instead of human-readable format.
    """
    if as_json:
        # Remove internal fields for JSON output
        clean_results = [{k: v for k, v in r.items() if not k.startswith("_")} for r in results]
        print(json.dumps(clean_results, indent=2, ensure_ascii=False))
        return

    if not results:
        print("No matches found.")
        return

    # Group by matched term
    by_term: Dict[str, List[Dict]] = {}
    for entry in results:
        term = entry.get("_matched_term", "unknown")
        if term not in by_term:
            by_term[term] = []
        by_term[term].append(entry)

    for term, entries in by_term.items():
        print(f"\n=== Results for \"{term}\" ({len(entries)} match{'es' if len(entries) != 1 else ''}) ===\n")

        for i, entry in enumerate(entries):
            if i > 0:
                print()
            print(format_entry(entry, columns))

    print(f"\nTotal: {len(results)} match{'es' if len(results) != 1 else ''}")


def show_info() -> None:
    """Display information about the cached dictionary."""
    if not META_PATH.exists():
        print("No dictionary cache found. Run with --refresh to download.")
        return

    metadata = json.loads(META_PATH.read_text())
    print("Interslavic Dictionary Cache Info")
    print("-" * 40)
    print(f"Last downloaded: {metadata.get('last_download', 'unknown')}")
    print(f"Entries: {metadata.get('row_count', 'unknown')}")
    print(f"Columns: {', '.join(metadata.get('columns', []))}")
    print(f"Cache location: {DB_PATH}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Search the Interslavic cross-language dictionary.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s water              Search for "water" in all languages
  %(prog)s --lang ru вода     Search for "вода" and show Russian translations
  %(prog)s --refresh water    Force refresh cache, then search
  %(prog)s --json water fire  Output results as JSON
  %(prog)s --info             Show cache information
        """
    )

    parser.add_argument(
        "words",
        nargs="*",
        help="Words to search for (substring matching)"
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Force re-download of dictionary data"
    )
    parser.add_argument(
        "--lang",
        metavar="CODE",
        help="Filter results to show only entries with this language (e.g., en, ru, pl)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show information about the cached dictionary"
    )

    args = parser.parse_args()

    # Handle --info
    if args.info:
        show_info()
        return 0

    # Require words unless just showing info
    if not args.words and not args.refresh:
        parser.print_help()
        return 1

    # Check for schema updates
    if DB_PATH.exists() and needs_schema_update():
        print("Database schema update required. Refreshing...", file=sys.stderr)
        args.refresh = True

    # Refresh cache if requested or if cache doesn't exist
    if args.refresh or not DB_PATH.exists():
        try:
            csv_data = download_csv()
            init_database(csv_data)
        except urllib.error.URLError as e:
            print(f"Error downloading dictionary: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error initializing database: {e}", file=sys.stderr)
            return 1

    # If no words provided (just --refresh), we're done
    if not args.words:
        print("Dictionary cache refreshed successfully.")
        return 0

    # Search
    try:
        results = search(args.words, args.lang)
        columns = get_columns()
        print_results(results, columns, args.json)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error during search: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
