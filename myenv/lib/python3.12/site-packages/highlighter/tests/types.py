import unittest

from packaging.markers import Marker

from ..types import EnvironmentMarkers


class EnvironmentMarkersTest(unittest.TestCase):
    def test_platforms(self) -> None:
        e = EnvironmentMarkers(sys_platform="win32")
        self.assertEqual("nt", e.os_name)
        e = EnvironmentMarkers(sys_platform="darwin")
        self.assertEqual("posix", e.os_name)
        e = EnvironmentMarkers(python_version="2.7.5")
        self.assertEqual("linux2", e.sys_platform)
        with self.assertRaises(TypeError):
            e = EnvironmentMarkers(sys_platform="x")

    def test_match_empty(self) -> None:
        m = Marker("implementation_name=='cpython'")
        e = EnvironmentMarkers.for_python("3.7.5")
        self.assertTrue(e.match(m))

    def test_match_lt_3(self) -> None:
        m = Marker("python_version < '3'")
        e = EnvironmentMarkers.for_python("2.7.0")
        self.assertTrue(e.match(m))

    def test_match_3(self) -> None:
        m = Marker("python_version < '3'")
        e = EnvironmentMarkers.for_python("3.7.5")
        self.assertFalse(e.match(m))

    def test_no_extras(self) -> None:
        m = Marker("extra == ''")
        e = EnvironmentMarkers.for_python("3.7.5")
        self.assertTrue(e.match(m))
        self.assertTrue(e.match(m, ()))
        self.assertFalse(e.match(m, ("foo",)))

    def test_extras(self) -> None:
        m = Marker("extra == 'foo'")
        e = EnvironmentMarkers.for_python("3.7.5")
        self.assertFalse(e.match(m, ()))
        self.assertTrue(e.match(m, ("foo",)))
        self.assertTrue(e.match(m, ("a", "foo")))
        self.assertTrue(e.match(m, ("foo", "a")))
        self.assertFalse(e.match(m, ("food",)))
