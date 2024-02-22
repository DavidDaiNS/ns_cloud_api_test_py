import xml.etree.ElementTree as ET
import xml.dom.minidom

def prettify_xml(element:ET.Element):
    xml_str = ET.tostring(element, encoding='utf-8')
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = dom.toprettyxml(indent='  ')
    # return "\n".join(line for line in pretty_xml_str.split("\n") if not line.strip().startswith('<?xml'))
    return pretty_xml_str

def prettify_xml_string(xml_str:str):
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml_str = dom.toprettyxml(indent='  ')
    return "\n".join(line for line in pretty_xml_str.split("\n") if not line.strip().startswith('<?xml'))