"""
Citation Style Formatter
Supports multiple citation formats: APA, MLA, Chicago, IEEE, Nature
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import re


def format_citation_apa(paper: Dict[str, Any]) -> str:
    """
    Format citation in APA style
    
    APA Format: Author, A. A. (Year). Title. Journal, Volume(Issue), Pages. https://doi.org/xx
    """
    authors = paper.get('authors', [])
    title = paper.get('title', 'Unknown')
    year = _extract_year(paper)
    
    # Format authors
    if authors:
        if len(authors) == 1:
            author_str = _format_author_apa(authors[0])
        elif len(authors) <= 6:
            author_str = ", ".join([_format_author_apa(a) for a in authors[:-1]])
            author_str += f", & {_format_author_apa(authors[-1])}"
        else:
            author_str = ", ".join([_format_author_apa(a) for a in authors[:6]])
            author_str += " et al."
    else:
        author_str = "Anonymous"
    
    citation = f"{author_str}"
    if year:
        citation += f" ({year})"
    citation += f". {title}."
    
    # Add URL or DOI if available
    url = paper.get('url', '')
    if url:
        citation += f" {url}"
    
    return citation


def format_citation_mla(paper: Dict[str, Any]) -> str:
    """
    Format citation in MLA style
    
    MLA Format: Author Last, First. "Title." Journal, vol. Volume, no. Issue, Year, pp. Pages.
    """
    authors = paper.get('authors', [])
    title = paper.get('title', 'Unknown')
    year = _extract_year(paper)
    
    # Format authors
    if authors:
        author_str = ", ".join([_format_author_mla(a) for a in authors])
        if len(authors) > 1:
            author_str = author_str.rsplit(", ", 1)[0] + ", and " + author_str.rsplit(", ", 1)[1]
    else:
        author_str = "Anonymous"
    
    citation = f"{author_str}. \"{title}.\""
    if year:
        citation += f" {year}."
    
    url = paper.get('url', '')
    if url:
        citation += f" {url}."
    
    return citation


def format_citation_chicago(paper: Dict[str, Any]) -> str:
    """
    Format citation in Chicago style
    
    Chicago Format: Author First Last. "Title." Journal Volume, no. Issue (Year): Pages.
    """
    authors = paper.get('authors', [])
    title = paper.get('title', 'Unknown')
    year = _extract_year(paper)
    
    # Format authors
    if authors:
        if len(authors) == 1:
            author_str = _format_author_chicago(authors[0])
        elif len(authors) <= 10:
            author_str = ", ".join([_format_author_chicago(a) for a in authors[:-1]])
            author_str += f", and {_format_author_chicago(authors[-1])}"
        else:
            author_str = ", ".join([_format_author_chicago(a) for a in authors[:10]])
            author_str += " et al."
    else:
        author_str = "Anonymous"
    
    citation = f"{author_str}. \"{title}.\""
    if year:
        citation += f" ({year})."
    
    url = paper.get('url', '')
    if url:
        citation += f" {url}."
    
    return citation


def format_citation_ieee(paper: Dict[str, Any]) -> str:
    """
    Format citation in IEEE style
    
    IEEE Format: A. Author, "Title," Journal, vol. Volume, no. Issue, pp. Pages, Year.
    """
    authors = paper.get('authors', [])
    title = paper.get('title', 'Unknown')
    year = _extract_year(paper)
    
    # Format authors (IEEE uses initials)
    if authors:
        author_str = ", ".join([_format_author_ieee(a) for a in authors])
        if len(authors) > 6:
            author_str = ", ".join([_format_author_ieee(a) for a in authors[:6]])
            author_str += " et al."
    else:
        author_str = "Anonymous"
    
    citation = f"{author_str}, \"{title},\""
    if year:
        citation += f" {year}."
    
    url = paper.get('url', '')
    if url:
        citation += f" {url}."
    
    return citation


def format_citation_nature(paper: Dict[str, Any]) -> str:
    """
    Format citation in Nature style
    
    Nature Format: Author, A. Title. Journal Volume, Pages (Year).
    """
    authors = paper.get('authors', [])
    title = paper.get('title', 'Unknown')
    year = _extract_year(paper)
    
    # Format authors (similar to APA but more compact)
    if authors:
        if len(authors) <= 5:
            author_str = ", ".join([_format_author_nature(a) for a in authors])
        else:
            author_str = ", ".join([_format_author_nature(a) for a in authors[:5]])
            author_str += " et al."
    else:
        author_str = "Anonymous"
    
    citation = f"{author_str} {title}."
    if year:
        citation += f" ({year})"
    
    url = paper.get('url', '')
    if url:
        citation += f" {url}"
    
    return citation


def format_citations(
    papers: List[Dict[str, Any]],
    style: str = "apa"
) -> List[str]:
    """
    Format multiple papers in specified citation style
    
    Args:
        papers: List of paper dictionaries
        style: Citation style ("apa", "mla", "chicago", "ieee", "nature")
    
    Returns:
        List of formatted citation strings
    """
    style_functions = {
        "apa": format_citation_apa,
        "mla": format_citation_mla,
        "chicago": format_citation_chicago,
        "ieee": format_citation_ieee,
        "nature": format_citation_nature
    }
    
    formatter = style_functions.get(style.lower(), format_citation_apa)
    
    return [formatter(paper) for paper in papers]


def _format_author_apa(author: str) -> str:
    """Format author name for APA style"""
    if not author:
        return "Anonymous"
    
    parts = author.split()
    if len(parts) >= 2:
        last = parts[-1]
        first_initials = " ".join([p[0] + "." for p in parts[:-1]])
        return f"{last}, {first_initials}"
    return author


def _format_author_mla(author: str) -> str:
    """Format author name for MLA style"""
    if not author:
        return "Anonymous"
    
    parts = author.split()
    if len(parts) >= 2:
        last = parts[-1]
        first = " ".join(parts[:-1])
        return f"{last}, {first}"
    return author


def _format_author_chicago(author: str) -> str:
    """Format author name for Chicago style"""
    if not author:
        return "Anonymous"
    
    parts = author.split()
    if len(parts) >= 2:
        last = parts[-1]
        first = " ".join(parts[:-1])
        return f"{first} {last}"
    return author


def _format_author_ieee(author: str) -> str:
    """Format author name for IEEE style (initials + last name)"""
    if not author:
        return "Anonymous"
    
    parts = author.split()
    if len(parts) >= 2:
        last = parts[-1]
        initials = ". ".join([p[0] for p in parts[:-1]]) + "."
        return f"{initials} {last}"
    return author


def _format_author_nature(author: str) -> str:
    """Format author name for Nature style"""
    if not author:
        return "Anonymous"
    
    parts = author.split()
    if len(parts) >= 2:
        last = parts[-1]
        first_initials = " ".join([p[0] + "." for p in parts[:-1]])
        return f"{last}, {first_initials}"
    return author


def _extract_year(paper: Dict[str, Any]) -> Optional[str]:
    """Extract publication year from paper"""
    if 'year' in paper:
        return str(paper['year'])
    
    if 'published_date' in paper:
        date_str = str(paper['published_date'])
        year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
        if year_match:
            return year_match.group(0)
    
    paper_id = paper.get('id', '')
    year_match = re.search(r'(19|20)\d{2}', paper_id)
    if year_match:
        return year_match.group(0)
    
    return None

