from lexer import lex
from pars import JSONParser
from types_ import JSONType


def JSONDecode(chars: str) -> JSONType:
    return JSONParser(lex(chars)).json_parse().value
