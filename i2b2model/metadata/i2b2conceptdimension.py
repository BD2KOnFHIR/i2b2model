from dynprops import Local, Parent

from i2b2model.metadata.commondimension import CommonDimension


class ConceptDimension(CommonDimension):
    concept_path: Local[str] = lambda self: self.path()
    concept_cd: Local[str] = lambda self: self.cd()
    name_char: Local[str] = lambda self: self.name_char_()
    concept_blob: Local[str] = lambda self: self.blob()
    _: Parent

    def __lt__(self, other):
        return self.concept_path < other.concept_path

    def __eq__(self, other):
        return self.concept_path == other.concept_path
