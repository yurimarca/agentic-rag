import argparse
from dotenv import load_dotenv
load_dotenv()

from graph.graph import app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the graph application.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--demo", action="store_true", help="Run with the default question.")
    group.add_argument("--question", type=str, help="Run with a specified question.")

    args = parser.parse_args()

    print("Running the graph application...")

    if args.demo:
        question = "What is agent memory?"
    elif args.question:
        question = args.question

    print(app.invoke({"question": question}))