import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
import pandas as pd
import tempfile
import requests

from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
from fake_useragent import UserAgent # type: ignore

from app.db.session import engine

BASE_PATH: str = os.path.dirname(os.path.realpath(__file__))

# Constants
PSGC_URL = "https://psa.gov.ph/classification/psgc"
GEO_LEVELS = {
    'Reg': 0,
    'Prov': 1,
    'Dist': 1,
    'City': 2,
    'Mun': 2,
    'Bgy': 3,
}

# Utility function
def is_within_level(level: str, within: str) -> bool:
    return GEO_LEVELS[level] >= GEO_LEVELS[within]

def set_region(row: pd.Series) -> str | None:
    if is_within_level(row['geo_level'], 'Reg'):
        return Code(row['code']).region
    
    return None

def set_province_district(row: pd.Series) -> str | None:
    if is_within_level(row['geo_level'], 'Prov'):
        return Code(row['code']).province_district
    
    return None

def set_city_municipality(row: pd.Series) -> str | None:
    if is_within_level(row['geo_level'], 'City'):
        return Code(row['code']).city_municipality
    
    return None

def set_barangay(row: pd.Series) -> str | None:
    if is_within_level(row['geo_level'], 'Bgy'):
        return Code(row['code']).barangay
    
    return None

def preprocess(row: pd.Series) -> pd.Series:
    row['region'] = set_region(row)
    row['province'] = set_province_district(row)
    row['city_municipality'] = set_city_municipality(row)
    # row['barangay'] = set_barangay(row)
    
    return row

@dataclass
class Code:

    code: str
    region_section = 2
    province_district_section = 5
    city_municipality_section = 7

    # def __init__(self, code: str):
    #     self.code = code

    @property
    def region(self) -> str:
        return self.code[:self.region_section].ljust(10, '0')

    @property
    def province_district(self) -> str:
        return self.code[:self.province_district_section].ljust(10, '0')

    @property
    def city_municipality(self) -> str:
        return self.code[:self.city_municipality_section].ljust(10, '0')

    @property
    def barangay(self) -> str:
        return self.code


def main() -> None:
    # Download PSGC data
    ua = UserAgent()

    res = requests.get(PSGC_URL, headers={'User-Agent': ua.random})
    soup = BeautifulSoup(res.text, 'html.parser')
    tag = soup.find('a', text='Publication')
    if not tag or not isinstance(tag, Tag):
        raise Exception("Unable to find PSGC publication link")

    start = time.time()

    geo_data = pd.read_excel(
        # os.path.join(BASE_PATH, 'PSGC-3Q-2023-Publication-Datafile.xlsx'),
        tag.get('href'),
        sheet_name="PSGC",
        usecols=[
            '10-digit PSGC',
            'Name',
            'Geographic Level',
        ],
        dtype=str
    )

    geo_data = geo_data.rename(columns={
        '10-digit PSGC': 'code',
        'Name': 'name',
        'Geographic Level': 'geo_level',
    })

    geo_data = geo_data.dropna(subset=['code', 'geo_level'], how='any')
    geo_data = geo_data.drop(geo_data[~geo_data['geo_level'].isin(GEO_LEVELS)].index)

    # Preprocess region, province, district, city and municipality columns
    geo_data = geo_data.apply(preprocess, axis=1)

    end = time.time()
    print(f"Data loaded in {end - start} seconds")
    print("Saving to database...")
    geo_data.to_sql('locations', engine, if_exists='append', index=False)
    print("Done!")


if __name__ == "__main__":
    main()