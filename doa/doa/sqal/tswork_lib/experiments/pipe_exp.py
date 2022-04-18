"""experiment of pipes modulee."""
import pipes

from rich import print as rprint

if __name__ == "__main__":
    # creates a file for input. This is not directly related to pipes, just a sample file.
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write("shin saito 齋藤 新")
    with open("test2.txt", "w", encoding="sjis") as f:
        f.write("shin saito 齋藤 新")

    # play with pipes.
    t = pipes.Template()
    t.debug(True)

    # specify pipeline
    t.append("tr a-z A-Z", "--")  # convert to uppercase
    t.append("sed -e \"s/ /_/g\"", "--")  # replace whitespaces

    # read from sample file (actually through pipeline just created.)
    f = t.open("test.txt", "r")  # specify input of pipeline
    rprint(f.read())
    f.close()

    # with statement can be used?
    with t.open("test.txt", "r") as f:  # specify input of pipeline
        rprint(f.read())

    # test of copy method:
    # defined pipeline reads from stdin and writes to stdout
    t2 = pipes.Template()
    t2.debug(True)
    # convert to UTF-8, convert unix linebreaks (\n)
    t2.append("nkf -w -d", "--")
    t2.append("tr a-z A-Z", "--")  # convert to uppercase
    t2.copy("test2.txt", "tested2.txt")
    rprint("OK.")
