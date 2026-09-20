# uni-report

Turn university assignments into structured reports with an AI coding agent, then build them into HTML and PDF.

This repository is the **workspace and report pipeline**. The AI agent reads your methodology and assignment files, completes the requested work, writes the report, and verifies the result. `uni-report` provides the repository conventions, report structure, templates, and build step.

> It does **not** include an AI model or agent runtime. Use it with OpenCode or another coding agent.

## Quick start with OpenCode

### 1. Clone the repository

```sh
git clone https://github.com/loppify/uni-report.git
cd uni-report
```

### 2. Install dependencies

You need Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
```

PDF generation uses [WeasyPrint](https://doc.courtbou.me/weasyprint/stable/first_steps.html), so your system may also need its native libraries.

### 3. Add your assignment materials

Put the methodology, assignment, starter files, screenshots, datasets, and any other source material into:

```text
input/
```

Do not commit personal data, university credentials, tokens, cookies, or private files.

### 4. Open the repository in OpenCode

Start OpenCode from the repository root. The detailed agent workflow is documented in [AGENTS.md](AGENTS.md).

A minimal prompt can be:

```text
Read AGENTS.md and all relevant files in input/.

Complete the requested university assignment from the provided materials.
Determine the correct requirements and variant from the source files.
Run and verify the actual work instead of inventing results.
Create a separate report directory under report/ for every independently submitted work.
Build the final HTML and PDF files and verify the generated output.

My request:
<describe which lab/practical/assignment you want completed>

Optional details:
- variant:
- journal number:
- teacher:
- work numbers:
```

For example:

```text
Read AGENTS.md and all relevant files in input/.

Complete laboratory work 5 from the methodology.
My variant is 8.
Run the implementation, verify the result, generate the report,
build the HTML and PDF, and check the final PDF before finishing.
```

### 5. Check the result

Every independent work should end up as:

```text
report/<work_id>/
    report.md
    metadata.yaml
    code/
    images/
    artifacts/
```

Built files are written to:

```text
build/<work_id>.html
build/<work_id>.pdf
```

Before submitting anything, review the implementation, calculations, sources, screenshots, personal data, and final PDF yourself.

## How the workflow works

1. Put source materials in `input/`.
2. Tell the coding agent what work you want completed.
3. The agent reads the methodology and assignment files.
4. It determines the requirements and the correct variant.
5. It performs and verifies the actual implementation or calculations.
6. It creates an independent directory under `report/` for each submitted work.
7. It writes `report.md` and `metadata.yaml` and stores code/images/artifacts alongside them.
8. It builds HTML and PDF output.
9. It checks the generated files and fixes problems before finishing.

The repository's [AGENTS.md](AGENTS.md) contains the full autonomous workflow and Definition of Done.

## Build reports manually

Build one work:

```sh
uv run python scripts/build.py <work_id>
```

Build all discovered works:

```sh
uv run python scripts/build.py --all
```

Run renderer checks:

```sh
uv run python -m unittest discover -s tests -p 'test_*.py'
```

The build validates that local image, code, and artifact references in the generated HTML exist before creating the PDF.

## Minimal report structure

A work needs at least:

```text
report/practice_01/
    metadata.yaml
    report.md
```

Example `metadata.yaml`:

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

Use relative paths such as `images/result.png` inside the report.

Generated reports, source materials, and student profiles are ignored by Git because they commonly contain personal or assignment-specific information.

## Project structure

```text
AGENTS.md              Instructions for the AI coding agent
scripts/build.py        Build HTML and PDF reports
templates/              Report and title-page templates
input/                  Local methodology and assignment materials
report/<work_id>/       Generated work, code, images, and artifacts
build/                  Generated HTML/PDF output
tests/                  Renderer/build checks
```

## Limitations

- This repository does not provide an AI model or agent runtime. Use OpenCode or another coding agent separately.
- AI-generated work is not automatically correct. Verify code, calculations, sources, and output before submission.
- Assignment quality depends on the source materials you provide.
- PDF rendering depends on system libraries and installed fonts.
- MathJax is loaded for browser HTML, but JavaScript-dependent math rendering may not be available in PDF output.
- Never put secrets, real credentials, or sensitive student data in files intended for a public repository.

## Academic use

The tool automates repetitive implementation and report assembly. You remain responsible for understanding what you submit and for following your university's academic-integrity rules.
