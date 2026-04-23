
__all__ = ['format_canvas_axes', 'create_canvas', 'create_ratio_canvas', 'format_ratio_canvas_axes']

from typing import Optional, List
from ROOT import TCanvas, TPad
import ROOT
import rootplotlib as rpl
import uuid



def generate_canvas_name() -> str:
    """
    Generates a random 8-character UUID string.

    Returns
    -------
    str
        An 8-character random string.
    """
    return "canvas_"+str(uuid.uuid4())[:8]



def create_canvas(canw: int=700,
                  canh: int=500,
                  name: str="",
                  title: str =""
                ) -> 'rpl.Figure':
                
    """
    Creates a Figure object with the given canvas parameters

    Parameters
    ----------
    name : str
        Canvas name
    title : str, optional
        Canvas title, by default ""
    canw : int, optional
        Canvas width as defined by ROOT.TCanvas, by default 700
    canh : int, optional
        Canvas height as defined by ROOT.TCanvas, by default 500

    Returns
    -------
    rpl.Figure
        Created Figure object
    """
    name = generate_canvas_name() if name=="" else name
    canvas = TCanvas( name, title, canw, canh )
    fig = rpl.Figure(canvas)
    rpl.set_figure(fig)
    return fig

def create_ratio_canvas(canw: int=700,
                        canh: int=500,
                        name: str="",
                        title: str="",
                        ratio_size_as_fraction: float=0.35,
                        drawopt: str='pE1') -> 'rpl.Figure':
    """
    Creates a Figure object with a canvas with two pads:
    - A bigger one on top named pad_top
    - A smaller one on the bottom named pad_bot

    Parameters
    ----------
    name : str
        Canvas name
    title : str, optional
        Canvas title, by default ""
    canw : int, optional
        Canvas width as defined by ROOT.TCanvas, by default 700
    canh : int, optional
        Canvas height as defined by ROOT.TCanvas, by default 500
    ratio_size_as_fraction : float, optional
        Pecentage of canvas vertical size occuppied by the
        bottom pad, by default 0.35
    drawopt : str, optional
        ROOT draw operation, by default 'pE1'

    Returns
    -------
    rpl.Figure
        Rootplotlib figure with the canvas created
    """
    name = generate_canvas_name() if name=="" else name
    canvas = ROOT.TCanvas(name,title,canw,canh)
    fig = rpl.Figure(canvas)
    rpl.set_figure(fig)
    canvas.SetFillStyle(4050)

    # Top
    canvas.cd()
    top = ROOT.TPad("pad_top",
                    "This is the top pad",
                    0.0,ratio_size_as_fraction,1.0,1.0)
    top.SetBottomMargin(0.02/float(top.GetHNDC()))
    top.SetTopMargin(0.04/float(top.GetHNDC()))
    top.SetRightMargin(0.05)
    top.SetLeftMargin(0.16)
    top.SetFillColor(0)
    top.Draw(drawopt)
    fig.append(top)

    # Bot
    canvas.cd()
    bot = ROOT.TPad("pad_bot",
                    "This is the bottom pad",
                    0.0,0.0,1.0,ratio_size_as_fraction)
    bot.SetBottomMargin(0.12/float(bot.GetHNDC()))
    bot.SetTopMargin(0.02/float(bot.GetHNDC()))
    bot.SetRightMargin(0.05)
    bot.SetLeftMargin(0.16)
    bot.SetFillColor(0)
    bot.Draw(drawopt)
    fig.append(bot)
    
    return fig



