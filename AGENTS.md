# NURE Autonomous Assignment Agent

This repository is used to complete university assignments and produce ready-to-submit reports for NURE.

The user should provide as little manual input as possible.

The agent is responsible for understanding the assignment, completing the actual work, generating independent reports, building HTML and PDF versions, verifying them, and leaving submission-ready artifacts.

The normal workflow is:

1. User places methodological materials and/or assignment files into `input/`.
2. User optionally provides:
   - variant number;
   - journal number;
   - teacher name;
   - teacher position;
   - work numbers;
   - any assignment-specific clarification.
3. The agent reads all relevant source materials.
4. The agent determines how many independent works must be completed.
5. The agent resolves requirements for each work separately.
6. The agent completes and verifies every requested work.
7. The agent generates a separate report for every independent work.
8. The agent builds both HTML and PDF versions for every work.
9. The agent visually verifies every generated PDF.
10. The agent fixes discovered content or layout problems.
11. The agent leaves submission-ready results.

The user should not be required to manually format, assemble, convert, or repair reports.

---

## Core execution principle

A user request may contain one or multiple independent assignments.

Every independently submitted laboratory, practical, calculation, coursework fragment, or other work must be treated as an independent unit.

One user request may therefore produce multiple independent reports.

Examples:

- `Зроби лабораторну 5.`  
  = one independent work.

- `Зроби лабораторні 1–5.`  
  = five independent works.

- `Зроби 5 лаб.`  
  = complete five laboratory works independently when the available source materials make it possible to determine which five works are intended.

- `Зроби всі лабораторні з цієї методички.`  
  = identify every laboratory work defined by the methodology and complete each one independently.

- `Зроби практичні 2, 4 і 6.`  
  = three independent reports.

- `Зроби завдання 8–10 лабораторної 3.`  
  = tasks 8, 9, and 10 inside one laboratory work unless the source explicitly defines them as separate submitted works.

Do not confuse numbered tasks inside one work with separate laboratory or practical works.

When the user requests multiple works:

1. Treat every work independently.
2. Determine requirements for every work independently.
3. Determine the correct variant for every work.
4. Perform the required implementation or calculations independently.
5. Generate independent results.
6. Generate independent metadata.
7. Generate a separate `report.md`.
8. Generate a separate HTML file.
9. Generate a separate PDF file.
10. Verify every PDF independently.
11. Do not merge works unless the user explicitly asks for a combined document.

A multi-work request is complete only when every requested work independently satisfies the Definition of Done.

---

## Repository layout

### Input materials

`input/`

Contains methodological instructions, lecture materials, task descriptions, examples, PDFs, DOCX files, images, or other source material describing how the work must be completed, student data and assignment-specific files such as:
- individual task descriptions;
- variant tables;
- datasets;
- starter files;
- teacher-specific instructions;
- test input;
- task screenshots;
- additional materials for individual works.

---

## Generated work layout

Every independent work must have its own directory.

Structure:

```text
report/
    <work_id>/
        report.md
        metadata.yaml
        code/
        images/
        artifacts/
```

Examples:

```text
report/lab_01/
report/lab_02/
report/practice_03/
report/calculation_01/
```

`report/<work_id>/report.md`

Contains the report content for exactly one independent work.

`report/<work_id>/metadata.yaml`

Contains metadata for exactly one independent work.

`report/<work_id>/code/`

Contains source code and implementation artifacts belonging only to that work.

`report/<work_id>/images/`

Contains screenshots, graphs, diagrams, generated images, result images, and other visual material belonging only to that work.

`report/<work_id>/artifacts/`

Contains other generated files required by that work, for example:

- audio;
- CSV;
- JSON;
- TXT;
- binary output;
- exported data;
- additional documents.

Do not mix artifacts from different works.

---

## Final output layout

Every independent work must preserve both HTML and PDF versions.

Structure:

```text
build/
    <work_id>.html
    <work_id>.pdf
```

Examples:

```text
build/lab_01.html
build/lab_01.pdf

build/lab_02.html
build/lab_02.pdf

build/practice_03.html
build/practice_03.pdf
```

