from typing import Annotated

import typer
from dotenv import load_dotenv

load_dotenv()


def main(name: Annotated[str, typer.Option(help="The name to greet.", envvar="NAME")] = "World"):
    """
    A simple CLI.
    """
    print(f"Hello, {name}!")


if __name__ == "__main__":
    typer.run(main)
