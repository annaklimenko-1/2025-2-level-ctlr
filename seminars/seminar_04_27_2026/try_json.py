"""
Listing for practice with json module
"""

# pylint: disable=unspecified-encoding

import json


def main() -> None:
    """
    Entrypoint for a seminar's listing
    """
    # 1. Create JSON file from a dictionary
    student = {"name": "John", "surname": "Davis", "age": 15, "hobbies": ["sport", "reading"]}

    # 2. Write dict to JSON
    with open("sample.json", "w", encoding="utf-8") as f:
        json.dump(student, f, ensure_ascii=True, indent=4, separators=(", ", ": "))

    # 3. Read from JSON
    with open("sample.json", "r", encoding="utf-8") as f:
        content = json.load(f)

    print(f"JSON from file: {content}")

    # 4. Create from string
    raw_student: str = """
        {
            "name": "John",
            "surname": "Davis",
            "age": 15,
            "hobbies": [
                "sport",
                "reading"
            ]
        }
    """

    parsed_json = json.loads(raw_student)
    print(f"JSON from JSON-string: {parsed_json}")
    print(f"Get values: {parsed_json.values()}")
    print(f"Get keys: {parsed_json.keys()}")
    print(f"Access hobbies: {parsed_json.get('hobbies')}")


if __name__ == "__main__":
    main()
