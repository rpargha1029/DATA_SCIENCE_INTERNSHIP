"""Week 2 Hands-On: Data Structures, Functions, Lambda, Recursion, and Comprehensions."""

from typing import Dict, List, Set, Tuple


def sum_of_squares(numbers: List[int]) -> int:
    """Compute the sum of squares using list comprehension."""
    return sum([n ** 2 for n in numbers])


def recursive_sum(numbers: List[int]) -> int:
    """Recursively compute the sum of a list of integers."""
    if not numbers:
        return 0
    return numbers[0] + recursive_sum(numbers[1:])


def filter_even_numbers(numbers: List[int]) -> List[int]:
    """Filter even numbers using filter() and a lambda function."""
    return list(filter(lambda x: x % 2 == 0, numbers))


def demonstrate_data_structures() -> None:
    """Demonstrate lists, tuples, dictionaries, and sets."""
    # List: ordered, mutable
    scores: List[int] = [85, 92, 78, 92, 88]
    # Tuple: ordered, immutable
    coordinates: Tuple[float, float] = (28.6139, 77.2090)
    # Set: unordered, unique elements
    unique_scores: Set[int] = set(scores)
    # Dictionary: key-value mapping
    student_grades: Dict[str, str] = {"Alice": "A", "Bob": "B+", "Charlie": "A-"}

    print("=== Data Structures ===")
    print(f"List (scores):        {scores}")
    print(f"Tuple (coordinates):  {coordinates}")
    print(f"Set (unique scores):  {sorted(unique_scores)}")
    print(f"Dict (grades):        {student_grades}")

    sample_nums = [1, 2, 3, 4, 5, 6]
    squared_evens = [x ** 2 for x in sample_nums if x % 2 == 0]
    print("\n=== Functions, Lambda, Recursion, Comprehension ===")
    print(f"Input numbers:        {sample_nums}")
    print(f"Sum of squares:       {sum_of_squares(sample_nums)}")
    print(f"Recursive sum:        {recursive_sum(sample_nums)}")
    print(f"Even numbers (lambda):{filter_even_numbers(sample_nums)}")
    print(f"Squared evens (comp): {squared_evens}")


if __name__ == "__main__":
    demonstrate_data_structures()
