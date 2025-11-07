"""
Tests for PSL Header Parser
"""

import pytest
from src.parser.header_parser import PSLHeaderParser


class TestPSLHeaderParser:
    def setup_method(self):
        self.parser = PSLHeaderParser()
    
    def test_basic_header_parsing(self):
        header_text = """
        !psl v0.1
        context: kitchen
        goal: test goal
        constraints: time<=10min
        """
        
        result = self.parser.parse(header_text)
        
        assert result['version'] == '0.1'
        assert result['context'] == 'kitchen'
        assert result['goal'] == 'test goal'
        assert result['constraints'] == ['time<=10min']
    
    def test_full_header_parsing(self):
        header_text = """
        !psl v0.1
        context: woodworking
        goal: create invisible joint
        constraints: time<=40min; tools=basic; damage=none
        resources: [saw, sandpaper, glue]
        skill: hobbyist
        """
        
        result = self.parser.parse(header_text)
        
        assert result['version'] == '0.1'
        assert result['context'] == 'woodworking'
        assert result['goal'] == 'create invisible joint'
        assert len(result['constraints']) == 3
        assert 'saw' in result['resources']
        assert result['skill'] == 'hobbyist'
