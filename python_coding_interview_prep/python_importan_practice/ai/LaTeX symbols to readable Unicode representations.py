import re


def convert_latex_to_text(latex_str: str) -> str:
    """Converts a LaTeX equation string into clean human-readable math and plain text explanations."""
    # Mapping LaTeX symbols to readable Unicode representations
    replacements = {
        r"\Delta": "Δ",
        r"\alpha": "α",
        r"\cdot": "·",
        r"\mathbf": "",
        r"\vec": "",
        r"\_": "_",
        r"\ ": " ",
    }

    cleaned = latex_str
    for k, v in replacements.items():
        cleaned = cleaned.replace(k, v)

    # Convert \frac{num}{den} -> (num / den)
    cleaned = re.sub(r"\\frac\{([^}]+)\}\{([^}]+)\}", r"(\1 / \2)", cleaned)

    # Clean up excess whitespace/brackets
    cleaned = re.sub(r"[{}]", "", cleaned)

    return cleaned


def print_formula_breakdown(latex_str: str):
    readable = convert_latex_to_text(latex_str)

    print("=" * 60)
    print("ORIGINAL LATEX:")
    print(latex_str)
    print("-" * 60)
    print("HUMAN-READABLE FORMULA:")
    print(f"  {readable}")
    print("=" * 60)


if __name__ == "__main__":
    # The LoRA (Low-Rank Adaptation) linear transformation equation
    cryptic_equation = r"h = W_0 x + \Delta W x = W_0 x + \frac{\alpha}{r} (B \cdot A) x"

    print_formula_breakdown(cryptic_equation)