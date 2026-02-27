import csv
from pprint import pprint
from typing import Any

PRICE_CATALOG_FILE = "data/pricat_1.csv"
MAPPING_FILE = "data/mappings_1.csv"


def process_price_catalog(mapping):
    result = []
    with open(PRICE_CATALOG_FILE) as file:
        catalog = csv.DictReader(file, delimiter=';')
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

def get_mapping():
    mapping: dict[str, Any] = dict()
    
    with open(MAPPING_FILE) as file:
        mappings = csv.reader(file, delimiter=';')
        header = next(mappings)
        print(header)

        for row in mappings:
            source, destination, source_type, destination_type = row
            if source_type in mapping:
                mapping[source_type]["values"][source] = destination
            else:
                mapping[source_type] = {
                    "destination_type": destination_type,
                    "values": {source: destination}
                }
                
    return mapping 
            



        

def main():
    catalog_mapping = get_mapping()
    # print(catalog_mapping)
    reformated = process_price_catalog(catalog_mapping)
    print(len(reformated))
    
    
if __name__ == "__main__":
    main()