def format_canvas_axes( XTitleSize: int = 22
                        ,XTitleOffset: float = 0.98
                        ,XTitleFont: int = 43
                        ,XLabelSize: int = 22
                        ,XLabelOffset: float = 0.002
                        ,XLabelFont: int = 43
                        ,XNDiv: Optional[List[int]] = None

                        ,YTitleSize: int = 22
                        ,YTitleOffset: float = 1.75
                        ,YTitleFont: int = 43
                        ,YLabelSize: int = 22
                        ,YLabelOffset: float = 0.006
                        ,YLabelFont: int = 43
                        ,YNDiv: List[int] = [10, 5, 0]

                        ,ZTitleSize: int = 22
                        ,ZTitleOffset: float = 0.85
                        ,ZTitleFont: int = 43
                        ,ZLabelSize: int = 22
                        ,ZLabelOffset: float = 0.002
                        ,ZLabelFont: int = 43
                        ,pad: Optional[str] = None
                        ,fig: Optional['rpl.Figure'] = None
                        ) -> None:
    """
    Sets advanced formatting options for X, Y, and Z axes for a specific pad.

    Parameters
    ----------
    XTitleSize : int, optional
        Font size for the X-axis title, by default 22.
    XTitleOffset : float, optional
        Offset for the X-axis title, by default 0.98.
    XTitleFont : int, optional
        Font style for the X-axis title, by default 43.
    XLabelSize : int, optional
        Font size for the X-axis labels, by default 22.
    XLabelOffset : float, optional
        Offset for the X-axis labels, by default 0.002.
    XLabelFont : int, optional
        Font style for the X-axis labels, by default 43.
    XNDiv : List[int], optional
        Number of divisions for the X-axis [nPrimary, nSecondary, nTertiary].
    YTitleSize : int, optional
        Font size for the Y-axis title, by default 22.
    YTitleOffset : float, optional
        Offset for the Y-axis title, by default 1.75.
    YTitleFont : int, optional
        Font style for the Y-axis title, by default 43.
    YLabelSize : int, optional
        Font size for the Y-axis labels, by default 22.
    YLabelOffset : float, optional
        Offset for the Y-axis labels, by default 0.006.
    YLabelFont : int, optional
        Font style for the Y-axis labels, by default 43.
    YNDiv : List[int], optional
        Number of divisions for the Y-axis, by default [10, 5, 0].
    ZTitleSize : int, optional
        Font size for the Z-axis title, by default 22.
    ZTitleOffset : float, optional
        Offset for the Z-axis title, by default 0.85.
    ZTitleFont : int, optional
        Font style for the Z-axis title, by default 43.
    ZLabelSize : int, optional
        Font size for the Z-axis labels, by default 22.
    ZLabelOffset : float, optional
        Offset for the Z-axis labels, by default 0.002.
    ZLabelFont : int, optional
        Font style for the Z-axis labels, by default 43.
    pad : str, optional
        The name of the pad to format.
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.
    """
    
    fig = rpl.get_figure() if fig is None else fig
    canvas = fig.get_pad(pad)

    for primitive in canvas.GetListOfPrimitives() :
        if not hasattr(primitive,'GetXaxis') :
            continue
        primitive.GetXaxis().SetTitleSize  (XTitleSize  )
        primitive.GetXaxis().SetTitleOffset(XTitleOffset/float(canvas.GetHNDC()))
        primitive.GetXaxis().SetTitleFont  (XTitleFont  )
        primitive.GetXaxis().SetLabelSize  (XLabelSize  )
        primitive.GetXaxis().SetLabelOffset(XLabelOffset/float(canvas.GetHNDC()))
        primitive.GetXaxis().SetLabelFont  (XLabelFont  )
        primitive.GetXaxis().SetTickLength(0.02/float(canvas.GetHNDC()))
        if XNDiv:
            primitive.GetXaxis().SetNdivisions (XNDiv[0],XNDiv[1],XNDiv[2])
        primitive.GetYaxis().SetTitleSize  (YTitleSize  )
        primitive.GetYaxis().SetTitleOffset(YTitleOffset)
        primitive.GetYaxis().SetTitleFont  (YTitleFont  )
        primitive.GetYaxis().SetLabelSize  (YLabelSize  )
        primitive.GetYaxis().SetLabelOffset(YLabelOffset)
        primitive.GetYaxis().SetLabelFont  (YLabelFont  )
        primitive.GetYaxis().SetNdivisions (YNDiv[0],YNDiv[1],YNDiv[2])
        if not hasattr(primitive,'GetZaxis') :
            continue
        primitive.GetZaxis().SetTitleSize  (ZTitleSize  )
        primitive.GetZaxis().SetTitleOffset(ZTitleOffset)
        primitive.GetZaxis().SetTitleFont  (ZTitleFont  )
        primitive.GetZaxis().SetLabelSize  (ZLabelSize  )
        primitive.GetZaxis().SetLabelOffset(ZLabelOffset)
        primitive.GetZaxis().SetLabelFont  (ZLabelFont  )
        # if here, we setup x, y and z axis
        break
    canvas.Modified()
    canvas.Update()




