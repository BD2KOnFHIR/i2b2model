
import unittest


class VisualAttributesTestCase(unittest.TestCase):

    def test_visual_attributes(self):
        from i2b2model.metadata.i2b2ontologyvisualattributes import VisualAttributes
        # text, leaf, approximate, draggable, concept
        c1_states = [("LAE", True, False, False, True),
                     ("CAE", False, False, False, True),
                     ("FAE", False, False, True, True),
                     ("MAE", True, True, False, True),
                     ("OAE", False, False, False, False),
                     ("DAE", False, False, True, False),
                     ("RAE", True, False, False, False)]
        for text, leaf, approximate, draggable, concept in c1_states:
            va = VisualAttributes(text)
            self.assertEqual(va.leaf, leaf)
            self.assertEqual(va.approximate, approximate)
            self.assertEqual(va.draggable, draggable)
            self.assertEqual(va.concept, concept)
            va = VisualAttributes()
            va.leaf = leaf
            va.approximate = approximate
            va.draggable = draggable
            va.concept = concept
            self.assertEqual(text, str(va))

        va = VisualAttributes("LAE")
        self.assertTrue(va.active)
        self.assertFalse(va.hidden)
        va = VisualAttributes("LIE")
        self.assertFalse(va.active)
        self.assertFalse(va.hidden)
        va = VisualAttributes("LHE")
        self.assertFalse(va.active)
        self.assertTrue(va.hidden)

        va = VisualAttributes()
        self.assertTrue(va.active)
        self.assertFalse(va.hidden)
        self.assertEqual("FAE", str(va))
        va.active = False
        self.assertEqual("FIE", str(va))
        va.hidden = True
        self.assertEqual("FHE", str(va))

        va = VisualAttributes("LAE")
        self.assertTrue(va.editable)
        va = VisualAttributes("LA ")
        self.assertFalse(va.editable)
        va = VisualAttributes("LA")
        self.assertFalse(va.editable)

        with self.assertRaises(AssertionError):
            _ = VisualAttributes("AAE")
        with self.assertRaises(AssertionError):
            _ = VisualAttributes("LDE")
        with self.assertRaises(AssertionError):
            _ = VisualAttributes("LAH")


if __name__ == '__main__':
    unittest.main()
