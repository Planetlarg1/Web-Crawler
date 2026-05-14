"""
Search Utilities for web scraping.
Target website: https://quotes.toscrape.com/

Functionality:
- Retrieve inverted index for a particular word for 'find' command
- Retrieve all documents containing a given multi-term query
"""

from __future__ import annotations

from src.indexer import tokenise


def get_index_for_word(index_data: dict, word: str) -> dict:
    """
    Returns the inverted index entry for a given word.

    Input:
        index_data: Full index structure to search
        word: Inputted word used to search index
    
    Output:
        Dictionary mapping of all documents for the given word
    """
    # Only accept 1 token
    tokens = tokenise(word)

    if len(tokens) != 1:
        return {}
    
    term = tokens[0]

    return index_data.get("index", {}).get(term, {})


def find_query(index_data: dict, query: str) -> dict:
    """
    Returns all documents that contain all query terms.

    Input: 
        index_data: Full index structure to search
        query: Inputted query made up of tokens to search index

    Output:
        Dictionary mapping of all documents for given query
    """
    # Tokenise query
    query_terms = tokenise(query)

    # Empty query
    if not query_terms:
        return []
    
    # Generate indexes
    inverted_index = index_data.get("index", {})
    documents = index_data.get("documents", {})

    postings_by_terms = {}

    # Iterate through all tokens and store index entries
    for term in query_terms:
        postings = inverted_index.get(term)

        # Query term not found
        if not postings:
            return []
        
        postings_by_terms[term] = postings

    matching_document_ids: set[str] | None = None

    # Iterate through documents containing terms and find intersection
    for postings in postings_by_terms.values():
        document_ids = set(postings.keys())

        if matching_document_ids is None:
            matching_document_ids = document_ids
        else:
            matching_document_ids = matching_document_ids.intersection(document_ids)

    # No intersection
    if not matching_document_ids:
        return []
    
    results = []

    # Calculate score for ranking
    for doc_id in matching_document_ids:
        document = documents.get(doc_id, {})

        # Score is determined by summing the appearances of all terms in the query in a given document
        score = sum(
            postings_by_terms[term][doc_id]["frequency"]
            for term in query_terms
        )

        results.append(
            {
                "document_id": doc_id,
                "url": document.get("url", ""),
                "title": document.get("title", ""),
                "score": score,
                "matched_terms": query_terms
            }
        )

    # Sort by score descending then by result ascending
    return sorted(
        results,
        key=lambda result: (-result["score"], result["document_id"])
    )