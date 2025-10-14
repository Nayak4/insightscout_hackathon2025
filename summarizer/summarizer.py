from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from llm.azure import azure_generate
from config import USER_PROFILES


def summarize_documents(documents, max_workers=5):
    summaries = [None] * len(documents)

    def summarize_one(idx_doc_tuple):
        idx, doc = idx_doc_tuple
        prompt = (
            "You are InsightScout, an expert assistant for internal product, engineering, and data platform documentation. "
            "Summarize the following document, extracting all relevant insights for future Q&A:\n\n"
            f"Title: {doc['title']}\nSource: {doc['source']}\nDate: {doc['date']}\nContent:\n{doc['content']}\n\n"
            "Instructions:\n"
            "- Summarize the main points, technical details, and outcomes.\n"
            "- Extract key decisions, issues, results, mappings, plans, features, and strategic context.\n"
            "- Include any performance metrics, migration steps, schema/licensing notes, bug fixes, or use case features mentioned.\n"
            "- Use bullet points or tables for clarity if appropriate.\n"
        )
        summary = azure_generate(prompt)
        return idx, summary

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(summarize_one, (i, doc)) for i, doc in enumerate(documents)]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Summarizing documents"):
            idx, summary = future.result()
            summaries[idx] = summary
    return summaries


def aggregate_summaries(summaries):
    combined = "\n\n".join(summaries)
    prompt = (
        "You are InsightScout, an expert assistant for internal documentation. "
        "Aggregate the following document summaries into a single, unified summary for future Q&A:\n\n"
        f"{combined}\n\n"
        "Instructions:\n"
        "- Provide a concise, high-quality summary covering all major topics, technical details, decisions, issues, results, mappings, plans, features, and strategic context.\n"
        "- Include performance metrics, migration/integration steps, schema/licensing notes, bug fixes, and use case features if present.\n"
        "- Use bullet points or tables for clarity if appropriate.\n"
        "- Avoid repetition and keep the summary focused and readable.\n"
    )
    return azure_generate(prompt)


def answer_on_summary(query, user_profile, unified_summary):
    prompt = (
        "You are InsightScout, an expert assistant for internal product, engineering, and data platform documentation. "
        "ONLY use the information in the summary below to answer the user's question. "
        "Do NOT make up information or use outside knowledge.\n\n"
        "=== UNIFIED SUMMARY START ===\n"
        f"{unified_summary}\n"
        "=== UNIFIED SUMMARY END ===\n\n"
        f"User profile: {user_profile} ({USER_PROFILES.get(user_profile, '')})\n"
        f"User question: {query}\n\n"
        "Instructions:\n"
        "- Provide a clear, concise, and accurate answer tailored to the user profile.\n"
        "- Reference specific details, results, mappings, plans, issues, features, or decisions as relevant to the question.\n"
        "- If the answer is not present in the summary, say 'Not found in the provided summary.'\n"
        "- Use bullet points, tables, or numbered lists if appropriate for clarity.\n"
    )
    return azure_generate(prompt)
