# rootplotlib

[![CI](https://github.com/ringer-ufrj-br/rootplotlib/actions/workflows/test.yml/badge.svg)](https://github.com/ringer-ufrj-br/rootplotlib/actions/workflows/test.yml)

`rootplotlib` is a Python library designed to simplify and enhance plotting with ROOT (PyROOT), providing a more "matplotlib-like" interface and utilities for high-energy physics plots.

## How to Install?

You can install `rootplotlib` directly from the GitHub repository using `pip`:

```bash
pip install git+https://github.com/ringer-ufrj-br/rootplotlib.git
```

## Quick Start / Examples

Here is a simple example of how to use `rootplotlib` to plot multiple histograms:

```python
import ROOT
import rootplotlib as rpl

# Create dummy histograms
h1 = ROOT.TH1F("h1", "Histogram 1", 50, -4, 4)
h1.FillRandom("gaus", 10000)
h2 = ROOT.TH1F("h2", "Histogram 2", 50, -4, 4)
h2.FillRandom("gaus", 5000)

# Plot histograms
fig = rpl.plot_hist(
    [h1, h2],
    xlabel="Energy [GeV]",
    ylabel="Events",
    colors=[ROOT.kBlue, ROOT.kRed],
    markers=[20, 21]
)

# Save the figure
fig.save_as("my_plot.pdf")
```

### Plotting Ratios

```python
fig = rpl.plot_hist_ratios(
    [h1, h2],
    xlabel="Energy [GeV]",
    ylabel="Events",
    ratio_label="Ratio",
    colors=[ROOT.kBlue, ROOT.kRed],
    markers=[20, 21]
)
```

## Coding Style

We strictly follow the **snake_case** naming convention for variables, functions, and constants.

✅ **Do:**
- `my_awesome_variable = 10`
- `def calculate_efficiency(pass, total):`
- `number_of_events = 1000`

❌ **Don't:**
- `myAwesomeVariable = 10` (camelCase)
- `CalculateEfficiency(pass, total)` (PascalCase for functions)
- `NUMBER_OF_EVENTS = 1000` (SCREAMING_SNAKE_CASE - use regular snake_case instead)

## CI Testing

This repository includes a GitHub Actions workflow that automatically verifies the library can be imported in a ROOT-enabled environment. Ensure any new contributions do not break the core imports.
