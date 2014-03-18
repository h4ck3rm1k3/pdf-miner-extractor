#import pdftranslator
#from pdftranslator import PDFQueryTranslator
import Tkinter as tkinter

from lxml import etree
parser = etree.XMLParser()
tree = etree.parse

# quad tree
import quadpy
from quadpy.rectangle import Rectangle
quad = quadpy.Node(0, 0, 10700, 10700, max_depth=9)

filename = 'page61.xml'; # 61 - 94
f = open (filename)
tree = etree.fromstring(f.read())

from Tkinter import Listbox

root = tkinter.Tk()
def gui ():


    xscrollbar = tkinter.Scrollbar(root, orient=tkinter.HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky=tkinter.E+tkinter.W)

    yscrollbar = tkinter.Scrollbar(root)
    yscrollbar.grid(row=0, column=1, sticky=tkinter.N + tkinter.S)
    
    #canvas = tkinter.Canvas()
    canvas = tkinter.Canvas(root, 
                            width=500, 
                            height=500, 
                            scrollregion=(0,0,1600,1600),
#                            highlightthickness=0,
                            background='white',
#                            ,
#                            yscrollcommand=yscrollbar.set
    )
    
    canvas.pack( fill='y', side='left', expand=True, padx=6, pady=6)
    canvas.grid(row=0, column=0, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)


    xscrollbar.config(command=canvas.xview)
    canvas.config(xscrollcommand=xscrollbar.set)

    yscrollbar.config(command=canvas.yview)
    canvas.config(yscrollcommand=yscrollbar.set)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    root.resizable(True, True)

#    xscrollbar.config(command=canvas.xview)
#    yscrollbar.config(command=canvas.yview)
    return canvas


#root.bind("<MouseWheel>",self.zoom)

canvas = gui() 

i = 0;

def textline(e) :

    box = bbox(e, "yellow")

    c=[]
    for t in e  :
        box = bbox(t, "green")
        if (box) :
            pos = box.center
#            print center, box.bounds
            text_id = canvas.create_text(pos[0],pos[1],text=t.text)
            c.append(t.text)

    t = "".join(c)
    t = t.strip()
    #if (t):
    #print "TextLine '%s'" % t

class MyRect (Rectangle):
    def __repr__(self):
        return "{0} '{1}' ({2}, {3}, {4}, {5})".format(self.__class__.__name__,
                                                      self.data,
                                                      *self.bounds)
    @property 
    def center(self):
        return [ 
            self.bounds[0] + ((self.bounds[2] - self.bounds[0])/2),
            self.bounds[1] + ((self.bounds[3] - self.bounds[1])/2)
        ]

def bbox(e, color):
    bbox = e.get("bbox")
    if not bbox:
        # there are empty text objects
        return None

    (minx, miny, maxx, maxy) = [float(f) for f in bbox.split(",")]
    scale = 2
    bounds = (minx *  scale, 
              miny *  scale, 
              maxx *  scale, 
              maxy *  scale)
    rect = MyRect(*bounds)
    rect.canvas_id = canvas.create_rectangle(bounds, outline=color)
    quad.insert(rect)
    return rect

def textbox(e) :
    """
    final
    """
    bbox(e, "blue")

def textgroup(e) :

    bbox(e, "red")

    for t in e  :
        tag = t.tag
        if tag == "textgroup":

            
            textgroup(t)       
        elif tag == "textbox": 
            textbox(t)       
        

def element(e):
    tag = e.tag
    if tag == "textline" :
        textline(e)
    elif tag == "textgroup" :
        textgroup(e)
    else:
        raise Exception(tag)


for page in tree  :
    for e in page  :
        element(e)

root.mainloop()
