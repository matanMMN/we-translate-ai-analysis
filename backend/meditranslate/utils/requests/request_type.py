from enum import Enum


class RequestType(str, Enum):
    DELETION = "DELETION"
    TERM = "TERM"
    GLOSSARY = "GLOSSARY"

