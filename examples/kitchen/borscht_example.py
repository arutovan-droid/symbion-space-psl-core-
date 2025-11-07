"""
Borscht Example from §9.1 specification
Demonstrates complete PSL contract for cooking
"""

BORSCHT_PSL = """
!psl v0.1
context: kitchen
goal: transform basic borscht into "family masterpiece" with repeatable results
constraints: time<=90min; budget<=12usd; serves=6; repeatability>=0.9
skill: novice

[FACT]
- Broth: beef brisket 600g, onion 1, carrot 1, bay leaf 2, 70-80 min.
- Sauté: beetroot 400g + tomato paste 2 tbsp + vinegar 1 tsp (stable color).
- Balance: sugar 1 tsp + lemon 1 tsp for acid-sweet profile.
- Finish: garlic 2 cloves, dill, sour cream 15%; rest 15 min covered.

[TECHNIQUE]
- Sequence: broth → potatoes → cabbage → sauté → salt/pepper → rest.
- Control: taste salt/acidity before rest; maintain timing.

[HYP]
- Bake beetroot 45 min instead of stewing for richer flavor.

[ROLLBACK]
- If beetroot tastes "earthy" — return to stewing + 1 tsp tomato paste.

[SAFETY]
- Dairy/vinegar allergies — warn; store max 48h at 0-4°C.

[CHECKLIST]
- time ≤90 min; budget ≤$12; 6 servings; taste stable with ≥90% repeatability.

[3C]
clear: yes cheap: yes safe: yes

[GLOSS]
Ritual delivering stable taste: order, timing, acidity control.
"""


def demonstrate_parsing():
    """Demonstrate parsing the borscht example"""
    from src.parser.header_parser import PSLHeaderParser
    
    parser = PSLHeaderParser()
    header = parser.parse(BORSCHT_PSL)
    print("Parsed Header:", header)


if __name__ == "__main__":
    demonstrate_parsing()
  
