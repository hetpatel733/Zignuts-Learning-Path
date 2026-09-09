import csv
from pathlib import Path


def read_csv(file_path):
    with open(file_path, 'r') as f:
        for row in csv.reader(f):
            print(row)


read_csv(Path(__file__).parent / "sample_data.csv")
