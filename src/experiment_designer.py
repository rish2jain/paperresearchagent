"""
Experiment Design Assistant Module
Provides methodology guidance and experiment design templates
"""

from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ExperimentDesign:
    """Represents an experiment design"""
    design_type: str  # 'randomized_controlled', 'quasi_experimental', 'observational', etc.
    description: str
    methodology: str
    sample_size_recommendation: str
    control_group: Optional[str]
    intervention: Optional[str]
    outcome_measures: List[str]
    statistical_tests: List[str]
    validity_considerations: List[str]
    domain: str


class ExperimentDesigner:
    """
    Assists with experiment design based on research questions
    """
    
    def __init__(self, reasoning_client=None):
        self.reasoning_client = reasoning_client
        
        # Design templates by domain
        self.design_templates = {
            "machine_learning": {
                "randomized_controlled": {
                    "description": "Randomized controlled trial for ML model comparison",
                    "methodology": "Randomly assign datasets/samples to treatment (new model) or control (baseline model)",
                    "sample_size": "Power analysis based on effect size and desired statistical power (typically n≥30 per group)",
                    "statistical_tests": ["t-test", "Mann-Whitney U", "Wilcoxon signed-rank"],
                    "validity_considerations": ["Train/test split", "Cross-validation", "External validation"]
                },
                "quasi_experimental": {
                    "description": "Quasi-experimental design for pre/post comparisons",
                    "methodology": "Compare model performance before and after intervention",
                    "statistical_tests": ["Paired t-test", "Repeated measures ANOVA"],
                    "validity_considerations": ["Temporal confounds", "Selection bias"]
                }
            },
            "clinical": {
                "randomized_controlled": {
                    "description": "Randomized controlled trial for clinical interventions",
                    "methodology": "Randomly assign patients to treatment or control group",
                    "sample_size": "Power analysis: typically n≥100 per group for clinical trials",
                    "statistical_tests": ["Chi-square", "Fisher's exact test", "Logistic regression"],
                    "validity_considerations": ["Blinding", "Randomization", "Attrition"]
                }
            },
            "social_science": {
                "observational": {
                    "description": "Observational study design",
                    "methodology": "Observe and measure variables without intervention",
                    "statistical_tests": ["Correlation", "Regression", "Chi-square"],
                    "validity_considerations": ["Confounding variables", "Selection bias", "Measurement validity"]
                }
            }
        }
    
    async def design_experiment(
        self,
        research_question: str,
        domain: str = "machine_learning",
        design_type: Optional[str] = None
    ) -> ExperimentDesign:
        """
        Design an experiment for a research question
        
        Args:
            research_question: Research question to design for
            domain: Research domain (e.g., 'machine_learning', 'clinical')
            design_type: Specific design type (optional)
            
        Returns:
            ExperimentDesign object
        """
        # Determine design type if not specified
        if not design_type:
            design_type = self._recommend_design_type(research_question, domain)
        
        # Get template
        template = self.design_templates.get(domain, {}).get(design_type)
        
        if not template:
            # Generate custom design using reasoning model
            if self.reasoning_client:
                return await self._generate_custom_design(research_question, domain)
            else:
                # Fallback to generic design
                template = {
                    "description": "Experimental study design",
                    "methodology": "Standard experimental methodology",
                    "sample_size": "Determine via power analysis",
                    "statistical_tests": ["t-test", "ANOVA"],
                    "validity_considerations": ["Internal validity", "External validity"]
                }
        
        # Enhance with reasoning model if available
        if self.reasoning_client:
            enhanced = await self._enhance_design(template, research_question, domain)
            return enhanced
        
        # Create design from template
        return ExperimentDesign(
            design_type=design_type,
            description=template.get("description", ""),
            methodology=template.get("methodology", ""),
            sample_size_recommendation=template.get("sample_size", ""),
            control_group=None,
            intervention=None,
            outcome_measures=[],
            statistical_tests=template.get("statistical_tests", []),
            validity_considerations=template.get("validity_considerations", []),
            domain=domain
        )
    
    def _recommend_design_type(self, research_question: str, domain: str) -> str:
        """Recommend appropriate design type based on question"""
        question_lower = research_question.lower()
        
        # Keywords for different design types
        if any(word in question_lower for word in ["compare", "versus", "better", "superior"]):
            return "randomized_controlled"
        elif any(word in question_lower for word in ["effect", "impact", "influence", "causes"]):
            return "randomized_controlled"
        elif any(word in question_lower for word in ["relationship", "association", "correlation"]):
            return "observational"
        elif any(word in question_lower for word in ["before", "after", "change"]):
            return "quasi_experimental"
        else:
            return "observational"
    
    async def _enhance_design(
        self,
        template: Dict[str, Any],
        research_question: str,
        domain: str
    ) -> ExperimentDesign:
        """Enhance design template using reasoning model"""
        prompt = f"""
Enhance this experiment design for the research question:

Question: {research_question}
Domain: {domain}
Current Design: {template.get('description', '')}

Provide enhanced design details including:
1. Control group specification
2. Intervention details
3. Outcome measures
4. Statistical analysis plan
5. Validity considerations

Format as JSON:
{{
    "control_group": "...",
    "intervention": "...",
    "outcome_measures": ["measure1", "measure2"],
    "statistical_tests": ["test1", "test2"],
    "validity_considerations": ["consideration1", "consideration2"]
}}
"""
        
        try:
            response = await self.reasoning_client.complete(
                prompt,
                temperature=0.3,
                max_tokens=800
            )
            
            # Parse enhanced design
            import json
            import re
            json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
            if json_match:
                enhanced = json.loads(json_match.group())
                
                return ExperimentDesign(
                    design_type=template.get("design_type", "experimental"),
                    description=template.get("description", ""),
                    methodology=template.get("methodology", ""),
                    sample_size_recommendation=template.get("sample_size", ""),
                    control_group=enhanced.get("control_group"),
                    intervention=enhanced.get("intervention"),
                    outcome_measures=enhanced.get("outcome_measures", []),
                    statistical_tests=enhanced.get("statistical_tests", template.get("statistical_tests", [])),
                    validity_considerations=enhanced.get("validity_considerations", template.get("validity_considerations", [])),
                    domain=domain
                )
        except Exception as e:
            logger.error(f"Design enhancement error: {e}")
        
        # Fallback to template
        return ExperimentDesign(
            design_type="experimental",
            description=template.get("description", ""),
            methodology=template.get("methodology", ""),
            sample_size_recommendation=template.get("sample_size", ""),
            control_group=None,
            intervention=None,
            outcome_measures=[],
            statistical_tests=template.get("statistical_tests", []),
            validity_considerations=template.get("validity_considerations", []),
            domain=domain
        )
    
    async def _generate_custom_design(
        self,
        research_question: str,
        domain: str
    ) -> ExperimentDesign:
        """Generate custom design from scratch"""
        prompt = f"""
Design an experiment for this research question:

Question: {research_question}
Domain: {domain}

Provide a complete experiment design including methodology, sample size, statistical tests, and validity considerations.

Format as JSON:
{{
    "design_type": "...",
    "description": "...",
    "methodology": "...",
    "sample_size": "...",
    "statistical_tests": ["test1", "test2"],
    "validity_considerations": ["consideration1", "consideration2"]
}}
"""
        
        try:
            response = await self.reasoning_client.complete(
                prompt,
                temperature=0.3,
                max_tokens=800
            )
            
            import json
            import re
            json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
            if json_match:
                design_data = json.loads(json_match.group())
                
                return ExperimentDesign(
                    design_type=design_data.get("design_type", "experimental"),
                    description=design_data.get("description", ""),
                    methodology=design_data.get("methodology", ""),
                    sample_size_recommendation=design_data.get("sample_size", ""),
                    control_group=None,
                    intervention=None,
                    outcome_measures=[],
                    statistical_tests=design_data.get("statistical_tests", []),
                    validity_considerations=design_data.get("validity_considerations", []),
                    domain=domain
                )
        except Exception as e:
            logger.error(f"Custom design generation error: {e}")
        
        # Ultimate fallback
        return ExperimentDesign(
            design_type="experimental",
            description="Experimental study design",
            methodology="Standard experimental methodology",
            sample_size_recommendation="Determine via power analysis",
            control_group=None,
            intervention=None,
            outcome_measures=[],
            statistical_tests=["t-test", "ANOVA"],
            validity_considerations=["Internal validity", "External validity"],
            domain=domain
        )
    
    def validate_design(self, design: ExperimentDesign) -> Dict[str, Any]:
        """
        Validate an experiment design
        
        Returns:
            Dictionary with validation results
        """
        issues = []
        warnings = []
        
        # Check required fields
        if not design.methodology:
            issues.append("Missing methodology description")
        
        if not design.statistical_tests:
            warnings.append("No statistical tests specified")
        
        if not design.validity_considerations:
            warnings.append("No validity considerations provided")
        
        # Check sample size
        if "power analysis" in design.sample_size_recommendation.lower():
            if "n≥" not in design.sample_size_recommendation:
                warnings.append("Sample size recommendation should specify minimum sample size")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "score": max(0, 1.0 - len(issues) * 0.3 - len(warnings) * 0.1)
        }

