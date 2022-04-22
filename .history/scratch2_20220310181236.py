def add(x: int, y: int) -> int:
  return x + y

def somefunc():
  pass


somefunc.__code__ = somefunc.__code__.replace(co_argcount=2, co_varnames=("x", "y"), co_code=add.__code__.co_code, co_name="hello")
print(somefunc(3))