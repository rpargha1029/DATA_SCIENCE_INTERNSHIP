"""Week 1 Hands-On: Basic Calculator with Exception Handling."""

import argparse


def calculate(num1: float, num2: float, operator: str) -> float:
    """Perform arithmetic operation (+, -, *, /, **, %) on two numbers."""
    if operator == "+":
        return num1 + num2
    if operator == "-":
        return num1 - num2
    if operator == "*":
        return num1 * num2
    if operator == "/":
        if num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return num1 / num2
    if operator == "**":
        return num1 ** num2
    if operator == "%":
        if num2 == 0:
            raise ZeroDivisionError("Cannot compute modulo by zero.")
        return num1 % num2
    raise ValueError(f"Unsupported operator: {operator}")


def run_demo() -> None:
    """Run sample calculations."""
    cases = [
        (12, 4, "+"),
        (12, 4, "-"),
        (12, 4, "*"),
        (12, 4, "/"),
        (2, 5, "**"),
        (10, 0, "/"),
    ]
    print("=== Calculator Demo ===")
    for a, b, op in cases:
        try:
            res = calculate(a, b, op)
            print(f"{a} {op} {b} = {res}")
        except (ZeroDivisionError, ValueError) as exc:
            print(f"{a} {op} {b} -> Error: {exc}")


def run_interactive() -> None:
    """Interactive calculator loop."""
    print("=== Interactive Calculator ===")
    while True:
        op = input("\nEnter operator (+, -, *, /, **, %) or 'q' to quit: ").strip()
        if op.lower() == "q":
            print("Goodbye!")
            break
        try:
            a = float(input("Enter first number: ").strip())
            b = float(input("Enter second number: ").strip())
            print(f"Result: {calculate(a, b, op)}")
        except (ValueError, ZeroDivisionError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Python Calculator")
    parser.add_argument("--demo", action="store_true", help="Run non-interactive demo")
    args = parser.parse_args()
    if args.demo:
        run_demo()
    else:
        run_interactive()
