import os
import json
import fitz
from datetime import datetime
from bs4 import BeautifulSoup
from utils.text_utils import clean_text, extract_date_only, get_earliest_date


def load_documents():
    documents = []

    # Load JIRA tickets
    if os.path.exists('dal_sprint_tickets.json'):
        with open('dal_sprint_tickets.json', 'r', encoding='utf-8') as f:
            tickets = json.load(f)
        for ticket in tickets:
            title = ticket.get('summary', '')
            source = 'JIRA'
            dates = [ticket.get('created', ''), ticket.get('updated', '')]
            comments = ticket.get('comments', [])
            comment_dates = [c.get('created', '') for c in comments]
            all_dates = dates + comment_dates
            date = get_earliest_date(all_dates)
            content_lines = [
                f"Key: {ticket.get('key', '')}",
                f"Summary: {clean_text(title)}",
                f"Status: {ticket.get('status', '')}",
                f"Assignee: {ticket.get('assignee', '')}",
                f"Priority: {ticket.get('priority', '')}",
                f"Issue Type: {ticket.get('issue_type', '')}",
                f"Description: {clean_text(ticket.get('description', ''))}",
            ]
            if comments:
                content_lines.append("Comments:")
                for c in comments:
                    content_lines.append(
                        f"  - {c.get('author', '')} ({extract_date_only(c.get('created', ''))}): {clean_text(c.get('body', ''))}")
            content = "\n".join(content_lines)
            documents.append({
                "title": title,
                "source": source,
                "date": date,
                "content": content
            })

    # Load Confluence pages
    if os.path.exists('confluence_pages.json'):
        with open('confluence_pages.json', 'r', encoding='utf-8') as f:
            confluence = json.load(f)
        for title, page in confluence.items():
            source = 'Confluence'
            dates = [page.get('created', ''), page.get('last_modified', '')]
            date = get_earliest_date(dates)
            content_lines = [
                f"Title: {clean_text(title)}",
                f"ID: {page.get('id', '')}",
                f"Last Modified: {extract_date_only(page.get('last_modified', ''))}",
                f"Space: {page.get('space', '')}",
                f"Content: {clean_text(page.get('content', ''))}",
            ]
            content = "\n".join(content_lines)
            documents.append({
                "title": title,
                "source": source,
                "date": date,
                "content": content
            })

    # Load PDF and HTML files from source_files/
    source_folder = "source_files"
    if os.path.exists(source_folder):
        for fname in os.listdir(source_folder):
            fpath = os.path.join(source_folder, fname)
            # Determine source by filename prefix
            source = None
            if fname.lower().startswith("sp_"):
                source = "SharePoint"
            elif fname.lower().startswith("com_"):
                source = ".COM"
            elif fname.lower().startswith("ns_"):
                source = "Non solus"
            else:
                source = "Other"

            if fname.lower().endswith(".pdf"):
                try:
                    doc = fitz.open(fpath)
                    text = ""
                    for page in doc:
                        text += page.get_text()
                    doc.close()
                    title = fname
                    date = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%d")
                    documents.append({
                        "title": title,
                        "source": source,
                        "date": date,
                        "content": text
                    })
                except Exception as e:
                    print(f"Error reading PDF {fname}: {e}")
            elif fname.lower().endswith(".html") or fname.lower().endswith(".htm"):
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        html = f.read()
                    soup = BeautifulSoup(html, "html.parser")
                    text = soup.get_text(separator=' ', strip=True)
                    title = fname
                    date = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%d")
                    documents.append({
                        "title": title,
                        "source": source,
                        "date": date,
                        "content": text
                    })
                except Exception as e:
                    print(f"Error reading HTML {fname}: {e}")

    return documents
