
from typing import Optional
import rootplotlib as rpl
from ROOT import TLatex, gPad

__all__ = [
    'set_lorenzetti_style',
    'set_lorenzetti_label',
]


def set_lorenzetti_style() -> None:
    """
    Applies the Lorenzetti style (currently based on ATLAS style).
    """
    rpl.set_atlas_style ()


def set_lorenzetti_label( x: float, y: float, text: str, pad: Optional[str] = None) -> None:
  """
  Draws the 'Lorenzetti' label with additional status text.

  Parameters
  ----------
  x : float
      X-coordinate in NDC.
  y : float
      Y-coordinate in NDC.
  text : str
      Status text to display next to 'Lorenzetti'.
  pad : str, optional
      The name of the pad.
  """

  fig = rpl.get_figure()
  canvas = fig.get_pad(pad)
  canvas.cd()
  experiment = TLatex()
  experiment.SetNDC()
  experiment.SetTextFont(72)
  experiment.SetTextColor(1)
  delx = 0.17*696*gPad.GetWh()/(472*gPad.GetWw())
  experiment.DrawLatex(x,y,'Lorenzetti')
  label = TLatex()
  label.SetNDC()
  label.SetTextFont(42)
  label.SetTextColor(1)
  label.DrawLatex(x+delx,y,text)
  fig.append(label)
  fig.append(experiment)
  canvas.Modified()
  canvas.Update()
