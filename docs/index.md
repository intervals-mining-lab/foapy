---
hide:
  - toc
  - navigation
---

# FoaPy

FoaPy is a Python library for Formal Order Analysis of sequences.

This approach defines an Order as a special sequence property and provides various characteristics that can be used to describe and analyze different aspects of it.


```pyodide install="foapy,numpy"
import foapy
import numpy as np

source = ['a', 'b', 'a', 'c', 'a', 'd']
order = foapy.order(source)
intervals = foapy.intervals(order, foapy.binding.start, foapy.mode.normal)
print(intervals)
```
