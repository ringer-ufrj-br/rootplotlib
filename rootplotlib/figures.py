
__all__ = ['Figure']


from typing import Any, Optional, Tuple, List, Union
import ROOT
from ROOT import TH1, TH2
import itertools
import gc
import sys

class Figure( object ):
    """
    Main object to handle ROOT plots and canvases.
    """

    def __init__(self, canvas: Optional[ROOT.TCanvas] = None) -> None:
        """
        Initializes the Figure object.

        Parameters
        ----------
        canvas : ROOT.TCanvas, optional
            A ROOT canvas to associate with this figure. If None, it will be blank.
        """
        self.__canvas = canvas
        self.__collections = []


    def canvas(self) -> Optional[ROOT.TCanvas]:
        """
        Returns the associated ROOT canvas.

        Returns
        -------
        ROOT.TCanvas or None
            The associated canvas.
        """
        return self.__canvas


    def set_canvas( self , canvas: ROOT.TCanvas ) -> None:
        """
        Sets a new ROOT canvas for the figure.

        Parameters
        ----------
        canvas : ROOT.TCanvas
            The new canvas to associate.
        """
        self.__canvas = canvas
        self.__collections = []


    def clear(self) -> None:
        """
        Closes the canvas and deletes all stored objects in the figure.
        """
        if self.__canvas:
            self.__canvas.Close()
        for obj, delete in self.__collections:
            if obj and hasattr(obj,'Delete') and delete:
                obj.Delete()
        self.__collections = []
        gc.collect()


    def append(self, obj: Any, delete: bool = True) -> None:
        """
        Appends an object to the figure's internal collection to prevent garbage collection.

        Parameters
        ----------
        obj : Any
            The ROOT object to store.
        delete : bool, optional
            Whether to delete the object when the figure is cleared, by default True.
        """
        self.__collections.append((obj, delete))


    def get_pad( self, pad: Optional[str] = None ) -> Union[ROOT.TCanvas, ROOT.TPad]:
        """
        Returns a specific pad by name or the main canvas.

        Parameters
        ----------
        pad : str, optional
            The name of the pad. If None or not found, returns the main canvas.

        Returns
        -------
        Union[ROOT.TCanvas, ROOT.TPad]
            The requested pad or canvas.
        """

        if pad and any(pad==primitive.GetName() for primitive in self.__canvas.GetListOfPrimitives()):
            canvas = self.__canvas.GetPrimitive(pad)
        else:
            canvas = self.__canvas  
        return canvas


    def add_hist(self, hist: Union[TH1, TH2],  drawopt: str = '', pad: Optional[str] = None) -> None:
        """
        Adds a histogram to the figure and draws it.

        Parameters
        ----------
        hist : Union[TH1, TH2]
            The histogram to add.
        drawopt : str, optional
            ROOT draw options, by default ''.
        pad : str, optional
            The name of the pad to draw to.
        """
        canvas = self.get_pad(pad)
        if not "same" in drawopt: drawopt += ' sames'
        canvas.cd()
        hist.Draw(drawopt)
        canvas.Modified()
        canvas.Update()
        # add into the list of primitives
        self.append( hist, False )


    def add_legend(self, leg: ROOT.TLegend, pad: Optional[str] = None) -> None:
        """
        Adds a legend to the figure.

        Parameters
        ----------
        leg : ROOT.TLegend
            The legend object to add.
        pad : str, optional
            The name of the pad to draw to.
        """
        canvas = self.get_pad(pad)
        canvas.cd()
        leg.Draw() # add into the list of primitives
        canvas.Modified()
        canvas.Update()
        self.append(leg)


    def set_xlabel(self, xlabel: str, pad: Optional[str] = None) -> None:
        """
        Sets the title for the X-axis.

        Parameters
        ----------
        xlabel : str
            The label text.
        pad : str, optional
            The name of the pad.
        """

        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives() :
            if hasattr(primitive,'GetXaxis') :
                primitive.GetXaxis().SetTitle(xlabel)
                break
        canvas.Modified()
        canvas.Update()



    def set_ylabel(self, ylabel: str, pad: Optional[str] = None) -> None:
        """
        Sets the title for the Y-axis.

        Parameters
        ----------
        ylabel : str
            The label text.
        pad : str, optional
            The name of the pad.
        """

        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives() :
            if hasattr(primitive,'GetYaxis') :
                primitive.GetYaxis().SetTitle(ylabel)
                break
        canvas.Modified()
        canvas.Update()
        
        
    def set_zlabel(self, zlabel: str, pad: Optional[str] = None) -> None:
        """
        Sets the title for the Z-axis.

        Parameters
        ----------
        zlabel : str
            The label text.
        pad : str, optional
            The name of the pad.
        """

        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives() :
            if hasattr(primitive,'GetZaxis') :
                primitive.GetZaxis().SetTitle(zlabel)
                break
        canvas.Modified()
        canvas.Update()


    def get_xaxis(self, pad: Optional[str] = None) -> Optional[ROOT.TAxis]:
        """
        Finds and returns the X-axis of the first histogram in the pad.

        Parameters
        ----------
        pad : str, optional
            The name of the pad.

        Returns
        -------
        ROOT.TAxis or None
            The X-axis object.
        """

        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives():
            if issubclass(type(primitive),TH1):
                return primitive.GetXaxis()
            elif issubclass(type(primitive),TH2):
                return primitive.GetXaxis()

        return None

    def get_yaxis(self, pad: Optional[str] = None) -> Optional[ROOT.TAxis]:
        """
        Finds and returns the Y-axis of the first histogram in the pad.

        Parameters
        ----------
        pad : str, optional
            The name of the pad.

        Returns
        -------
        ROOT.TAxis or None
            The Y-axis object.
        """

        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives():
            if issubclass(type(primitive),TH1):
                return primitive.GetYaxis()
            elif issubclass(type(primitive),TH2):
                return primitive.GetYaxis()
        return None



    def get_xaxis_ranges(self, only_filled: bool = False, pad: Optional[str] = None) -> Tuple[float, float]:
        """
        Calculates the min and max X values currently displayed in the pad.

        Parameters
        ----------
        only_filled : bool, optional
            If True, only considers bins with content > 0, by default False.
        pad : str, optional
            The name of the pad.

        Returns
        -------
        Tuple[float, float]
            (xmin, xmax)
        """
    
        xmin = sys.float_info.max
        xmax = sys.float_info.min
        canvas = self.get_pad(pad)
        for primitive in canvas.GetListOfPrimitives():
            if issubclass(type(primitive),TH1):
                axis = primitive.GetXaxis()
                if only_filled:
                    bins = [primitive.GetBinCenter(idx) for idx in range(1,primitive.GetNbinsX()+1) if primitive.GetBinContent(idx)>0]
                    if len(bins)>=2:
                        xmin = min(xmin,bins[0])
                        xmax = max(xmax,bins[-1])
                else:
                    xmin = min(xmin,axis.GetXmin())
                    xmax = max(xmax,axis.GetXmax())
        return xmin, xmax



    def set_xaxis_ranges(self, xmin: float, xmax: float, for_all: bool = False, pad: Optional[str] = None) -> None:
        """
        Sets the displayed X-axis range.

        Parameters
        ----------
        xmin : float
            Lower bound.
        xmax : float
            Upper bound.
        for_all : bool, optional
            If True, sets the range for all objects; if False, uses SetLimits, by default False.
        pad : str, optional
            The name of the pad.
        """

        # Get the axis from canvas
        axis = self.get_xaxis(pad)
        canvas = self.get_pad(pad)
        if not axis:
            print ('Warning: set_x_axis_ranges had no effect. Check that your canvas has plots in it.')
        else:
            if for_all: 
                axis.SetRangeUser(xmin,xmax)
            else: 
                axis.SetLimits(xmin,xmax)
            canvas.Modified()
            canvas.Update()


    def get_yaxis_ranges(self, pad: Optional[str] = None, ignore_zeros: bool = False, ignore_errors: bool = False) -> Tuple[float, float]:
        """
        Calculates the min and max Y values currently displayed in the pad.

        Parameters
        ----------
        pad : str, optional
            The name of the pad.
        ignore_zeros : bool, optional
            If True, ignores bins with zero content, by default False.
        ignore_errors : bool, optional
            If True, ignores bin errors when calculating range, by default False.

        Returns
        -------
        Tuple[float, float]
            (ymin, ymax)
        """

        ymin = sys.float_info.max
        ymax = sys.float_info.min
        canvas = self.get_pad(pad)

        for primitive in canvas.GetListOfPrimitives():

            if isinstance(primitive, TH2):
                y = primitive.GetYaxis()
                nx = primitive.GetNbinsY()
                ny = primitive.GetNbinsY()
                # This is just a workaround for candles/violins
                for rxc, ryc in itertools.product( range(1,nx+1), range(1,ny+1)):
                    z = primitive.GetBinContent(rxc,ryc)
                    if ignore_zeros and z == 0 :
                        continue
                    ymin = min(ymin,y.GetBinCenter(ryc))
                    ymax = max(ymax,y.GetBinCenter(ryc))
                return ymin, ymax

            elif issubclass(type(primitive),TH1) :
                ysum = 0
                for bin in range(primitive.GetNbinsX()) :
                    ysum = ysum+primitive.GetBinContent(bin+1)
                if ysum == 0: ignore_zeros = 0
                for bin in range(primitive.GetNbinsX()) :
                    y = primitive.GetBinContent(bin+1)
                    if ignore_errors :
                        ye = 0
                    else :
                        ye = primitive.GetBinError(bin+1)
                    if ignore_zeros and y == 0 :
                        continue
                    ymin = min(ymin,y-ye)
                    ymax = max(ymax,y+ye)

        return ymin, ymax


    def set_yaxis_ranges(self, ymin: float, ymax: float, pad: Optional[str] = None) -> None:
        """
        Sets the displayed Y-axis range.

        Parameters
        ----------
        ymin : float
            Lower bound.
        xmax : float
            Upper bound.
        pad : str, optional
            The name of the pad.
        """

        axis = self.get_yaxis(pad)
        canvas = self.get_pad(pad)
        if not axis :
            print ('Warning: SetYaxisRange had no effect. Check that your canvas has plots in it.')
        else:
            axis.SetRangeUser(ymin,ymax)
            canvas.Modified()
            canvas.Update()


    def savefig(self, output: str) -> None:
        """
        Saves the figure to a file.

        Parameters
        ----------
        output : str
            The output file path.
        """
        if self.__canvas:
            self.__canvas.SaveAs(output)


    def show(self) -> None:
        """
        Draws the main canvas.
        """
        if self.__canvas:
            self.__canvas.Draw()

