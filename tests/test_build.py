import unittest

from scripts import build


class BuildTests(unittest.TestCase):
    def test_discover_works(self):
        self.assertIn("practice_01", build.discover_works())

    def test_work_id_is_validated(self):
        with self.assertRaises(ValueError):
            build.get_work_dir("../practice_01")

    def test_rendered_assets_exist(self):
        work_id = "practice_01"
        build.copy_assets(work_id)
        html = build.render_html(work_id).read_text(encoding="utf-8")
        build.validate_local_assets(html)

        self.assertIn('href="assets/practice_01/README.md"', html)
        self.assertTrue(
            (build.BUILD / "assets/practice_01/README.md").is_file()
        )

    def test_missing_asset_is_reported(self):
        with self.assertRaises(FileNotFoundError):
            build.validate_local_assets('<img src="assets/missing/image.png">')


if __name__ == "__main__":
    unittest.main()