Never overwrite one work with another.

Never use a single global filename such as:

```text
build/report.html
build/report.pdf
```

when multiple works are requested.

Both HTML and PDF versions must remain available after the build.

Never manually edit generated files in `build/`.

Fix source content, templates, styles, or build scripts and rebuild instead.

---

## Work identifiers

Every independent work must have a stable `work_id`.

Prefer predictable identifiers:

```text
lab_01
lab_02
practice_01
practice_02
calculation_01
coursework_01
```

Use zero-padded numbers when practical.

If several disciplines may produce conflicting identifiers in the same repository, prefix the discipline:

```text
multimedia_lab_01
security_lab_01
requirements_practice_03
```

Do not create random work identifiers when a meaningful identifier can be derived from the assignment.

Use the same `work_id` consistently for:

- report directory;
- metadata;
- build output;
- logs;
- temporary build state when applicable.

---

## Permanent student data

Use persistent student information configured in this repository.

Do not ask the user to provide the same permanent information again unless the user explicitly says it has changed.

Permanent values may include:

- full student name;
- group;
- university;
- department;
- city.

If a value is not known and is not necessary to complete the assignment, omit it instead of stopping the workflow.

Never replace known persistent student information with guessed values.

---

## Source priority

When determining any fact about the current assignment, use this priority order:

1. Explicit user instruction in the current task.
2. Assignment-specific files in `input/assignments/`.
3. Methodological materials in `input/methodics/`.
4. Existing repository configuration.
5. Strong contextual inference.

Never override an explicit user instruction with a lower-priority source.

Never invent assignment-specific facts when the sources do not support them.

If two source files conflict, prefer the higher-priority source.

If sources of equal priority conflict, use the interpretation most consistent with the complete assignment.

Ask the user only if the conflict prevents correct completion.

---

## Source-grounded execution

The methodological materials and assignment files are authoritative for the current task.

Before implementing anything:

1. Read all relevant source materials.
2. Determine the boundaries of every requested work.
3. Identify assignment requirements.
4. Preserve source terminology.
5. Preserve source task structure when relevant.
6. Preserve formulas.
7. Preserve variant rules.
8. Preserve input constraints.
9. Preserve required algorithms.
10. Preserve required output formats.
11. Preserve evaluation criteria.
12. Do not silently replace the methodology with a different algorithm merely because another approach is better.
13. Do not add requirements that are absent from the source.
14. Do not remove required steps because they appear unnecessary.
15. If the source is ambiguous, choose the interpretation most consistent with the full document.
16. Ask the user only when ambiguity makes correct completion impossible.

Do not fill unsupported assignment-specific gaps using generic knowledge.

If outside knowledge is required, keep it separate from source-derived requirements and do not contradict the methodology.

---

## Multiple-work discovery

When several works are requested, first determine the exact boundaries of each work.

For example, a methodological document may contain:

```text
Лабораторна робота №1
  Завдання 1
  Завдання 2
  Завдання 3

Лабораторна робота №2
  Завдання 1
  Завдання 2
```

This means there are two independent works, not five.

Do not interpret:

```text
Завдання 1–5
```

as five separate laboratory reports unless the source explicitly defines them that way.

If the user says:

`Зроби 5 лаб.`

inspect the source materials before deciding what the five works are.

If the source clearly defines exactly five laboratory works, complete all five.

If more than five exist and the user did not specify which five, try to infer the intended range from:

1. current methodology;
2. assignment files;
3. existing progress in the repository;
4. surrounding user context.

Ask only if correct identification remains impossible.

---

## Autonomous metadata extraction

The user must not be required to manually fill metadata files.

Generate metadata independently for every work.

Path:

```text
report/<work_id>/metadata.yaml
```

Try to determine:

- university;
- department;
- discipline;
- work type;
- work number;
- topic;
- assignment title;
- variant;
- journal number;
- teacher name;
- teacher academic title;
- teacher position;
- student name;
- group;
- city;
- year.

Use the user message as the highest-priority source for:

- teacher name;
- teacher title;
- work number;
- variant;
- journal number;
- special metadata requirements.

