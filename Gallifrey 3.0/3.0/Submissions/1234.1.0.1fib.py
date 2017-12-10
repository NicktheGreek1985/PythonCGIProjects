import argparse
number = input('Number: ')
def fib(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a+b
    return a

def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument(number, help='The Fibonacci number you wish to calculate', type=int)

    args = parser.parse_args()

    result = fib(args.number)

    print('The', str(args.number) + 'th fib number is', str(result))

if __name__ == '__main__':
    Main()
