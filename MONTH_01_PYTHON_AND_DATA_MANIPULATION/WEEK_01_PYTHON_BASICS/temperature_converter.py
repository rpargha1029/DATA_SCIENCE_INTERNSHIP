"""Week 1 Hands-On: Temperature Converter (Celsius, Fahrenheit, Kelvin)."""

import argparse


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9.0 / 5.0) + 32.0


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32.0) * 5.0 / 9.0


def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin."""
    if celsius < -273.15:
        raise ValueError("Temperature cannot be below absolute zero (-273.15 C).")
    return celsius + 273.15


def run_demo() -> None:
    """Run non-interactive sample conversions."""
    samples_c = [0.0, 25.0, 37.0, 100.0]
    print("=== Temperature Converter Demo ===")
    for temp_c in samples_c:
        temp_f = celsius_to_fahrenheit(temp_c)
        temp_k = celsius_to_kelvin(temp_c)
        print(f"{temp_c:6.2f} C -> {temp_f:6.2f} F | {temp_k:6.2f} K")


def run_interactive() -> None:
    """Interactive CLI temperature converter using loops and conditionals."""
    print("=== Interactive Temperature Converter ===")
    while True:
        print("\nOptions: 1) C to F  2) F to C  3) C to K  4) Exit")
        choice = input("Select an option (1-4): ").strip()
        if choice == "4":
            print("Exiting temperature converter.")
            break
        if choice not in {"1", "2", "3"}:
            print("Invalid option. Please choose 1, 2, 3, or 4.")
            continue
        try:
            value = float(input("Enter temperature value: ").strip())
            if choice == "1":
                print(f"Result: {celsius_to_fahrenheit(value):.2f} F")
            elif choice == "2":
                print(f"Result: {fahrenheit_to_celsius(value):.2f} C")
            elif choice == "3":
                print(f"Result: {celsius_to_kelvin(value):.2f} K")
        except ValueError as exc:
            print(f"Input error: {exc}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Temperature Converter")
    parser.add_argument("--demo", action="store_true", help="Run non-interactive demo")
    args = parser.parse_args()
    if args.demo:
        run_demo()
    else:
        run_interactive()
