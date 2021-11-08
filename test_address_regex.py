from typing import Optional
from dataclasses import dataclass
from unittest import TestCase
import re

from scrape_latest_sales_prices import address_pattern


@dataclass
class Case:
    raw: str
    street: str
    number: str
    floor: Optional[str]
    zip_code: str
    city: str

class TestRegex(TestCase):
    cases = [
        Case(
            'Tyge Krabbes Vej 16, kl 2300 København S',
            'Tyge Krabbes Vej',
            '16',
            'kl',
            '2300',
            'København S'
        ),
        Case(
            'Ove Billes Vej 17, 2. 8 2300 København S',
            'Ove Billes Vej',
            '17',
            '2. 8',
            '2300',
            'København S'
        ),
        Case(
            'Gimles Allé 2B, 2. th 2300 København S',
            'Gimles Allé',
            '2B',
            '2. th',
            '2300',
            'København S' 
        ),
        Case(
            'Gimles Allé 2A, st. tv 2300 København S',
            'Gimles Allé',
            '2A',
            'st. tv',
            '2300',
            'København S'
        ),
        Case(
            'Ingolfs Allé 25, st 2300 København S',
            'Ingolfs Allé',
            '25',
            'st',
            '2300',
            'København S'
        ),
        Case(
            'Ingolfs Allé 25, 1 2300 København S',
            'Ingolfs Allé',
            '25',
            '1',
            '2300',
            'København S'
        ),
        Case(
            'Ingolfs Allé 25, 2300 København S',
            'Ingolfs Allé',
            '25',
            None,
            '2300',
            'København S'
        )
    ]

    def test_matches(self):
        for case in self.cases:
            m = re.match(address_pattern, case.raw)
            self.assertIsNotNone(m, f'no match for {case}')
            self.assertEqual(m.group('street').strip(), case.street)
            self.assertEqual(m.group('number').strip(), case.number)
            floor = (m.group('floor').strip() 
                     if m.group('floor') is not None 
                     else None)
            self.assertEqual(floor, case.floor)
            self.assertEqual(m.group('street').strip(), case.street)
            self.assertEqual(m.group('zip').strip(), case.zip_code)
            self.assertEqual(m.group('city').strip(), case.city)
