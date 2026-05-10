from typing import Annotated

import typer
from dotenv import load_dotenv

load_dotenv()


def main(name: Annotated[str, typer.Option(help="The name to greet.", envvar="NAME")] = "World") -> None:
    """
    A simple CLI.
    """
    print(f"Hello, {name}!")


def cli() -> None:
    typer.run(main)


if __name__ == "__main__":
    cli()
