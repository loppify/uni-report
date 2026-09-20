import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts import build


SAMPLE_METADATA = """\
university:
  name: Example University
  department: Example Department
report:
  type: Practical work
  number: "1"
  title: Example topic
student:
  name: Test Student
  group: TEST-01
teacher: {}
location:
  city: Test City
  year: "2026"
"""


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.root = Path(self.temp.name)

        self.original_report = build.REPORT
        self.original_build = build.BUILD
        self.original_assets = build.ASSETS

        build.REPORT = self.root / "report"
        build.BUILD = self.root / "build"
        build.ASSETS = build.BUILD / "assets"

        work = build.REPORT / "practice_01"
        (work / "images").mkdir(parents=True)
        (work / "code").mkdir()
        (work / "artifacts").mkdir()

        (work / "metadata.yaml").write_text(SAMPLE_METADATA, encoding="utf-8")
        (work / "report.md").write_text(
            """# Test report

Inline math: $x^2 + y^2$.

$$
\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}
$$

![Example image](images/example.svg)

[Work notes](README.md)
""",
            encoding="utf-8",
        )
        (work / "README.md").write_text("Example work notes.", encoding="utf-8")
        (work / "images" / "example.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
            '<rect width="10" height="10" fill="black"/>'
            "</svg>",
            encoding="utf-8",
        )

    def tearDown(self):
        build.REPORT = self.original_report
        build.BUILD = self.original_build
        build.ASSETS = self.original_assets
        self.temp.cleanup()

    def test_discover_works(self):
        self.assertEqual(["practice_01"], build.discover_works())

    def test_work_id_is_validated(self):
        with self.assertRaises(ValueError):
            build.get_work_dir("../practice_01")

    def test_rendered_assets_exist(self):
        build.copy_assets("practice_01")
        html = build.render_html("practice_01").read_text(encoding="utf-8")
        build.validate_local_assets(html)
        self.assertIn('href="assets/practice_01/README.md"', html)
        self.assertTrue((build.ASSETS / "practice_01" / "README.md").is_file())

    def test_math_is_rendered_to_static_svg(self):
        build.copy_assets("practice_01")
        html = build.render_html("practice_01").read_text(encoding="utf-8")
        build.validate_local_assets(html)
        math_dir = build.ASSETS / "practice_01" / "math"
        self.assertTrue(math_dir.is_dir())
        self.assertGreaterEqual(len(list(math_dir.glob("*.svg"))), 2)
        self.assertIn('class="math-inline"', html)
        self.assertIn('class="math-display"', html)

    def test_missing_asset_is_reported(self):
        build.BUILD.mkdir(parents=True, exist_ok=True)
        with self.assertRaises(FileNotFoundError):
            build.validate_local_assets('<img src="assets/missing/image.png">')

    def test_full_html_and_pdf_smoke_build(self):
        build.copy_css()
        build.build_work("practice_01")
        html = build.BUILD / "practice_01.html"
        pdf = build.BUILD / "practice_01.pdf"
        self.assertTrue(html.is_file())
        self.assertTrue(pdf.is_file())
        self.assertGreater(pdf.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
