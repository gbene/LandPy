from .landxml import LandXML



def read_lxml(file):
    with open(file,'rb') as f:
        xml = f.read().decode('iso-8859-1').encode('ascii')

    lxml_obj = LandXML(xml)
    return lxml_obj


def write_lxml(file):
    ...