#!/usr/bin/env python3
"""
Probabilistic Era Decision Maker - Advanced Analysis Engine
Based on "Building AI Products In The Probabilistic Era" by Gian Segato

This script provides advanced decision-making capabilities for navigating
the transition from deterministic to probabilistic systems.
"""

import json
import math
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, Optional
from enum import Enum
import argparse

class SystemType(Enum):
    DETERMINISTIC = "deterministic"
    PROBABILISTIC = "probabilistic"
    HYBRID = "hybrid"

class IndustryType(Enum):
    SOFTWARE = "software"
    FINTECH = "fintech"
    HEALTHCARE = "healthcare"
    ECOMMERCE = "ecommerce"
    EDUCATION = "education"
    MEDIA = "media"
    GAMING = "gaming"
    ENTERPRISE = "enterprise"
    STARTUP = "startup"

class StageType(Enum):
    IDEATION = "ideation"
    MVP = "mvp"
    EARLY = "early"
    GROWTH = "growth"
    SCALE = "scale"
    ENTERPRISE = "enterprise"

@dataclass
class ScenarioInput:
    """Input parameters for scenario analysis"""
    industry: IndustryType
    product_type: str
    challenge: str
    stage: StageType
    uncertainty_tolerance: int  # 1-10
    innovation_priority: int    # 1-10
    cost_sensitivity: int       # 1-10
    team_size: Optional[int] = None
    current_revenue: Optional[float] = None
    user_base_size: Optional[int] = None

@dataclass
class SystemMetrics:
    """Metrics for evaluating system approaches"""
    fit_score: float
    cost_efficiency: float
    development_speed: float
    control_predictability: float
    scalability_potential: float
    risk_level: float
    learning_curve: float
    maintenance_overhead: float

@dataclass
class Recommendation:
    """Individual recommendation with priority and rationale"""
    title: str
    description: str
    priority: int  # 1-5
    effort_level: str  # "Low", "Medium", "High"
    timeline: str
    success_metrics: List[str]
    risks: List[str]
    next_steps: List[str]

@dataclass
class AnalysisResult:
    """Complete analysis result"""
    scenario: ScenarioInput
    deterministic_metrics: SystemMetrics
    probabilistic_metrics: SystemMetrics
    recommended_approach: SystemType
    confidence_score: float
    recommendations: List[Recommendation]
    key_insights: List[str]
    trajectory_analysis: Dict[str, any]

