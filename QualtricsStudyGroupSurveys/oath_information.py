from dataclasses import dataclass


@dataclass
class OathInformation:
    client_id: str
    client_secret: str
    scope: str = "manage:all"
