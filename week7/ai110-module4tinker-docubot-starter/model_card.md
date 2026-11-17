# DocuBot Model Card

This model card is a short reflection on your DocuBot system. Fill it out after you have implemented retrieval and experimented with all three modes:

1. Naive LLM over full docs  
2. Retrieval only  
3. RAG (retrieval plus LLM)

Use clear, honest descriptions. It is fine if your system is imperfect.

---

## 1. System Overview

**What is DocuBot trying to do?**  
Describe the overall goal in 2 to 3 sentences.

DocuBot is a lightweight documentation assistant that answers developer questions about a software project's internal docs. It retrieves relevant snippets from local markdown files and uses an LLM to generate grounded, concise answers instead of relying on the model's general knowledge.

**What inputs does DocuBot take?**  
For example: user question, docs in folder, environment variables.

A natural language question from the user, a folder of markdown documentation files (`docs/`), and optionally a `GEMINI_API_KEY` environment variable to enable LLM-powered modes.

**What outputs does DocuBot produce?**

Depending on the mode: raw document snippets with filenames (retrieval only), a full LLM-generated answer based on the entire corpus (naive), or a grounded LLM answer citing only the retrieved snippets (RAG). When no relevant information is found, it returns "I do not know based on these docs."

---

## 2. Retrieval Design

**How does your retrieval system work?**  
Describe your choices for indexing and scoring.

- How do you turn documents into an index?
- How do you score relevance for a query?
- How do you choose top snippets?

Documents are split into section-level chunks using markdown `##` headers, so each chunk contains a full section with its heading and content. An inverted index maps lowercase, punctuation-stripped words to the filenames they appear in. For scoring, the query is tokenized and stop words are removed; the score is the count of query terms that appear in the chunk text. Chunks are sorted by score descending and the top-k (default 3) are returned. A guardrail filters out chunks with a score below 1.

**What tradeoffs did you make?**  
For example: speed vs precision, simplicity vs accuracy.

Simplicity over accuracy. The keyword-matching approach is fast and easy to understand but cannot handle synonyms, typos, or semantic similarity. Section-level splitting balances granularity — paragraph-level was too fine (splitting headers from their content), while whole-document retrieval returned too much irrelevant text.

---

## 3. Use of the LLM (Gemini)

**When does DocuBot call the LLM and when does it not?**  
Briefly describe how each mode behaves.

- Naive LLM mode: The LLM receives the entire concatenated documentation corpus plus the user query. It generates an answer from all available text with no retrieval filtering.
- Retrieval only mode: No LLM is used at all. The system returns the top matching chunks directly to the user as raw text with filenames.
- RAG mode: The retrieval system first selects the top relevant chunks, then passes only those chunks plus the query to the LLM, which generates a grounded answer.

In all modes, if retrieval finds no relevant chunks (score below threshold), DocuBot refuses to answer and returns "I do not know based on these docs." without calling the LLM.

**What instructions do you give the LLM to keep it grounded?**  
Summarize the rules from your prompt. For example: only use snippets, say "I do not know" when needed, cite files.

The LLM is instructed to answer using only the provided snippets, cite the source filename, and say "I do not know" if the snippets do not contain enough information to answer the question.

---

## 4. Experiments and Comparisons

Run the **same set of queries** in all three modes. Fill in the table with short notes.

| Query | Naive LLM: helpful or harmful? | Retrieval only: helpful or harmful? | RAG: helpful or harmful? | Notes |
|-------|--------------------------------|--------------------------------------|--------------------------|-------|
| Where is the auth token generated? | Harmful — gave generic OAuth/JWT overview unrelated to this project | Helpful — returned AUTH.md section mentioning `generate_access_token` in `auth_utils.py` | Helpful — answered `POST /api/login` with source citation | Naive sounded confident but was completely project-unaware |
| How do I connect to the database? | Harmful — generic database connection advice | Helpful — returned DATABASE.md and SETUP.md sections | Helpful — concise answer about `DATABASE_URL` env var with examples | RAG synthesized info from multiple chunks clearly |
| Which endpoint lists all users? | Harmful — generic REST API patterns | Helpful — returned the correct API_REFERENCE.md section | Helpful — one-line answer: `GET /api/users` | After fixing chunk splitting, retrieval found the right section |
| How does a client refresh an access token? | Harmful — generic token refresh explanation | Helpful — returned AUTH.md client workflow section | Helpful — cited `/api/refresh` endpoint from docs | RAG combined auth workflow with API reference |

**What patterns did you notice?**  
- When does naive LLM look impressive but untrustworthy?  
- When is retrieval only clearly better?  
- When is RAG clearly better than both?

Naive LLM always sounds fluent and authoritative but answers from general knowledge, not project docs — it is most dangerous when the question has a project-specific answer that differs from common patterns. Retrieval only is better when the user can read raw docs and just needs to find the right section quickly. RAG is clearly better when the answer spans information from multiple chunks or when the raw snippets are too long and need summarization.

---

## 5. Failure Cases and Guardrails

**Describe at least two concrete failure cases you observed.**

**Failure case 1:** When documents were split by `\n\n` (paragraph level), the heading `### GET /api/users` was separated from its description "Returns a list of all users." This caused the retrieval to miss the correct chunk because the heading and content had different keyword matches.

**Failure case 2:** The query "What is the weather today?" initially returned results because common words like "the", "is", and "what" matched many chunks. Before adding stop word filtering, the system returned irrelevant API documentation instead of refusing to answer.

**When should DocuBot say "I do not know based on the docs I have"?**

1. When the query topic is completely outside the documentation scope (e.g., weather, sports, general knowledge questions).
2. When all retrieved chunks have very low relevance scores, meaning no meaningful keyword overlap exists between the query and any document section.

**What guardrails did you implement?**

A stop word list filters out common English words before scoring so they don't inflate relevance. A minimum score threshold (>= 1) ensures only chunks with at least one meaningful keyword match are returned. If no chunk passes the threshold, the system refuses to answer instead of guessing.

---

## 6. Limitations and Future Improvements

**Current limitations**

1. Keyword matching cannot handle synonyms or semantic similarity (e.g., "auth" vs "authentication", "DB" vs "database")
2. The scoring method treats all non-stop words as equally important — no TF-IDF or term weighting
3. Section-level chunking depends on consistent markdown formatting; poorly structured docs would produce bad chunks

**Future improvements**

1. Replace keyword scoring with embedding-based semantic search (e.g., using sentence-transformers) for better relevance matching
2. Add TF-IDF weighting so rare, distinctive terms score higher than common ones
3. Implement a confidence score that the LLM returns alongside its answer, allowing the UI to flag low-confidence responses

---

## 7. Responsible Use

**Where could this system cause real world harm if used carelessly?**

If developers trust DocuBot's answers without verifying against the actual source docs, they could misconfigure authentication secrets, database connections, or API permissions. In naive mode especially, the LLM may confidently describe behavior that does not match the actual codebase, leading to security vulnerabilities or broken deployments.

**What instructions would you give real developers who want to use DocuBot safely?**

- Always verify DocuBot's answers against the original documentation files before making configuration or code changes
- Use RAG mode instead of naive mode to ensure answers are grounded in actual project docs
- Treat "I do not know" responses as a feature, not a bug — it means the docs don't cover that topic and you need to investigate manually
- Keep documentation files up to date; DocuBot can only be as accurate as the docs it reads