class ProbabilisticEraAnalyzer:
    """Main analyzer class for decision-making"""
    
    def __init__(self):
        self.industry_weights = self._initialize_industry_weights()
        self.stage_multipliers = self._initialize_stage_multipliers()
    
    def _initialize_industry_weights(self) -> Dict[IndustryType, Dict[str, float]]:
        """Initialize industry-specific weight factors"""
        return {
            IndustryType.SOFTWARE: {
                "uncertainty_factor": 1.2,
                "innovation_factor": 1.3,
                "cost_factor": 1.0,
                "ai_readiness": 0.9
            },
            IndustryType.FINTECH: {
                "uncertainty_factor": 0.7,
                "innovation_factor": 1.1,
                "cost_factor": 0.8,
                "ai_readiness": 0.8
            },
            IndustryType.HEALTHCARE: {
                "uncertainty_factor": 0.5,
                "innovation_factor": 0.9,
                "cost_factor": 0.6,
                "ai_readiness": 0.7
            },
            IndustryType.ECOMMERCE: {
                "uncertainty_factor": 1.0,
                "innovation_factor": 1.2,
                "cost_factor": 1.1,
                "ai_readiness": 0.8
            },
            IndustryType.EDUCATION: {
                "uncertainty_factor": 0.8,
                "innovation_factor": 1.0,
                "cost_factor": 0.9,
                "ai_readiness": 0.6
            }
        }
    
    def _initialize_stage_multipliers(self) -> Dict[StageType, Dict[str, float]]:
        """Initialize stage-specific multipliers"""
        return {
            StageType.IDEATION: {
                "speed_multiplier": 1.3,
                "cost_multiplier": 1.2,
                "risk_tolerance": 1.4
            },
            StageType.MVP: {
                "speed_multiplier": 1.2,
                "cost_multiplier": 1.1,
                "risk_tolerance": 1.2
            },
            StageType.EARLY: {
                "speed_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "risk_tolerance": 1.0
            },
            StageType.GROWTH: {
                "speed_multiplier": 0.9,
                "cost_multiplier": 0.8,
                "risk_tolerance": 0.8
            },
            StageType.SCALE: {
                "speed_multiplier": 0.7,
                "cost_multiplier": 0.6,
                "risk_tolerance": 0.6
            },
            StageType.ENTERPRISE: {
                "speed_multiplier": 0.6,
                "cost_multiplier": 0.5,
                "risk_tolerance": 0.4
            }
        }
    
    def analyze_scenario(self, scenario: ScenarioInput) -> AnalysisResult:
        """Perform complete scenario analysis"""
        
        # Calculate system metrics
        deterministic_metrics = self._calculate_deterministic_metrics(scenario)
        probabilistic_metrics = self._calculate_probabilistic_metrics(scenario)
        
        # Determine recommended approach
        recommended_approach, confidence = self._determine_recommendation(
            scenario, deterministic_metrics, probabilistic_metrics
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(scenario, recommended_approach)
        
        # Generate insights
        insights = self._generate_insights(scenario, deterministic_metrics, probabilistic_metrics)
        
        # Trajectory analysis
        trajectory = self._analyze_trajectory(scenario, recommended_approach)
        
        return AnalysisResult(
            scenario=scenario,
            deterministic_metrics=deterministic_metrics,
            probabilistic_metrics=probabilistic_metrics,
            recommended_approach=recommended_approach,
            confidence_score=confidence,
            recommendations=recommendations,
            key_insights=insights,
            trajectory_analysis=trajectory
        )
    
    def _calculate_deterministic_metrics(self, scenario: ScenarioInput) -> SystemMetrics:
        """Calculate metrics for deterministic approach"""
        industry_weights = self.industry_weights.get(scenario.industry, self.industry_weights[IndustryType.SOFTWARE])
        stage_multipliers = self.stage_multipliers.get(scenario.stage, self.stage_multipliers[StageType.EARLY])
        
        # Base calculations
        fit_score = max(1, 10 - scenario.uncertainty_tolerance - (scenario.innovation_priority - 5))
        fit_score *= industry_weights.get("uncertainty_factor", 1.0)
        
        cost_efficiency = max(1, 8 - scenario.cost_sensitivity)
        cost_efficiency *= stage_multipliers.get("cost_multiplier", 1.0)
        
        development_speed = 8 if scenario.stage in [StageType.MVP, StageType.EARLY] else 6
        development_speed *= stage_multipliers.get("speed_multiplier", 1.0)
        
        control_predictability = 9  # High for deterministic
        
        scalability_potential = 7 if "traditional" in scenario.product_type else 5
        
        risk_level = max(1, 10 - scenario.uncertainty_tolerance)
        learning_curve = 4  # Lower learning curve
        maintenance_overhead = 5  # Moderate maintenance
        
        return SystemMetrics(
            fit_score=min(10, max(1, fit_score)),
            cost_efficiency=min(10, max(1, cost_efficiency)),
            development_speed=min(10, max(1, development_speed)),
            control_predictability=min(10, max(1, control_predictability)),
            scalability_potential=min(10, max(1, scalability_potential)),
            risk_level=min(10, max(1, risk_level)),
            learning_curve=learning_curve,
            maintenance_overhead=maintenance_overhead
        )
    
    def _calculate_probabilistic_metrics(self, scenario: ScenarioInput) -> SystemMetrics:
        """Calculate metrics for probabilistic approach"""
        industry_weights = self.industry_weights.get(scenario.industry, self.industry_weights[IndustryType.SOFTWARE])
        stage_multipliers = self.stage_multipliers.get(scenario.stage, self.stage_multipliers[StageType.EARLY])
        
        # Base calculations
        fit_score = max(1, scenario.uncertainty_tolerance + (scenario.innovation_priority - 3))
        fit_score *= industry_weights.get("ai_readiness", 0.8)
        
        cost_efficiency = max(3, scenario.cost_sensitivity + 2)
        cost_efficiency *= (1 / stage_multipliers.get("cost_multiplier", 1.0))
        
        development_speed = 8 if scenario.stage in [StageType.GROWTH, StageType.SCALE] else 5
        development_speed *= industry_weights.get("innovation_factor", 1.0)
        
        control_predictability = max(2, 7 - scenario.uncertainty_tolerance)
        
        scalability_potential = 9 if "ai-native" in scenario.product_type else 7
        
        risk_level = scenario.uncertainty_tolerance
        learning_curve = 8  # Higher learning curve
        maintenance_overhead = 7  # Higher maintenance overhead
        
        return SystemMetrics(
            fit_score=min(10, max(1, fit_score)),
            cost_efficiency=min(10, max(1, cost_efficiency)),
            development_speed=min(10, max(1, development_speed)),
            control_predictability=min(10, max(1, control_predictability)),
            scalability_potential=min(10, max(1, scalability_potential)),
            risk_level=min(10, max(1, risk_level)),
            learning_curve=learning_curve,
            maintenance_overhead=maintenance_overhead
        )
    
    def _determine_recommendation(self, scenario: ScenarioInput, 
                                det_metrics: SystemMetrics, 
                                prob_metrics: SystemMetrics) -> Tuple[SystemType, float]:
        """Determine the recommended approach and confidence level"""
        
        # Calculate weighted scores
        det_score = (
            det_metrics.fit_score * 0.25 +
            det_metrics.cost_efficiency * 0.2 +
            det_metrics.development_speed * 0.15 +
            det_metrics.control_predictability * 0.2 +
            det_metrics.scalability_potential * 0.2
        )
        
        prob_score = (
            prob_metrics.fit_score * 0.25 +
            prob_metrics.cost_efficiency * 0.2 +
            prob_metrics.development_speed * 0.15 +
            prob_metrics.control_predictability * 0.1 +
            prob_metrics.scalability_potential * 0.3
        )
        
        # Determine recommendation
        score_diff = abs(det_score - prob_score)
        confidence = min(0.95, max(0.55, score_diff / 10 + 0.5))
        
        if score_diff < 1.5:
            return SystemType.HYBRID, confidence * 0.8
        elif det_score > prob_score:
            return SystemType.DETERMINISTIC, confidence
        else:
            return SystemType.PROBABILISTIC, confidence
    
    def _generate_recommendations(self, scenario: ScenarioInput, 
                                approach: SystemType) -> List[Recommendation]:
        """Generate specific recommendations based on analysis"""
        recommendations = []
        
        if approach == SystemType.PROBABILISTIC:
            recommendations.extend([
                Recommendation(
                    title="Implement Minimum Viable Intelligence Framework",
                    description="Establish quality thresholds that preserve AI flexibility while meeting market acceptance levels.",
                    priority=5,
                    effort_level="Medium",
                    timeline="2-4 weeks",
                    success_metrics=["User satisfaction > 80%", "Task completion rate > 70%", "Hallucination rate < 5%"],
                    risks=["Over-constraining the model", "Insufficient quality control"],
                    next_steps=["Define quality metrics", "Implement evaluation pipeline", "Set up monitoring"]
                ),
                Recommendation(
                    title="Transition to Empirical Development",
                    description="Adopt scientific method for product development with hypothesis-driven experiments.",
                    priority=4,
                    effort_level="High",
                    timeline="1-3 months",
                    success_metrics=["A/B test velocity increase", "Data-driven decisions > 80%", "Feature success rate improvement"],
                    risks=["Team resistance to change", "Longer initial development cycles"],
                    next_steps=["Train team on empirical methods", "Set up experimentation infrastructure", "Define success metrics"]
                ),
                Recommendation(
                    title="Build Trajectory Analysis System",
                    description="Implement user journey tracking for probabilistic interactions instead of traditional funnels.",
                    priority=3,
                    effort_level="High",
                    timeline="2-4 months",
                    success_metrics=["User journey visibility", "Improved retention prediction", "Better feature discovery"],
                    risks=["Complex implementation", "Privacy concerns", "Data storage costs"],
                    next_steps=["Design trajectory schema", "Implement tracking", "Build analysis dashboards"]
                )
            ])
        
        elif approach == SystemType.DETERMINISTIC:
            recommendations.extend([
                Recommendation(
                    title="Optimize Traditional SLOs and Metrics",
                    description="Strengthen existing reliability and performance monitoring systems.",
                    priority=5,
                    effort_level="Low",
                    timeline="1-2 weeks",
                    success_metrics=["99.9% uptime", "Response time < 200ms", "Error rate < 0.1%"],
                    risks=["Over-optimization", "Reduced innovation speed"],
                    next_steps=["Audit current metrics", "Implement monitoring", "Set up alerting"]
                ),
                Recommendation(
                    title="Selective AI Enhancement",
                    description="Add AI features to non-critical areas while maintaining deterministic core.",
                    priority=3,
                    effort_level="Medium",
                    timeline="1-2 months",
                    success_metrics=["Feature adoption > 60%", "No impact on core reliability", "User satisfaction increase"],
                    risks=["Feature complexity", "Inconsistent user experience"],
                    next_steps=["Identify enhancement opportunities", "Prototype AI features", "A/B test implementations"]
                )
            ])
        
        else:  # HYBRID
            recommendations.extend([
                Recommendation(
                    title="Implement Hybrid Architecture",
                    description="Design system with deterministic core and probabilistic enhancement layers.",
                    priority=5,
                    effort_level="High",
                    timeline="2-6 months",
                    success_metrics=["System reliability maintained", "AI feature adoption", "Performance balance achieved"],
                    risks=["Architecture complexity", "Integration challenges", "Maintenance overhead"],
                    next_steps=["Design architecture", "Implement core systems", "Add AI layers incrementally"]
                )
            ])
        
        # Add stage-specific recommendations
        if scenario.stage in [StageType.IDEATION, StageType.MVP]:
            recommendations.append(
                Recommendation(
                    title="Focus on Speed and Validation",
                    description="Prioritize rapid market validation over perfect implementation.",
                    priority=4,
                    effort_level="Medium",
                    timeline="2-8 weeks",
                    success_metrics=["Time to market", "User feedback quality", "Iteration speed"],
                    risks=["Technical debt", "Scalability issues"],
                    next_steps=["Define MVP scope", "Build quickly", "Gather feedback", "Iterate rapidly"]
                )
            )
        
        return sorted(recommendations, key=lambda x: x.priority, reverse=True)
    
    def _generate_insights(self, scenario: ScenarioInput, 
                         det_metrics: SystemMetrics, 
                         prob_metrics: SystemMetrics) -> List[str]:
        """Generate key insights from the analysis"""
        insights = []
        
        # Uncertainty tolerance insights
        if scenario.uncertainty_tolerance >= 8:
            insights.append("Your high uncertainty tolerance positions you well for probabilistic systems that can handle ambiguous inputs and provide creative solutions.")
        elif scenario.uncertainty_tolerance <= 3:
            insights.append("Your preference for predictability suggests focusing on deterministic systems with clear input-output mappings.")
        
        # Innovation vs reliability insights
        if scenario.innovation_priority >= 8:
            insights.append("Your innovation focus aligns with probabilistic approaches that can discover unexpected use cases and capabilities.")
        elif scenario.innovation_priority <= 3:
            insights.append("Your reliability focus suggests optimizing deterministic systems with proven engineering practices.")
        
        # Stage-specific insights
        if scenario.stage in [StageType.GROWTH, StageType.SCALE]:
            insights.append("Your stage provides the user base and data volume needed to effectively implement probabilistic systems.")
        elif scenario.stage in [StageType.IDEATION, StageType.MVP]:
            insights.append("At your stage, focus on rapid validation rather than perfect systems - consider hybrid approaches.")
        
        # Industry-specific insights
        industry_insights = {
            IndustryType.FINTECH: "Financial services require balancing innovation with regulatory compliance - consider hybrid approaches.",
            IndustryType.HEALTHCARE: "Healthcare applications need high reliability for critical functions while benefiting from AI in diagnostic support.",
            IndustryType.SOFTWARE: "Software development tools can leverage AI for code generation while maintaining deterministic build processes.",
            IndustryType.ECOMMERCE: "E-commerce benefits from AI personalization while keeping transaction processing deterministic."
        }
        
        if scenario.industry in industry_insights:
            insights.append(industry_insights[scenario.industry])
        
        return insights
    
    def _analyze_trajectory(self, scenario: ScenarioInput, approach: SystemType) -> Dict[str, any]:
        """Analyze potential trajectories and outcomes"""
        
        trajectory = {
            "approach": approach.value,
            "timeline_phases": [],
            "success_probability": 0.0,
            "risk_factors": [],
            "success_indicators": []
        }
        
        # Define phases based on approach
        if approach == SystemType.PROBABILISTIC:
            trajectory["timeline_phases"] = [
                {"phase": "Foundation", "duration": "1-3 months", "focus": "Data infrastructure and evaluation systems"},
                {"phase": "Implementation", "duration": "3-6 months", "focus": "Core AI features and user feedback loops"},
                {"phase": "Optimization", "duration": "6-12 months", "focus": "Trajectory analysis and empirical improvements"},
                {"phase": "Scale", "duration": "12+ months", "focus": "Advanced AI capabilities and market expansion"}
            ]
            trajectory["success_probability"] = min(0.9, 0.5 + (scenario.uncertainty_tolerance + scenario.innovation_priority) / 20)
            
        elif approach == SystemType.DETERMINISTIC:
            trajectory["timeline_phases"] = [
                {"phase": "Optimization", "duration": "2-4 weeks", "focus": "SLO improvements and monitoring"},
                {"phase": "Enhancement", "duration": "1-3 months", "focus": "Selective AI feature addition"},
                {"phase": "Refinement", "duration": "3-6 months", "focus": "Performance optimization and reliability"},
                {"phase": "Evolution", "duration": "6+ months", "focus": "Gradual AI integration where appropriate"}
            ]
            trajectory["success_probability"] = min(0.95, 0.7 + (20 - scenario.uncertainty_tolerance - scenario.innovation_priority) / 40)
        
        else:  # HYBRID
            trajectory["timeline_phases"] = [
                {"phase": "Architecture", "duration": "1-2 months", "focus": "Hybrid system design"},
                {"phase": "Core Build", "duration": "2-4 months", "focus": "Deterministic foundation"},
                {"phase": "AI Integration", "duration": "3-6 months", "focus": "Probabilistic layer addition"},
                {"phase": "Optimization", "duration": "6+ months", "focus": "Balance and performance tuning"}
            ]
            trajectory["success_probability"] = 0.75
        
        # Risk factors
        if scenario.cost_sensitivity >= 8:
            trajectory["risk_factors"].append("High cost sensitivity may limit AI implementation options")
        if scenario.stage == StageType.ENTERPRISE:
            trajectory["risk_factors"].append("Enterprise constraints may slow innovation adoption")
        if scenario.uncertainty_tolerance <= 3 and approach == SystemType.PROBABILISTIC:
            trajectory["risk_factors"].append("Low uncertainty tolerance conflicts with probabilistic approach")
        
        # Success indicators
        trajectory["success_indicators"] = [
            "User engagement metrics improvement",
            "Feature adoption rates",
            "System reliability maintenance",
            "Cost efficiency achievement",
            "Team productivity increase"
        ]
        
        return trajectory

def main():
    """Command-line interface for the analyzer"""
    parser = argparse.ArgumentParser(description="Probabilistic Era Decision Maker")
    parser.add_argument("--industry", type=str, required=True, choices=[e.value for e in IndustryType])
    parser.add_argument("--product-type", type=str, required=True)
    parser.add_argument("--challenge", type=str, required=True)
    parser.add_argument("--stage", type=str, required=True, choices=[e.value for e in StageType])
    parser.add_argument("--uncertainty", type=int, required=True, choices=range(1, 11))
    parser.add_argument("--innovation", type=int, required=True, choices=range(1, 11))
    parser.add_argument("--cost", type=int, required=True, choices=range(1, 11))
    parser.add_argument("--output", type=str, default="analysis_result.json")
    
    args = parser.parse_args()
    
    # Create scenario
    scenario = ScenarioInput(
        industry=IndustryType(args.industry),
        product_type=args.product_type,
        challenge=args.challenge,
        stage=StageType(args.stage),
        uncertainty_tolerance=args.uncertainty,
        innovation_priority=args.innovation,
        cost_sensitivity=args.cost
    )
    
    # Analyze
    analyzer = ProbabilisticEraAnalyzer()
    result = analyzer.analyze_scenario(scenario)
    
    # Output results
    output_dict = asdict(result)
    
    with open(args.output, 'w') as f:
        json.dump(output_dict, f, indent=2, default=str)
    
    print(f"Analysis complete! Results saved to {args.output}")
    print(f"Recommended approach: {result.recommended_approach.value}")
    print(f"Confidence: {result.confidence_score:.2%}")
    print(f"Top recommendation: {result.recommendations[0].title}")

if __name__ == "__main__":
    main()