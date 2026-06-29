#!/usr/bin/env python3

from new_pipeline_engine import TACEEngine
from new_query_engine import QueryEngine


def menu():

    print("\n========================")
    print("       Tegmark-Aquinas Conceptual Ecosystem")
    print("========================")
    print("1. Session Knowledge")
    print("2. TACE Knowledge")
    print("3. Ask TACE")
    print("4. Reasoning")
    print("0. Exit")

    return input("\nOption: ").strip()


def main():

    engine = TACEEngine()

    query = QueryEngine()

    while True:

        option = menu()

        if option == "1":

            while True:

                print("\n=========================")
                print("     Session Items")
                print("=========================\n")

                items = engine.session.all()

                if not items:

                    print("1. text")

                else:

                    for i, item in enumerate(items, 1):

                        print(f"{i}. {item}")

                cmd = input(
                    "\n> 1. replace text; no numbered text = new item; blank = Back; 0 = Clear All\n> "
                ).strip()

                if cmd == "0":

                    confirm = input(
                        "\nClear ALL Session Knowledge? (y/N): "
                    ).strip().lower()

                    if confirm == "y":

                        engine.session.clear()
                        engine.load_session()

                    continue

                if cmd == "":
                    break

                if "." in cmd and cmd.split(".",1)[0].isdigit():

                    n, txt = cmd.split(".",1)

                    idx = int(n) - 1

                    txt = txt.strip()

                    if not items and idx == 0:

                        if txt:

                            engine.session.add(txt)

                        engine.load_session()

                    elif 0 <= idx < len(items):

                        if txt:

                            engine.session.replace(idx, txt)

                            engine.load_session()

                        else:

                            engine.session.remove(idx)

                            engine.load_session()

                    else:

                        print("\nInvalid item.")

                else:

                    engine.session.add(cmd)

                engine.load_session()

        elif option == "2":

            engine.show()

        elif option == "3":

            question = input("\nQuestion: ")

            answer = query.ask(

                engine.universe,

                question,

            )

            print()

            if isinstance(answer, dict):

                print(f'[{answer["source"]}]\n')

                print(answer["answer"])

                note = answer.get("note")

                if note:

                    print("\nNote:")

                    print(note)

            else:

                print(answer)

        elif option == "4":

            print("\nDerived Knowledge\n")

            if not engine.universe.derived:

                print("(none)")

            else:

                for relation in engine.universe.derived:

                    print(relation)

        elif option == "0":

            break

        else:

            print("\nInvalid option.")


if __name__ == "__main__":

    main()
