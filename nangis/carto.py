# mabase functionality using cartopy

from warnings import warn

try:
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
except ImportError:
    warn("The 'cartopy' package is missing from this Python setup. The carto module is disabled", ImportWarning)

import numpy as np
import matplotlib.pyplot as plt
from nangis.os_utils import is_vec

class MAP_CANVAS:
    """
     A tool to plot  a map.
     use beginMap  before plotting
     terminate with endMap()

     Properties:
        etopo.scale - scale of etopo wrap, default is 2
        etopo.opacity - default = 0.9

    """

    def __init__(self, **kwargs):
        """
         Constructor
        """
        self.figure = None
        self.map_extent = None
        self._latdel = None
        self._londel = None
        self.wants_etopo = False
        self.wants_rivers = False

        self.ocean_color = 'deepskyblue' #'#D1E5F0' # 'lemonchiffon'
        self.land_color = 'lightgrey' #'#E0E0E0'
        self.river_color = 'blue'
        self.lake_color = 'lightblue'

        self.river_width = 2.5
        self.river_style = ':'
        #self.continents_color = 'lemonchiffon'


        self.wants_borders = True
        self.border_color = 'black' #'darkgrey'
        self.border_width = 3
        self.border_style = ':'

        self.etopo_scale = 2.0
        self.etopo_opacity = 0.9

        self.wants_etopo = False
        self.wants_rivers = False

        #self.rivers_color = 'blue'



        self.borders_linewidth = 2.8
        self.borders_color = 'tomato'
        self.borders_linestyle = 'solid'


        self.gridline_width = 2
        self.gridline_color = 'darkgrey'
        self.gridline_style = ':'


        self.mapframe_width = 2  # map frame width
        self.map_areatresh = 1000.0  # unused
        self.__bValid = False
        self.cls = ccrs.PlateCarree()
        self.fig_ncols = 1 # change this according to the numbers of figures you need
        self.fig_nrows = 1
        self._ax = None # axis for this figure

        self.lab_left = True
        self.lab_right = False
        self.lab_bottom = True
        self.lab_top = False
        self.lab_fontsize = 12

        self.map_extent = [0, -25.0,14.9, 0] # [-25.0, 12.0, -5.0, 32.0]
        self._map_scale = '10m'

    def _set_mapscale_high(self):
        self._map_scale = '10m'

    def _set_mapscale_low(self):
        self._map_scale = '110m'

    def _set_mapscale_medium(self):
        self._map_scale = '50m'

    def set_property(self, ** kwargs):

        """
         Creates map object

        :keyword extent:      Geographical range of the map: [lat1, lon1, lat2, lon2]
        :keyword cls          sets projection for this map (e.g. ccrs.PlateCarree())
                              if omitted NW Africa limit is used
        :keyword hires:      (optional) high resolution map (high resolution, slow rendering)
        :keyword mediumres:   (optional) medium resolution for maps
        :keyword lowres:      (optional) low resolution for maps (fastest render)
        :keyword wants_etopo:      (boolean, optional) plot background etopo map
        :keyword wants_rivers:      (optional) draws rivers
        :keyword wants_borders:    (optional) country borders
        :keyword border_color:    (optional) color of borders
        :keyword border_width:    (optional) width of borders
        :keyword border_style:    (optional) style of borders

        :keyword latdel:     (optional) latitude step
        :keyword londel:    (optional) longitude step
        :keyword lab_left:    (optional) labels on the left T/F
        :keyword lab_right:   (optional) labels on the right T/F
        :keyword lab_top:     (optional) labels on the top T/F
        :keyword lab_bottom:   (optional) labels on the bottom T/F@
        :keyword lab_fontsize: (optional)  map label size

        :keyword land_color: (optional)  color of the land
        :keyword ocean_color: (optional)  color of the continents
        :keyword river_color: (optional)  color of the rivers and lakes (edge)
        :keyword lake_color: (optional)  color of the lakes

        :keyword gridline_color:    (optional) color of borders
        :keyword gridline_width:    (optional) width of borders
        :keyword gridline_style:    (optional) style of borders


        :keyword river_width: (oprional) width of the rivers
        :keyword river_style: (optional) style of the river line _ -- or -. or  :

        :keyword etopo_scale: (optional) scale of etopo wrap, default is 2
        :keyword index:      (optional) which figure to plot (index (rew - 1) * ncols + ncol default one
        :keyword ncols:      (optional) number of figure columns default 1
        :keyword nrows:      (optional) number of figure rows   default 1
        :keyword figure:     (optional) figure to plot if omitted this function creates and returns a new figure
        :return: the current figure object

        """


        if 'extent' in kwargs:
            limit = kwargs['extent']
            if is_vec(limit, length=4):
                self.map_extent = limit

        if 'cls' in kwargs:
            self.cls = kwargs['cls']

        if 'hires' in kwargs:
            self._set_mapscale_high()
        if 'lowres' in kwargs:
            self._set_mapscale_low()
        if 'mediumres' in kwargs:
            self._set_mapscale_medium()

        if 'land_color' in kwargs:
            self.land_color = kwargs['land_color']
        if 'ocean_color' in kwargs:
            self.ocean_color = kwargs['ocean_color']
        if 'river_color' in kwargs:
            self.river_color = kwargs['river_color']
        if 'lake_color' in kwargs:
            self.lake_color = kwargs['lake_color']

        if 'river_width' in kwargs:
            self.river_width = kwargs['river_width']
        if 'river_style' in kwargs:
            self.river_style = kwargs['river_style']


        self.figure = kwargs.get('figure', None)

        lon_0 = None
        lat_0 = None

        hires = kwargs.get('hires', False)


        if 'latdel' in kwargs:
            self._latdel = kwargs['latdel']
        if 'londel' in kwargs:
            self._londel = kwargs['londel']

        if 'wants_etopo' in kwargs:
            self.wants_etopo = kwargs['wants_etopo']
        if 'wants_rivers' in kwargs:
            self.wants_rivers = kwargs['wants_rivers']


        if 'wants_borders' in kwargs:
            self.wants_borders = kwargs['wants_borders']


        if 'border_color' in kwargs:
            self.border_color = kwargs['border_color']

        if 'border_width' in kwargs:
            self.border_width = kwargs['border_width']

        if 'border_style' in kwargs:
            self.border_style = kwargs['border_style']


        if 'gridline_color' in kwargs:
            self.gridline_color = kwargs['gridline_color']

        if 'gridline_width' in kwargs:
            self.gridline_width = kwargs['gridline_width']

        if 'gridline_style' in kwargs:
            self.gridline_style = kwargs['gridline_style']

        if 'lab_left' in kwargs:
            self.lab_left = kwargs['lab_left']
        if 'lab_right' in kwargs:
            self.lab_right = kwargs['lab_right']
        if 'lab_bottom' in kwargs:
            self.lab_bottom = kwargs['lab_bottom']
        if 'lab_top' in kwargs:
            self.lab_top = kwargs['lab_top']
        if 'lab_fontsize' in kwargs:
            self.lab_fontsize =  kwargs['lab_fontsize']




        # # print('londel = {} '.format(self.__londel))
        #
        # if (not is_vec(limit, length=4)):
        #     self.map_extent = [-25.0, 12.0, -5.0, 32.0]
        # else:
        #     self.map_extent = limit  # Capital letters take precedence



    def render(self, **kwargs):
        """
         Creates map object

        :keyword extent:      Geographical range of the map: [lat1, lon1, lat2, lon2]
                              if omitted NW Africa limit is used
        :keyword hires:      (optional) high resolution map (high resolution, slow rendering)
        :keyword mediumres:   (optional) medium resolution for maps
        :keyword lowres:      (optional) low resolution for maps (fastest render)
        :keyword mercator:   (optional) Mercator projection. Default is cylindrical equidistance
        :keyword ortho:      (optional) orthographic projection
        :keyword vangd:      (optional) van Der Grinten projection
        :keyword etopo:      (boolean, optional) plot background etopo map
        :keyword rivers:      (optional) draws rivers
        :keyword borders:    (optional) country borders
        :keyword latdel:     (optional) latitude step
        :keyword lonstep:    (optional) longitude step
        :keyword index:      (optional) which figure to plot (index (rew - 1) * ncols + ncol default one
        :keyword ncols:      (optional) number of figure columns default 1
        :keyword nrows:      (optional) number of figure rows   default 1
        :keyword figure:     (optional) figure to plot if omitted this function creates and returns a new figure
        :return: the current figure object

        """
        self.set_property(**kwargs)
       #  limit = kwargs.get('extent', None)
       #  self.figure = kwargs.get('figure', None)
       # # mercator = kwargs.get('mercator', None)
       #  #ortho = kwargs.get('ortho', None)
       #  #vandg = kwargs.get('vangd', None)
       #  lon_0 = None
       #  lat_0 = None
       #
       #  hires = kwargs.get('hires', False)
       #
       #  self.__latdel = kwargs.get('latdel', None)
       #  self.__londel = kwargs.get('londel', None)
       #  self.bEtopo = kwargs.get('etopo', False)
       #  self.bRivers = kwargs.get('rivers', False)
       #  self.bBorders = kwargs.get('borders', True)
       #
       #
       #
       #
       #  # print('londel = {} '.format(self.__londel))
       #
       #  if (not is_vec(limit, length=4)):
       #      self.__mapLimit = [-25.0, 12.0, -5.0, 32.0]
       #  else:
       #      self.__mapLimit = limit  # Capital letters take precedence

        if self.figure is None:
            fig, axs = plt.subplots(self.fig_nrows, self.fig_ncols, subplot_kw={'projection': self.cls})
            if is_vec(axs):
                ax = axs[1, 1]
            else:
                ax = axs
        else:
            ax = self.figure.add_subplot(self.fig_nrows, self.fig_ncols, subplot_kw={'projection': self.cls})

        #Add land and ocean features

        ax.add_feature(cfeature.LAND.with_scale(self._map_scale), facecolor=self.land_color)
        ax.add_feature(cfeature.OCEAN.with_scale(self._map_scale), facecolor=self.ocean_color)
        ax.add_feature(cfeature.COASTLINE.with_scale(self._map_scale))
        ax.add_feature(cfeature.BORDERS.with_scale(self._map_scale)
                       ,  linestyle=self.border_style, edgecolor=self.border_color, linewidth=self.border_width)
        if self.wants_rivers:
            ax.add_feature(cfeature.RIVERS.with_scale(self._map_scale)
                    , edgecolor=self.river_color, linestyle=self.river_style, linewidth=self.river_width)
            ax.add_feature(cfeature.LAKES.with_scale(self._map_scale), edgecolor=self.river_color, facecolor=self.lake_color)

        if self.wants_etopo:
            ax.stock_img()

        ax.set_extent([self.map_extent[0], self.map_extent[2], self.map_extent[1], self.map_extent[3]], crs=self.cls)


        ax.set_xticks([])  # Remove all x-axis ticks
        ax.set_yticks([])  #
        ax.set_xticks(np.arange(self.map_extent[0], self.map_extent[2], self._londel), self.cls)
        ax.set_yticks(np.arange(self.map_extent[1], self.map_extent[3], self._latdel), self.cls)


        self._ax = ax  # hold axis for the closure

          # Add gridlines
        gl = ax.gridlines(draw_labels=True
                           , linestyle=self.gridline_style
                           , color=self.gridline_color
                           , linewidth=self.gridline_width
                          )
        gl.top_labels = self.lab_top
        gl.right_labels = self.lab_right
        gl.bottom_labels = self.lab_bottom

        gl.xlabel_style = {'size': self.lab_fontsize}   # , 'color': 'blue'}
        gl.ylabel_style = {'size': self.lab_fontsize}   # , 'color': 'green'}
        return self.figure, ax


def draw_map(**kwargs):
    ca = MAP_CANVAS()
    return ca.render(**kwargs)



if __name__ == '__main__':
    from nangis.os_utils import figsize
    import cartopy

    figsize(15, 15)
    #ca = MAP_CANVAS()
    draw_map(
        lab_fontsize=20,
        hires=True,
        wants_rivers=True,
        latdel=1,
        londel=1,
        river_width=5,
        river_style='-',
        gridline_width=4,
        gridline_style='--',
        gridline_color='red',
        extent=[12, -7, 14, -5]   #[12, -6.5, 14, -5]
    )
    #ca.render()
    plt.show()
    #plt.clf()
    #plt.close('all')
    #print(cartopy.config['data_dir'])









