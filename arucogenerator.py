#! /usr/bin/env python -t
import json
'''
Generates Aruco Code sheet
'''
__version__ = "1.0" ### please report bugs, suggestions etc at https://github.com/bradgoodman/arucogenerator ###

import os,sys,inkex,simplestyle,gettext,math
from copy import deepcopy
_ = gettext.gettext

# Aruco 4x4_1000
ardict = [[181,50],[15,154],[51,45],[153,70],[84,158],[121,205],[158,46],[196,242],[254,218],[207,86],[249,145]];

linethickness = 1 # default unless overridden by settings

def log(text):
  if 'SCHROFF_LOG' in os.environ:
    f = open(os.environ.get('SCHROFF_LOG'), 'a')
    f.write(text + "\n")

def newGroup(canvas):
  # Create a new group and add element created from line string
  panelId = canvas.svg.get_unique_id('panel')
  group = canvas.svg.get_current_layer().add(inkex.Group(id=panelId))
  return group
  
def getLine(XYstring,stroke="#000000"):
  line = inkex.PathElement()
  line.style = { 'stroke': stroke, 'stroke-width'  : str(linethickness), 'fill': 'none' }
  line.path = XYstring
  #inkex.etree.SubElement(parent, inkex.addNS('path','svg'), drw)
  return line

# jslee - shamelessly adapted from sample code on below Inkscape wiki page 2015-07-28
# http://wiki.inkscape.org/wiki/index.php/Generating_objects_from_extensions
def getCircle(r, c):
    (cx, cy) = c
    log("putting circle at (%d,%d)" % (cx,cy))
    circle = inkex.PathElement.arc((cx, cy), r)
    circle.style = { 'stroke': '#000000', 'stroke-width': str(linethickness), 'fill': 'none' }
    return circle

def draw_SVG_square(x,y,w,h,fill="#000000"):
    style = {   'stroke'        : 'none',
                'stroke-width'  : '1',
                'fill'          : fill
            }
                
    attribs = {
        'height'    : str(h),
        'width'     : str(w),
        'x'         : str(x),
        'y'         : str(y)
            }
    s=f"M {x},{y} "
    s+=f"l {w},0 "
    s+=f"l 0,{h} "
    s+=f"l {-w},0 "
    s+=f"l 0,{-h} "
    s+="Z"
    line = inkex.PathElement()
    line.style = style
    line.path = s
    return line


    
  
markerwidth={
        "aruco":5,
        "4x4_1000":4,
        "5x5_1000":5,
        "6x6_1000":5,
        "7x7_1000":7
}

"""
    // "Pixels"
    for (var i = 0; i < height; i++) {
        for (var j = 0; j < width; j++) {
            var color = bits[i * height + j] ? '#e0e0e0' : 'black';
            var pixel = $('<rect/>').attr({
                width: 1,
                height: 1,
                x: j + 1,
                y: i + 1,
                fill: color
            });
            if ((bits[i * height + j])) {
            pixel.appendTo(svg);
            }
        }
    }
"""

