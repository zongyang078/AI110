"""
Core DocuBot class responsible for:
- Loading documents from the docs/ folder
- Building a simple retrieval index (Phase 1)
- Retrieving relevant snippets (Phase 1)
- Supporting retrieval only answers
- Supporting RAG answers when paired with Gemini (Phase 2)
"""

import os
import glob

class DocuBot:

    def __init__(self, docs_folder="docs", llm_client=None):
        """
        docs_folder: directory containing project documentation files
        llm_client: optional Gemini client for LLM based answers
        """
        self.docs_folder = docs_folder
        self.llm_client = llm_client

        # Load documents into memory
        raw_docs = self.load_documents()  # List of (filename, text)

        # Split into smaller chunks for precise retrieval
        self.documents = self.split_into_chunks(raw_docs)

        # Build a retrieval index (implemented in Phase 1)
        self.index = self.build_index(self.documents)

    # -----------------------------------------------------------
    # Document Loading
    # -----------------------------------------------------------

    def load_documents(self):
        """
        Loads all .md and .txt files inside docs_folder.
        Returns a list of tuples: (filename, text)
        """
        docs = []
        pattern = os.path.join(self.docs_folder, "*.*")
        for path in glob.glob(pattern):
            if path.endswith(".md") or path.endswith(".txt"):
                with open(path, "r", encoding="utf8") as f:
                    text = f.read()
                filename = os.path.basename(path)
                docs.append((filename, text))
        return docs

    def split_into_chunks(self, documents):
        """Split each document into section-level chunks using markdown headers."""
        chunks = []
        for filename, text in documents:
            # Split by markdown headers (## or ###), keeping the header with its content
            sections = []
            current = []
            for line in text.split("\n"):
                if line.startswith("## ") and current:
                    sections.append("\n".join(current))
                    current = [line]
                else:
                    current.append(line)
            if current:
                sections.append("\n".join(current))
            for section in sections:
                section = section.strip()
                if len(section) > 30:
                    chunks.append((filename, section))
        return chunks

    # -----------------------------------------------------------
    # Index Construction (Phase 1)
    # -----------------------------------------------------------

    def build_index(self, documents):
        index = {}
        for filename, text in documents:
            words = text.lower().split()
            for word in words:
                cleaned = word.strip(".,;:!?()[]{}\"'`#*-_/\\")
                if cleaned:
                    if cleaned not in index:
                        index[cleaned] = set()
                    index[cleaned].add(filename)
        # Convert sets to lists for consistency
        return {k: list(v) for k, v in index.items()}

    # -----------------------------------------------------------
    # Scoring and Retrieval (Phase 1)
    # -----------------------------------------------------------

    def score_document(self, query, text):
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "do", "does",
                      "how", "what", "which", "who", "where", "when", "why",
                      "i", "my", "to", "in", "of", "and", "or", "for", "it",
                      "this", "that", "on", "at", "by", "with", "from"}
        query_words = [w for w in query.lower().split() if w not in stop_words]
        text_lower = text.lower()
        score = 0
        for word in query_words:
            if word in text_lower:
                score += 1
        return score

    def retrieve(self, query, top_k=3):
        results = []
        for filename, text in self.documents:
            score = self.score_document(query, text)
            if score > 0:
                results.append((score, filename, text))
        results.sort(key=lambda x: x[0], reverse=True)
        # Guardrail: only return results with meaningful relevance
        filtered = [(fn, txt) for s, fn, txt in results if s >= 1]
        if not filtered:
            return []
        return filtered[:top_k]

    # -----------------------------------------------------------
    # Answering Modes
    # -----------------------------------------------------------

    def answer_retrieval_only(self, query, top_k=3):
        """
        Phase 1 retrieval only mode.
        Returns raw snippets and filenames with no LLM involved.
        """
        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        formatted = []
        for filename, text in snippets:
            formatted.append(f"[{filename}]\n{text}\n")

        return "\n---\n".join(formatted)

    def answer_rag(self, query, top_k=3):
        """
        Phase 2 RAG mode.
        Uses student retrieval to select snippets, then asks Gemini
        to generate an answer using only those snippets.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Bonus Helper: concatenated docs for naive generation mode
    # -----------------------------------------------------------

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
        This is used in Phase 0 for naive 'generation only' baselines.
        """
        return "\n\n".join(text for _, text in self.documents)
