"""
Incremental Synthesizer for progressive research synthesis.

This module implements progressive synthesis that processes papers incrementally,
providing real-time updates as each paper is analyzed. This eliminates timeouts
and provides a better user experience with continuous feedback.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

from nim_clients import ReasoningNIMClient, EmbeddingNIMClient
from agents import Synthesis

logger = logging.getLogger(__name__)


@dataclass
class Theme:
    """Represents a research theme with confidence and supporting papers"""
    name: str
    confidence: float
    papers: List[str] = field(default_factory=list)
    key_findings: List[str] = field(default_factory=list)


@dataclass
class Contradiction:
    """Represents a contradiction between findings"""
    finding_a: str
    finding_b: str
    explanation: str
    severity: str = "medium"


@dataclass
class ResearchGap:
    """Represents a research gap or opportunity"""
    description: str
    importance: str = "medium"
    suggested_directions: List[str] = field(default_factory=list)


@dataclass
class SynthesisUpdate:
    """Represents an incremental update to the running synthesis."""

    paper_number: int
    paper_title: str
    timestamp: str

    # New discoveries
    new_themes: List[Theme] = field(default_factory=list)
    new_contradictions: List[Contradiction] = field(default_factory=list)
    new_gaps: List[ResearchGap] = field(default_factory=list)

    # Updated state
    theme_updates: List[Dict[str, Any]] = field(default_factory=list)  # Themes that gained confidence
    merged_themes: List[Dict[str, str]] = field(default_factory=list)  # Theme merge events

    # Current complete synthesis
    current_synthesis: Optional[Synthesis] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "paper_number": self.paper_number,
            "paper_title": self.paper_title,
            "timestamp": self.timestamp,
            "new_themes": [self._theme_to_dict(t) for t in self.new_themes],
            "new_contradictions": [self._contradiction_to_dict(c) for c in self.new_contradictions],
            "new_gaps": [self._gap_to_dict(g) for g in self.new_gaps],
            "theme_updates": self.theme_updates,
            "merged_themes": self.merged_themes,
            "current_synthesis": self._synthesis_to_dict(self.current_synthesis) if self.current_synthesis else None
        }

    @staticmethod
    def _theme_to_dict(theme: Theme) -> Dict[str, Any]:
        return {
            "name": theme.name,
            "confidence": theme.confidence,
            "papers": theme.papers,
            "key_findings": theme.key_findings
        }

    @staticmethod
    def _contradiction_to_dict(contradiction: Contradiction) -> Dict[str, Any]:
        return {
            "finding_a": contradiction.finding_a,
            "finding_b": contradiction.finding_b,
            "explanation": contradiction.explanation,
            "severity": contradiction.severity
        }

    @staticmethod
    def _gap_to_dict(gap: ResearchGap) -> Dict[str, Any]:
        return {
            "description": gap.description,
            "importance": gap.importance,
            "suggested_directions": gap.suggested_directions
        }

    @staticmethod
    def _synthesis_to_dict(synthesis: Synthesis) -> Dict[str, Any]:
        # Synthesis uses List[str] for themes/gaps, List[Dict] for contradictions
        return {
            "themes": synthesis.common_themes,
            "contradictions": synthesis.contradictions,
            "gaps": synthesis.gaps,
            "recommendations": synthesis.recommendations
        }


class IncrementalSynthesizer:
    """
    Progressive synthesizer that processes papers incrementally.

    Instead of batch processing all papers at once, this synthesizer:
    1. Processes papers one at a time
    2. Updates running synthesis after each paper
    3. Uses embedding-based filtering to reduce comparison complexity
    4. Provides real-time updates via streaming

    Complexity reduction:
    - Batch: O(n²) where n=total findings (~900 comparisons for 30 findings)
    - Progressive: O(k×m) where k=new findings, m=top candidates (~15 comparisons per paper)
    - Total: ~100-150 comparisons vs 900 (85% reduction)
    """

    def __init__(
        self,
        reasoning_client: ReasoningNIMClient,
        embedding_client: EmbeddingNIMClient,
        similarity_threshold: float = 0.7,
        top_k_candidates: int = 5
    ):
        self.reasoning_client = reasoning_client
        self.embedding_client = embedding_client
        self.similarity_threshold = similarity_threshold
        self.top_k_candidates = top_k_candidates

        # Running state - Synthesis uses List[str] for themes/gaps, List[Dict] for contradictions
        # But we maintain internal Theme objects for incremental processing
        self.running_synthesis = Synthesis(
            common_themes=[],
            contradictions=[],
            gaps=[],
            recommendations=[],
            enhanced_insights=None  # Will be populated after all papers are processed
        )
        # Internal Theme objects for incremental processing
        self.themes: List[Theme] = []
        self.processed_papers: List[Dict[str, Any]] = []
        self.all_findings: List[str] = []
        self.finding_embeddings: List[List[float]] = []
        self.finding_to_paper: Dict[str, str] = {}  # Maps finding to paper title

    async def add_analysis(
        self,
        analysis: Any,
        paper_info: Dict[str, str]
    ) -> SynthesisUpdate:
        """
        Add a newly analyzed paper to the running synthesis.

        Args:
            analysis: Analysis object with key_findings
            paper_info: Dict with paper metadata (title, authors, etc.)

        Returns:
            SynthesisUpdate with new discoveries and updated synthesis
        """
        logger.info(f"🧩 Incremental Synthesizer: Adding paper {len(self.processed_papers) + 1}")

        self.processed_papers.append(paper_info)
        new_findings = analysis.key_findings

        # Track which findings came from this paper
        for finding in new_findings:
            self.finding_to_paper[finding] = paper_info["title"]

        # Embed new findings
        new_embeddings = await self.embedding_client.embed_batch(
            new_findings,
            input_type="passage"
        )

        # Update themes incrementally
        new_themes, theme_updates, merged_themes = await self._update_themes(
            new_findings,
            new_embeddings,
            paper_info
        )

        # Check contradictions (NEW vs EXISTING only with filtering)
        new_contradictions = await self._check_contradictions_filtered(
            new_findings,
            new_embeddings
        )

        # Identify gaps (periodically, not every paper)
        new_gaps = []
        if len(self.processed_papers) % 5 == 0:  # Every 5 papers
            new_gaps = await self._identify_gaps()

        # Update running state
        self.all_findings.extend(new_findings)
        self.finding_embeddings.extend(new_embeddings)

        # Create synthesis update
        update = SynthesisUpdate(
            paper_number=len(self.processed_papers),
            paper_title=paper_info["title"],
            timestamp=datetime.utcnow().isoformat() + "Z",
            new_themes=new_themes,
            new_contradictions=new_contradictions,
            new_gaps=new_gaps,
            theme_updates=theme_updates,
            merged_themes=merged_themes,
            current_synthesis=self.running_synthesis
        )

        logger.info(
            f"✅ Incremental Synthesizer: Paper {len(self.processed_papers)} complete "
            f"({len(new_themes)} new themes, {len(new_contradictions)} contradictions)"
        )

        return update

    async def _update_themes(
        self,
        new_findings: List[str],
        new_embeddings: List[List[float]],
        paper_info: Dict[str, str]
    ) -> tuple[List[Theme], List[Dict[str, Any]], List[Dict[str, str]]]:
        """
        Update themes incrementally by comparing new findings to existing themes.

        Returns:
            (new_themes, theme_updates, merged_themes)
        """
        new_themes = []
        theme_updates = []
        merged_themes = []

        # Compare each new finding to existing themes
        for idx, finding in enumerate(new_findings):
            finding_embedding = new_embeddings[idx]

            # Find most similar existing theme
            best_match_theme = None
            best_similarity = 0.0

            for theme in self.themes:
                # Calculate average similarity to theme's findings
                if not theme.key_findings:
                    continue

                # Get embeddings for theme findings
                theme_finding_indices = [
                    self.all_findings.index(tf) for tf in theme.key_findings
                    if tf in self.all_findings
                ]

                if not theme_finding_indices:
                    continue

                similarities = [
                    self._cosine_similarity(finding_embedding, self.finding_embeddings[i])
                    for i in theme_finding_indices
                ]
                avg_similarity = sum(similarities) / len(similarities)

                if avg_similarity > best_similarity:
                    best_similarity = avg_similarity
                    best_match_theme = theme

            # Add to existing theme or create new one
            if best_match_theme and best_similarity >= self.similarity_threshold:
                # Update existing theme
                old_confidence = best_match_theme.confidence
                best_match_theme.key_findings.append(finding)
                best_match_theme.papers.append(paper_info["title"])
                best_match_theme.confidence = min(
                    0.95,
                    best_match_theme.confidence + (best_similarity - self.similarity_threshold) * 0.1
                )

                theme_updates.append({
                    "theme_name": best_match_theme.name,
                    "old_confidence": old_confidence,
                    "new_confidence": best_match_theme.confidence,
                    "new_finding": finding,
                    "similarity": best_similarity
                })

                logger.info(
                    f"📈 Theme strengthened: '{best_match_theme.name}' "
                    f"({old_confidence:.0%} → {best_match_theme.confidence:.0%})"
                )
            else:
                # Create new theme
                theme_name = await self._generate_theme_name([finding])
                new_theme = Theme(
                    name=theme_name,
                    confidence=0.45,  # Initial confidence for single-paper theme
                    papers=[paper_info["title"]],
                    key_findings=[finding]
                )
                # Add to internal themes list
                self.themes.append(new_theme)
                new_themes.append(new_theme)

                logger.info(f"🎯 New theme emerged: '{theme_name}' (confidence: 45%)")

        # Check if themes should be merged
        merged = await self._merge_similar_themes()
        merged_themes.extend(merged)

        return new_themes, theme_updates, merged_themes

    async def _check_contradictions_filtered(
        self,
        new_findings: List[str],
        new_embeddings: List[List[float]]
    ) -> List[Contradiction]:
        """
        Check for contradictions using embedding-based filtering.

        Key optimization: Only compare new findings against top K most similar
        existing findings instead of all existing findings.

        Complexity:
        - Without filtering: n_new × n_existing (e.g., 3 × 27 = 81)
        - With filtering: n_new × top_k (e.g., 3 × 5 = 15)
        """
        contradictions = []

        if not self.all_findings:  # No existing findings yet
            return contradictions

        logger.info(
            f"🔍 Checking contradictions: {len(new_findings)} new findings "
            f"vs top {self.top_k_candidates} candidates"
        )

        for idx, new_finding in enumerate(new_findings):
            new_embedding = new_embeddings[idx]

            # Find top K most similar existing findings (potential contradictions)
            candidates = await self._find_contradiction_candidates(
                new_finding,
                new_embedding,
                top_k=self.top_k_candidates
            )

            # Check each candidate for contradiction
            for candidate_finding, similarity in candidates:
                # High similarity suggests discussing same topic (necessary for contradiction)
                if similarity >= 0.6:
                    is_contradiction = await self._is_contradiction(
                        new_finding,
                        candidate_finding
                    )

                    if is_contradiction:
                        # Get paper titles for both findings
                        paper_a = self.finding_to_paper.get(new_finding, "Unknown")
                        paper_b = self.finding_to_paper.get(candidate_finding, "Unknown")

                        explanation = await self._explain_contradiction(
                            new_finding,
                            candidate_finding,
                            paper_a,
                            paper_b
                        )

                        contradiction = Contradiction(
                            finding_a=new_finding,
                            finding_b=candidate_finding,
                            explanation=explanation,
                            severity="medium"  # Could be enhanced with severity detection
                        )
                        contradictions.append(contradiction)
                        # Convert Contradiction to Dict for Synthesis.contradictions
                        self.running_synthesis.contradictions.append({
                            "finding_a": contradiction.finding_a,
                            "finding_b": contradiction.finding_b,
                            "explanation": contradiction.explanation,
                            "severity": contradiction.severity
                        })

                        logger.info(
                            f"⚠️ Contradiction discovered: "
                            f"'{new_finding[:50]}...' vs '{candidate_finding[:50]}...'"
                        )

        return contradictions

    async def _find_contradiction_candidates(
        self,
        new_finding: str,
        new_embedding: List[float],
        top_k: int = 5
    ) -> List[tuple[str, float]]:
        """Find top K most similar existing findings as contradiction candidates."""
        similarities = []

        for idx, existing_finding in enumerate(self.all_findings):
            existing_embedding = self.finding_embeddings[idx]
            similarity = self._cosine_similarity(new_embedding, existing_embedding)
            similarities.append((existing_finding, similarity))

        # Sort by similarity and return top K
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    async def _is_contradiction(self, finding_a: str, finding_b: str) -> bool:
        """Use Reasoning NIM to determine if two findings contradict."""
        prompt = f"""Analyze these two research findings and determine if they contradict each other.

