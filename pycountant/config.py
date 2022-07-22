from pydantic import BaseSettings


class Config(BaseSettings):
    # vat_pct: float = 20.0
    income_tax_pct: float = 30.0


config = Config()
