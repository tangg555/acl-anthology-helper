class StringTools(object):
    @classmethod
    def match(cls, one: str, two: str):
        return one.lower() == two.lower()

    @classmethod
    def contain(cls, text: str, keyword: str):
        return keyword.lower() in text.lower()

    @classmethod
    def multi_or_contain(cls, text: str, keywords: list):
        return bool(sum([one.lower() in text.lower() for one in keywords]))

    @classmethod
    def multi_and_contain(cls, text: str, keywords: list):
        return bool(sum([one.lower() in text.lower() for one in keywords]) == len(keywords))

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
    def filename_norm(cls, string: str):
        return ''.join(filter(cls._is_valid_for_file, string))
