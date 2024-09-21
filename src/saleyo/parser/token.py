from typing import List, Self


class Token:
    """Token is used to parse a function and modify it"""

    decorators: List[str]
    declearation: List[str]
    code: List[str]
    source: str
    minspace: str
    auto_code_indent: bool

    def __init__(self, source: str, auto_code_indent: bool = True) -> None:
        self.source = source
        self.declearation = []
        self.decorators = []
        self.code = []
        self.auto_code_indent = auto_code_indent
        self.parse()

    def add_decorator(self, decorator: str) -> Self:
        self.decorators.append(decorator)
        return self

    def insert_decorator(self, index: int, decorator: str) -> Self:
        self.decorators.insert(index, decorator)
        return self

    def add_code(self, code: str) -> Self:
        self.code.append(code)
        return self

    def insert_code(self, index: int, code: str) -> Self:
        self.code.insert(index, code)
        return self

    def build(self):
        decorators = "\n".join(self.decorators)
        declearation = "\n".join(self.declearation)
        code = "\n".join(
            map(lambda code: self.minspace + code, self.code)
            if self.auto_code_indent
            else self.code
        )
        return f"{decorators}\n{declearation}\n{code}"

    def parse(self):
        sourcelines = self.source.splitlines()
        first = sourcelines[0]
        self.minspace = first.removesuffix(first.lstrip())

        define_flag = False

        for raw in sourcelines:
            line = raw.removeprefix(self.minspace)

            if line.startswith("@"):
                self.decorators.append(line)
            elif line.startswith("def") and len(self.declearation) == 0:
                if line.rstrip()[-1] != ":":
                    define_flag = True
                self.declearation.append(line)
            elif define_flag:
                self.declearation.append(line)
                if line.rstrip()[-1] == ":":
                    define_flag = False
            else:
                self.code.append(
                    line.removeprefix(self.minspace) if self.auto_code_indent else line
                )

    def __str__(self):
        decorators = "\n".join(self.decorators)
        declearation = "\n".join(self.declearation)

        code = "\n".join(
            map(lambda code: self.minspace + code, self.code)
            if self.auto_code_indent
            else self.code
        )

        return f"""
# Token
    
## Decorator
    
{decorators}

## Declearation

{declearation}

## Code

{code}
    """
