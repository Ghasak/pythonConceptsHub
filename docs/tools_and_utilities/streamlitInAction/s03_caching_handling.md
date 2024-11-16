# How to Handle Caches
<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [How to Handle Caches](#how-to-handle-caches)
    - [Concept](#concept)
        - [Example: Using `@st.cache_data` to Load Proxies](#example-using-stcache_data-to-load-proxies)
        - [How It Works:](#how-it-works)
        - [Advanced: Cache Invalidation](#advanced-cache-invalidation)
            - [Example with Cache Clearing:](#example-with-cache-clearing)
        - [When to Use Caching for Proxies](#when-to-use-caching-for-proxies)
    - [Remove the spinning wheel](#remove-the-spinning-wheel)

<!-- markdown-toc end -->

## Concept

How to Use a Cache Decorator for Faster Loading of Proxy Lists.

- This aims to explain how to leverage a cache decorator for efficiently loading a
  list of proxies. The goal is to accelerate the process by storing previously
  loaded proxy data in a cache, avoiding redundant fetching and improving
  performance.

- To efficiently manage and reload a list of proxies in Streamlit, you can use the
  `@st.cache_data` decorator. This ensures that the function responsible for
  loading the proxies is cached, reducing redundant operations and improving
  performance.

Here’s how you can implement it:

---

### Example: Using `@st.cache_data` to Load Proxies

```python
import streamlit as st

# Simulate a function to load proxies (e.g., from a file or API)
@st.cache_data
def load_proxies():
    # Example: Simulate reading from a file or making a network call
    proxies = [
        "http://proxy1.example.com:8080",
        "http://proxy2.example.com:8080",
        "http://proxy3.example.com:8080",
    ]
    return proxies

# Streamlit app
st.title("Proxy Loader with Cache")

# Load proxies using the cached function
proxies = load_proxies()

# Display proxies
st.subheader("Loaded Proxies:")
st.write(proxies)
```

---

### How It Works:

1. **`@st.cache_data` Decorator**:

   - Caches the function's result based on the input arguments.
   - In this case, `load_proxies()` has no arguments, so the result is cached after the first execution.
   - Subsequent calls to `load_proxies()` retrieve the result from the cache without re-executing the function.

2. **Efficiency**:
   - If your proxy list is loaded from an external source (e.g., a file or API), the cache avoids redundant reads/calls, significantly speeding up your app.

---

### Advanced: Cache Invalidation

If the proxy list changes (e.g., a new proxy is added), you can **invalidate the cache** by using the `clear` parameter.

#### Example with Cache Clearing:

```python
import streamlit as st

@st.cache_data
def load_proxies():
    proxies = [
        "http://proxy1.example.com:8080",
        "http://proxy2.example.com:8080",
        "http://proxy3.example.com:8080",
    ]
    return proxies

st.title("Proxy Loader with Cache and Invalidation")

# Load proxies
proxies = load_proxies()
st.write("Loaded Proxies:", proxies)

# Button to clear the cache and reload proxies
if st.button("Refresh Proxies"):
    load_proxies.clear()  # Clear the cache
    st.experimental_rerun()  # Reload the app to re-fetch proxies
```

---

### When to Use Caching for Proxies

- **Ideal Use Cases**:

  - Proxy lists are relatively static and do not change frequently.
  - Proxies are loaded from a time-intensive source (e.g., a database or external API).

- **Avoid Caching**:
  - If the proxy list changes frequently or dynamically during runtime.
  - If you want real-time updates every time the app reruns.

---

Would you like to see an example with real file reading or API integration for the proxies?

## Remove the spinning wheel

- Simply by handling the `show_spinner` and pass it to the decorator.
- Read more [here](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_data)

```python
st.cache_data(func=None, *, ttl, max_entries, show_spinner, persist, experimental_allow_widgets, hash_funcs=None)

# For example

@st.cache_data(show_spinner=False)
def generate_items():
    # Placeholder function to generate or fetch items
    items = save_valid_proxies()

    return items #["Item A", "Item B", "Item C", "Item D", "Item E"]

```
