import argparse
import os

from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="A simple CLI.")
    parser.add_argument("--name", default=os.getenv("NAME", "World"), help="The name to greet.")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()
