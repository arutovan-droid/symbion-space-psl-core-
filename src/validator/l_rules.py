# src/validator/l_rules.py
class LRuleValidator:
    """Complete L-rules validator according to §6 specification"""
    
    def __init__(self):
        self.issues = []
    
    def validate(self, document: PSLDocument) -> List[Dict]:
        """Validate document against all L-rules"""
        self.issues = []
        
        self._validate_l01_section_order(document)
        self._validate_l02_hyp_rollback_pairing(document)
        self._validate_l03_numbers_outside_fact(document)
        self._validate_l04_unit_normalization(document)
        self._validate_l05_constraints_parsing(document)
        self._validate_l06_checklist_constraints_link(document)
        self._validate_l07_three_c_completeness(document)
        self._validate_l08_safety_requirements(document)
        self._validate_l09_duplicate_items(document)
        self._validate_l10_sentence_clarity(document)
        
        return self.issues
    
    def _validate_l01_section_order(self, doc: PSLDocument):
        """L-01: Strict section ordering from §3.2"""
        expected_order = ['FACT', 'TECHNIQUE', 'HYP', 'ROLLBACK', 'SAFETY', 
                         'ASSUMPTIONS', 'CHECKLIST', '3C', 'GLOSS']
        
        actual_sections = [s for s in doc.sections.keys() if s in expected_order]
        expected_actual = [s for s in expected_order if s in actual_sections]
        
        if actual_sections != expected_actual:
            self.issues.append({
                'rule': 'L-01',
                'level': 'error',
                'message': f'Section order violation. Expected: {expected_actual}, Got: {actual_sections}'
            })
    
    def _validate_l02_hyp_rollback_pairing(self, doc: PSLDocument):
        """L-02: HYP/ROLLBACK pairing requirement"""
        hyp_count = len(doc.sections.get('HYP', []))
        rollback_count = len(doc.sections.get('ROLLBACK', []))
        
        if hyp_count != rollback_count:
            self.issues.append({
                'rule': 'L-02', 
                'level': 'error',
                'message': f'HYP/ROLLBACK count mismatch. HYP: {hyp_count}, ROLLBACK: {rollback_count}'
            })
    
    def _validate_l03_numbers_outside_fact(self, doc: PSLDocument):
        """L-03: Numbers outside [FACT] generate warnings"""
        number_pattern = r'\b\d+\.?\d*\s*(?:usd|min|g|kg|kcal|°C|mm|cm)\b'
        
        for section_name, items in doc.sections.items():
            if section_name == 'FACT':
                continue
                
            for i, item in enumerate(items):
                if re.search(number_pattern, item, re.IGNORECASE):
                    self.issues.append({
                        'rule': 'L-03',
                        'level': 'warning', 
                        'message': f'Number found in [{section_name}]: {item}'
                    })
