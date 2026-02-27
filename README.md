# Fashion Cloud Coding Challenge

Here is my solution for the coding challenge.

This is a pure python implementation written in python 3.13.
The program accepts a price catalog file in CSV format, mapping file in CSV format and generates a json file, containig the data grouped by brand and article.

## Prerequisites
Python 3.13 must be installed (earlier versions should work as well but they weren't tested)

## Installation
Not required.
Extra libraries are not needed until you want to run tests. Tests are written using pytest, therefore this library will be required.

## Run the tests
```commandline
python -m pytest
```

## Running the program
```commandline
python -m src.transform --pricat <path_to_pricat.csv> --mappings <path_to_mappings.csv> --output <output_file.json>
```