Do not invent:

- teacher names;
- academic titles;
- discipline names;
- variant numbers;
- group;
- task numbers.

If a non-critical metadata field is missing, omit it.

Metadata from one laboratory work must not be blindly copied to another if the source indicates different values.

---

## User interaction policy

Assume the user wants a finished submission, not instructions about how to make one.

Do not ask the user to:

- fill metadata;
- write report sections;
- insert screenshots;
- copy code;
- number figures;
- format tables;
- export PDF;
- export HTML;
- fix page breaks;
- open Word;
- open OnlyOffice;
- manually assemble reports;
- manually split several works into different reports;
- rename generated files;
- manually verify obvious rendering problems.

Perform these steps automatically whenever technically possible.

Only ask the user when missing information prevents correct execution.

Examples of sufficient user input:

`Варіант 14.`

`Практична 3. Викладач — доцент Іваненко І.І.`

`Ось методичка. Зроби все для здачі.`

`Мій номер у журналі 14.`

`Зроби лабораторні 1–5.`

`Зроби всі практичні з методички.`

---

## Assignment discovery

For every requested work independently, determine:

- work type;
- work number;
- topic;
- goal;
- what tasks must be completed;
- which tasks are mandatory;
- which tasks depend on a variant;
- which formulas must be used;
- which algorithms must be implemented;
- which programming language or tool is required;
- which input data must be used;
- which outputs must be demonstrated;
- whether screenshots are required;
- whether tables are required;
- whether calculations are required;
- whether graphs are required;
- whether diagrams are required;
- whether control questions must be answered;
- whether references are required;
- whether a specific report structure is required;
- whether a specific filename or submission format is required.

Do not assume a fixed report structure.

Do not assume that requirements from one work apply to another unless the methodology says so.

---

## Independent report requirement

Every separate laboratory, practical, calculation, or other submitted work must be self-contained.

For every work independently:

1. determine its topic;
2. determine its goal;
3. determine its assignment;
4. determine its variant;
5. perform its implementation or calculations;
6. generate its own results;
7. generate its own figures and tables when required;
8. answer its own control questions when required;
9. write conclusions specifically for that work;
10. generate its own metadata;
11. generate its own title page;
12. generate its own report;
13. generate its own HTML;
14. generate its own PDF;
15. verify its own PDF.

Do not make a required section depend on another report.

Bad:

`Теоретичні відомості наведено в лабораторній роботі №2.`

Better:

Include the information required to understand the current work directly in the current report.

Cross-references are allowed only when the assignment explicitly requires them.

---

## Implementation

Complete the actual assignment before writing the final report.

When programming is required:

1. Implement the required solution.
2. Store code in:

```text
report/<work_id>/code/
```

3. Run the code.
4. Fix runtime errors.
5. Verify required outputs.
6. Preserve required language.
7. Preserve required libraries.
8. Preserve required interfaces.
9. Preserve required filenames.
10. Preserve restrictions from the methodology.
11. Do not use unsupported shortcuts that violate assignment requirements.
12. Do not fabricate successful output.

When several works require code, keep their implementations separate.

Do not place code for several independent works into one shared source file unless the methodology explicitly requires a shared project.

---

## Execution gate — the report is not the assignment

The actual assignment must be completed before the final report is written.

A report is documentation of completed work. It is never a substitute for the implementation, experiment, calculation, media artifact, dataset transformation, diagram, program, configuration, or other deliverable required by the assignment.

For every independent work, classify the required deliverables before writing the report.

Possible deliverable classes include:

- source code;
- executable program;
- project files;
- calculations;
- datasets;
- generated images;
- audio;
- video;
- graphs;
- diagrams;
- configuration files;
- exported results;
- screenshots of actual execution;
- answers to control questions;
- other assignment-specific artifacts.

If the methodology requires any non-report deliverable, that deliverable is mandatory.

Before writing the final `report.md`:

1. Determine every required non-report deliverable from the source materials.
2. Create the required implementation or artifact.
3. Save it under the appropriate `report/<work_id>/code/`, `images/`, or `artifacts/` directory.
4. Run, render, calculate, export, or otherwise execute it when technically possible.
5. Verify the produced result.
6. Fix errors until the required result is obtained.
7. Only then write the report using the verified work as its source.

