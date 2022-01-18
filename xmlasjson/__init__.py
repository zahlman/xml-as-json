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


def simple(element):
    result = dict(element.attrib)
    anames = set(result.keys())
    # we don't care about the root tag name, and child tag names will
    # be implicit in the dict we're making.
    lead = normalize(element.text)
    for c in element:
        if c.tag in anames:
            raise ValueError(c.tag, 'conflict between attributes and children')
        if normalize(c.tail):
            raise ValueError('mixed text data and child tags found')
        to_add = simple(c)
        lname = f'[{c.tag}]'
        if lname in result:
            result[lname].append(to_add)
        elif c.tag in result:
            result[lname] = [result[c.tag], to_add]
            del result[c.tag]
        else:
            result[c.tag] = to_add
    if lead and result:
        raise ValueError('mixed text data and attributes/child tags found')
    if result:
        return result
    if lead:
        for cast in (int, float):
            try:
                return cast(lead)
            except ValueError:
                pass
        return lead
    return True # blank tag


def parse(source, builder='build'):
    if isinstance(source, str) and source.startswith('<'):
        xml = ET.fromstring(source)
    else:
        xml = ET.parse(source).getroot()
    return {'build': build, 'simple': simple}[builder](xml)
