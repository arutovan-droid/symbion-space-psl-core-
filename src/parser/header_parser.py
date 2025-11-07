"""
PSL Header Parser
Implementation of §3.1 specification header parsing
"""

from typing import Dict, List


class PSLHeaderParser:
    """PSL header parser according to §3.1 specification"""
    
    def parse(self, header_text: str) -> Dict:
        """
        Parses PSL header:
        !psl v0.1
        context: kitchen
        goal: transform basic borscht into masterpiece
        constraints: time<=90min; budget<=12usd
        """
        result = {}
        lines = [line.strip() for line in header_text.split('\n') if line.strip()]
        
        for line in lines:
            if line.startswith('!psl'):
                result['version'] = self._parse_version(line)
            elif line.startswith('context:'):
                result['context'] = line.split(':', 1)[1].strip()
            elif line.startswith('goal:'):
                result['goal'] = line.split(':', 1)[1].strip()
            elif line.startswith('constraints:'):
                result['constraints'] = self._parse_constraints(line)
            elif line.startswith('resources:'):
                result['resources'] = self._parse_resources(line)
            elif line.startswith('skill:'):
                result['skill'] = self._parse_skill(line)
                
        return result
    
    def _parse_version(self, line: str) -> str:
        """Extract version from !psl declaration"""
        return line.split('v')[-1].strip()
    
    def _parse_constraints(self, line: str) -> List[str]:
        """Parse constraints into list"""
        constraints_str = line.split(':', 1)[1].strip()
        return [c.strip() for c in constraints_str.split(';') if c.strip()]
    
    def _parse_resources(self, line: str) -> List[str]:
        """Parse resources list"""
        resources_str = line.split(':', 1)[1].strip()
        if resources_str.startswith('[') and resources_str.endswith(']'):
            resources_str = resources_str[1:-1]
        return [r.strip() for r in resources_str.split(',') if r.strip()]
    
    def _parse_skill(self, line: str) -> str:
        """Parse skill level"""
        return line.split(':', 1)[1].strip()
