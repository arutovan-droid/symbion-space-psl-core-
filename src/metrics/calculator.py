"""
PSL Metrics Calculator
Implementation of acceptance metrics according to §5 specification
"""

from typing import Dict, List, Optional
from ..ast.models import PSLDocument, Constraint


class PSLMetricsCalculator:
    """
    Calculate PSL acceptance metrics according to §5 specification:
    - CSR (Constraint Satisfaction Rate)
    - HRR (Hallucination Rejection Rate) 
    - PSL-Coverage
    - 3C-Score
    """
    
    def calculate_all_metrics(self, document: PSLDocument, 
                            execution_result: Optional[Dict] = None) -> Dict[str, float]:
        """
        Calculate all acceptance metrics for a PSL document
        
        Args:
            document: Parsed PSL document
            execution_result: Optional execution results for constraint validation
            
        Returns:
            Dictionary with all metric scores
        """
        return {
            'csr': self.calculate_csr(document, execution_result),
            'hrr': self.calculate_hrr(document),
            'psl_coverage': self.calculate_psl_coverage(document),
            'three_c_score': self.calculate_three_c_score(document)
        }
    
    def calculate_csr(self, document: PSLDocument, 
                     execution_result: Optional[Dict] = None) -> float:
        """
        CSR - Constraint Satisfaction Rate (§5)
        Percentage of satisfied constraints from execution results
        
        Args:
            document: PSL document with constraints
            execution_result: Dict with actual values for constraint validation
                           Example: {'time': 85, 'budget': 10, 'serves': 6}
        
        Returns:
            Float between 0.0 and 1.0 representing satisfaction rate
        """
        if not document.constraints:
            return 1.0  # No constraints = fully satisfied
            
        if not execution_result:
            return 0.0  # Cannot validate without execution results
            
        satisfied_count = 0
        
        for constraint in document.constraints:
            actual_value = execution_result.get(constraint.name)
            
            if actual_value is None:
                continue  # Skip constraints without execution data
                
            if self._is_constraint_satisfied(constraint, actual_value):
                satisfied_count += 1
        
        return satisfied_count / len(document.constraints) if document.constraints else 1.0
    
    def calculate_hrr(self, document: PSLDocument) -> float:
        """
        HRR - Hallucination Rejection Rate (§5)
        Measures anti-hallucination effectiveness
        
        Scoring:
        - 1.0: Perfect (no facts outside [FACT], all HYP have ROLLBACK)
        - <1.0: Penalties for violations
        
        Returns:
            Float between 0.0 and 1.0
        """
        base_score = 1.0
        penalties = 0.0
        
        # Check for numbers outside [FACT] section
        numbers_outside_fact = self._count_numbers_outside_fact(document)
        if numbers_outside_fact > 0:
            penalties += numbers_outside_fact * 0.1  # 10% penalty per violation
        
        # Check HYP/ROLLBACK pairing
        hyp_count = len(document.sections.get('HYP', []))
        rollback_count = len(document.sections.get('ROLLBACK', []))
        if hyp_count != rollback_count:
            penalties += 0.2  # 20% penalty for pairing mismatch
        
        # Check for mandatory safety when risks exist
        if self._has_risk_constraints(document) and 'SAFETY' not in document.sections:
            penalties += 0.15  # 15% penalty for missing safety
        
        return max(0.0, base_score - penalties)
    
    def calculate_psl_coverage(self, document: PSLDocument) -> float:
        """
        PSL-Coverage - Percentage of mandatory sections completed (§5)
        
        Mandatory sections: FACT, TECHNIQUE, HYP, ROLLBACK, SAFETY, CHECKLIST, 3C
        
        Returns:
            Float between 0.0 and 1.0
        """
        mandatory_sections = ['FACT', 'TECHNIQUE', 'HYP', 'ROLLBACK', 'SAFETY', 'CHECKLIST', '3C']
        
        completed = 0
        for section in mandatory_sections:
            if section in document.sections:
                # For 3C, check if it's properly parsed
                if section == '3C' and document.three_c is not None:
                    completed += 1
                elif section != '3C':
                    completed += 1
        
        return completed / len(mandatory_sections)
    
    def calculate_three_c_score(self, document: PSLDocument) -> float:
        """
        3C-Score - Assessment of Clear/Cheap/Safe qualities (§5)
        
        Returns:
            Float between 0.0 and 1.0 based on 3C assessment
        """
        if not document.three_c:
            return 0.0
            
        score = 0.0
        if document.three_c.clear:
            score += 0.34
        if document.three_c.cheap:
            score += 0.33
        if document.three_c.safe:
            score += 0.33
            
        return score
    
    def _is_constraint_satisfied(self, constraint: Constraint, actual_value: float) -> bool:
        """Check if a constraint is satisfied by actual value"""
        try:
            if constraint.operator == '<=':
                return actual_value <= constraint.value
            elif constraint.operator == '>=':
                return actual_value >= constraint.value
            elif constraint.operator == '<':
                return actual_value < constraint.value
            elif constraint.operator == '>':
                return actual_value > constraint.value
            elif constraint.operator == '=':
                return actual_value == constraint.value
            else:
                return False
        except (TypeError, ValueError):
            return False
    
    def _count_numbers_outside_fact(self, document: PSLDocument) -> int:
        """Count numbers with units outside FACT section"""
        import re
        number_pattern = r'\b\d+\.?\d*\s*(?:usd|min|g|kg|kcal|°C|mm|cm|serves)\b'
        count = 0
        
        for section_name, items in document.sections.items():
            if section_name == 'FACT':
                continue
                
            for item in items:
                if re.search(number_pattern, item, re.IGNORECASE):
                    count += 1
        
        return count
    
    def _has_risk_constraints(self, document: PSLDocument) -> bool:
        """Check if document has constraints indicating risks"""
        risk_keywords = ['allerg', 'danger', 'risk', 'safe', 'toxic', 'harm', 'warn']
        
        for constraint in document.constraints:
            constraint_str = f"{constraint.name} {constraint.operator} {constraint.value} {constraint.unit or ''}"
            if any(keyword in constraint_str.lower() for keyword in risk_keywords):
                return True
        
        for section_name, items in document.sections.items():
            for item in items:
                if any(keyword in item.lower() for keyword in risk_keywords):
                    return True
        
        return False


