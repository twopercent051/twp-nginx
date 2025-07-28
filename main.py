import sys
import subprocess


def main():
    command = sys.argv[1:]

    if not command:
        print("Использование: утилита <команда> <аргументы>")
        sys.exit(1)

    if command[0] == "info":
        subprocess.run(["python", "info.py"])
    elif command[0] == "add":
        subprocess.run(["python", "add.py"] + command[1:])
    elif command[0] == "remove":
        subprocess.run(["python", "remove.py"] + command[1:])
    elif command[0] == "pull":
        print("Команда pull выполняется...")
    elif command[0] == "push":
        print("Команда push выполняется...")
    else:
        print("Неизвестная команда")
        sys.exit(1)


if __name__ == "__main__":
    main()
