import sys

def func_close_stdout(console, f, stdout_file):
    # change stdout to default
    sys.stdout = console
    f.close()

    # print stdout file
    f = open(stdout_file, 'r')
    print(f.read())
    f.close()
    