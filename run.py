import argparse
import subprocess

def run_chat_api():
    subprocess.run(['python3', './api/main.py'])

def run_streamlit():
    subprocess.run(['streamlit', 'run', './interface/streamlit_app.py'])

def run_train_model():
    subprocess.run(['python3', './src/train_model.py'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run different parts of the RAG sales assistant.")
    parser.add_argument("step", choices=["host_api", "interface"], help="Select which step to run.")
    args = parser.parse_args()

    if args.step == "host_api":
        run_chat_api()
    elif args.step == "interface":
        run_streamlit()