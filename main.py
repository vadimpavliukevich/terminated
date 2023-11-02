from agent import run_agent


def main_loop():
    while True:
        user_input = input("Enter a command or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            break
        result = run_agent(user_input)
        print(result)


if __name__ == "__main__":
    main_loop()
