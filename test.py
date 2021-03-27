arr = ["www.asd.com", "mailto: test", "asd.si"]

for a in arr:
    if "mailto" in a:
        arr.remove(a)
print(arr)