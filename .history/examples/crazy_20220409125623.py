class Person:
  greeting = "hello"

  def __init__(self, name, age):
    self.name = name
    self.age = age
  
  def hello(self):
    print("hello")

Person.__setattr__(Person, "greeting", "bye")