Finding A: {finding_a}

Finding B: {finding_b}

A contradiction exists when:
1. Both findings address the same topic/phenomenon
2. They make incompatible claims (one says X, the other says not-X)
3. The incompatibility is not easily resolved by context or temporal differences

Respond with ONLY "yes" or "no".
"""

        try:
            response = await self.reasoning_client.complete(
                prompt,
                max_tokens=10,
                temperature=0.1
            )
            return response.strip().lower() == "yes"
        except Exception as e:
            logger.warning(f"Error checking contradiction: {e}")
            return False

    async def _explain_contradiction(
        self,
        finding_a: str,
        finding_b: str,
        paper_a: str,
        paper_b: str
    ) -> str:
        """Generate explanation for why findings contradict."""
        prompt = f"""Explain the contradiction between these research findings:

Finding A (from {paper_a}): {finding_a}

Finding B (from {paper_b}): {finding_b}

Provide a concise 1-2 sentence explanation of the contradiction. Consider:
- What specific claims conflict?
- Are there temporal, methodological, or contextual differences?
- What might explain the disagreement?

Explanation:"""

        try:
            response = await self.reasoning_client.complete(
                prompt,
                max_tokens=150,
                temperature=0.3
            )
            return response.strip()
        except Exception as e:
            logger.warning(f"Error explaining contradiction: {e}")
            return "These findings present conflicting claims about the same phenomenon."

    async def _merge_similar_themes(self) -> List[Dict[str, str]]:
        """Merge themes that have become very similar."""
        merged = []
        themes_to_remove = set()

        # Compare all pairs of themes
        for i, theme_a in enumerate(self.running_synthesis.themes):
            if i in themes_to_remove:
                continue

            for j, theme_b in enumerate(self.running_synthesis.themes[i+1:], start=i+1):
                if j in themes_to_remove:
                    continue

                # Calculate similarity between themes based on their findings
                if not theme_a.key_findings or not theme_b.key_findings:
                    continue

                # Get embeddings for both themes' findings
                theme_a_indices = [
                    self.all_findings.index(f) for f in theme_a.key_findings
                    if f in self.all_findings
                ]
                theme_b_indices = [
                    self.all_findings.index(f) for f in theme_b.key_findings
                    if f in self.all_findings
                ]

                if not theme_a_indices or not theme_b_indices:
                    continue

                # Calculate average cross-similarity
                similarities = []
                for a_idx in theme_a_indices:
                    for b_idx in theme_b_indices:
                        sim = self._cosine_similarity(
                            self.finding_embeddings[a_idx],
                            self.finding_embeddings[b_idx]
                        )
                        similarities.append(sim)

                avg_similarity = sum(similarities) / len(similarities)

                # Merge if very similar
                if avg_similarity >= 0.85:
                    # Merge theme_b into theme_a
                    theme_a.key_findings.extend(theme_b.key_findings)
                    theme_a.papers.extend([p for p in theme_b.papers if p not in theme_a.papers])
                    theme_a.confidence = max(theme_a.confidence, theme_b.confidence)

                    themes_to_remove.add(j)
                    merged.append({
                        "merged_from": theme_b.name,
                        "merged_into": theme_a.name,
                        "similarity": avg_similarity
                    })

                    logger.info(
                        f"🔗 Merged themes: '{theme_b.name}' → '{theme_a.name}' "
                        f"(similarity: {avg_similarity:.0%})"
                    )

        # Remove merged themes
        self.themes = [
            theme for i, theme in enumerate(self.themes)
            if i not in themes_to_remove
        ]

        return merged

    async def _generate_theme_name(self, findings: List[str]) -> str:
        """Generate a concise name for a theme based on its findings."""
        prompt = f"""Based on these research findings, generate a concise 3-5 word theme name:

