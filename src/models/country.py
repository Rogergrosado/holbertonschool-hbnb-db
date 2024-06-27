class Country:
    name: str
    code: str
    cities: list

    def __init__(self, name: str, code: str, **kw) -> None:
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        from src.persistence import db

        countries: list["Country"] = db.get_all("country")

        return countries

    @staticmethod
    def get(code: str) -> "Country | None":
        for country in Country.get_all():
            if country.code == code:
                return country
        return None

    @staticmethod
    def create(name: str, code: str) -> "Country":
        from src.persistence import db

        country = Country(name, code)

        db.save(country)

        return country
