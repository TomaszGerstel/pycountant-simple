from dataclasses import dataclass


@dataclass
class Config:
    vat_pct: float = 20.0
    income_tax_pct: float = 30.0


config = Config()