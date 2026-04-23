__all__ = ['get_color']

from typing import Union, Tuple, Optional
from ROOT import TColor


def get_color(color: Union[str, int, Tuple[int, ...]], transparency: Optional[float] = None) -> int:
    """
    Returns a ROOT color integer from various input formats.

    Parameters
    ----------
    color : Union[str, int, Tuple[int, ...]]
        Color in various formats:
        - str: Hex string (e.g., '#ff0000') or named color.
        - int: ROOT color code.
        - Tuple[int, ...]: RGB tuple (0-255).
    transparency : float, optional
        Transparency level from 0.0 (opaque) to 1.0 (transparent), by default None.

    Returns
    -------
    int
        ROOT color code.
    """
    try:
      color = TColor.GetColor( *color ) # type: ignore
    except:
      if type(color) is not int: color = TColor.GetColor( color ) # type: ignore
    if transparency is not None:
      color = TColor.GetColorTransparent( color, transparency )
    return color
