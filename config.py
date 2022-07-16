from dataclasses import dataclass


@dataclass
class Config:
    vat_pct: float = 20.0


config = Config()