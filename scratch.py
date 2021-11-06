from functools import partial

class FailureMonad:
    def __init__(self, value, failed=False):
        self.value = value
        self.failed = failed

    def __str__(self):
        return f"value: {self.value} | failed: {self.failed}"

    def bind(self, func):
        if self.failed:
            return self
        try:
            new_value = func(self.value)
            return FailureMonad(new_value)
        except:
            return FailureMonad(None, True)


def errorFunc():
    raise Exception('Something went wrong')

def add(num1, num2):
    return num1 + num2

def math(num1, num2, operator):
    return operator(num1, num2)

def addone(num):
    print("Called addone")
    return num + 1

def toInt(num):
    print("Called toInt")
    return int(num)

def toStr(num):
    print("Called toStr")
    return str(num)


x = "1"
result = FailureMonad(x).bind(toInt).bind(addone).bind(toStr)
print(result)

