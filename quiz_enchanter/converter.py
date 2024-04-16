import csv
import json

from . import Vocabularies


class JsonLoader:
    def dumps(self, vocabularies, indent=2):
        return json.dumps(vocabularies.json, indent=indent)

    def dump(self, file, vocabularies, indent=2, encoding="utf-8"):
        json.dump(vocabularies.json, file, encoding=encoding, indent=indent)

    def loads(self, string):
        return Vocabularies.from_json(json.loads(string))

    def load(self, file, encoding="utf-8"):
        return Vocabularies.from_json(json.load(file, encoding=encoding))


class CSVLoader:
    CSV_FIELDNAMES = ("sources", "translations", "right_tries", "wrong_tries", "source_example", "target_example")

    def dump(self, file, vocabularies):
        writer = csv.DictWriter(
            file,
            fieldnames=self.CSV_FIELDNAMES,
            delimiter=";",
            lineterminator="\n"
        )
        writer.writeheader()

        for vocabulary in vocabularies.json["entries"]:
            raw_json = vocabulary
            formatted_json = dict(
                sources=raw_json["sources"],
                translations=raw_json["translations"],
                right_tries=raw_json["stats"]["right_tries"],
                wrong_tries=raw_json["stats"]["wrong_tries"],
                source_example=raw_json["source_example"],
                target_example=raw_json["target_example"]
            )
            writer.writerow(formatted_json)

    def load(self, file):
        reader = csv.DictReader(
            file
        )  # TODO

