---
hide:
  - toc
  - navigation
---

# FoaPy

FoaPy is a Python library for Formal Order Analysis of sequences.

This approach defines an Order as a special sequence property and provides various characteristics that can be used to describe and analyze different aspects of it.

<div id="test"></div>
<script type="module">
  import { mount } from "https://cdn.jsdelivr.net/npm/@stlite/browser@0.80.4/build/stlite.js";
  mount(
    {
      streamlitConfig: {
        "theme.base": "dark",
        "theme.primaryColor": "#00b4d8",
        "theme.backgroundColor": "#03045e",
        "theme.secondaryBackgroundColor": "#0077b6",
        "theme.textColor": "#caf0f8",
        "client.toolbarMode": "viewer",
        "client.showErrorDetails": false,
        "layout.width": "800px",
        "layout.maxWidth": "800px"
      },
      // requirements: ["http://localhost:8000/assets/streamlit_sortables-0.3.1-py3-none-any.whl", "foapy"],
      requirements: ["https://intervals-mining-lab.github.io/foapy/streamlit-frontpage/assets/streamlit_sortables-0.3.1-py3-none-any.whl", "foapy"],
      entrypoint: "streamlit_app.py",
      files: {
        "streamlit_sortables-0.3.1-py3-none-any.whl": {
          url: "./assets/streamlit_sortables-0.3.1-py3-none-any.whl",
        },
        "streamlit_app.py": `
import streamlit as st
import foapy
from streamlit_sortables import sort_items

style = """
.sortable-item {
    margin-bottom: 5px;
    margin-top: 5px;
    margin-left: 0;
    margin-right: 0;
    border-radius: 0;
    border: 1px solid #000;
}

.sortable-item:hover {
    margin-bottom: 5px;
    margin-top: 5px;
    margin-left: 0;
    margin-right: 0;
    border-radius: 0;
    border: 1px solid #000;
}
"""

toungle_twister = """
Peter Piper picked a peck of pickled peppers
A peck of pickled peppers Peter Piper picked
If Peter Piper picked a peck of pickled peppers
Where's the peck of pickled peppers Peter Piper picked
"""

for i in toungle_twister.splitlines():
  st.write(i)

source = toungle_twister.lower().split()
sorted_source = sort_items(source, custom_style=style)

intervals = foapy.intervals(sorted_source, foapy.binding.start, foapy.mode.cycle)
g = foapy.characteristics.average_remoteness(intervals)
st.write(f'g: {g}')
`,
      },
      streamlitConfig: {
        // Streamlit configuration
        "client.toolbarMode": "minimal",
      },
    },
    document.getElementById("test"),
  );
</script>
