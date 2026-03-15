from src.parser.section_parser import parse_sections


def test_parse_sections_with_onto_and_resonance():
    lines = [
        "[FACT]",
        "- Verified statement",
        "[ONTO]",
        "- Ontological statement",
        "[RESONANCE]",
        "- Resonance statement",
        "[ROLLBACK]",
        "- Rollback statement",
        "[GLOSS]",
        "One-line gloss",
    ]

    doc = parse_sections(lines)

    assert "FACT" in doc
    assert "ONTO" in doc
    assert "RESONANCE" in doc
    assert "ROLLBACK" in doc
    assert "GLOSS" in doc

    assert doc["FACT"] == ["- Verified statement"]
    assert doc["ONTO"] == ["- Ontological statement"]
    assert doc["RESONANCE"] == ["- Resonance statement"]
    assert doc["ROLLBACK"] == ["- Rollback statement"]
    assert doc["GLOSS"] == "One-line gloss"
