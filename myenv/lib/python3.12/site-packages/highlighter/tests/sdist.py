import unittest

from ..sdist import convert_sdist_requires


class ConvertSdistRequiresTest(unittest.TestCase):
    def test_blank_line(self) -> None:
        self.assertEqual(
            ["a"],
            convert_sdist_requires("a\n\n"),
        )

    def test_section(self) -> None:
        self.assertEqual(
            ["a; python_version < '3.4'", "b; python_version < '3.4'"],
            convert_sdist_requires("[:python_version < '3.4']\na\nb\n"),
        )

    def test_combine_markers(self) -> None:
        self.assertEqual(
            ["a; python_version < '3.4'", "b; python_version < '3.4'"],
            convert_sdist_requires("[:python_version < '3.4']\na\nb\n"),
        )

    def test_absl_py_0_9_0(self) -> None:
        self.assertEqual(
            ["six", 'enum34; python_version < "3.4"'],
            convert_sdist_requires(
                """\
six

[:python_version < "3.4"]
enum34
"""
            ),
        )

    def test_requests_2_22_0(self) -> None:
        self.assertEqual(
            [
                "PySocks!=1.5.7,>=1.5.6; extra == 'socks'",
                'win_inet_pton; (sys_platform == "win32" and python_version == "2.7") and extra == \'socks\'',
            ],
            convert_sdist_requires(
                """\
[socks]
PySocks!=1.5.7,>=1.5.6

[socks:sys_platform == "win32" and python_version == "2.7"]
win_inet_pton
"""
            ),
        )
