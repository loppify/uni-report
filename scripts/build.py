from argparse import ArgumentParser
from pathlib import Path
import re
import shutil

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup
from weasyprint import HTML


ROOT = Path(__file__).parent.parent
REPORT = ROOT / "report"
TEMPLATES = ROOT / "templates"
BUILD = ROOT / "build"
ASSETS = BUILD / "assets"

BUILD.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)


def get_work_dir(work_id: str) -> Path:
    work_dir = REPORT / work_id

    if not work_dir.is_dir():
        raise FileNotFoundError(
            f"Work directory does not exist: {work_dir}"
        )

    return work_dir


def load_metadata(work_id: str) -> dict:
    path = get_work_dir(work_id) / "metadata.yaml"

    if not path.exists():
        raise FileNotFoundError(
            f"Metadata file does not exist: {path}"
        )

    with path.open(encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def rewrite_asset_paths(html: str, work_id: str) -> str:
    prefix = f"assets/{work_id}/"

    html = re.sub(
        r'(<img[^>]+src=["\'])(images/)',
        rf"\1{prefix}images/",
        html,
        flags=re.IGNORECASE,
    )

    html = re.sub(
        r'(<a[^>]+href=["\'])(code/)',
        rf"\1{prefix}code/",
        html,
        flags=re.IGNORECASE,
    )

    html = re.sub(
        r'(<a[^>]+href=["\'])(artifacts/)',
        rf"\1{prefix}artifacts/",
        html,
        flags=re.IGNORECASE,
    )

    return html


def wrap_images_in_figures(html: str) -> str:
    pattern = re.compile(
        r'<p><img alt="([^"]*)" src="([^"]+)" /></p>'
    )

    def replace(match: re.Match) -> str:
        caption = match.group(1)
        src = match.group(2)

        return (
            "<figure>"
            f'<img src="{src}" alt="{caption}">'
            f"<figcaption>{caption}</figcaption>"
            "</figure>"
        )

    return pattern.sub(replace, html)


def number_figures(html: str) -> str:
    counter = 0

    def replace(match: re.Match) -> str:
        nonlocal counter
        counter += 1

        caption = match.group(1)

        return (
            "<figcaption>"
            f"Рисунок {counter} – {caption}"
            "</figcaption>"
        )

    return re.sub(
        r"<figcaption>(.*?)</figcaption>",
        replace,
        html,
        flags=re.DOTALL,
    )


def render_markdown(work_id: str) -> str:
    path = get_work_dir(work_id) / "report.md"

    if not path.exists():
        raise FileNotFoundError(
            f"Report file does not exist: {path}"
        )

    source = path.read_text(encoding="utf-8")

    html = markdown.markdown(
        source,
        extensions=[
            "fenced_code",
            "tables",
            "sane_lists",
        ],
    )

    html = html.replace(
        "<!-- pagebreak -->",
        '<div class="page-break"></div>',
    )

    html = rewrite_asset_paths(html, work_id)
    html = wrap_images_in_figures(html)
    html = number_figures(html)

    return html


def copy_directory(source: Path, target: Path) -> None:
    if not source.exists():
        return

    shutil.copytree(
        source,
        target,
        dirs_exist_ok=True,
    )


def copy_assets(work_id: str) -> None:
    work_dir = get_work_dir(work_id)
    target = ASSETS / work_id

    if target.exists():
        shutil.rmtree(target)

    target.mkdir(parents=True, exist_ok=True)

    copy_directory(
        work_dir / "images",
        target / "images",
    )

    copy_directory(
        work_dir / "code",
        target / "code",
    )

    copy_directory(
        work_dir / "artifacts",
        target / "artifacts",
    )


def copy_css() -> None:
    css_source = TEMPLATES / "report.css"
    css_target = BUILD / "report.css"

    if not css_source.exists():
        raise FileNotFoundError(
            f"CSS file does not exist: {css_source}"
        )

    shutil.copy2(
        css_source,
        css_target,
    )


def render_html(work_id: str) -> Path:
    metadata = load_metadata(work_id)
    content = render_markdown(work_id)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = env.get_template("report.html")

    html = template.render(
        **metadata,
        content=Markup(content),
        work_id=work_id,
    )

    output = BUILD / f"{work_id}.html"
    output.write_text(
        html,
        encoding="utf-8",
    )

    return output


def render_pdf(html_path: Path, work_id: str) -> Path:
    output = BUILD / f"{work_id}.pdf"

    HTML(
        filename=str(html_path),
        base_url=str(BUILD),
    ).write_pdf(
        str(output),
    )

    return output


def build_work(work_id: str) -> None:
    print(f"Building: {work_id}")

    copy_assets(work_id)

    html_path = render_html(work_id)
    pdf_path = render_pdf(html_path, work_id)

    print(f"Generated: {html_path}")
    print(f"Generated: {pdf_path}")


def discover_works() -> list[str]:
    if not REPORT.exists():
        return []

    works = []

    for path in sorted(REPORT.iterdir()):
        if not path.is_dir():
            continue

        if (
            (path / "report.md").exists()
            and (path / "metadata.yaml").exists()
        ):
            works.append(path.name)

    return works


def parse_args():
    parser = ArgumentParser()

    parser.add_argument(
        "work_ids",
        nargs="*",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        dest="build_all",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    copy_css()

    if args.build_all:
        work_ids = discover_works()
    elif args.work_ids:
        work_ids = args.work_ids
    else:
        work_ids = discover_works()

    if not work_ids:
        raise RuntimeError(
            "No works found in report/"
        )

    failed = []

    for work_id in work_ids:
        try:
            build_work(work_id)
        except Exception as exc:
            failed.append((work_id, exc))
            print(f"Failed: {work_id}")
            print(exc)

    if failed:
        names = ", ".join(
            work_id
            for work_id, _ in failed
        )

        raise RuntimeError(
            f"Build failed for: {names}"
        )


if __name__ == "__main__":
    main()