from dynprops import Local, Parent

from i2b2model.metadata.commondimension import CommonDimension


class ModifierDimension(CommonDimension):
    modifier_path: Local[str] = lambda self: self.path()
    modifier_cd: Local[str] = lambda self: self.cd()
    name_char: Local[str] = lambda self: self.name_char_()
    modifier_blob: Local[str] = lambda self: self.blob()
    _: Parent

    def __lt__(self, other):
        return self.modifier_path < other.modifier_path

    def __eq__(self, other):
        return self.modifier_path == other.modifier_path
