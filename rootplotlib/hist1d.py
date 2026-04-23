from typing import Union, List
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
            'rebin',
          ]


def new( name: str, bins: int, xmin: float, xmax: float, title: str = '') -> ROOT.TH1F:
    """
    Creates a new TH1F histogram with fixed bin widths.

    Parameters
    ----------
    name : str
        Histogram name.
    bins : int
        Number of bins.
    xmin : float
        Lower bound of the range.
    xmax : float
        Upper bound of the range.
    title : str, optional
        Histogram title, by default ''.

    Returns
    -------
    ROOT.TH1F
        The created histogram.
    """
    return ROOT.TH1F(name, title, bins, xmin, xmax)


def new2( name: str, xbins: Union[List[float], np.ndarray, array.array], title: str = '') -> ROOT.TH1F:
    """
    Creates a new TH1F histogram with variable bin widths.

    Parameters
    ----------
    name : str
        Histogram name.
    xbins : Union[List[float], np.ndarray, array.array]
        List or array of bin edges.
    title : str, optional
        Histogram title, by default ''.

    Returns
    -------
    ROOT.TH1F
        The created histogram.
    """
    if isinstance(xbins, list):
        _xbins = array.array('d', xbins)
    elif isinstance(xbins, np.ndarray):
        _xbins = array.array('d', xbins.tolist())
    else:
        _xbins = xbins
    return ROOT.TH1F(name, title, len(_xbins)-1, _xbins)


def fill( hist: ROOT.TH1, values: Union[List[float], np.ndarray] ) -> None:
    """
    Fills a histogram with a collection of values using TH1::FillN.

    Parameters
    ----------
    hist : ROOT.TH1
        The histogram to fill.
    values : Union[List[float], np.ndarray]
        Collection of values to fill into the histogram.
    """
    if isinstance(values, list):
        values = np.array(values)
    w = array.array( 'd', np.ones_like( values ) )
    hist.FillN(len(values), array.array('d',  values),  w)

    
def density( hist: ROOT.TH1 ) -> ROOT.TH1:
    """
    Creates a density clone of the histogram (normalized to integral = 1).

    Parameters
    ----------
    hist : ROOT.TH1
        The input histogram.

    Returns
    -------
    ROOT.TH1
        The normalized clone.
    """
    h = hist.Clone()
    h.SetName( hist.GetName() + '_density')
    h.Scale(1/h.Integral())
    return h


def divide( hist_num: ROOT.TH1, hist_den: ROOT.TH1 ) -> ROOT.TH1:
    """
    Divides two histograms with binomial error calculation.

    Parameters
    ----------
    hist_num : ROOT.TH1
        Numerator histogram.
    hist_den : ROOT.TH1
        Denominator histogram.

    Returns
    -------
    ROOT.TH1
        The ratio histogram.
    """
    hist = hist_num.Clone()
    hist.SetName(hist_num.GetName()+'_ratio')
    hist.Divide( hist_num, hist_den,1.,1.,'B' )
    return hist


def shift( hist: ROOT.TH1, shift_units: int ) -> ROOT.TH1:
    """
    Creates a clone of the histogram shifted by a certain number of bins.

    Parameters
    ----------
    hist : ROOT.TH1
        The input histogram.
    shift_units : int
        Number of bins to shift (positive or negative).

    Returns
    -------
    ROOT.TH1
        The shifted clone.
    """
    h = hist.Clone()
    h.SetName( hist.GetName() + '_shift')
    h.Reset('M')
    for b in range(1, hist.GetNbinsX()):
        content = hist.GetBinContent(b)
        h.SetBinContent(b+shift_units, content)
    return h



def rebin( hist: ROOT.TH1, nbins: int, xmin: float, xmax: float ) -> ROOT.TH1F:
  """
  Resizes/Rebins a histogram to a new range and number of bins by sampling the original.

  Parameters
  ----------
  hist : ROOT.TH1
      The input histogram.
  nbins : int
      New number of bins.
  xmin : float
      New lower bound.
  xmax : float
      New upper bound.

  Returns
  -------
  ROOT.TH1F
      The rebinned histogram.
  """
  h = ROOT.TH1F(hist.GetName()+'_resize', hist.GetTitle(), nbins,xmin,xmax)
  for bin in range(h.GetNbinsX()):
    x = h.GetBinCenter(bin+1)
    m_bin = hist.FindBin(x)
    y = hist.GetBinContent(m_bin)
    error = hist.GetBinError(m_bin)
    h.SetBinContent(bin+1,y)
    h.SetBinError(bin+1,error)
  return h


