"""
from: djangosnippets.org and I will put the link here when I can find it again.
Template filter to allow a way to access a list item by index.

A common use-case is for splitting a list into a table with columns::

  <li>List2 element: {{ list2|get_at_index:forloop.counter0 }}</li>
  
"""

from django.template import Library

register = Library()

def get_at_index(list, index):
    return list[index]


register.filter(get_at_index)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()