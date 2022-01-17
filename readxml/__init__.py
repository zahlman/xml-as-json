from xml.etree import ElementTree as ET


__version__ = '0.1.0'


def normalize(text):
    if text is None:
        return ''
    return text.strip()


def children(element):
    lead = normalize(element.text)
    if lead:
        yield lead
    for c in element:
        yield c
        trail = normalize(c.tail)
        if trail:
            yield trail


def build(element):
    if isinstance(element, str):
        return element
    result = dict(element.attrib)
    result[''] = element.tag
    result['[[]]'] = [build(c) for c in children(element)]
    return result


def parse(source):
    if isinstance(source, str) and source.startswith('<'):
        xml = ET.fromstring(source)
    else:
        xml = ET.parse(source).getroot()
    return build(xml)
