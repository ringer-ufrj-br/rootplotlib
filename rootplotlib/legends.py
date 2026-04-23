from typing import Optional, List
from ROOT import TLegend, TLatex, TH1, TH2
import rootplotlib as rpl

__all__ = ['add_text', 'add_legend']

def add_text(x: float, y: float, text: str, color: int = 1, textfont: int = 42, textsize: float = 0.1, pad: Optional[str] = None, fig: Optional['rpl.Figure'] = None) -> None:
    """
    Adds a text label (TLatex) to a specific pad or the current figure.

    Parameters
    ----------
    x : float
        X-coordinate in NDC.
    y : float
        Y-coordinate in NDC.
    text : str
        The text to display.
    color : int, optional
        ROOT color code, by default 1 (black).
    textfont : int, optional
        ROOT font style, by default 42.
    textsize : float, optional
        Text size in NDC, by default 0.1.
    pad : str, optional
        The name of the pad.
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.
    """
    fig = rpl.get_figure() if not fig else fig
    pad_obj = fig.get_pad(pad)
    pad_obj.cd()
    tex = TLatex()
    tex.SetNDC()
    tex.SetTextFont(textfont)
    tex.SetTextColor(color)
    tex.SetTextSize(textsize)
    tex.DrawLatex(x,y,text)
    fig.add_legend(tex)


def add_legend(legends: List[str], x1: float = .8, y1: float = .8, x2: float = .9, y2: float = .9,
               pad: Optional[str] = None, textsize: int = 18, ncolumns: int = 1,
               option: str = 'f', squarebox: bool = True, title: str = '',
               fig: Optional['rpl.Figure'] = None) -> None:
    """
    Creates and adds a TLegend to the figure, automatically linking entries to primitives in the pad.

    Parameters
    ----------
    legends : List[str]
        List of texts for each legend entry.
    x1 : float, optional
        Lower-left X in NDC, by default 0.8.
    y1 : float, optional
        Lower-left Y in NDC, by default 0.8.
    x2 : float, optional
        Upper-right X in NDC, by default 0.9.
    y2 : float, optional
        Upper-right Y in NDC, by default 0.9.
    pad : str, optional
        The name of the pad.
    textsize : int, optional
        Font size in pixels, by default 18.
    ncolumns : int, optional
        Number of columns in the legend, by default 1.
    option : str, optional
        Draw option for entries (e.g., 'f', 'p', 'l'), by default 'f'.
    squarebox : bool, optional
        If True, attempts to adjust margin for square boxes, by default True.
    title : str, optional
        Legend header title, by default ''.
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.
    """

    fig = rpl.get_figure() if not fig else fig
    canvas = fig.get_pad(pad)
    leg = TLegend(x1,y1,x2,y2,title)
    leg.SetName('legend' + ("_" + title if title else ""))
    leg.SetTextFont(43)
    leg.SetTextSize(textsize)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetNColumns(ncolumns)

    primitives = []
    for primitive in canvas.GetListOfPrimitives():
        if isinstance(primitive, (TH1, TH2)):
            primitives.append( primitive )

    for idx, legend in enumerate(legends): 
        if idx < len(primitives):
            leg.AddEntry(primitives[idx], legend, option) # plef

    # recipe for making roughly square boxes
    if squarebox:
        h = leg.GetY2()-leg.GetY1()
        w = leg.GetX2()-leg.GetX1()
        if leg.GetNRows():
            leg.SetMargin(leg.GetNColumns()*h/float(leg.GetNRows()*w))
    leg.SetHeader("#font[63]{" + title + "}")
    fig.add_legend(leg)
 
