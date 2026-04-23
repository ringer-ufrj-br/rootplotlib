from typing import Union, List, Optional
import array
import rootplotlib as rpl
import ROOT
import numpy as np

__all__ = [
            'new',
            'new2',
            'fill',
            'density',
            'divide',
            'shift',
            'make_hist',
          ]


def new( name: str, xbins: int, xmin: float, xmax: float, ybins: int, ymin: float, ymax: float, title: str = '') -> ROOT.TH2F:
    """
    Creates a new TH2F histogram with fixed bin widths.

    Parameters
    ----------
    name : str
        Histogram name.
    xbins : int
        Number of bins in X.
    xmin : float
        Lower bound of the X range.
    xmax : float
        Upper bound of the X range.
    ybins : int
        Number of bins in Y.
    ymin : float
        Lower bound of the Y range.
    ymax : float
        Upper bound of the Y range.
    title : str, optional
        Histogram title, by default ''.

    Returns
    -------
    ROOT.TH2F
        The created histogram.
    """
    return ROOT.TH2F(name, title, xbins, xmin, xmax, ybins, ymin, ymax)


def new2( name: str, xbins: Union[List[float], np.ndarray, array.array], ybins: Union[List[float], np.ndarray, array.array], title: str = '') -> ROOT.TH2F:
    """
    Creates a new TH2F histogram with variable bin widths in both X and Y.

    Parameters
    ----------
    name : str
        Histogram name.
    xbins : Union[List[float], np.ndarray, array.array]
        Collection of bin edges for X.
    ybins : Union[List[float], np.ndarray, array.array]
        Collection of bin edges for Y.
    title : str, optional
        Histogram title, by default ''.

    Returns
    -------
    ROOT.TH2F
        The created histogram.
    """
    if isinstance(xbins, list):
        _xbins = array.array('d', xbins)
    elif isinstance(xbins, np.ndarray):
        _xbins = array.array('d', xbins.tolist())
    else:
        _xbins = xbins

    if isinstance(ybins, list):
        _ybins = array.array('d', ybins)
    elif isinstance(ybins, np.ndarray):
        _ybins = array.array('d', ybins.tolist())
    else:
        _ybins = ybins
    return ROOT.TH2F(name, title, len(_xbins)-1, _xbins, len(_ybins)-1, _ybins)



def fill( hist: ROOT.TH2, xvalues: Union[List[float], np.ndarray], yvalues: Union[List[float], np.ndarray] ) -> None:
    """
    Fills a 2D histogram with collections of X and Y values.
    Uses TH2::FillN if possible, otherwise falls back to Fill in a loop.

    Parameters
    ----------
    hist : ROOT.TH2
        The histogram to fill.
    xvalues : Union[List[float], np.ndarray]
        Collection of X values.
    yvalues : Union[List[float], np.ndarray]
        Collection of Y values.
    """

    if isinstance(xvalues, list):
        xvalues = np.array(xvalues)
    if isinstance(yvalues, list):
        yvalues = np.array(yvalues)

    w = array.array( 'd', np.ones_like( xvalues ) )

    # treat x values
    _xvalues = array.array('d', xvalues.tolist()) if isinstance(xvalues, np.ndarray) else array.array('d', xvalues)

    # treat y values
    _yvalues = array.array('d', yvalues.tolist()) if isinstance(yvalues, np.ndarray) else array.array('d', yvalues)

    if len(_xvalues) != len(_yvalues):
        print('It is not possible to fill the histogram. x/y values must be the same size')
    else:
        # This is a Hack, for some reason, sometimes, the FillN option breaks
        # and raises a TypeError. Fill is slower but always works.
        try:
            hist.FillN( len(_xvalues), _xvalues, _yvalues,  w)
        except TypeError:
            for xval, yval in zip(_xvalues, _yvalues):
                hist.Fill(xval, yval)

    
def density( hist: ROOT.TH2 ) -> ROOT.TH2:
    """
    Creates a density clone of the 2D histogram (normalized to integral = 1).

    Parameters
    ----------
    hist : ROOT.TH2
        The input histogram.

    Returns
    -------
    ROOT.TH2
        The normalized clone.
    """
    h = hist.Clone()
    h.SetName( hist.GetName() + '_density')
    h.Scale(1/h.Integral())
    return h


def divide( hist_num: ROOT.TH2, hist_den: ROOT.TH2 ) -> ROOT.TH2:
    """
    Divides two 2D histograms.

    Parameters
    ----------
    hist_num : ROOT.TH2
        Numerator histogram.
    hist_den : ROOT.TH2
        Denominator histogram.

    Returns
    -------
    ROOT.TH2
        The ratio histogram.
    """
    h = hist_num.Clone()
    h.SetName(hist_num.GetName()+'_ratio')
    h.Divide( hist_den )
    return h


def shift( hist: ROOT.TH2, shift_units: int ) -> ROOT.TH2:
    """
    Creates a clone of the 2D histogram shifted in X.

    Parameters
    ----------
    hist : ROOT.TH2
        The input histogram.
    shift_units : int
        Number of bins to shift in X.

    Returns
    -------
    ROOT.TH2
        The shifted clone.
    """
    h = hist.Clone()
    h.SetName( hist.GetName() + '_shift')
    h.Reset('M')
    for b in range(1, hist.GetNbinsX()):
        content = hist.GetBinContent(b)
        h.SetBinContent(b+shift_units, content)
    return h


def make_hist(name: str, xaxis_values: Union[List[float], np.ndarray], yaxis_values: Union[List[float], np.ndarray], xbins: int, xmin: float, xmax: float, ybins: int, ymin: float, ymax: float, title: Optional[str] = None) -> ROOT.TH2F:
    """
    Creates and fills a 2D histogram from data.

    Parameters
    ----------
    name : str
        Histogram name for ROOT.
    xaxis_values : Union[List[float], np.ndarray]
        The values to be used for the X-axis.
    yaxis_values : Union[List[float], np.ndarray]
        The values to be used for the Y-axis.
    xbins : int
        Number of bins in X.
    xmin : float
        Minimum value in X.
    xmax : float
        Maximum value in X.
    ybins : int
        Number of bins in Y.
    ymin : float
        Minimum value in Y.
    ymax : float
        Maximum value in Y.
    title : str, optional
        Histogram title.

    Returns
    -------
    ROOT.TH2F
        The created and filled histogram.
    """
    
    xbin_size = (xmax - xmin)/xbins    
    ybin_size = (ymax - ymin)/ybins

    # create the bin edges
    binx = np.arange(xmin, xmax, step=xbin_size)
    biny = np.arange(ymin, ymax, step=ybin_size)

    if title is None:
        title = ''
    hist = ROOT.TH2F( name, title, len(binx)-1, xmin, xmax, len(biny)-1, ymin, ymax)
    fill(hist, xaxis_values, yaxis_values)
    return hist