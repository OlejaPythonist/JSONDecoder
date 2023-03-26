import re
from types_ import Tag, Token
from exceptions import IllegalCharacter, EOFErrorJSON


STR = re.compile(r"\"(\\.|[^\"])*\"")
NUMBER = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))


def lex(chars: str) -> list[Token]:
    response = []
    position = 0
    max_position = len(chars)
    while position < max_position:
        if chars[position] in (" ", "\t", "\n"):
            position += 1

        elif chars[position] in ["{", "}", "[", "]", ":", ","]:
            response.append(Token(chars[position], Tag.RESERVED))
            position += 1

        elif chars[position] == "t"\
                and chars[position:position + 4] == "true":
            response.append(Token(True, Tag.CALCULATED))
            position += 4

        elif chars[position] == "f"\
                and chars[position:position + 5] == "false":
            response.append(Token(False, Tag.CALCULATED))
            position += 5

        elif chars[position] == "n"\
                and chars[position:position + 4] == "null":
            response.append(Token(None, Tag.CALCULATED))
            position += 4

        elif chars[position] in ['"', "'"]:
            string = STR.match(chars, position)
            if not string:
                raise EOFErrorJSON(f"String position: {position}")
            response.append(
                Token(
                    string.group(0)[1:-1].encode().decode('unicode_escape'),
                    Tag.STR
                )
            )
            position = string.end(0)

        elif (num := NUMBER.match(chars, position)):
            integer, float_, exp = num.groups(default=None)
            if integer and\
                    (float_ or exp):
                result = float(f"{integer}{(float_ or '')}{exp or ''}")
            elif integer is not None:
                result = int(integer)
            response.append(Token(result, Tag.CALCULATED))
            position = num.end()

        else:
            raise IllegalCharacter(
                f"position: {position}, "
                f"char: {chars[position]}"
            )

    return response
