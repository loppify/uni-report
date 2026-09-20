# uni-report

Small Python utility for turning Markdown-based university reports into HTML and PDF files. It is intended to be used with an AI coding agent that prepares the assignment, while this repository provides the report layout and build step.

## Workflow

1. Put the methodology, assignment files, and any student-specific data in `input/`.
2. Ask your AI coding agent to read those materials, complete the requested work, and create an independent directory under `report/`.
3. Each work directory must contain `report.md` and `metadata.yaml`. Store its code, images, and other deliverables in `code/`, `images/`, and `artifacts/`.
4. Build one work or all discovered works:

```sh
uv run python scripts/build.py <work_id>
uv run python scripts/build.py --all
```

The outputs are written to `build/<work_id>.html` and `build/<work_id>.pdf`.

Run the renderer checks with:

```sh
uv run python -m unittest discover -s tests -p 'test_*.py'
```

The build validates that every local image, code, and artifact reference in the generated HTML exists before creating the PDF.

The agent is responsible for understanding the source materials, selecting the requested variant, implementing and running required work, and writing the report from verified results. This utility only renders the prepared Markdown and copies work assets into the generated document.

## Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- System libraries required by [WeasyPrint](https://doc.courtbou.me/weasyprint/stable/first_steps.html#installation)

Install the Python dependencies with:

```sh
uv sync
```

## Minimal example

Create `report/practice_01/metadata.yaml` and `report/practice_01/report.md`, then run:

```sh
uv run python scripts/build.py practice_01
```

`metadata.yaml` follows the structure used by `templates/title-page.html`, for example:

```yaml
university:
  name: Example University
  department: Example Department
report:
  type: Practical work
  number: "1"
  title: Example topic
student:
  name: Student Name
  group: Group
teacher: {}
location:
  city: City
  year: "2026"
```

Use relative paths such as `images/result.png` in the report. Generated reports, source materials, and student profiles are ignored by Git because they commonly contain personal or assignment-specific information.

## Limitations

- The repository does not provide an AI model, agent runtime, or assignment-specific implementation. Use it with an AI coding agent separately.
- The agent's generated work is not automatically correct. Review calculations, code, sources, personal data, and the final PDF before submission.
- PDF rendering depends on system libraries and installed fonts. MathJax is loaded for browser HTML, but JavaScript-dependent math rendering may not be available in PDF output.
- Do not put secrets or real student data in files intended for a public repository.

## Project structure

```text
scripts/build.py       Build HTML and PDF reports
templates/              Report and title-page templates
report/<work_id>/       Local, generated work input
input/                  Local methodology and assignment materials
build/                  Local generated output
```