def format_ratio_canvas_axes(  XTitleSize: int = 22
                               ,XTitleOffset: float = 0.98
                               ,XTitleFont: int = 43
                               ,XLabelSize: int = 22
                               ,XLabelOffset: float = 0.002
                               ,XLabelFont: int = 43
       
                               ,YTitleSize: int = 22
                               ,YTitleOffset: float = 1.75
                               ,YTitleFont: int = 43
                               ,YLabelSize: int = 22
                               ,YLabelOffset: float = 0.006
                               ,YLabelFont: int = 43
                               ,YNDiv: List[int] = [10, 5, 0]
       
                               ,ZTitleSize: int = 22
                               ,ZTitleOffset: float = 0.85
                               ,ZTitleFont: int = 43
                               ,ZLabelSize: int = 22
                               ,ZLabelOffset: float = 0.002
                               ,ZLabelFont: int = 43
                               ,fig: Optional['rpl.Figure'] = None
                               ) -> None:
    """
    Specifically formats the axes for a ratio canvas (both top and bottom pads).

    Parameters
    ----------
    XTitleSize : int, optional
        Font size for the X-axis title, by default 22.
    ... [same as format_canvas_axes]
    fig : rpl.Figure, optional
        The figure to use. If None, the current global figure is used.
    """
       
    format_canvas_axes(fig=fig, pad='pad_top',XLabelOffset=0.1
                     ,XTitleSize=XTitleSize,XTitleOffset=XTitleOffset,XTitleFont=XTitleFont
                     ,XLabelSize=XLabelSize,XLabelFont=XLabelFont
                     ,YTitleSize=YTitleSize,YTitleOffset=YTitleOffset,YTitleFont=YTitleFont
                     ,YLabelSize=YLabelSize,YLabelOffset=YLabelOffset,YLabelFont=YLabelFont
                     ,YNDiv=YNDiv
                     ,ZTitleSize=ZTitleSize,ZTitleOffset=ZTitleOffset,ZTitleFont=ZTitleFont
                     ,ZLabelSize=ZLabelSize,ZLabelOffset=ZLabelOffset,ZLabelFont=ZLabelFont
                       )
    format_canvas_axes(fig=fig, pad='pad_bot',YLabelOffset=0.009
                     ,XTitleSize=XTitleSize,XTitleOffset=XTitleOffset,XTitleFont=XTitleFont
                     ,XLabelSize=XLabelSize,XLabelOffset=XLabelOffset,XLabelFont=XLabelFont
                     ,YTitleSize=YTitleSize,YTitleOffset=YTitleOffset,YTitleFont=YTitleFont
                     ,YLabelSize=YLabelSize,YLabelFont=YLabelFont
                     ,YNDiv = [5,5,0]
                     ,ZTitleSize=ZTitleSize,ZTitleOffset=ZTitleOffset,ZTitleFont=ZTitleFont
                     ,ZLabelSize=ZLabelSize,ZLabelOffset=ZLabelOffset,ZLabelFont=ZLabelFont
                     )


def savefig( output: str, fig: Optional['rpl.Figure'] = None ) -> None:
    """
    Saves the current global figure or a specific Figure object to a file.

    Parameters
    ----------
    output : str
        Path to the output file (e.g., 'plot.pdf').
    fig : rpl.Figure, optional
        The figure to save. If None, the current global figure is used.
    """
    fig = rpl.get_figure() if not fig else fig
    fig.savefig(output)
