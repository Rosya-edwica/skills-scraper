from dotenv import load_dotenv
import os
from typing import NamedTuple

env_is_loaded = load_dotenv(".env")

class __Settings(NamedTuple):
    Host: str
    Port: str
    Database: str
    User: str
    Password: str


SETTINGS = __Settings(
    Host=os.getenv("MYSQL_HOST"),
    Port=os.getenv("MYSQL_PORT"),
    Database=os.getenv("MYSQL_DATABASE"),
    User=os.getenv("MYSQL_USER"),
    Password=os.getenv("MYSQL_PASSWORD"),
)

class Region(NamedTuple):
    Id:     str
    Name:   str