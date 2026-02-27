from src.transform import process_price_catalog, get_mapping, group_price_catalog


class TestTransform:
    def test_mapping(self):
        mapping = get_mapping("./tests/mappings_test.csv")
        # Alternatively we can put the expected result in a file
        assert mapping == {
            "article_structure_code": {
                "destination_type": "article_structure",
                "values": {
                    "10": "Pump",
                    "4": "Boot",
                    "5": "Sneaker",
                    "6": "Slipper",
                    "7": "Loafer",
                    "8": "Mocassin",
                    "9": "Sandal",
                },
            },
            "collection": {
                "destination_type": "collection",
                "values": {"NW 17-18": "Winter Collection 2017/2018"},
            },
            "color_code": {
                "destination_type": "color",
                "values": {
                    "1": "Nero",
                    "2": "Marrone",
                    "3": "Brandy Nero",
                    "4": "Indaco Nero",
                    "5": "Fucile",
                    "6": "Bosco Nero",
                },
            },
            "season": {
                "destination_type": "season",
                "values": {"summer": "Summer", "winter": "Winter"},
            },
            "size_group_code|size_code": {
                "destination_type": "size",
                "values": {
                    "EU|36": "European size 36",
                    "EU|37": "European size 37",
                    "EU|38": "European size 38",
                    "EU|39": "European size 39",
                    "EU|40": "European size 40",
                    "EU|41": "European size 41",
                    "EU|42": "European size 42",
                },
            },
        }

    def test_process_price_catalog(self):
        mapping = get_mapping("./tests/mappings_test.csv")
        result = process_price_catalog("./tests/pricat_test.csv", mapping)
        assert len(result) == 5, "We should process all the records from the file"
        # Alternatively we can put the expected result in a file
        assert result == [
            {
                "article_number": "15189-02",
                "article_number_2": "15189-02 Aviation Nero",
                "article_number_3": "Aviation",
                "article_structure": "Pump",
                "brand": "Via Vai",
                "catalog_code": "",
                "collection": "Winter Collection 2017/2018",
                "color": "Nero",
                "currency": "EUR",
                "discount_rate": "",
                "ean": "8719245200978",
                "material": "Aviation",
                "price_buy_gross": "",
                "price_buy_net": "58.5",
                "price_sell": "139.95",
                "season": "Winter",
                "size": "European size 38",
                "size_code": "38",
                "size_group_code": "EU",
                "size_name": "38",
                "supplier": "Rupesco BV",
                "target_area": "Woman Shoes",
            },
            {
                "article_number": "15189-02",
                "article_number_2": "15189-02 Aviation Nero",
                "article_number_3": "Aviation",
                "article_structure": "Pump",
                "brand": "Via Vai",
                "catalog_code": "",
                "collection": "Winter Collection 2017/2018",
                "color": "Nero",
                "currency": "EUR",
                "discount_rate": "",
                "ean": "8719245201005",
                "material": "Aviation",
                "price_buy_gross": "",
                "price_buy_net": "58.5",
                "price_sell": "139.95",
                "season": "Winter",
                "size": "European size 41",
                "size_code": "41",
                "size_group_code": "EU",
                "size_name": "41",
                "supplier": "Rupesco BV",
                "target_area": "Woman Shoes",
            },
            {
                "article_number": "15189-02",
                "article_number_2": "15189-02 Mojito Bosco Nero",
                "article_number_3": "Mojito",
                "article_structure": "Pump",
                "brand": "Via Vai",
                "catalog_code": "",
                "collection": "Winter Collection 2017/2018",
                "color": "Bosco Nero",
                "currency": "EUR",
                "discount_rate": "",
                "ean": "8719245231637",
                "material": "Mojito",
                "price_buy_gross": "",
                "price_buy_net": "62.5",
                "price_sell": "149.95",
                "season": "Winter",
                "size": "European size 40",
                "size_code": "40",
                "size_group_code": "EU",
                "size_name": "40",
                "supplier": "Rupesco BV",
                "target_area": "Woman Shoes",
            },
            {
                "article_number": "15189-02",
                "article_number_2": "15189-02 Mojito Bosco Nero",
                "article_number_3": "Mojito",
                "article_structure": "Pump",
                "brand": "Via Vai",
                "catalog_code": "",
                "collection": "Winter Collection 2017/2018",
                "color": "Bosco Nero",
                "currency": "EUR",
                "discount_rate": "",
                "ean": "8719245231606",
                "material": "Mojito",
                "price_buy_gross": "",
                "price_buy_net": "62.5",
                "price_sell": "149.95",
                "season": "Winter",
                "size": "European size 37",
                "size_code": "37",
                "size_group_code": "EU",
                "size_name": "37",
                "supplier": "Rupesco BV",
                "target_area": "Woman Shoes",
            },
            {
                "article_number": "15189-02",
                "article_number_2": "15189-02 Mojito Brandy Nero",
                "article_number_3": "Mojito",
                "article_structure": "Pump",
                "brand": "Via Vai",
                "catalog_code": "",
                "collection": "Winter Collection 2017/2018",
                "color": "Brandy Nero",
                "currency": "EUR",
                "discount_rate": "",
                "ean": "8719245231682",
                "material": "Mojito",
                "price_buy_gross": "",
                "price_buy_net": "62.5",
                "price_sell": "149.95",
                "season": "Winter",
                "size": "European size 37",
                "size_code": "37",
                "size_group_code": "EU",
                "size_name": "37",
                "supplier": "Rupesco BV",
                "target_area": "Woman Shoes",
            },
        ]

    def test_group_price_catalog(self):
        # No time to craft testing data
        mapping = get_mapping("./data/mappings_1.csv")
        transformed = process_price_catalog("./data/pricat_1.csv", mapping)
        result = group_price_catalog(transformed)
        assert result["catalog"]["brand"] == "Via Vai"
        assert result["catalog"]["articles"][0]["article_number"] == "15189-02"
        assert len(result["catalog"]["articles"][0]["variations"]) == 28
        assert result["catalog"]["articles"][1]["article_number"] == "4701013-00"
        assert len(result["catalog"]["articles"][1]["variations"]) == 21