# Utility function for quick metric assessment
def assess_psl_quality(psl_text: str, execution_result: Optional[Dict] = None) -> Dict:
    """
    Quick quality assessment for PSL text
    
    Args:
        psl_text: Raw PSL text
        execution_result: Optional execution results
        
    Returns:
        Dict with metrics and quality assessment
    """
    from ..parser.full_parser import PSLFullParser
    from ..validator.l_rules import LRuleValidator
    
    try:
        # Parse document
        parser = PSLFullParser()
        document = parser.parse(psl_text)
        
        # Validate
        validator = LRuleValidator()
        issues = validator.validate(document)
        
        # Calculate metrics
        calculator = PSLMetricsCalculator()
        metrics = calculator.calculate_all_metrics(document, execution_result)
        
        # Overall quality score (weighted average)
        weights = {'csr': 0.3, 'hrr': 0.4, 'psl_coverage': 0.2, 'three_c_score': 0.1}
        quality_score = sum(metrics[key] * weights[key] for key in weights)
        
        return {
            'metrics': metrics,
            'quality_score': quality_score,
            'validation_issues': len(issues),
            'quality_level': _get_quality_level(quality_score),
            'document': document
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'metrics': {},
            'quality_score': 0.0,
            'validation_issues': 0,
            'quality_level': 'ERROR'
        }


def _get_quality_level(score: float) -> str:
    """Convert numeric score to quality level"""
    if score >= 0.9:
        return 'EXCELLENT'
    elif score >= 0.7:
        return 'GOOD'
    elif score >= 0.5:
        return 'FAIR'
    else:
        return 'POOR'
