from typing import Optional, Sequence, Any
import ROOT
import rootplotlib as rpl
from rootplotlib.figures import Figure

__all__ = ["plot_profiles",
           "add_hist",
           "plot_hist",
           "plot_hist_ratios"]


def add_hist(hist: ROOT.TH1,
             drawopt: str="pE1",
             pad: Optional[str]=None,
             fig: Optional[Figure]=None) -> None:
    """
    Adds histogram to current figure

    Parameters
    ----------
    hist : ROOT.TH1
        Histogram object to add
    drawopt : str, optional
        ROOT draw operation, by default "pE1"
    pad : str, optional
        Pad to draw to, by default None
    """
    fig = rpl.get_figure() if fig is None else fig
    fig.add_hist(hist, drawopt, pad)


def hist_divide(num: ROOT.TH1, den: ROOT.TH1) -> ROOT.TH1:
    """
    Divides one histogram by another

    Parameters
    ----------
    num : ROOT.TH1
        Numerator histogram
    den : ROOT.TH1
        Denominator histogram

    Returns
    -------
    ROOT.TH1
        Quotient histogram
    """
    
    num_name = num.GetName()
    den_name = den.GetName()
    ratio_name = f"{num_name}_over_{den_name}"
    ratio = num.Clone()
    ratio.SetName(ratio_name)
    ratio.Divide(den)
    
    return ratio
    


def plot_profiles(hists: Sequence[ROOT.TH1],
                  xlabel: str,
                  ylabel: str,
                  colors: Sequence[int], 
                  markers: Sequence[int],
                  drawopt: str="pE1",
                  doRatioCanvas: bool=False,
                  ratio_label: str="Ratio",
                  ref_place: str="den",
                  **canvas_kwargs: Any) -> rpl.Figure:
    
    """
    Plots profile histograms, optionally on a ratio canvas.

    Parameters
    ----------
    hists : Sequence[ROOT.TH1]
        Sequence of histograms to be plotted.
    xlabel : str
        X-axis label.
    ylabel : str
        Y-axis label.
    colors : Sequence[int]
        Collection of ROOT colors for each histogram.
    markers : Sequence[int]
        Collection of ROOT marker styles for each histogram.
    drawopt : str, optional
        ROOT draw operation, by default "pE1".
    doRatioCanvas : bool, optional
        If True, creates a ratio canvas (requires >1 histogram), by default False.
    ratio_label : str, optional
        Label for the ratio Y-axis, by default "Ratio".
    ref_place : str, optional
        If 'den', use first hist as denominator; if 'num', use as numerator in ratio, by default "den".
    **canvas_kwargs : Any
        Additional keyword arguments for create_canvas or create_ratio_canvas.

    Returns
    -------
    rpl.Figure
        Figure with the histograms plotted.
    """
    doRatio = True if (doRatioCanvas and (len(hists)>1)) else False
    if doRatio:
        fig = plot_hist_ratios(hists,
                               xlabel=xlabel,
                               ylabel=ylabel,
                               ratio_label=ratio_label,
                               colors=colors,
                               markers=markers,
                               ref_place=ref_place,
                               drawopt=drawopt,
                               **canvas_kwargs)
    else:
        fig = plot_hist(hists,
                        xlabel=xlabel,
                        ylabel=ylabel,
                        colors=colors,
                        markers=markers,
                        drawopt=drawopt,
                        **canvas_kwargs)
    return fig


def plot_hist(hists: Sequence[ROOT.TH1],
              xlabel: str,
              ylabel: str,
              colors: Sequence[int],
              markers: Sequence[int],
              drawopt: str="pE1",
              **canvas_kwargs: Any) -> rpl.Figure:
    """
    Plots several histograms from a sequence

    Parameters
    ----------
    hists : Sequence[ROOT.TH1]
        Sequence of histograms to be plotted
    xlabel : str
        X axis label
    ylabel : str
        Y axis label
    colors : Sequence[int]
        Marker and line colors per histogram
    markers : Sequence[int]
        Marker styles per histogram
    drawopt : str, optional
        ROOT draw operation, by default "pE1"

    Returns
    -------
    rpl.Figure
        Figure with the histograms plotted
    """
    fig = rpl.create_canvas(**canvas_kwargs) if canvas_kwargs else rpl.create_canvas("canvas", "", 700, 500)
    rpl.set_figure(fig)
    for hist, color, marker in zip(hists, colors, markers):
        hist.GetXaxis().SetLabelSize(0)
        hist.SetLineColor(color)
        hist.SetMarkerColor(color)
        hist.SetMarkerStyle(marker)
        hist.SetMarkerSize(1)
        fig.add_hist(hist, drawopt)
    
    fig.set_xlabel(xlabel)
    fig.set_ylabel(ylabel)
    rpl.format_canvas_axes(XLabelSize=18, YLabelSize=18, XTitleOffset=0.87, YTitleOffset=1.5, fig=fig)
    
    return fig


def plot_hist_ratios(hists: Sequence[ROOT.TH1],
                     xlabel: str,
                     ylabel: str,
                     ratio_label: str,
                     colors: Sequence[int], 
                     markers: Sequence[int],
                     ref_place: str="den",
                     drawopt: str="pE1",
                     **canvas_kwargs: Any) -> rpl.Figure:
    """
    Plots several histogram on a ratio canvas. This function considers the first histogram
    as the reference one. On the top pad the histograms are plotted.
    On the bottom pad a ratio between the current histogram and the first
    one is plotted

    Parameters
    ----------
    hists : Sequence[ROOT.TH1]
        Sequence of histograms to be plotted
    xlabel : str
        X axis label
    ylabel : str
        Y axis label
    ratio_label : str
        Bottom pad Y axis label
    colors : Sequence[int]
        Marker and line colors per histogram
    markers : Sequence[int]
        Marker styles per histogram
    ref_place : str, optional
        If den, the ratio operation considers the ref hist as the denominator.
        Else, the ratio operation considers the ref hist as the numerator.
        By default "den"
    drawopt : str, optional
        ROOT draw operation, by default "pE1"

    Returns
    -------
    rpl.Figure
        Figure with the histograms plotted
    """
    fig = rpl.create_ratio_canvas(**canvas_kwargs) if canvas_kwargs else rpl.create_ratio_canvas("canvas", "", 700, 500)
    rpl.set_figure(fig)
    for idx, (hist, color, marker) in enumerate(zip(hists, colors, markers)):
        hist.GetXaxis().SetLabelSize(0)
        hist.SetLineColor(color)
        hist.SetMarkerColor(color)
        hist.SetMarkerStyle(marker)
        hist.SetMarkerSize(1)
        fig.add_hist(hist, drawopt, pad="pad_top")
        if idx == 0:
            hist_ref = hist
        else:
            hist_ratio = hist_divide(hist, hist_ref) if ref_place == "den" else hist_divide(hist_ref, hist)
            hist_ratio.SetLineColor(color)
            hist_ratio.SetMarkerColor(color)
            hist_ratio.SetMarkerStyle(marker)
            hist_ratio.SetMarkerSize(1)
            fig.add_hist(hist_ratio, "P", pad="pad_bot")
    
    fig.set_xlabel(xlabel, pad="pad_bot")
    fig.set_ylabel(ratio_label, pad="pad_bot")
    fig.set_ylabel(ylabel, pad="pad_top")
    rpl.set_axis_labels(xlabel,ylabel,ratio_label)
    rpl.format_ratio_canvas_axes(XTitleOffset=0, fig=fig)       
    
    return fig