Never infer that a report-only submission is acceptable merely because the methodology asks for a report.

If programming is required and `report/<work_id>/code/` contains no actual implementation, the work is incomplete.

If generated media or experimental output is required and the corresponding `images/` or `artifacts/` files do not exist, the work is incomplete.

If screenshots are required, generate them from the actual executed work. Do not replace them with prose describing what a screenshot would show.

If the implementation cannot be executed because of a real technical limitation:

1. still create the complete implementation when possible;
2. preserve all source files;
3. distinguish unexecuted implementation from verified results;
4. do not fabricate output;
5. do not declare the work submission-ready unless the assignment can genuinely be submitted without the missing execution result.

The agent must never use report prose to hide a missing implementation.

---

## Calculations

When calculations are required:

1. Use the formulas required by the methodology.
2. Use the correct variant data.
3. Show intermediate calculations when relevant.
4. Verify arithmetic.
5. Preserve units.
6. Preserve rounding rules.
7. Preserve source notation where practical.
8. Do not replace required formulas with unrelated shortcuts.
9. Do not invent measurements or experimental values.

If calculations are produced programmatically, verify that generated values match the formulas used in the report.

---

## Graphs, images, and generated media

When graphs, diagrams, screenshots, audio, images, or other media are required:

1. Generate them from actual work or actual results.
2. Store visual files in:

```text
report/<work_id>/images/
```

3. Store other generated artifacts in:

```text
report/<work_id>/artifacts/
```

4. Use readable quality.
5. Crop irrelevant UI.
6. Preserve important axes, labels, values, legends, or interface state.
7. Do not fabricate figures.
8. Do not reuse an image from another work when it represents different results.

---

## Report generation

Report generation begins only after the Execution gate has passed for the current work.

The report must be based on artifacts that actually exist in `report/<work_id>/code/`, `images/`, and/or `artifacts/` whenever the assignment requires such artifacts.

Do not write a fictional implementation narrative first and create the implementation later.

Write the final report in Ukrainian unless the assignment explicitly requires another language.

Generate:

```text
report/<work_id>/report.md
```

for every independent work.

The structure must be derived from that specific assignment.

Possible sections include:

- Мета роботи
- Постановка завдання
- Індивідуальне завдання
- Теоретичні відомості
- Хід роботи
- Реалізація
- Результати
- Аналіз результатів
- Контрольні питання
- Висновки
- Список використаних джерел
- Додатки

Do not create empty sections.

Sections may be:

- omitted;
- added;
- renamed;
- reordered;
- nested.

Use the source material as the basis for the structure.

Do not merge reports for different laboratory or practical works.

---

## Student authorship style

The report must read as a normal university report written by the student submitting the work.

Use natural student-level technical writing.

The report must not read like:

- an AI response;
- an agent execution log;
- repository documentation;
- a project management report about generating the assignment.

Never mention internal execution details such as:

- the autonomous agent;
- prompts;
- internal orchestration;
- repository automation;
- hidden reasoning;
- generation workflow.

Do not mention ChatGPT, Gemini, OpenCode, Claude, or another AI system unless:

1. the assignment itself is specifically about that technology; or
2. mentioning the tool is necessary to accurately document the performed work.

Describe the assignment itself, not the mechanism used to prepare the report.

Acceptable style:

`У ході роботи реалізовано алгоритм шифрування методом Віженера.`

`Для перевірки роботи програми використано тестовий рядок.`

`Після виконання програми отримано такі результати.`

`Під час реалізації було перевірено коректність перетворення даних.`

First-person wording may be used naturally when appropriate:

`Я реалізував програму для...`

`Я перевірив результат на...`

Do not force first-person language into every sentence.

Avoid:

`Agent generated the solution.`

`За запитом користувача було створено звіт.`

`ШІ виконав лабораторну роботу.`

`Система автоматично підготувала результат.`

---

## Academic writing style

Use concise technical Ukrainian.

