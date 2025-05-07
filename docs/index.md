---
hide:
  - toc
  - navigation
---
<style>
h1 {
  display: none;
}
</style>
# FoaPy
FoaPy is a library for Formal Order Analysis of symbol sequences.

This approach treats "order" as a fundamental symbol sequence property and provides order-dependent measures to differentiate and compare sequences.
<div id="playground-root"></div>
<script type="module">
  import { mount } from './assets/js/playground.js';
  const helpersCode=`import streamlit as st
import foapy
import numpy as np
from streamlit_sortables import sort_items

def add_theme():
  st.markdown('<link rel="stylesheet" href="assets/css/streamlit.css">', unsafe_allow_html=True)

def source_widget(text):
    source = st.text_area("", text,
      key="source")
    source = source.replace("\\n", " ").lower()
    separator = st.text_input("Split by", " ").lower()
    if separator:
      return source.split(separator)
    return list(source)

def palette(seq):
  import numpy as np
  import seaborn as sns

  power = len(seq)
  palette = "husl" if power > 20 else "tab20"
  return np.asarray(
    sns.color_palette(palette, power).as_hex()
  )

def display(seq, colors):
  from streamlit_extras.tags import tagger_component

  if len(seq) != len(colors):
    tagger_component("", seq, list(colors[seq]))
  else:
    tagger_component("", seq, list(colors))

def array2image(seq, colors):
  import io
  import base64
  import numpy as np
  from skimage.transform import rescale
  from PIL import Image

  # Create a 1D image from the colors array
  colors_array = np.array(
    [
      tuple(
        int(c.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)
      ) for c in colors[seq]
    ]
  )

  colors_array = colors_array.reshape(1, len(colors[seq]), 3)
  colors_array = rescale(colors_array, [25, 5, 1], order=0)

  # Convert to base64
  buffered = io.BytesIO()
  img = Image.fromarray(np.uint8(colors_array))
  img.save(buffered, format="PNG")
  img_str = base64.b64encode(buffered.getvalue()).decode()
  return f"data:image/png;base64,{img_str}"

column_config = {
  "order": None,
  "img": st.column_config.ImageColumn(
    "Order",
    help="Order",
    width="medium"
  ),
  "arithmetic mean": st.column_config.NumberColumn(
    "Δa",
    help="Arithmetic mean",
  ),
  "geometric mean": st.column_config.NumberColumn(
    "Δg",
    help="Geometric mean",
  ),
  "average remotness": st.column_config.NumberColumn(
    "g",
    help="Average remotness",
  ),
  "depth": st.column_config.NumberColumn(
    "G",
    help="Depth",
  ),
  "identifying information": st.column_config.NumberColumn(
    "H",
    help="Identifying informations / Entropy",
  ),
  "descriptive information": st.column_config.NumberColumn(
    "D",
    help="Descriptive information",
  ),
  "regularity": st.column_config.NumberColumn(
    "r",
    help="Regularity",
  ),
  "uniformity": st.column_config.NumberColumn(
    "u",
    help="Uniformity",
  )
}

def store_data(item):
  import pandas as pd
  if 'characteristics' not in st.session_state:
      st.session_state['characteristics'] = []

  def form_callback(data):
    for item in st.session_state['characteristics']:
      if item["img"] == data["img"]:
        return
    st.session_state['characteristics'].append(data)

  df = pd.DataFrame([item])

  st.dataframe(df,
    column_config=column_config,
    use_container_width=True,
    hide_index=True,
    key="current"
  )

  st.button("Add to chart",
    help="Add measures to chart",
    on_click=form_callback,
    args=(item,),
    type="secondary",
    use_container_width=True
  )

def display_data(current):
  import altair as alt
  import pandas as pd

  data = st.session_state.characteristics if st.session_state.characteristics else [current]

  df = pd.DataFrame(data)

  df_chart = pd.DataFrame([current] + st.session_state.characteristics)

  chart, table = st.tabs(["Chart", "Data"])

  with table:
    st.dataframe(df,
      column_config=column_config,
      use_container_width=True,
      hide_index=True
    )

  options = list(current.keys())[1:]

  def options_format_callback(option):
    if column_config[option]:
      data = column_config[option]
      return f"{data['label']} ({data['help']})"
    return option.title()

  with chart:
    with st.popover("axis", use_container_width=True):
      x = st.selectbox(
          "X",
          key="x",
          index=0,
          options=options,
          format_func=options_format_callback
      )
      y = st.selectbox(
          "Y",
          key="y",
          index=1,
          options=options[1:],
          format_func=options_format_callback
      )

    if x == "order":
      x_encode = alt.X(x, type="ordinal")
      x_order_encode = alt.X(x, type="ordinal", axis=alt.Axis(labelExpr=""))
    else:
      x_encode = x
      x_order_encode = alt.X(x, type="ordinal", axis=alt.Axis(labelExpr=""))
    c = (
       alt.Chart(df_chart)
       .mark_line(point = True)
       .encode(
         x=x_encode,
         y=alt.Y(y, type="quantitative"),
       )
       +
       alt.Chart(df_chart)
       .mark_image(height=10)
       .transform_calculate(y, "-.4")
       .encode(
         x=x_order_encode,
         y=alt.Y(y, type="quantitative", scale=alt.Scale(domain=[0, 10])),
         url=alt.Url("img", type="nominal"),
         tooltip=alt.Tooltip("order"),
       )
    )

    st.altair_chart(c, use_container_width=True)

def form(item):
  store_data(item)
  display_data(item)
`;

  const code=`import streamlit as st
import foapy
import numpy as np
from streamlit_sortables import sort_items
from helpers import form, palette, display
from helpers import array2image, add_theme, source_widget

add_theme()

'''
### Formal Order Analysis decomposes
'''

with st.popover("__a sequence__", use_container_width=True):
    source = source_widget(
"""Peter Piper picked a peck of pickled peppers
A peck of pickled peppers Peter Piper picked
If Peter Piper picked a peck of pickled peppers
Where's the peck of pickled peppers Peter Piper picked"""
)

sequence = sort_items(source)

'into'

order, alphabet = foapy.order(
  sequence, return_alphabet=True
)
orderCongeneric = foapy.ma.order(np.asarray(sequence))

colors = palette(alphabet)

'''### alphabet'''
display(alphabet, colors)
'and'
'''### order'''
display(order, colors)

'''
### and provides various order-sensitive measures
'''
intervals = foapy.intervals(
  order, foapy.binding.start, foapy.mode.cycle
)
intervalsCongeneric = foapy.ma.intervals(
  orderCongeneric, foapy.binding.start, foapy.mode.cycle
)

current = {
  "img": array2image(order, colors),
  "order": np.array2string(order),
  "arithmetic mean": foapy.characteristics.arithmetic_mean(intervals),
  "geometric mean": foapy.characteristics.geometric_mean(intervals),
  "average remotness": foapy.characteristics.average_remoteness(intervals),
  "depth": foapy.characteristics.depth(intervals),
  "identifying information": foapy.characteristics.identifying_information(intervalsCongeneric),
  "descriptive information": foapy.characteristics.descriptive_information(intervalsCongeneric),
  "regularity": foapy.characteristics.regularity(intervalsCongeneric),
  "uniformity": foapy.characteristics.uniformity(intervalsCongeneric),
}

form(current)
`

      // The library is available as ReactStlitePlayground
      mount({
        initialCode: code,
        files: {
          "helpers.py": helpersCode,
        },
        requirements: [
          "https://intervals-mining-lab.github.io/foapy/streamlit-frontpage/assets/streamlit_sortables-0.3.1-py3-none-any.whl",
          "foapy",
          "pandas",
          "streamlit-extras==0.6.0",
          "seaborn",
          "scikit-image"
        ],
      },
      document.getElementById("playground-root")
      );
</script>
