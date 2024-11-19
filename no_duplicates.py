import json

def make_hashable(value):
    """Recursively converts a non-hashable value (list/dict) to a hashable type."""
    if isinstance(value, dict):
        return tuple((k, make_hashable(v)) for k, v in sorted(value.items()))
    elif isinstance(value, list):
        return tuple(make_hashable(i) for i in value)
    return value  # If it's already hashable (str, int, etc.), return it as is.

def clean_entry(entry):
    """Removes unwanted keys from an entry."""
    keys_to_remove = ["id", "_version_"]
    return {k: v for k, v in entry.items() if k not in keys_to_remove}

def remove_duplicates_and_clean(json_data):
    """Removes duplicates and specified keys from JSON data."""
    seen = set()
    unique_data = []
    for entry in json_data:
        cleaned_entry = clean_entry(entry)  # Remove unwanted fields
        entry_tuple = tuple((k, make_hashable(v)) for k, v in sorted(cleaned_entry.items()))
        if entry_tuple not in seen:
            seen.add(entry_tuple)
            unique_data.append(cleaned_entry)
    return unique_data

# Example usage
if __name__ == "__main__":
    # Load JSON data from file
    with open("drugs_subset.json", "r") as infile:
        json_data = json.load(infile)

    # Remove duplicates and unwanted fields
    cleaned_data = remove_duplicates_and_clean(json_data)

    # Write cleaned JSON data to a new file
    with open("drugs_subset_normalized.json", "w") as outfile:
        json.dump(cleaned_data, outfile, indent=4)

    print("Duplicates removed and unwanted fields cleaned. Saved to 'drugs_subset_normalized.json'")