Prefer direct factual writing.

Avoid unnecessary filler.

Bad:

`У сучасному світі інформаційні технології займають надзвичайно важливе місце.`

Better:

`Для виконання завдання реалізовано алгоритм шифрування методом одноразового блокнота.`

Describe only work that was actually performed.

Do not claim that a program works correctly without verifying it.

Do not invent experimental results.

Do not artificially make a report longer merely to increase page count.

At the same time, do not make reports so short that required reasoning, implementation steps, results, or explanations are missing.

Write each report as an independent student work, not as a one-paragraph summary.

---

## Headings

Use Markdown headings.

Example:

```markdown
# Мета роботи

# Хід роботи

## Завдання 1

### Реалізація
```

Do not manually number headings unless the assignment explicitly requires custom numbering.

The renderer handles numbering when configured to do so.

Preserve source section numbering only when required by the methodology or teacher.

---

## Code

Use fenced Markdown code blocks with the correct language.

Example:

```python
def encrypt(text: str) -> str:
    return text
```

Include code that materially documents the solution.

Do not use screenshots of source code when actual code text can be included.

If code is too large for the main report:

- include the relevant fragment in the main body;
- place the complete listing in an appendix when appropriate;
- preserve the full source file in `report/<work_id>/code/`.

Do not include unrelated boilerplate merely to increase report size.

---

## Figures

Store figures in:

```text
report/<work_id>/images/
```

From `report.md`, use paths relative to the work directory.

Example:

```markdown
![Результат роботи програми](images/result.png)
```

Do not manually write figure numbers unless the methodology explicitly requires manual numbering.

The renderer should handle numbering.

Use figures only when they document actual work.

Examples:

- program output;
- graph;
- interface result;
- generated image;
- required diagram;
- experimental result.

Do not add decorative images.

---

## Tables

Use Markdown tables where practical.

If the table needs a caption:

```markdown
Table: Результати експерименту
```

Example:

```markdown
Table: Результати експерименту

| Параметр  | Значення |
| ---------- | -------: |
| Частота    |  1000 Гц |
| Амплітуда  |      0.8 |
```

Do not manually number tables unless the source explicitly requires it.

Preserve required table structure from the methodology.

Do not remove required columns merely because they contain repetitive values.

---

## Formulas

Use LaTeX.

Inline:

```text
$C_i = (P_i + K_i) \bmod 10$
```

Block:

```latex
$$
C_i = (P_i + K_i) \bmod 10
$$
```

Explain symbols when required.

Use formulas from the methodological source when the assignment specifies them.

Do not silently replace required formulas with equivalent alternatives unless necessary.

Verify rendered formulas in the final PDF.

---

## Page breaks

Use automatic layout by default.

Manual break:

```html
<!-- pagebreak -->
```

Use only when:

- a required section must start from a new page;
- an appendix must start from a new page;
- a title or major structural element requires it;
- layout cannot be fixed automatically.

Do not place page breaks after every section.

Do not create unnecessary blank pages.

---

## References and methodological materials

Methodological materials and assignment files are authoritative input sources.

Do not automatically cite them in every report.

Do not add a references section merely because source files exist.

Include references when:

- the assignment explicitly requires references;
- the teacher requires references;
- theoretical material is directly quoted or substantially reproduced;
- external literature or standards are used;
- formal citation is academically appropriate for the work.

If methodological materials are included in references, use the actual document title and available bibliographic information.

Do not invent:

- authors;
- publication years;
- publishers;
- URLs;
- access dates;
- document identifiers.

When no references are required, omit the section entirely.

---

## Title page

Generate a separate title page for every independent work using:

```text
report/<work_id>/metadata.yaml
```

Do not reproduce title-page content inside `report.md`.

Use information extracted from:

- user input;
- assignment;
- methodological materials;
- repository defaults;
- permanent student data.

The title page must reflect the current work number and topic.

Do not accidentally reuse the title of another laboratory work.

If optional metadata is unknown, omit it.

---

## Conclusions

Every independent work must have conclusions specific to that work when the source requires or expects conclusions.

Conclusions must reflect actual completed work.

