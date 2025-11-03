"""
Boolean Search Support
Parses and processes boolean search operators (AND, OR, NOT) in queries
"""

from typing import List, Set, Dict, Any, Optional
import re
import logging

logger = logging.getLogger(__name__)


def parse_boolean_query(query: str) -> Dict[str, Any]:
    """
    Parse a boolean search query with AND, OR, NOT operators

    Examples:
        "machine learning AND medical imaging"
        "deep learning OR neural networks"
        "transformer NOT GPT"
        "AI AND (medical OR clinical) NOT review"

    Args:
        query: Search query string

    Returns:
        Dictionary with parsed query structure
    """
    original_query = query.strip()

    # Check if query contains boolean operators
    has_boolean = bool(re.search(r"\b(AND|OR|NOT)\b", query, re.IGNORECASE))

    if not has_boolean:
        # Simple query, no boolean operators
        return {
            "type": "simple",
            "original": original_query,
            "terms": [original_query],
            "operator": None,
        }

    # Normalize operators (handle case variations)
    query_normalized = re.sub(r"\bAND\b", " AND ", query, flags=re.IGNORECASE)
    query_normalized = re.sub(r"\bOR\b", " OR ", query_normalized, flags=re.IGNORECASE)
    query_normalized = re.sub(
        r"\bNOT\b", " NOT ", query_normalized, flags=re.IGNORECASE
    )

    # Parse boolean expression
    # Simple parser for AND, OR, NOT (without complex parentheses handling for now)
    parts = re.split(r"\s+(AND|OR|NOT)\s+", query_normalized, flags=re.IGNORECASE)

    # Reconstruct with proper operator case
    terms = []
    operators = []

    i = 0
    while i < len(parts):
        term = parts[i].strip()
        if term:
            terms.append(term)

        if i + 1 < len(parts):
            op = parts[i + 1].strip().upper()
            if op in ["AND", "OR", "NOT"]:
                operators.append(op)
            i += 2
        else:
            i += 1

    return {
        "type": "boolean",
        "original": original_query,
        "terms": terms,
        "operators": operators,
        "parsed_expression": _build_expression(terms, operators),
    }


def _build_expression(terms: List[str], operators: List[str]) -> Dict[str, Any]:
    """Build a structured expression tree"""
    if not operators:
        return {"term": terms[0] if terms else ""}

    # Build left-to-right expression tree
    # This is simplified - for complex expressions, use proper parser
    expression = {
        "left": terms[0] if terms else "",
        "operator": operators[0] if operators else None,
        "right": None,
    }

    if len(terms) > 1 and len(operators) > 0:
        if len(terms) == 2:
            expression["right"] = terms[1]
        else:
            # Recursively build right side
            expression["right"] = _build_expression(terms[1:], operators[1:])

    return expression


def expand_boolean_query(parsed_query: Dict[str, Any]) -> List[str]:
    """
    Expand boolean query into multiple simple queries for search

    For boolean queries, we generate variations:
    - AND: Search for combined terms
    - OR: Search for each term separately
    - NOT: Remove excluded terms from results

    Args:
        parsed_query: Parsed query dictionary

    Returns:
        List of query strings to search
    """
    if parsed_query["type"] == "simple":
        return [parsed_query["original"]]

    queries = []
    terms = parsed_query["terms"]
    operators = parsed_query["operators"]

    # Strategy: Generate multiple query variations
    # For OR: search each term separately
    # For AND: search combined terms
    # For NOT: handled in post-processing

    if "OR" in operators:
        # For OR queries, search each term separately
        for term in terms:
            queries.append(term.strip())
    elif "AND" in operators:
        # For AND queries, search combined terms
        combined = " ".join(terms)
        queries.append(combined)
        # Also try individual terms for broader coverage
        queries.extend([t.strip() for t in terms if t.strip()])
    else:
        # NOT queries - search positive terms, filter negative
        positive_terms = [
            t
            for i, t in enumerate(terms)
            if i == 0 or (i < len(operators) and operators[i] != "NOT")
        ]
        if positive_terms:
            queries.append(" ".join(positive_terms))

    # Fallback to original if empty
    if not queries:
        queries = [parsed_query["original"]]

    return queries


def filter_by_boolean_terms(
    papers: List[Dict[str, Any]], parsed_query: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Filter papers based on boolean query terms

    Args:
        papers: List of paper dictionaries
        parsed_query: Parsed boolean query

    Returns:
        Filtered list of papers
    """
    if parsed_query["type"] == "simple":
        return papers

    terms = parsed_query["terms"]
    operators = parsed_query["operators"]

    filtered = []

    for paper in papers:
        # Extract searchable text
        searchable_text = " ".join(
            [
                paper.get("title", ""),
                paper.get("abstract", ""),
                " ".join(paper.get("authors", [])),
            ]
        ).lower()

        # Process terms with operators
        term_results = {}
        for term in terms:
            term_lower = term.lower()
            term_results[term] = term_lower in searchable_text

        # Apply boolean logic
        if not operators:
            # Single term
            result = term_results.get(terms[0], False)
        else:
            # Multiple terms with operators
            # Simple left-to-right evaluation
            result = term_results.get(terms[0], False)

            for i, op in enumerate(operators):
                next_term = terms[i + 1] if i + 1 < len(terms) else None
                if next_term is None:
                    break

                next_result = term_results.get(next_term, False)

                if op == "AND":
                    result = result and next_result
                elif op == "OR":
                    result = result or next_result
                elif op == "NOT":
                    result = result and not next_result

        if result:
            filtered.append(paper)

    return filtered


def format_boolean_query_hint(query: str) -> Optional[str]:
    """
    Provide hints for boolean query syntax

    Args:
        query: User's query

    Returns:
        Hint message if boolean operators detected, None otherwise
    """
    has_boolean = bool(re.search(r"\b(AND|OR|NOT)\b", query, re.IGNORECASE))

    if has_boolean:
        return (
            "💡 Boolean search detected! "
            "Use AND to require terms, OR to include alternatives, "
            "and NOT to exclude terms. Example: 'AI AND (medical OR clinical) NOT review'"
        )

    return None
