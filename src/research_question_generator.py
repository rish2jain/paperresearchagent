"""
Research Question Generation Module
Identifies research gaps and generates promising research questions
"""

from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ResearchQuestion:
    """Represents a generated research question"""
    question: str
    priority: str  # 'HIGH', 'MEDIUM', 'LOW'
    feasibility: str  # 'HIGH', 'MEDIUM', 'LOW'
    gap_related: bool
    novelty_score: float  # 0.0-1.0
    impact_score: float  # 0.0-1.0
    suggested_methods: List[str]
    related_gaps: List[str]


class ResearchQuestionGenerator:
    """
    Generates research questions from identified gaps
    """
    
    def __init__(self, reasoning_client=None):
        self.reasoning_client = reasoning_client
    
    async def generate_questions(
        self,
        gaps: List[str],
        themes: List[str],
        contradictions: List[Dict[str, Any]],
        top_k: int = 10
    ) -> List[ResearchQuestion]:
        """
        Generate research questions from gaps and analysis
        
        Args:
            gaps: List of identified research gaps
            themes: List of common themes
            contradictions: List of contradictions
            top_k: Number of questions to return
            
        Returns:
            List of ResearchQuestion objects
        """
        if not self.reasoning_client:
            # Fallback: generate simple questions from gaps
            return self._generate_simple_questions(gaps, top_k)
        
        # Use reasoning model to generate sophisticated questions
        prompt = f"""
Based on this research synthesis, generate promising research questions.

Research Gaps Identified:
{chr(10).join(f"- {gap}" for gap in gaps[:10])}

Common Themes:
{chr(10).join(f"- {theme}" for theme in themes[:10])}

Contradictions:
{chr(10).join(f"- {c}" for c in contradictions[:5])}

Generate research questions that:
1. Address the identified gaps
2. Resolve contradictions
3. Explore under-researched areas
4. Are feasible and impactful

For each question, provide:
- The research question
- Priority (HIGH/MEDIUM/LOW)
- Feasibility (HIGH/MEDIUM/LOW)
- Suggested research methods
- Related gap

Format as JSON:
{{
    "questions": [
        {{
            "question": "...",
            "priority": "HIGH",
            "feasibility": "MEDIUM",
            "suggested_methods": ["method1", "method2"],
            "related_gap": "..."
        }}
    ]
}}
"""
        
        try:
            response = await self.reasoning_client.complete(
                prompt,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse response
            questions = self._parse_questions(response, gaps)
            return questions[:top_k]
            
        except Exception as e:
            logger.error(f"Question generation error: {e}")
            return self._generate_simple_questions(gaps, top_k)
    
    def _parse_questions(self, response: str, gaps: List[str]) -> List[ResearchQuestion]:
        """Parse questions from model response"""
        import json
        import re
        
        questions = []
        
        # Try to extract JSON
        try:
            json_match = re.search(r'\{[^{}]*"questions"[^{}]*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                for q_data in data.get("questions", []):
                    questions.append(ResearchQuestion(
                        question=q_data.get("question", ""),
                        priority=q_data.get("priority", "MEDIUM"),
                        feasibility=q_data.get("feasibility", "MEDIUM"),
                        gap_related=True,
                        novelty_score=0.7,
                        impact_score=0.7,
                        suggested_methods=q_data.get("suggested_methods", []),
                        related_gaps=[q_data.get("related_gap", "")]
                    ))
        except Exception:
            pass
        
        # Fallback: extract questions from text
        if not questions:
            question_lines = re.findall(r'[Qq]uestion\s*\d*[:\-]\s*(.+?)(?=\n|$)', response)
            for q_text in question_lines[:10]:
                if q_text.strip():
                    questions.append(ResearchQuestion(
                        question=q_text.strip(),
                        priority="MEDIUM",
                        feasibility="MEDIUM",
                        gap_related=True,
                        novelty_score=0.6,
                        impact_score=0.6,
                        suggested_methods=[],
                        related_gaps=gaps[:1] if gaps else []
                    ))
        
        return questions
    
    def _generate_simple_questions(self, gaps: List[str], top_k: int) -> List[ResearchQuestion]:
        """Generate simple questions from gaps (fallback)"""
        questions = []
        
        for gap in gaps[:top_k]:
            question_text = f"How can we address {gap.lower()}?"
            questions.append(ResearchQuestion(
                question=question_text,
                priority="MEDIUM",
                feasibility="MEDIUM",
                gap_related=True,
                novelty_score=0.5,
                impact_score=0.5,
                suggested_methods=["Literature review", "Experimental study"],
                related_gaps=[gap]
            ))
        
        return questions
    
    def rank_questions(
        self,
        questions: List[ResearchQuestion]
    ) -> List[ResearchQuestion]:
        """
        Rank questions by priority, feasibility, and impact
        
        Args:
            questions: List of research questions
            
        Returns:
            Ranked list of questions
        """
        # Scoring function
        def score_question(q: ResearchQuestion) -> float:
            priority_score = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(q.priority, 1)
            feasibility_score = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(q.feasibility, 1)
            
            return (
                priority_score * 0.4 +
                feasibility_score * 0.3 +
                q.novelty_score * 0.15 +
                q.impact_score * 0.15
            )
        
        # Sort by score
        ranked = sorted(questions, key=score_question, reverse=True)
        return ranked

