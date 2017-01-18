from zlib import adler32


def make_entity_tag(body):
    checksum = adler32(body.encode())
    return '"{checksum}"'.format(checksum=checksum)
