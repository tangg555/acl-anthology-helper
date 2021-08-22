class String(object):
    @classmethod
    def match(cls, one: str, two: str):
        return one.lower() == two.lower()

    @classmethod
    def contain(cls, subj: str, obj: str):
        return obj.lower() in subj.lower()

    @classmethod
    def fileNameNorm(cls, obj):
        return ''.join(filter(str.isalnum, obj))
