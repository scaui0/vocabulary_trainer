import json

# path = Path(__file__).parent / input("Path: ")
path = "test.json"
while True:
    names = []
    while True:
        if name := input("Source name: "):
            names.append(name)
        else:
            break

    translations = []
    while True:
        if name := input("Translation: "):
            translations.append(name)
        else:
            break

    source_example = input("Source example: ")
    target_example = input("Translation example: ")

    with open(path, "r+") as file:
        current_data = json.load(file)
        current_data["entries"].append({
            "word": names,
            "translation": translations,
            "example": {
                "source": source_example,
                "target": target_example
            }
        })
        file.seek(0)
        json.dump(current_data, file, indent=2)
        # file.append(json.dumps(current_data))
        # json.dump(current_data, file)
