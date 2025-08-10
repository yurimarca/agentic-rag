from dotenv import load_dotenv
load_dotenv()

from graph.graph import app

if __name__ == '__main__':
	print("Running the graph application...")
	print(app.invoke({"question": "What is agent memory?"}))