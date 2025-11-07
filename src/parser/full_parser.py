# src/parser/full_parser.py
class PSLFullParser:
    """Complete PSL parser according to §3.2-3.3 specification"""
    
    def parse(self, psl_text: str) -> PSLDocument:
        """
        Parse complete PSL document with all sections
        """
        lines = [line.rstrip() for line in psl_text.split('\n')]
        header_end = self._find_header_end(lines)
        
        # Parse header and sections separately
        header_text = '\n'.join(lines[:header_end])
        sections_text = '\n'.join(lines[header_end:])
        
        header_data = self._parse_header(header_text)
        sections_data = self._parse_sections(sections_text)
        
        return PSLDocument(
            version=header_data['version'],
            context=header_data['context'],
            goal=header_data['goal'],
            constraints=header_data['constraints'],
            resources=header_data.get('resources'),
            skill=header_data.get('skill'),
            sections=sections_data,
            three_c=sections_data.get('3C'),
            gloss=sections_data.get('GLOSS')
        )
    
    def _parse_sections(self, text: str) -> Dict[str, List[str]]:
        """Parse all PSL sections according to §3.2 order"""
        sections = {}
        current_section = None
        current_items = []
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check for section header
            if line.startswith('[') and line.endswith(']'):
                # Save previous section
                if current_section:
                    sections[current_section] = current_items
                
                # Start new section
                current_section = line[1:-1].split(':')[0]  # Remove brackets
                current_items = []
            elif current_section and line.startswith(('-', '1)', '2)')):
                # Parse list item
                item = line.lstrip('- ').lstrip('1234567890) ')
                current_items.append(item)
            elif current_section == '3C' and ':' in line:
                # Special handling for 3C section
                sections['3C'] = self._parse_three_c(text)
                break
        
        # Don't forget the last section
        if current_section and current_items:
            sections[current_section] = current_items
            
        return sections
    
    def _parse_three_c(self, text: str) -> ThreeC:
        """Parse [3C] section with clear/cheap/safe values"""
        clear = 'clear: yes' in text.lower()
        cheap = 'cheap: yes' in text.lower() 
        safe = 'safe: yes' in text.lower()
        return ThreeC(clear=clear, cheap=cheap, safe=safe)
