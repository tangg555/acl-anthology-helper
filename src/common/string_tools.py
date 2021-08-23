class StringTools(object):
    @classmethod
    def match(cls, one: str, two: str):
        return one.lower() == two.lower()

    @classmethod
    def contain(cls, subj: str, obj: str):
        return obj.lower() in subj.lower()

    @classmethod
    def isssymbols(cls, c: chr):
        """
        :param c: character
        :return:
        is special symbols like !@#$%^%......
        """
        return str.isalnum(c) | str.isspace(c)

    @classmethod
    def _is_valid_for_file(cls, c: chr):
        """
        :param c: character
        :return:
        is special symbols like !@#$%^%......
        """
        return False if c in "\\/:*?*<>|" else True

    @classmethod
    def fileNameNorm(cls, string: str):
        return ''.join(filter(cls._is_valid_for_file, string))
