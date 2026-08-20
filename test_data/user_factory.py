from dataclasses import asdict, dataclass
from uuid import uuid4


@dataclass
class UserData:
    name: str
    email: str
    password: str
    title: str
    birth_date: str
    birth_month: str
    birth_year: str
    firstname: str
    lastname: str
    company: str
    address1: str
    address2: str
    country: str
    zipcode: str
    state: str
    city: str
    mobile_number: str

    def to_payload(self) -> dict[str, str]:
        return asdict(self)


def build_user() -> UserData:
    unique_id = uuid4().hex[:10]

    return UserData(
        name="QA Automation",
        email=f"qa.automation.{unique_id}@example.com",
        password=f"QaPassword-{unique_id}",
        title="Mr",
        birth_date="10",
        birth_month="5",
        birth_year="1994",
        firstname="QA",
        lastname="Automation",
        company="Test Company",
        address1="Test Street 123",
        address2="",
        country="Canada",
        zipcode="12345",
        state="Test State",
        city="Test City",
        mobile_number="1234567890",
    )
