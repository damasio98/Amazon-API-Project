def formatar(s):
    i = 0
    for c in s:
        if c in ['[', '{']:
            print(c)
            i += 2
            print(i*' ', end='')
        elif c in [']', '}']:
            print("")
            i -= 2
            print(i*' ', end='')
            print(c, end='')
        elif c == ',':
            print(c)
            print((i-1)*' ', end='')
        else:
            print(c, end='')
        print("")