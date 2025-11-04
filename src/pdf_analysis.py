"""
Full-Text PDF Analysis Module
Downloads and analyzes full PDF text of papers to extract methodologies,
experimental details, and results beyond abstracts.
"""

from typing import List, Dict, Any, Optional
import logging
import os
import re

# Optional PDF parsing dependencies
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

logger = logging.getLogger(__name__)


class PDFAnalyzer:
    """Analyzes full-text PDF documents for research papers"""
    
    def __init__(self, reasoning_client=None):
        """
        Initialize PDF analyzer
        
        Args:
            reasoning_client: Reasoning NIM client for advanced extraction
        """
        self.reasoning_client = reasoning_client
        self.use_pdfplumber = HAS_PDFPLUMBER  # Prefer pdfplumber for better text extraction
    
    async def analyze_pdf(self, pdf_url: str, paper_id: str) -> Dict[str, Any]:
        """
        Download and analyze PDF from URL
        
        Args:
            pdf_url: URL to PDF file
            paper_id: Unique identifier for the paper
            
        Returns:
            Dictionary with extracted information:
            - full_text: Complete extracted text
            - methodology: Extracted methodology section
            - results: Extracted results section
            - experimental_setup: Experimental details
            - figures_tables: Metadata about figures and tables
            - citations_in_text: Citations found in text
        """
        if not (HAS_PYPDF2 or HAS_PDFPLUMBER):
            logger.warning("No PDF parsing libraries available. Install PyPDF2 or pdfplumber.")
            return {
                "error": "PDF parsing libraries not available",
                "paper_id": paper_id
            }
        
        try:
            # Download PDF
            pdf_content = await self._download_pdf(pdf_url)
            if not pdf_content:
                return {"error": "Failed to download PDF", "paper_id": paper_id}
            
            # Extract text
            full_text = self._extract_text(pdf_content)
            if not full_text:
                return {"error": "Failed to extract text from PDF", "paper_id": paper_id}
            
            # Extract structured information
            analysis = {
                "paper_id": paper_id,
                "full_text_length": len(full_text),
                "full_text_preview": full_text[:1000] + "..." if len(full_text) > 1000 else full_text,
                "methodology": self._extract_section(full_text, ["methodology", "methods", "method"]),
                "results": self._extract_section(full_text, ["results", "findings", "experimental results"]),
                "experimental_setup": self._extract_experimental_setup(full_text),
                "figures_tables": self._extract_figures_tables(full_text),
                "citations_in_text": self._extract_citations(full_text),
                "statistical_results": self._extract_statistical_results(full_text)
            }
            
            # Use reasoning NIM for advanced extraction if available
            if self.reasoning_client:
                enhanced_analysis = await self._enhanced_extraction(full_text, analysis)
                analysis.update(enhanced_analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"PDF analysis error for {paper_id}: {e}", exc_info=True)
            return {"error": str(e), "paper_id": paper_id}
    
    async def _download_pdf(self, url: str) -> Optional[bytes]:
        """Download PDF from URL"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        logger.warning(f"Failed to download PDF: HTTP {response.status}")
                        return None
        except ImportError:
            logger.warning("aiohttp not available, cannot download PDFs")
            return None
        except Exception as e:
            logger.error(f"PDF download error: {e}")
            return None
    
    def _extract_text(self, pdf_content: bytes) -> str:
        """Extract text from PDF content"""
        if self.use_pdfplumber and HAS_PDFPLUMBER:
            return self._extract_with_pdfplumber(pdf_content)
        elif HAS_PYPDF2:
            return self._extract_with_pypdf2(pdf_content)
        else:
            return ""
    
    def _extract_with_pdfplumber(self, pdf_content: bytes) -> str:
        """Extract text using pdfplumber (better quality)"""
        import io
        text_parts = []
        
        try:
            with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
        except Exception as e:
            logger.error(f"pdfplumber extraction error: {e}")
            return ""
        
        return "\n\n".join(text_parts)
    
    def _extract_with_pypdf2(self, pdf_content: bytes) -> str:
        """Extract text using PyPDF2 (fallback)"""
        import io
        text_parts = []
        
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
        except Exception as e:
            logger.error(f"PyPDF2 extraction error: {e}")
            return ""
        
        return "\n\n".join(text_parts)
    
    def _extract_section(self, text: str, section_keywords: List[str]) -> Optional[str]:
        """Extract a specific section from text"""
        text_lower = text.lower()
        
        for keyword in section_keywords:
            # Look for section headers
            pattern = rf'(?i)(?:^|\n)\s*{re.escape(keyword)}\s*(?:\n|:|\d+)'
            matches = list(re.finditer(pattern, text, re.MULTILINE))
            
            if matches:
                start = matches[0].end()
                # Find next major section (usually starts with uppercase or number)
                next_section = re.search(r'\n\s*(?:[A-Z][A-Z\s]+\n|Abstract|Introduction|Conclusion|References)', text[start:], re.MULTILINE)
                end = start + next_section.start() if next_section else len(text)
                
                section_text = text[start:end].strip()
                if len(section_text) > 100:  # Minimum meaningful length
                    return section_text[:5000]  # Limit length
        
        return None
    
    def _extract_experimental_setup(self, text: str) -> Dict[str, Any]:
        """Extract experimental setup details"""
        setup = {
            "datasets": [],
            "hardware": None,
            "hyperparameters": [],
            "software_frameworks": []
        }
        
        # Common patterns
        dataset_patterns = [
            r'dataset[s]?\s*:?\s*([A-Z][a-zA-Z\s]+)',
            r'using\s+([A-Z][a-zA-Z\s]+)\s+dataset',
            r'evaluated\s+on\s+([A-Z][a-zA-Z\s]+)'
        ]
        
        hardware_patterns = [
            r'GPU[s]?:?\s*([A-Za-z0-9\s]+)',
            r'CPU[s]?:?\s*([A-Za-z0-9\s]+)',
            r'hardware[:\s]+([A-Za-z0-9\s]+)'
        ]
        
        framework_patterns = [
            r'(?:PyTorch|TensorFlow|Keras|JAX|scikit-learn|NumPy|Pandas)'
        ]
        
        # Extract datasets
        for pattern in dataset_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            setup["datasets"].extend([m.strip() for m in matches if len(m.strip()) > 2])
        
        # Extract hardware
        for pattern in hardware_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                setup["hardware"] = match.group(1).strip()
                break
        
        # Extract frameworks
        frameworks = re.findall(framework_patterns[0], text, re.IGNORECASE)
        setup["software_frameworks"] = list(set(frameworks))
        
        # Extract hyperparameters (simplified)
        hyperparam_pattern = r'(?:learning\s+rate|batch\s+size|epochs|optimizer)[:\s]+([0-9.]+|[A-Za-z]+)'
        hyperparams = re.findall(hyperparam_pattern, text, re.IGNORECASE)
        setup["hyperparameters"] = hyperparams[:10]  # Limit to 10
        
        return setup
    
    def _extract_figures_tables(self, text: str) -> Dict[str, Any]:
        """Extract metadata about figures and tables"""
        figures = []
        tables = []
        
        # Find figure references
        figure_pattern = r'Figure\s+(\d+)[:\s]+([^\n]+)'
        figure_matches = re.findall(figure_pattern, text, re.IGNORECASE)
        for num, caption in figure_matches:
            figures.append({"number": int(num), "caption": caption.strip()[:200]})
        
        # Find table references
        table_pattern = r'Table\s+(\d+)[:\s]+([^\n]+)'
        table_matches = re.findall(table_pattern, text, re.IGNORECASE)
        for num, caption in table_matches:
            tables.append({"number": int(num), "caption": caption.strip()[:200]})
        
        return {
            "figures_count": len(figures),
            "tables_count": len(tables),
            "figures": figures[:10],  # Limit to 10
            "tables": tables[:10]
        }
    
    def _extract_citations(self, text: str) -> List[str]:
        """Extract citation references from text"""
        # Common citation patterns: [1], [1,2], (Author, 2020), etc.
        citation_patterns = [
            r'\[(\d+(?:\s*,\s*\d+)*)\]',  # [1], [1,2,3]
            r'\(([A-Z][a-z]+\s+et\s+al\.?\s*,\s*\d{4})\)',  # (Author et al., 2020)
            r'\(([A-Z][a-z]+\s+and\s+[A-Z][a-z]+,\s*\d{4})\)'  # (Author and Author, 2020)
        ]
        
        citations = []
        for pattern in citation_patterns:
            matches = re.findall(pattern, text)
            citations.extend(matches)
        
        return list(set(citations))[:50]  # Limit to 50 unique citations
    
    def _extract_statistical_results(self, text: str) -> Dict[str, List[str]]:
        """Extract statistical results (p-values, effect sizes, etc.)"""
        results = {
            "p_values": [],
            "effect_sizes": [],
            "confidence_intervals": [],
            "correlations": []
        }
        
        # P-values
        p_pattern = r'p\s*[<>=]\s*0?\.\d+|p\s*=\s*0?\.\d+'
        p_matches = re.findall(p_pattern, text, re.IGNORECASE)
        results["p_values"] = list(set(p_matches))[:20]
        
        # Effect sizes
        effect_pattern = r'(?:Cohen\'?s\s+d|R²|r\s*=\s*|effect\s+size)[:\s]*([0-9.]+)'
        effect_matches = re.findall(effect_pattern, text, re.IGNORECASE)
        results["effect_sizes"] = effect_matches[:20]
        
        # Confidence intervals
        ci_pattern = r'(?:95%|99%)\s*CI[:\s]*\[([0-9.]+),\s*([0-9.]+)\]'
        ci_matches = re.findall(ci_pattern, text, re.IGNORECASE)
        results["confidence_intervals"] = [f"[{m[0]}, {m[1]}]" for m in ci_matches[:20]]
        
        return results
    
    async def _enhanced_extraction(self, full_text: str, basic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Use reasoning NIM for enhanced extraction"""
        if not self.reasoning_client:
            return {}
        
        prompt = f"""
Analyze this research paper's full text and extract key information.

Text preview (first 2000 chars):
{full_text[:2000]}

Extract:
1. Key experimental methodologies
2. Quantitative results and metrics
3. Novel contributions
4. Limitations mentioned
5. Future work suggestions

Provide JSON format response.
"""
        
        try:
            response = await self.reasoning_client.complete(
                prompt,
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse response (simplified - would need better JSON extraction)
            return {
                "enhanced_analysis": response[:500],  # Preview
                "extraction_method": "reasoning_nim"
            }
        except Exception as e:
            logger.error(f"Enhanced extraction error: {e}")
            return {}


async def analyze_papers_full_text(
    papers: List[Dict[str, Any]],
    reasoning_client=None,
    max_papers: int = 5
) -> Dict[str, Dict[str, Any]]:
    """
    Analyze full text of multiple papers (limited to avoid rate limits)
    
    Args:
        papers: List of paper dictionaries with PDF URLs
        reasoning_client: Optional reasoning client for enhanced extraction
        max_papers: Maximum number of papers to analyze (default: 5)
        
    Returns:
        Dictionary mapping paper_id to analysis results
    """
    analyzer = PDFAnalyzer(reasoning_client=reasoning_client)
    results = {}
    
    # Filter papers with PDF URLs
    papers_with_pdf = [
        p for p in papers 
        if p.get("pdf_url") or p.get("url", "").endswith(".pdf")
    ][:max_papers]
    
    if not papers_with_pdf:
        logger.info("No papers with PDF URLs found")
        return results
    
    import asyncio
    
    # Analyze in parallel (limited concurrency)
    semaphore = asyncio.Semaphore(3)  # Max 3 concurrent downloads
    
    async def analyze_one(paper):
        async with semaphore:
            pdf_url = paper.get("pdf_url") or paper.get("url", "")
            paper_id = paper.get("id", "")
            return await analyzer.analyze_pdf(pdf_url, paper_id)
    
    tasks = [analyze_one(p) for p in papers_with_pdf]
    analyses = await asyncio.gather(*tasks, return_exceptions=True)
    
    for paper, analysis in zip(papers_with_pdf, analyses):
        if isinstance(analysis, Exception):
            logger.error(f"PDF analysis failed for {paper.get('id')}: {analysis}")
            results[paper.get("id")] = {"error": str(analysis)}
        else:
            results[paper.get("id")] = analysis
    
    return results

