---
hide:
  - toc
  - navigation
---

# FoaPy

FoaPy is a Python library for Formal Order Analysis of sequences.

This approach defines an Order as a special sequence property and provides various characteristics that can be used to describe and analyze different aspects of it.
<div id="playground-root"></div>
<script type="module">
  import { mount } from './assets/js/index.es.js';
  const code=`style = """
.sortable-item{margin-bottom:5px;margin-top:5px;margin-left:0;margin-right:0;border-radius:0;border:1px solid#000;}
.sortable-item:hover{margin-bottom:5px;margin-top:5px;margin-left:0;margin-right:0;border-radius:0;border:1px solid#000;}
"""

import streamlit as st
import foapy
import pandas as pd
from streamlit_sortables import sort_items

toungle_twister = """
Peter Piper picked a peck of pickled peppers \n
A peck of pickled peppers Peter Piper picked \n
If Peter Piper picked a peck of pickled peppers \n
Where's the peck of pickled peppers Peter Piper picked \n
"""

def sortSeq():
  st.session_state['seq'] = sorted(st.session_state['seq'])

def resetSeq():
  st.session_state['seq'] = toungle_twister.lower().split()

def saveToDataFrame(value):
  st.session_state['gList'].append(value)

if 'seq' not in st.session_state:
  resetSeq()

if 'gList' not in st.session_state:
  st.session_state['gList'] = []

source = st.session_state['seq']

st.container(border=True).write(toungle_twister)

left, right = st.columns(2, gap="small")
left.button('Sort', on_click=sortSeq)
right.button('Reset', on_click=resetSeq)

sorted_source = sort_items(source, custom_style=style)
intervals = foapy.intervals(
  sorted_source, foapy.binding.start, foapy.mode.cycle
)
g = foapy.characteristics.average_remoteness(intervals)

col1, col2, col3 = st.columns(3)
col1.metric("Average remoteness (g)", g, border=True)

st.button('Add to chart',
  on_click=saveToDataFrame, args=(g, )
)

chart_data = pd.DataFrame(
  st.session_state['gList'], columns=["g"]
)

st.scatter_chart(chart_data)

`

      // The library is available as ReactStlitePlayground
      mount({
        initialCode: code,
        requirements: ["https://intervals-mining-lab.github.io/foapy/streamlit-frontpage/assets/streamlit_sortables-0.3.1-py3-none-any.whl", "foapy", "pandas"],
      },
      document.getElementById("playground-root")
      );
</script>
