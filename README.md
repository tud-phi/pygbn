# pygbn
[![ci](https://github.com/tud-phi/pygbn/actions/workflows/release.yml/badge.svg)](https://github.com/tud-phi/pygbn/actions/workflows/main.yml)
[![ci](https://github.com/tud-phi/pygbn/actions/workflows/test.yml/badge.svg)](https://github.com/tud-phi/pygbn/actions/workflows/test.yml)

This package implements the generalized binary noise (GBN) model of [[1]](#1) in Python. 
The code is based on the Matlab implementation revised by Ivo Houtzager in 2007 at the Delft Center of Systems and Control.

## Installation
You can very easily install the package using pip:
```bash
pip install pygbn
```
or after locally cloning the source code:
```bash
pip install .
```

## Usage
Below is an example of how to use the package.
```python
import matplotlib.pyplot as plt
from pygbn import gbn

if __name__ == '__main__':
    seed = 0 # random seed

    h = 0.05 # sampling period [s]
    T = 1 # length of signal [s]
    A = 1 # amplitude of signal
    ts = 1 # estimated settling time of the process [s]

    # flag indicating process damping properties
    # flag = 0 if the process is over-damped (default)
    # flag = 1 if the process is oscillary (min phase)
    # flag = 2 if the process is oscillary (non min phase)
    flag = 0

    # generate time array
    t = np.arange(start=0, stop=T, step=h)

    # generate the signal
    # the gbn function returns a time array and a signal array
    u = gbn(h, T, A, ts, flag, seed=seed)

    # optional: plot the generated signal
    plt.plot(t, u)
```

## Citations
<a id="1">[1]</a> Tulleken, H. J. (1990). 
Generalized binary noise test-signal concept for improved identification-experiment design. 
Automatica, 26(1), 37-49.
