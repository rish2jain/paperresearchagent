"""
Denario Integration Module
Integrates Denario features for enhanced research workflow
"""

import os
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import Denario
try:
    from denario import Denario
    from denario import Journal
    DENARIO_AVAILABLE = True
except ImportError:
    DENARIO_AVAILABLE = False
    logger.warning(
        "Denario not installed. Install with: pip install denario[app]\n"
        "Denario features will be disabled."
    )
    # Create dummy classes for type hints
    Denario = None
    Journal = None


class DenarioIntegration:
    """
    Integration with Denario for enhanced research features:
    - Research idea generation
    - Methodology suggestions
    - Paper generation
    """
    
    def __init__(self, project_dir: str = "./denario_projects", enabled: bool = True):
        """
        Initialize Denario integration
        
        Args:
            project_dir: Directory for Denario projects
            enabled: Whether to enable Denario features
        """
        self.enabled = enabled and DENARIO_AVAILABLE
        self.project_dir = Path(project_dir)
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        if self.enabled:
            try:
                self.denario = Denario(project_dir=str(self.project_dir))
                logger.info(f"✅ Denario integration enabled (project_dir: {self.project_dir})")
            except Exception as e:
                logger.error(f"Failed to initialize Denario: {e}")
                self.enabled = False
                self.denario = None
        else:
            self.denario = None
            if not DENARIO_AVAILABLE:
                logger.warning("Denario not available - features disabled")
            else:
                logger.info("Denario integration disabled")
    
    def is_available(self) -> bool:
        """Check if Denario is available and enabled"""
        return self.enabled and self.denario is not None
    
    def generate_research_ideas(self, synthesis_result: Dict[str, Any]) -> List[str]:
        """
        Generate research ideas from synthesis gaps and contradictions
        
        Args:
            synthesis_result: Synthesis result from agents
        
        Returns:
            List of research ideas
        """
        if not self.is_available():
            logger.warning("Denario not available - cannot generate research ideas")
            return []
        
        try:
            # Build data description from synthesis
            themes = synthesis_result.get('common_themes', [])
            gaps = synthesis_result.get('research_gaps', [])
            contradictions = synthesis_result.get('contradictions', [])
            
            data_description = f"""
Based on literature review synthesis:
- Common Themes: {', '.join(themes[:5]) if themes else 'None identified'}
- Research Gaps: {', '.join(gaps[:5]) if gaps else 'None identified'}
- Contradictions: {', '.join([c.get('description', str(c))[:100] for c in contradictions[:3]]) if contradictions else 'None identified'}
- Papers Analyzed: {synthesis_result.get('papers_analyzed', 0)}

Generate research ideas that address the identified gaps and contradictions.
"""
            
            self.denario.set_data_description(data_description)
            idea = self.denario.get_idea()
            
            # Parse idea into list (if it's a string, split by newlines or bullets)
            if isinstance(idea, str):
                ideas = [line.strip() for line in idea.split('\n') if line.strip()]
                # Filter out empty lines and clean up
                ideas = [idea for idea in ideas if idea and not idea.startswith('#')]
                return ideas[:5]  # Return top 5 ideas
            elif isinstance(idea, list):
                return idea[:5]
            else:
                return [str(idea)]
        
        except Exception as e:
            logger.error(f"Error generating research ideas: {e}")
            return []
    
    def suggest_methodology(self, research_idea: str) -> str:
        """
        Generate methodology for a research idea
        
        Args:
            research_idea: Research idea string
        
        Returns:
            Methodology description
        """
        if not self.is_available():
            logger.warning("Denario not available - cannot suggest methodology")
            return ""
        
        try:
            self.denario.set_idea(research_idea)
            method = self.denario.get_method()
            return str(method) if method else ""
        except Exception as e:
            logger.error(f"Error generating methodology: {e}")
            return ""
    
    def generate_paper_structure(
        self,
        synthesis: Dict[str, Any],
        journal_style: str = "APS"
    ) -> str:
        """
        Generate LaTeX paper structure using Denario
        
        Args:
            synthesis: Synthesis result from agents
            journal_style: Journal style ("APS", "Nature", "IEEE")
        
        Returns:
            LaTeX paper content
        """
        if not self.is_available():
            logger.warning("Denario not available - cannot generate paper")
            return ""
        
        try:
            # Map journal style to Denario Journal enum
            journal_map = {
                "APS": Journal.APS if Journal else None,
                "Nature": Journal.Nature if Journal else None,
                "IEEE": Journal.IEEE if Journal else None,
            }
            
            journal = journal_map.get(journal_style, Journal.APS if Journal else None)
            
            if journal is None:
                logger.warning(f"Unknown journal style: {journal_style}, using default")
                journal = Journal.APS if Journal else None
            
            # Set results from synthesis
            results_text = f"""
Literature Review Synthesis Results:

Common Themes:
{chr(10).join(f'- {theme}' for theme in synthesis.get('common_themes', []))}

Research Gaps:
{chr(10).join(f'- {gap}' for gap in synthesis.get('research_gaps', []))}

Key Findings:
{chr(10).join(f'- {finding}' for finding in synthesis.get('key_findings', [])[:10])}
"""
            
            self.denario.set_results(results_text)
            
            # Generate paper
            paper = self.denario.get_paper(journal=journal) if journal else self.denario.get_paper()
            
            return str(paper) if paper else ""
        
        except Exception as e:
            logger.error(f"Error generating paper: {e}")
            return ""
    
    def enhance_synthesis_with_ideas(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance synthesis result with Denario-generated research ideas
        
        Args:
            synthesis: Original synthesis result
        
        Returns:
            Enhanced synthesis with research ideas
        """
        if not self.is_available():
            return synthesis
        
        enhanced = synthesis.copy()
        
        # Generate research ideas
        ideas = self.generate_research_ideas(synthesis)
        if ideas:
            enhanced['research_ideas'] = ideas
            enhanced['denario_enhanced'] = True
            logger.info(f"Generated {len(ideas)} research ideas using Denario")
        
        return enhanced

