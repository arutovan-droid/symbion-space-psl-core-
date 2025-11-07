# symbion-space-psl-core-
PSL Core: First ontological language for symbiotic AI. Turns any task into executable reality contracts with anti-hallucination architecture. [FACT]/[HYP]/[ROLLBACK] structural honesty.
# PSL Core - Proto-Structural Language v0.1 (RC)


## 🏛️ Overview

PSL (Proto-Structural Language) is a declarative, contract-based language for hybrid intelligence (human × AI). It architecturally eliminates hallucinations by separating verified facts from creative hypotheses with mandatory rollback mechanisms.

> **Core Philosophy**: "Any garbage input, processed through PSL, transforms into structurally clean signal for resonant transformation"

## 🎯 Key Features

- **🧠 Anti-Hallucination Architecture**: Facts vs Hypotheses with mandatory rollbacks
- **📜 Declarative Contracts**: Describe **what** to achieve, not how to implement
- **⚡ Machine-Readable**: Simple AST and strict section ordering
- **🔍 Verifiable Metrics**: CSR, HRR, PSL-Coverage for quality assurance
- **🧩 Composable**: Reusable blocks and modular contract composition

## 🏗️ Architecture
PSL Core → Structural Gateway →Symbion space → Resonance Fabric → WuWei Engine


## 📦 Installation

```bash
git clone https://github.com/arutovan-droid/symbion-space-psl-core-.git
cd symbion-space-psl-core-
pip install -r requirements.txt
🚀 Quick Start
from src.parser.header_parser import PSLHeaderParser

# Parse PSL header
parser = PSLHeaderParser()
header = parser.parse("""
!psl v0.1
context: kitchen
goal: transform basic borscht into masterpiece
constraints: time<=90min; budget<=12usd
""")

print(header)
# {
#   'version': '0.1',
#   'context': 'kitchen',
#   'goal': 'transform basic borscht into masterpiece',
#   'constraints': ['time<=90min', 'budget<=12usd']
# }
📚 Examples
Kitchen - "Borscht as Family Masterpiece"
!psl v0.1
context: kitchen
goal: transform basic borscht into "family masterpiece" with repeatable results
constraints: time<=90min; budget<=12usd; serves=6; repeatability>=0.9
skill: novice

[FACT]
- Broth: beef brisket 600g, onion 1, carrot 1, bay leaf 2, 70-80 min.
- Sauté: beetroot 400g + tomato paste 2 tbsp + vinegar 1 tsp (stable color).

[TECHNIQUE]
- Sequence: broth → potatoes → cabbage → sauté → salt/pepper → rest.

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
🏷️ PSL Syntax (EBNF)
document      := header sections
header        := psl_decl context_decl goal_decl constraints_decl resources? skill?
psl_decl      := "!psl" "v" version
sections      := fact technique hyp rollback safety assumptions? checklist three_c gloss
fact          := "[FACT]" list
technique     := "[TECHNIQUE]" list
hyp           := "[HYP]" list
rollback      := "[ROLLBACK]" list
safety        := "[SAFETY]" list
checklist     := "[CHECKLIST]" list
three_c       := "[3C]" "clear:" yn "cheap:" yn "safe:" yn
gloss         := "[GLOSS]" textline

📊 Quality Metrics
CSR (Constraint Satisfaction Rate) - Percentage of satisfied constraints

HRR (Hallucination Rejection Rate) - Anti-hallucination effectiveness (1.0 = perfect)

PSL-Coverage - Percentage of mandatory sections completed

3C-Score - Clear/Cheap/Safe binary assessment
🔧 L-Rules Validator
python
from src.validator.l_rules import LRuleValidator

validator = LRuleValidator()
issues = validator.validate(psl_document)

# L-01: Strict section ordering (§3.2)
# L-02: HYP/ROLLBACK pairing requirement
# L-03: Numbers outside [FACT] generate warnings/errors
# L-04: Unit normalization (kcal, g, min, usd)
# L-05: Constraints must parse to valid predicates
# ... L-06 to L-10
🗂️ Project Structure
text
psl-core/
├── src/
│   ├── parser/          # EBNF parser (§3.3)
│   ├── validator/       # L-rules linter (§6)
│   ├── ast/            # JSON mapping (§7)
│   └── metrics/         # Acceptance metrics (§5)
├── examples/            # Specification examples (§9)
│   ├── kitchen/        # Cooking contracts
│   └── woodworking/    # Carpentry contracts
├── docs/               # Specification and documentation
├── tests/              # Unit and integration tests
└── requirements.txt
🎮 Integration with LUYS.OS
PSL Core serves as the foundational layer in the LUYS.OS architecture:

Structural Gateway → Extracts PSL from documents

Multimind Core → Generates thoughts based on PSL contracts

Resonance Fabric → Measures semantic resonance of PSL structures

WuWei Engine → Regulates control through PSL constraints

📖 Specification
Full PSL v0.1 (RC) specification available in /docs/specification.md covering:

§1 Philosophy and Ontology

§2 Design Goals

§3 EBNF Syntax

§4 Section Semantics

§5 Acceptance Metrics

§6 L-Rules Linter

§7 JSON AST Mapping

§8-14 Advanced Topics

🤝 Contributing
We welcome contributions! Please see our Contributing Guidelines for details.

Fork the repository

Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

Specification license: CC BY 4.0

🙏 Acknowledgments
Hovhannes - Architecture & Design

AI Co-author - Structural Synthesis

Symbion Space - Vision & Implementation

PSL Core - Building the ontological foundation for symbiotic intelligence. Every hypothesis insured, every fact verifiable, every contract executable.
