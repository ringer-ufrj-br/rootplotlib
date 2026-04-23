from typing import Optional, Tuple
import rootplotlib as rpl

__all__ = [ 'set_xlabel',
            'set_ylabel',
            'set_axis_labels',
            'fix_xaxis_ranges',
            'fix_yaxis_ranges',
            'set_yaxis_ranges',
            'get_yaxis_ranges',
           ]

def set_xlabel(xlabel: str, pad: Optional[str] = None, fig: Optional['rpl.Figure'] = None) -> None:
    """
    Sets the X-axis label for a specific pad or the current figure.

    Parameters
    ----------
    xlabel : str
        The label text for the X-axis.
    pad : str, optional
        The name of the pad to set the label for. If None, the main canvas is used.
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.
    """
    fig = rpl.get_figure() if not fig else fig
    fig.set_xlabel( xlabel, pad=pad )


def set_ylabel(ylabel: str, pad: Optional[str] = None, fig: Optional['rpl.Figure'] = None) -> None:
    """
    Sets the Y-axis label for a specific pad or the current figure.

    Parameters
    ----------
    ylabel : str
        The label text for the Y-axis.
    pad : str, optional
        The name of the pad to set the label for. If None, the main canvas is used.
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.
    """
    fig = rpl.get_figure() if not fig else fig
    fig.set_ylabel( ylabel, pad=pad )


def set_axis_labels(xlabel: str, ylabel: str, yratiolabel: str = 'ratio', fig: Optional['rpl.Figure'] = None) -> None:
    """
    Sets X, Y, and optionally ratio axis labels for the figure. 
    Handles both standard and ratio canvases automatically.

    Parameters
    ----------
    xlabel : str
        The label text for the X-axis.
    ylabel : str
        The label text for the Y-axis.
    yratiolabel : str, optional
        The label text for the ratio Y-axis (if applicable), by default 'ratio'.
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.
    """
    fig = rpl.get_figure() if not fig else fig
    if fig.get_pad('pad_top'):
        set_ylabel( ylabel, pad='pad_top')
        set_ylabel( yratiolabel, pad='pad_bot')
        set_xlabel( xlabel, pad='pad_bot')
    else:
        set_xlabel( xlabel )
        set_ylabel( ylabel )


def fix_xaxis_ranges(xminf: float = 1., xminc: float = 0., xmaxf: float = 1., xmaxc: float = 0., only_filled: bool = False, pad: Optional[str] = None, fig: Optional['rpl.Figure'] = None) -> None:
    """
    Adjusts the X-axis ranges based on current limits and scaling factors.

    Parameters
    ----------
    xminf : float, optional
        Multiplicative factor for the minimum X value, by default 1.
    xminc : float, optional
        Additive constant for the minimum X value, by default 0.
    xmaxf : float, optional
        Multiplicative factor for the maximum X value, by default 1.
    xmaxc : float, optional
        Additive constant for the maximum X value, by default 0.
    only_filled : bool, optional
        If True, only considers bins with content, by default False.
    pad : str, optional
        The name of the pad to use.
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.
    """
    fig = rpl.get_figure() if not fig else fig
    xmin, xmax = fig.get_xaxis_ranges( only_filled = only_filled , pad=pad)
    fig.set_xaxis_ranges(xmin*xminf+xminc, xmax*xmaxf+xmaxc, for_all=True, pad=pad)



def fix_yaxis_ranges(yminf: float = 1., yminc: float = 0., ymaxf: float = 1., ymaxc: float = 0., ignore_zeros: bool = True, ignore_errors: bool = False, pad: Optional[str] = None, fig: Optional['rpl.Figure'] = None) -> None:
    """
    Adjusts the Y-axis ranges based on current limits and scaling factors.

    Parameters
    ----------
    yminf : float, optional
        Multiplicative factor for the minimum Y value, by default 1.
    yminc : float, optional
        Additive constant for the minimum Y value, by default 0.
    ymaxf : float, optional
        Multiplicative factor for the maximum Y value, by default 1.
    ymaxc : float, optional
        Additive constant for the maximum Y value, by default 0.
    ignore_zeros : bool, optional
        If True, ignores bins with zero content when calculating ranges, by default True.
    ignore_errors : bool, optional
        If True, ignores bin errors when calculating ranges, by default False.
    pad : str, optional
        The name of the pad to use.
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.
    """
    fig = rpl.get_figure() if not fig else fig
    ymin, ymax = fig.get_yaxis_ranges(pad=pad, ignore_zeros=ignore_zeros, ignore_errors=ignore_errors)
    fig.set_yaxis_ranges(ymin*yminf+yminc, ymax*ymaxf+ymaxc, pad=pad)


def set_yaxis_ranges( ymin: float , ymax: float, pad: Optional[str] = None, fig: Optional['rpl.Figure'] = None) -> None:
    """
    Sets specific Y-axis ranges.

    Parameters
    ----------
    ymin : float
        The minimum Y value.
    ymax : float
        The maximum Y value.
    pad : str, optional
        The name of the pad to use.
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.
    """
    fig = rpl.get_figure() if not fig else fig
    fig.set_yaxis_ranges(ymin, ymax, pad=pad)


def get_yaxis_ranges( pad: Optional[str] = None, fig: Optional['rpl.Figure'] = None ) -> Tuple[float, float]:
    """
    Returns the current Y-axis ranges for a specific pad.

    Parameters
    ----------
    pad : str, optional
        The name of the pad to use.
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.

    Returns
    -------
    Tuple[float, float]
        A tuple containing (ymin, ymax).
    """
    fig = rpl.get_figure() if not fig else fig
    return fig.get_yaxis_ranges(pad=pad, ignore_zeros=False, ignore_errors=False)