class ArucoGenerator(inkex.Effect):
  def aruco(self,code,x,y,ww,hh,l,fontsize,codetype):
    if (ww<hh):
        sz = ww;
    else:
        sz = hh;
    group = newGroup(self)
    group.add(draw_SVG_square(x,y,sz,sz))
    codewidth = markerwidth[codetype]
    sz = sz/(codewidth+2)
    byts=self.ardict[codetype][code]

    for yy in range(0,codewidth):
            for xx in range(0,codewidth):
                bitnum = yy * codewidth + xx
                byte = byts[bitnum>>3]
                bt = byts[bitnum>>3] & (0x80>>bitnum%8)
                if (bt):
                    group.add(draw_SVG_square(x+((1+xx)*sz),y+(((yy)+1)*sz),sz,sz,'#ffffff'))
    

    t = inkex.TextElement()
    ts = inkex.Tspan()
    transform_string = f"translate({x+ww}, {y+hh}) rotate(-90)"
    t.set('transform', transform_string)
    if (fontsize==0):
            fontsize=ww
    t.set("style",f"font-size:{fontsize}")
    ts.text=l
    t.add(ts)
    group.add(t)
        
    return (group)

  def __init__(self):
      # Call the base class constructor.
      inkex.Effect.__init__(self)
      # Define options
      self.arg_parser.add_argument('--unit',action='store',type=str,
        dest='unit',default='mm',help='Measure Units')
      self.arg_parser.add_argument('--width',action='store',type=float,
        dest='width',default=100,help='Width of Box')
      self.arg_parser.add_argument('--height',action='store',type=float,
        dest='height',default=100,help='Height of Box')
      self.arg_parser.add_argument('--hairline',action='store',type=int,
        dest='hairline',default=0,help='Line Thickness')
      self.arg_parser.add_argument('--thickness',action='store',type=float,
        dest='thickness',default=10,help='Thickness of Material')
      self.arg_parser.add_argument('--kerf',action='store',type=float,
        dest='kerf',default=0.5,help='Kerf (width of cut)')
      self.arg_parser.add_argument('--boxtype',action='store',type=int,
        dest='boxtype',default=25,help='Box type')
      self.arg_parser.add_argument('--boxtop',action='store',type=int,
        dest='boxtop',default=25,help='Box Top')
      self.arg_parser.add_argument('--boxbottom',action='store',type=int,
        dest='boxbottom',default=25,help='Box Bottom')
      self.arg_parser.add_argument('--sidetab',action='store',type=str,
        dest='sidetab',help='Side Tab')
      self.arg_parser.add_argument('--foldlines',action='store',type=str,
        dest='foldlines',help='Add Cut Lines')

      self.arg_parser.add_argument('--cols',action='store',type=int,
        dest='cols',default=1,help='Columns')
      self.arg_parser.add_argument('--rows',action='store',type=int,
        dest='rows',default=1,help='Rows')
      self.arg_parser.add_argument('--hspace',action='store',type=float,
        dest='hspace',default=4,help='Horizontal Offset')
      self.arg_parser.add_argument('--vspace',action='store',type=float,
        dest='vspace',default=5,help='Vertical Offset')
      self.arg_parser.add_argument('--startcode',action='store',type=int,
        dest='startcode',default=1,help='Start Code')
      self.arg_parser.add_argument('--fontsize',action='store',type=float,
        dest='fontsize',default=1,help='Font Size')
      self.arg_parser.add_argument('--labels',action='store',type=str,
        dest='labels',default=1,help='Labels')
      self.arg_parser.add_argument('--code',action='store',type=str,
        dest='code',default="aruco",help='Code Type')

      fd=open("dict.json")
      self.ardict=json.load(fd)
      fd.close()

  def effect(self):
    global group,nomTab,equalTabs,tabSymmetry,dimpleHeight,dimpleLength,thickness,kerf,halfkerf,dogbone,divx,divy,hairline,linethickness,keydivwalls,keydivfloor
    
        # Get access to main SVG document element and get its dimensions.
    svg = self.document.getroot()
    
        # Get the attributes:
    #inkex.utils.errormsg("Testing")
    widthDoc  = self.svg.unittouu(svg.get('width'))
    heightDoc = self.svg.unittouu(svg.get('height'))
    group = newGroup(self)
    unit=self.options.unit
    startcode=self.options.startcode
    labels=self.options.labels
    boxtop = self.options.boxtop
    fontsize = self.options.fontsize
    boxbottom = self.options.boxbottom
    # Set the line thickness

     
    hh=self.svg.unittouu(str(self.options.height)+unit)
    ww=self.svg.unittouu(str(self.options.width)+unit)
    hspace=self.svg.unittouu(str(self.options.hspace)+unit)
    vspace=self.svg.unittouu(str(self.options.vspace)+unit)
    labels = labels.split("\\n")
    index = 0
    for x in range(0,self.options.cols):
        for y in range(0,self.options.rows):
            l=""
            if (len(labels) > index):
                l = labels[index]
            group.add(self.aruco(startcode+index,x*hspace,y*vspace,ww,hh,l,fontsize,self.options.code))
            index = index+1
    return


effect = ArucoGenerator()
effect.run()
