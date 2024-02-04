import xml.etree.ElementTree as et

def build_xml(path, img_string, file_string):
    root = et.Element('root')
    img = et.SubElement(root, 'i')
    img.text = img_string
    file = et.SubElement(root, 'f')
    file.text = file_string
    tree = et.ElementTree(root)
    tree.write(path, encoding='utf-8', xml_declaration=True)

def deconstruct_xml(path):
    t = et.parse(path)
    root = t.getroot()
    try:
        return (
            root.find('i').text, 
            root.find('f').text)
    except:
        raise ValueError("Given xml has incorrect indexes")

def xml_get_img(path): return deconstruct_xml(path)[0]
def xml_get_file(path): return deconstruct_xml(path)[1]