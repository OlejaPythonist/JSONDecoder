from types_ import Token, Tag, Result, JSONType
from exceptions import (
    InvalidJSONSyntax,
    InvalidKey,
    KeyDuplicate
)


class JSONParser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens

    def __parse_array(self, position: int = 0) -> Result:
        tokens = self.tokens
        response: list[JSONType] = []

        position += 1
        if tokens[position].value == "]":
            return Result(response, position + 1)

        result = self.json_parse(position)
        if result:
            response.append(result.value)
            position = result.position

        while result:
            if tokens[position].value != ",":
                break
            position += 1
            result = self.json_parse(position)
            position = result.position
            response.append(result.value)

        if tokens[position].value != "]":
            raise

        return Result(response, position + 1)

    def __parse_pair(
            self,
            position: int = 0) -> tuple[tuple[str, JSONType], int]:
        tokens = self.tokens
        key = tokens[position].value
        if not (type(key) == str):
            raise InvalidKey(
                f"The key of the JSON object must be a string."
                f"Token position: {position}, "
                f"token: {tokens[position]}, "
                f"key type: {type(key)}"
            )
        position += 1
        if tokens[position].value != ":":
            raise
        position += 1
        value = self.json_parse(position)
        position = value.position
        return ((key, value.value), position)

    def __parse_json_object(self, position: int = 0) -> Result:
        tokens = self.tokens

        response: dict[str, JSONType] = {}
        position += 1
        if tokens[position].value == "}":
            return Result(response, position + 1)

        value = None
        if tokens[position].tag == Tag.STR:
            ((key, value), position) = self.__parse_pair(position)
            response[key] = value

        while value:
            if tokens[position].value != ",":
                break
            position += 1
            if tokens[position].tag == Tag.STR:
                ((key, value), position) = self.__parse_pair(position)
                if not (response.get(key, ...) is ...):
                    raise KeyDuplicate(
                        f"key '{key}' "
                        f"already exists, token position: {position}"
                    )
                response[key] = value

        if tokens[position].value != "}":
            raise
        return Result(response, position + 1)

    def json_parse(self, position: int = 0) -> Result:
        tokens = self.tokens

        if tokens[position].tag == Tag.CALCULATED:
            return Result(tokens[position].value, position + 1)
        if tokens[position].tag == Tag.STR:
            return Result(tokens[position].value, position + 1)
        if tokens[position].value == "[":
            return self.__parse_array(position)
        if tokens[position].value == "{":
            return self.__parse_json_object(position)
        raise InvalidJSONSyntax(
            f"Token position: {position}, "
            f"token: {tokens[position]}"
        )
