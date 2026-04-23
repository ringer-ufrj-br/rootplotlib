# rootplotlib

[![CI](https://github.com/ringer-ufrj-br/rootplotlib/actions/workflows/test.yml/badge.svg)](https://github.com/ringer-ufrj-br/rootplotlib/actions/workflows/test.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![ROOT Version](https://img.shields.io/badge/ROOT-6.xx-orange)](https://root.cern/)

`rootplotlib` is a Python library designed to simplify and enhance plotting with ROOT (PyROOT), providing a more "matplotlib-like" interface and utilities for high-energy physics plots.

---

## ✨ Key Features

*   **Matplotlib-inspired API**: Simplify complex ROOT plotting commands with a familiar syntax.
*   **Ratio Plots**: Effortlessly create ratio pads with automatic alignment and formatting.
*   **Custom Styles**: Built-in support for ATLAS and Lorenzetti styles.
*   **Type Safety**: Comprehensive type hint support for better IDE experience and robust code.
*   **Global Figure Management**: Easily manage active canvases across your scripts.

---

## 🚀 Installation

You can install `rootplotlib` directly from the GitHub repository using `pip`:

```bash
pip install git+https://github.com/ringer-ufrj-br/rootplotlib.git
```

---

## 📚 Quick Start

### Basic Plotting

```python
import ROOT
import rootplotlib as rpl

# Apply a style
rpl.set_atlas_style()

# Create dummy histograms
h1 = ROOT.TH1F("h1", "Histogram 1", 50, -4, 4)
h1.FillRandom("gaus", 10000)
h2 = ROOT.TH1F("h2", "Histogram 2", 50, -4, 4)
h2.FillRandom("gaus", 5000)

# Create and plot
fig = rpl.plot_hist(
    [h1, h2],
    xlabel="Energy [GeV]",
    ylabel="Events",
    colors=[ROOT.kBlue, ROOT.kRed],
    markers=[20, 21]
)

# Add a label
rpl.set_atlas_label(0.2, 0.8, "Internal")

# Save the figure
fig.savefig("my_plot.pdf")
```

### Ratio Canvas

Creating a ratio plot is as simple as:

```python
fig = rpl.plot_hist_ratios(
    [h1, h2],
    xlabel="Energy [GeV]",
    ylabel="Events",
    ratio_label="Ratio",
    colors=[ROOT.kBlue, ROOT.kRed],
    markers=[20, 21]
)

fig.savefig("my_ratio_plot.pdf")
```

---

## 🛠️ Advanced Usage

### 2D Histograms
```python
import rootplotlib.hist2d as h2d
hist = h2d.new("my_hist", 50, -4, 4, 50, -4, 4)
h2d.fill(hist, x_data, y_data)
```

### Manual Canvas Management
```python
fig = rpl.create_canvas("my_canvas")
rpl.add_hist(h1, drawopt="hist")
rpl.format_canvas_axes()
fig.savefig("test.png")
```

---

## 🎨 Coding Style

We follow the **snake_case** naming convention for variables, functions, and constants to maintain consistency with the Python ecosystem.

✅ **Do:**
- `total_events = 100]`
- `def get_efficiency(h_pass, h_total):`

❌ **Don't:**
- `TotalEvents = 100` (PascalCase)
- `getEfficiency(h_pass, h_total)` (camelCase)

---

## 🤝 Contributing

Contributions are welcome! This repository includes a GitHub Actions workflow that automatically verifies the library can be imported. 

Ensure that:
1. New functions have proper **type hints**.
2. Code follows the **snake_case** convention.
3. You have tested the changes in a ROOT-enabled environment.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
