def make_entity_tag(body):
    checksum = hash(body) + (1 << 64)
    return '"{checksum}"'.format(checksum=checksum)
