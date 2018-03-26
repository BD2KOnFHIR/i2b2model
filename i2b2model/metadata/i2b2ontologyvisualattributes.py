from typing import Optional, cast, Sized


class VisualAttributes:
    """ i2b2 Metadata Visual attributes element

    """
    def __init__(self, string_value: Optional[str] = None) -> None:
        """
        Constructor from optional string value.
        :param string_value:
        """
        assert (string_value is None or len(string_value) in (2, 3))
        if string_value is not None:
            char1 = string_value[0]
            assert (char1 in "CFMLODR")
            self.leaf = char1 in 'LMR'
            self.approximate = char1 == 'M'
            self.draggable = char1 in 'FD'
            self.concept = char1 in 'CFML'

            char2 = string_value[1]
            assert (char2 in "AIH")
            self.active = char2 == 'A'
            self.hidden = char2 == 'H'

            char3 = string_value[2] if len(cast(Sized, string_value)) == 3 else ' '
            assert (char3 in " E")
            self.editable = char3 == 'E'
        else:
            self.leaf = False           # C
            self.approximate = False    # Leaf only - multiple targets
            self.draggable = True       # Folder only
            self.concept = True         # Concept or Modifier Dimension

            self.active = True
            self.hidden = False         # No commitment whether hidden is active

            self.editable = True

    def __str__(self):
        if self.concept:
            if self.leaf:
                rval = 'M' if self.approximate else 'L'
            else:
                rval = 'F' if self.draggable else 'C'
        else:
            if self.leaf:
                rval = 'R'
            else:
                rval = 'D' if self.draggable else 'O'
        rval += 'H' if self.hidden else 'A' if self.active else 'I'
        rval += 'E' if self.editable else ' '
        return rval

    def reify(self):
        return str(self)
