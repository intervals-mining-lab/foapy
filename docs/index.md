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
  import { mount } from './assets/js/playground.js';
  const code=`import streamlit as st
import foapy
import pandas as pd
from streamlit_sortables import sort_items

st.subheader('Formal Order Analysis decomposes a sequence')

toungle_twister = """
Peter Piper picked a peck of pickled peppers

A peck of pickled peppers Peter Piper picked

If Peter Piper picked a peck of pickled peppers

Where's the peck of pickled peppers Peter Piper picked

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

sequence = sort_items(source)
order, alphabet = foapy.order(
  sequence, return_alphabet=True
)

st.subheader('into')
st.subheader('alphabet')
sort_items(list(alphabet))
st.subheader('and')
st.subheader('order')
sort_items([str(i) for i in order])

intervals = foapy.intervals(
  order, foapy.binding.start, foapy.mode.cycle
)
g = foapy.characteristics.average_remoteness(intervals)


left, right = st.columns(2, gap="small")
left.button('Sort', on_click=sortSeq)
right.button('Reset', on_click=resetSeq)

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
        requirements: ["https://intervals-mining-lab.github.io/foapy/streamlit-frontpage/assets/streamlit_sortables-0.3.1-py3-none-any.whl", "foapy", "pandas", "st-annotated-text"],
      },
      document.getElementById("playground-root")
      );
</script>
