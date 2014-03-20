
from lxml import etree


#from pysvg.structure import *
from pysvg.structure import Svg
from pysvg.builders import StyleBuilder
from pysvg.text import Text
from pysvg.shape import Rect

class MyRect:

    def __init__(self, bounds):
        self.bounds = bounds

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

class Canvas :

    def __init__(self):
        self.svg = mySVG=Svg(0,0, width="100%", height="100%")

    def create_text(self, x, y, text):
        text = text.encode("ascii", "ignore")
        t = Text(text, x,y)
        self.svg.addElement(t)
        #print t

    def create_rectangle(self, bounds, outline):

        r = Rect(
                x= bounds[0], 
                y= bounds[1],
                width= bounds[2] - bounds[0],
                height= bounds[3] - bounds[1]
            )
        myStyle = StyleBuilder({'fill':None, 'stroke-width':0.5, 'stroke':outline})
        r.set_style(myStyle.getStyle())

        self.svg.addElement(
            r)

class Reader :
    def __init__(self, out):
        self.out = out

    def textline(self, e) :
        box = self.bbox(e, "yellow")
        c=[]
        for t in e  :
            box = self.bbox(t, "green")
            if (box) :
                pos = box.center
                canvas.create_text(pos[0],pos[1],text=t.text)
                c.append(t.text)
        t = "".join(c)
        t = t.strip()
        #print t

    def bbox(self, e, color):
        bbox = e.get("bbox")
        if not bbox:
            # there are empty text objects
            return None
        (minx, miny, maxx, maxy) = [float(f) for f in bbox.split(",")]
        scale = 1
        bounds = (minx *  scale, 
                  miny *  scale, 
                  maxx *  scale, 
                  maxy *  scale)
        rect = MyRect(bounds)
        #rect.canvas_id = 
        canvas.create_rectangle(bounds, color)
        #quad.insert(rect)
        return rect

    def textbox(self, e):
        """
        final
        """
        self.bbox(e, "blue")

    def textgroup(self, e):
        self.bbox(e, "red")
        for t in e  :
            tag = t.tag
            if tag == "textgroup":
                self.textgroup(t)       
            elif tag == "textbox": 
                self.textbox(t)       

    def element(self, e):
        tag = e.tag
        if tag == "textline" :
            self.textline(e)
        elif tag == "textgroup" :
            self.textgroup(e)
        else:
            raise Exception(tag)

    def process(self, tree):
        for page in tree  :
            for e in page  :
                self.element(e)

    def read(self, filename):
        parser = etree.XMLParser()
        tree = etree.parse
        f = open (filename)
        print "open %s" % filename
        tree = etree.fromstring(f.read())
        self.process(tree)

print "Hello"
canvas = Canvas()
reader = Reader(canvas)
reader.read('pages/page61.xml');

canvas.svg.save('test.svg')
