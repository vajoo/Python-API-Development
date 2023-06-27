import sys
import os
  
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
  
sys.path.append(parent_directory)
  
from app.calculations import add  

def test_add():
    print("testing add function")
    sum = add(5, 3)
    assert sum == 8

test_add()