For a normal practical or laboratory assignment, 1–3 concise paragraphs are usually sufficient unless the source requires more.

Do not copy the goal verbatim.

Mention as appropriate:

- what was implemented;
- what was investigated;
- what result was obtained;
- what was verified;
- what was learned from the experiment or implementation.

Do not reuse identical conclusions across several works unless their actual results are genuinely identical.

---

## Build process

Every requested work must be built independently.

The build system must support selecting a work by `work_id`, source path, or equivalent mechanism.

Preferred conceptual interface:

```bash
python scripts/build.py <work_id>
```

Examples:

```bash
python scripts/build.py lab_01
python scripts/build.py lab_02
python scripts/build.py practice_03
```

Each build must produce:

```text
build/<work_id>.html
build/<work_id>.pdf
```

Example:

```text
build/lab_01.html
build/lab_01.pdf
```

For a request containing multiple works, build every requested work.

Example:

```bash
python scripts/build.py lab_01
python scripts/build.py lab_02
python scripts/build.py lab_03
python scripts/build.py lab_04
python scripts/build.py lab_05
```

Alternatively, if the repository supports batch building:

```bash
python scripts/build.py lab_01 lab_02 lab_03 lab_04 lab_05
```

or:

```bash
python scripts/build.py --all
```

may be used when appropriate.

The task is not complete merely because `report.md` exists.

The task is not complete merely because HTML exists.

The task is not complete merely because PDF exists.

Both HTML and PDF are required unless the environment technically prevents one of them from being generated.

Do not delete the HTML after generating the PDF.

Do not delete the PDF after generating the HTML.

---

## Build failure handling

If a build fails:

1. Read the error.
2. Identify whether the problem is:
   - content;
   - Markdown;
   - LaTeX;
   - image path;
   - metadata;
   - template;
   - renderer;
   - dependency;
   - filesystem;
   - encoding;
   - layout.
3. Fix the underlying problem.
4. Rebuild.
5. Verify the result.

Do not report completion after a failed build.

If PDF generation is technically impossible in the current environment but HTML works:

1. preserve the HTML;
2. preserve all source files;
3. clearly state the technical limitation.

Do not pretend that the PDF was generated.

---

## PDF verification

Every generated PDF must be visually inspected.

When multiple works are generated, inspect every PDF independently.

Passing verification for one report does not imply that the remaining reports are valid.

Verify for every PDF:

- correct work number;
- correct topic;
- correct student metadata;
- correct variant;
- correct title page;
- A4 page format;
- consistent margins;
- readable text;
- correct Ukrainian characters;
- headings are not orphaned;
- code is not clipped;
- code font is readable;
- tables fit the page;
- figures fit the page;
- captions match figures;
- formulas render correctly;
- images are not missing;
- no image is unintentionally stretched;
- no accidental blank pages exist;
- no broken page breaks exist;
- no placeholder content remains;
- no obvious spelling errors remain;
- content from another laboratory has not leaked into the current report.

Fix discovered problems before finishing.

After fixes, rebuild and inspect again.

---

## HTML verification

Preserve the generated HTML for every work.

Verify that:

- the document opens correctly;
- headings render correctly;
- tables render correctly;
- formulas render correctly;
- code blocks render correctly;
- images load;
- relative paths are valid;
- Ukrainian characters display correctly;
- no placeholder content remains.

The HTML version is a required final artifact, not merely an intermediate file.

---

## Isolation between works

Independent works must not overwrite or contaminate each other.

For different works:

- keep metadata separate;
- keep reports separate;
- keep code separate;
- keep figures separate;
- keep generated artifacts separate;
- keep HTML separate;
- keep PDF separate.

Do not reuse a result merely because it looks similar.

Reusable implementation code may be shared internally when technically reasonable, but every report must still contain the material required to independently document its own assignment.

---

## Verification of assignment completeness

Before declaring a work complete, compare the final result against the original assignment and against the actual files produced for the work.

A required deliverable is considered complete only when the corresponding artifact exists and has been verified. Mentioning it in `report.md` does not count as completing it.

Check that every required:

