import pdftranslator
from pdftranslator import PDFQueryTranslator

from lxml import etree
parser = etree.XMLParser()
tree = etree.parse

filename = 'text.xml';
f = open (filename)
tree = etree.fromstring(f.read())

#from pyquery import PyQuery
#query  = PyQuery(tree, css_translator=PDFQueryTranslator())

i = 0;
for child in tree  :
    o = open("page%d.xml" % i, "w") 
    i = i +1 
    o.write(etree.tostring(child))
    o.close()
