import os
import pandas as pd
from sys import path
from typing import List

data_path = os.path.join(os.path.dirname(__file__), "")

COUNTRIES:List[str] = pd.read_csv(data_path + "countries.csv", header=None, names=["country"])\
    ["country"]\
    .to_list()
assert "Albania" in COUNTRIES

DOMAINS:List[str] = pd.read_csv(data_path + "domains.csv", header=None, names=["domain"])\
    ["domain"]\
    .to_list()
assert "Energy" in DOMAINS