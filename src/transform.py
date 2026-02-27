import argparse
import csv
import json
from itertools import groupby
from operator import itemgetter
from typing import Any

Mapping = dict[str, str | dict[str, str]]
GroupedCatalog = dict[str, str | dict[str, str | list[dict[str, str]]]]


def process_price_catalog(price_catalog_file: str, mapping) -> list[dict[str, str]]:
    result = []
    with open(price_catalog_file) as file:
        catalog = csv.DictReader(file, delimiter=";")
        for row in catalog:
            cur = {}
            for cat_field, value in row.items():
                if cat_field not in mapping:
                    cur[cat_field] = value
                else:
                    new_field_name = mapping[cat_field]["destination_type"]
                    value_mapping = mapping[cat_field]["values"]
                    cur[new_field_name] = value_mapping[value]

            # process composite fields
            for source in mapping:
                comp_filds = source.split("|")
                if len(comp_filds) > 1:
                    comp_value = []
                    for source_field in comp_filds:
                        comp_value.append(row[source_field])

                    new_field_name = mapping[source]["destination_type"]
                    value_mapping = mapping[source]["values"]
                    cur[new_field_name] = value_mapping["|".join(comp_value)]

            result.append(cur)

    return result


def get_mapping(mapping_file: str) -> Mapping:
    mapping: dict[str, Any] = dict()

    with open(mapping_file) as file:
        mappings = csv.reader(file, delimiter=";")
        # skip the header
        next(mappings)

        for row in mappings:
            source, destination, source_type, destination_type = row
            if source_type in mapping:
                mapping[source_type]["values"][source] = destination
            else:
                mapping[source_type] = {
                    "destination_type": destination_type,
                    "values": {source: destination},
                }

    return mapping


def group_price_catalog(reformatted_catalog) -> GroupedCatalog:
    grouped = {}

    get_article_number = itemgetter("article_number")
    reformatted_catalog.sort(key=get_article_number)
    grouped_data = {}
    for article_number, group in groupby(reformatted_catalog, key=get_article_number):
        grouped_data[article_number] = list(group)

    for article_number, variations in grouped_data.items():
        for variation in variations:
            if "brand" not in grouped:
                grouped["brand"] = variation["brand"]
            if "articles" not in grouped:
                grouped["articles"] = []

        grouped_variations = []
        for record in variations:
            del record[
                "brand"
            ]  # remove the brand (as it's required in the task) and keep other fields
            grouped_variations.append(record)

        variation = {"article_number": article_number, "variations": grouped_variations}
        grouped["articles"].append(variation)

    return {"catalog": grouped}


def dump_to_json(data: GroupedCatalog, output_file: str):
    with open(output_file, "w") as f:
        json.dump(data, f)


def transform(pricat: str, mapping: str, output: str):
    catalog_mapping = get_mapping(mapping)
    reformated = process_price_catalog(pricat, catalog_mapping)
    aggregated = group_price_catalog(reformated)
    dump_to_json(aggregated, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="FashionCloud challenge",
        description="The program takes the data from price catalog file, transforms it and saves the results into json.file",
    )
    parser.add_argument("--pricat", help="Price catalog csv file")
    parser.add_argument("--mappings", help="Mappins csv file")
    parser.add_argument("--output", help="Output json file")

    args = parser.parse_args()
    transform(args.pricat, args.mappings, args.output)
