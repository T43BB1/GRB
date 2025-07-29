def max_version(a):
    return max(a, key=lambda x:[int(y) for y in x.split('.')])
class FilterModule(object):
    def filters(self):
        return {
            'max_version': max_version,
        }