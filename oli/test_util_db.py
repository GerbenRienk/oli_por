

def try_this():
    v = "O pai é funcionário na escola que a criança "
    #v= nicode(v)
    #v.encode('ascii', 'xmlcharrefreplace')
    print(v.encode(encoding="ascii",errors="xmlcharrefreplace"))
    txt = "My name is Ståle"

    print(txt.encode(encoding="ascii",errors="backslashreplace"))
    print(txt.encode(encoding="ascii",errors="ignore"))
    print(txt.encode(encoding="ascii",errors="namereplace"))
    print(txt.encode(encoding="ascii",errors="replace"))
    print(txt.encode(encoding="ascii",errors="xmlcharrefreplace"))
    print(txt.encode(encoding="ascii",errors="strict"))



if __name__ == '__main__':
    try_this()