Findings:
{chr(10).join(f'- {f}' for f in findings)}

The theme name should:
- Capture the core concept
- Be specific but concise
- Use academic/technical language

Theme name:"""

        try:
            response = await self.reasoning_client.complete(
                prompt,
                max_tokens=20,
                temperature=0.3
            )
            return response.strip().strip('"').strip("'")
        except Exception as e:
            logger.warning(f"Error generating theme name: {e}")
            return "Emerging Research Theme"

    async def _identify_gaps(self) -> List[ResearchGap]:
        """Identify research gaps based on current synthesis."""
        # Simplified gap identification - could be enhanced
        gaps = []

        # Look for underexplored themes (low confidence, few papers)
        for theme in self.themes:
            if theme.confidence < 0.6 and len(theme.papers) < 3:
                gap = ResearchGap(
                    description=f"Limited research on {theme.name.lower()}",
                    importance="medium",
                    suggested_directions=[
                        f"More empirical studies on {theme.name.lower()}",
                        f"Theoretical frameworks for {theme.name.lower()}"
                    ]
                )
                gaps.append(gap)
                # Convert ResearchGap to string for Synthesis.gaps
                self.running_synthesis.gaps.append(gap.description)

        return gaps

    @staticmethod
    def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import math

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        magnitude_a = math.sqrt(sum(a * a for a in vec_a))
        magnitude_b = math.sqrt(sum(b * b for b in vec_b))

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (magnitude_a * magnitude_b)

    def get_final_synthesis(self) -> Synthesis:
        """Get the final complete synthesis."""
        # Generate key insights from all themes and findings
        # Update Synthesis with current state
        self.running_synthesis.common_themes = [theme.name for theme in self.themes]
        # contradictions and gaps already updated incrementally

        return self.running_synthesis
