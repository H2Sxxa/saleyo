from typing import List


class Token:
    """Token is used to parse a function and modify it easily"""

    decorators: List[str]
    declearation: List[str]
    code: List[str]
    source: str
    minspace: str

    def __init__(self, source: str) -> None:
        self.source = source
        self.declearation = []
        self.decorators = []
        self.code = []
        self.parse()

    def build(self):
        decorators = "\n".join(self.decorators)
        declearation = "\n".join(self.declearation)
        code = "\n".join(self.code)
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
                self.code.append(line)

    def __str__(self):
        decorators = "\n".join(self.decorators)
        declearation = "\n".join(self.declearation)
        code = "\n".join(self.code)

        return f"""
# Token
    
## Decorator
    
{decorators}

## Declearation

{declearation}

## Code

{code}
    """
