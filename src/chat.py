import os
import sys
import threading
import itertools
import time
from search import search_prompt, get_context
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()


def validate_env_vars():
    required_vars = [
        "OPENAI_API_KEY",
        "OPENAI_EMBEDDING_MODEL",
        "DATABASE_URL",
        "PG_VECTOR_COLLECTION_NAME",
        "PG_VECTOR_MAX_RESULTS",
        "OPENAI_EMBEDDING_MODEL"
    ]
    for var in required_vars:
        if not os.getenv(var):
            raise RuntimeError(f"Environment variable {var} is not set")


def spinner(stop_event, message="Pensando"):
    for frame in itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\r{frame} {message}... ")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(message) + 6) + "\r")
    sys.stdout.flush()


def ask_question(question: str) -> str:
    context = get_context(question)
    prompt = search_prompt()

    if not context:
        return "Não foi possível obter contexto para a pergunta."

    model = ChatOpenAI(model_name=os.getenv("OPENAI_MODEL"), temperature=0.5)
    chain = prompt | model
    result = chain.invoke({"context": context, "question": question})

    return result.content


def ask_with_spinner(question: str) -> str:
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
    spinner_thread.start()

    try:
        answer = ask_question(question)
    finally:
        stop_event.set()
        spinner_thread.join()

    return answer


def main():
    validate_env_vars()
    
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(f"PERGUNTA: {question}")
        answer = ask_with_spinner(question)
        print(f"RESPOSTA: {answer}\n")
   
    print("Modo chat ativado. Digite sua pergunta ou 'sair' para encerrar.")
    print("Faça sua pergunta:")
    while True:
        try:
            question = input("PERGUNTA: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando chat.")
            break

        if not question:
            continue

        if question.lower() in ("sair", "exit", "quit"):
            print("Encerrando chat.")
            break

        answer = ask_with_spinner(question)
        print(f"RESPOSTA: {answer}\n")


if __name__ == "__main__":
    main()