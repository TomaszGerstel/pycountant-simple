from pydantic import BaseSettings


class Config(BaseSettings):
    vat_pct: float = 20.0
    income_flat_tax_pct: float = 19.0
    default_lump_sum_tax_rate = 12.0


config = Config()
