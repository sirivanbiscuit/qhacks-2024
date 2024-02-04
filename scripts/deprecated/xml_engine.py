import xml.etree.ElementTree as et

def build_xml(path, img_string, file_string):
    root = et.fromstring(f'<root><i>{img_string}</i><f>{file_string}</f></root>')
    et.ElementTree(root).write(path, encoding='utf-8', xml_declaration=True)

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