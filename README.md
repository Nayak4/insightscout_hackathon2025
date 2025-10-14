# InsightScout AI

InsightScout AI is an internal documentation assistant that leverages Azure OpenAI to summarize, aggregate, and answer questions about product, engineering, and data platform documents. It provides a Streamlit dashboard for interactive analysis and Q&A.

## Features

- Loads documents from JIRA, Confluence, SharePoint, and other sources.
- Summarizes documents using Azure OpenAI.
- Aggregates summaries into a unified knowledge base.
- Answers user questions based on the aggregated summary.
- Interactive dashboard with metrics, charts, and query history.

## Architecture
flowchart TD
    A[User opens Streamlit Dashboard (app.py/ui/dashboard.py)]
    B[User selects filters and clicks 'Analyze Documents']
    C[Load Documents<br>(data/loader.py)]
    D[Clean Text & Extract Dates<br>(utils/text_utils.py)]
    E[Summarize Documents<br>(summarizer/summarizer.py)]
    F[Azure OpenAI API Call<br>(llm/azure.py)]
    G[Aggregate Summaries<br>(summarizer/summarizer.py)]
    H[Show Metrics, Charts, Unified Summary<br>(ui/dashboard.py)]
    I[User enters a question]
    J[Answer on Summary<br>(summarizer/summarizer.py)]
    K[Azure OpenAI API Call<br>(llm/azure.py)]
    L[Show Answer & History<br>(ui/dashboard.py)]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> E
    E --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> J
    J --> L
![InsightScout_architecture.png](diagram%2FInsightScout_architecture.png)
## Prerequisites

- Python 3.8+
- Azure OpenAI API access
- The following Python packages:
  - streamlit
  - pandas
  - plotly
  - openai
  - httpx
  - PyMuPDF (`fitz`)
  - beautifulsoup4
  - tqdm

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/nayak4/insightscout.git
    cd insightscout
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare your data:**
    - Place your `dal_sprint_tickets.json` and `confluence_pages.json` in the project root.
    - Place your PDF/HTML files in the `source_files/` directory.

4. **Configure Azure OpenAI:**
    - Edit `config.py` and set your `API_KEY`, `API_ENDPOINT`, and `CERT_PATH`.

## Running the App

```bash
streamlit run app.py