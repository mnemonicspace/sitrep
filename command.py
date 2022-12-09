from subprocess import PIPE, Popen


def main():
    while True:
        try:
            command = input()
        except KeyboardInterrupt:
            break
        except EOFError:
            break

        proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)

        out, errors = proc.communicate()

        out = out.decode()

        if errors:
            errors = errors.decode()
            out = out + errors

        print(out)


if __name__ == "__main__":
    main()
