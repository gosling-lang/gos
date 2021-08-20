import sys

def main():
    with open(sys.argv[1], mode='r') as f:
        contents = f.read().strip()
    contents = contents.split('\n')
    contents[-1] = 'print(' + contents[-1] + '.to_json())'
    exec("\n".join(contents))

if __name__ == '__main__':
    main()