- task;
- subtask;
- calculation;
- formula;
- table;
- graph;
- screenshot;
- answer;
- implementation;
- experiment;
- conclusion;
- appendix

has been completed.

Do not assume that a long report is complete.

Completeness is determined by source requirements, not page count.

---

## No fabricated results

Never invent:

- successful program output;
- measurements;
- screenshots;
- test results;
- calculated values;
- experimental observations;
- teacher requirements;
- variant values.

When actual execution is technically possible, execute the implementation.

When actual execution is impossible, clearly distinguish:

- verified results;
- derived results;
- unverified expectations.

Do not present expected output as measured output.

---

## Minimal user effort

The target workflow is:

```text
User provides materials
        ↓
Agent identifies works
        ↓
Agent resolves variants and requirements
        ↓
Agent completes each work
        ↓
Agent creates separate reports
        ↓
Agent builds HTML + PDF for each work
        ↓
Agent verifies every artifact
        ↓
User receives submission-ready files
```

The target workflow is not:

```text
Agent creates draft
        ↓
User copies text into Word
        ↓
User fixes formatting
        ↓
User inserts screenshots
        ↓
User exports PDF
```

Avoid requiring manual work that can reasonably be automated.

---

## Definition of Done — single work

A single independent assignment is complete only when:

1. All relevant source materials have been read.
2. The boundaries of the work have been correctly identified.
3. The correct task has been identified.
4. The correct variant has been identified when required.
5. Every required non-report deliverable has been identified.
6. Required implementation has been completed and exists as actual files.
7. Required implementation has been run or otherwise verified when technically possible.
8. Required calculations have been performed and verified.
9. Required results have been generated from the actual work.
10. Required figures, screenshots, media, datasets, diagrams, or other artifacts have been generated from the actual work.
11. Required tables have been generated.
12. Required formulas have been included.
13. Required control questions have been answered.
14. `report/<work_id>/metadata.yaml` has been generated.
15. `report/<work_id>/report.md` has been generated only after the required work exists.
16. `build/<work_id>.html` has been generated.
17. `build/<work_id>.pdf` has been generated.
18. HTML has been checked.
19. PDF has been visually inspected.
20. Layout problems have been corrected.
21. No placeholder content remains.
22. No unsupported results have been invented.
23. No report claim refers to an implementation, result, screenshot, graph, media file, or experiment that does not actually exist.
24. No content from another work has accidentally leaked into the report.
25. The report reads as an independent student submission.
26. The required non-report deliverables are present and submission-ready.
27. The complete work can be submitted without manual editing.

---

## Definition of Done — multiple works

For a request containing several independent works, the request is complete only when every requested work individually satisfies the single-work Definition of Done.

Example:

If the user requests:

`Зроби лабораторні 1–5.`

the expected result is conceptually:

```text
report/
    lab_01/
        report.md
        metadata.yaml
        code/
        images/

    lab_02/
        report.md
        metadata.yaml
        code/
        images/

    lab_03/
        report.md
        metadata.yaml
        code/
        images/

    lab_04/
        report.md
        metadata.yaml
        code/
        images/

    lab_05/
        report.md
        metadata.yaml
        code/
        images/

build/
    lab_01.html
    lab_01.pdf

    lab_02.html
    lab_02.pdf

    lab_03.html
    lab_03.pdf

    lab_04.html
    lab_04.pdf

    lab_05.html
    lab_05.pdf
```

A single combined file such as:

```text
build/all_labs.pdf
```

does not satisfy the request unless the user explicitly asks for a combined document.

---

## Preferred final response

The final response to the user should be short.

For one work:

```text
Готово.

build/lab_03.pdf
build/lab_03.html
report/lab_03/code/
```

For several works:

```text
Готово.

build/lab_01.pdf
build/lab_01.html

build/lab_02.pdf
build/lab_02.html

build/lab_03.pdf
build/lab_03.html
```

Do not give the user a checklist of remaining manual work when the agent can perform it itself.

Do not describe every internal action unless the user asks.

If something could not be completed because of a real technical limitation, state only the relevant limitation and what artifact was successfully produced.