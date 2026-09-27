# Math Academy Pipeline

`math-academy.py` is the top-level runner for the Math Academy ingestion and normalization pipeline. It executes five ordered stages:

1. `0-Ingest`
2. `1-Build-Course-Data`
3. `2-Consolidate`
4. `3-Capture`
5. `4-Update`

Together, those stages turn Math Academy's course pages and topic lessons into:

- a global topic graph
- per-course graph views
- normalized lesson source
- global lesson-data indexes
- per-course lesson-data views

## Stage Summary

| Stage | Main Job | Main Outputs |
| --- | --- | --- |
| `0-Ingest` | Capture raw course source from Math Academy | `SOURCE-*` course folders with `TOC`, `Overview`, `Graph`, and `Info` files |
| `1-Build-Course-Data` | Build structured per-course graph data | `DATA/Courses.csv`, `DATA/Course-Maps/*.md`, `Course-Map-*.md`, `GRAPH-*/Units.csv`, `Modules.csv`, `Topics.csv`, `Prerequisites.csv` |
| `2-Consolidate` | Merge per-course graph data into global tables | `DATA/Catalog.csv`, `Units.csv`, `Modules.csv`, `Topics.csv`, `Prerequisites.csv` |
| `3-Capture` | Capture and normalize lesson material per topic | `DATA/Lessons/<topic-id>/...`, `DATA/Lesson-Data/*.csv` |
| `4-Update` | Merge lesson-derived edges and publish per-course lesson views | updated `DATA/Prerequisites.csv`, plus `COURSES/.../LESSONS/*.csv` |

Stage-specific docs:

- [0-Ingest/ingest.md](/home/jake/Developer/MA/PIPELINE/Math-Academy/0-Ingest/ingest.md)
- [1-Build-Course-Data/build-course-data.md](/home/jake/Developer/MA/PIPELINE/Math-Academy/1-Build-Course-Data/build-course-data.md)
- [2-Consolidate/consolidate.md](/home/jake/Developer/MA/PIPELINE/Math-Academy/2-Consolidate/consolidate.md)
- [3-Capture/capture.md](/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/capture.md)
- [4-Update/update.md](/home/jake/Developer/MA/PIPELINE/Math-Academy/4-Update/update.md)

## End-to-End Data Model

The pipeline has three layers of structure:

1. raw captured source
2. normalized graph data
3. normalized lesson data

### 1. Raw Captured Source

Per-course source lives under:

`COURSES/Math-Academy/<Group>/<Course>/SOURCE-<Course>/`

Core files:

- `TOC-<Course>.html`
- `Overview-<Course>.html`
- `Graph-<Course>.html`
- `Info-<Course>.json`

Per-topic lesson source lives under:

`DATA/Lessons/<topic-id>/Source/`

Core files:

- `<topic-id>.html`
- `<topic-id>.json`
- `Sections/*.png`
- `Images/*`

### 2. Normalized Graph Data

Per-course graph data lives under:

`COURSES/Math-Academy/<Group>/<Course>/GRAPH-<Course>/`

Core files:

- `Units.csv`
- `Modules.csv`
- `Topics.csv`
- `Prerequisites.csv`

Global graph data lives under `DATA/`:

- `Courses.csv`
- `Catalog.csv`
- `Units.csv`
- `Modules.csv`
- `Topics.csv`
- `Prerequisites.csv`

### 3. Normalized Lesson Data

Global lesson-data indexes live under:

`DATA/Lesson-Data/`

Core files:

- `Key-Prerequisites.csv`
- `Steps.csv`
- `Questions.csv`

Per-course lesson views live under:

`COURSES/Math-Academy/<Group>/<Course>/LESSONS/`

Core files:

- `Key-Prerequisites.csv`
- `Steps.csv`
- `Questions.csv`

## Canonical Identifiers

The pipeline uses a small set of ids and derived codes repeatedly.

| Field | Meaning | Source |
| --- | --- | --- |
| `course_id` | Math Academy course id | captured from course dialog and `Info-*.json` |
| `course-code` | 3-character shorthand such as `4GM` | assigned in `DATA/Courses.csv` |
| `unit-id` | Math Academy unit id | parsed from TOC HTML |
| `module-id` | Math Academy module id | parsed from TOC HTML |
| `topic-id` | Math Academy topic id | parsed from TOC HTML and reused everywhere |
| `step-id` | lesson section / step id | parsed from topic lesson HTML |
| `question-id` | lesson question id | parsed from topic lesson HTML |

Derived codes are built from course-local numbering:

- `unit-code = <course-code>.<unit-number>`
- `module-code = <course-code>.<module-number>`
- `topic-code = <course-code>.<topic-number>`

Example:

- `4GM` is a course code
- `4GM.1` is a unit code
- `4GM.1.2` is a module code
- `4GM.1.2.3` is a topic code

## Join Keys and Relationships

The single most important key is `topic-id`.

`topic-id` joins:

- per-course graph topics
- global `DATA/Topics.csv`
- global `DATA/Catalog.csv`
- global `DATA/Prerequisites.csv`
- lesson JSON in `DATA/Lessons/<topic-id>/Source/<topic-id>.json`
- global lesson-data tables in `DATA/Lesson-Data/`
- per-course lesson views in `COURSES/.../LESSONS/`

Secondary joins:

- `step-id` joins lesson steps to lesson questions and step-level key prerequisites
- `course-code` embedded in `topic-code`, `module-code`, and `unit-code` maps a graph position back to a course

## Important Schema Rules

### Topics Are Global, Not Course-Local

`DATA/Topics.csv` is deduped by `topic-id`. The same `topic-id` can appear in multiple courses.

That means Math Academy is modeled here as a shared topic graph with multiple course views, not as one isolated graph per course.

### `Catalog.csv` Is a Placement Table

`DATA/Catalog.csv` is not a deduped topic table. It records where a global topic appears in a specific course path:

- `topic-id`
- `topic-code`
- `topic-name`

So a reused topic can appear multiple times in `Catalog.csv` with different `topic-code` values.

### Prerequisites Exist at Two Levels

Global topic prerequisites:

- stored in `DATA/Prerequisites.csv`
- schema: `topic,requires`

Step-level key prerequisites:

- stored in `DATA/Lesson-Data/Key-Prerequisites.csv`
- schema: `topic-id,step-id,requires`

These are different relationships:

- topic-level edges say a topic depends on another topic
- step-level key prerequisites say a specific step assumes another topic

### Per-Course Lesson Data Is Derived

`COURSES/.../LESSONS/*.csv` is not captured independently. It is created by filtering the global lesson-data tables by the course's `GRAPH-*/Topics.csv`.

So the per-course lesson exports are views over global lesson data.

## Core Output Schemas

### Global Graph Tables

`DATA/Courses.csv`

```csv
course-code,course-id,course-name
```

`DATA/Catalog.csv`

```csv
topic-id,topic-code,topic-name
```

`DATA/Units.csv`

```csv
unit-id,unit-code,unit-name
```

`DATA/Modules.csv`

```csv
module-id,module-code,module-name
```

`DATA/Topics.csv`

```csv
topic-id,topic-name
```

`DATA/Prerequisites.csv`

```csv
topic,requires
```

### Global Lesson Tables

`DATA/Lesson-Data/Key-Prerequisites.csv`

```csv
topic-id,step-id,requires
```

`DATA/Lesson-Data/Steps.csv`

```csv
topic-id,step-id,step-name,step-type
```

`DATA/Lesson-Data/Questions.csv`

```csv
topic-id,step-id,question-id,question-type,answer-cardinality
```

## Practical Mental Model

The cleanest way to think about the repository is:

- `Courses.csv` defines course identity
- `Catalog.csv` says where topics appear in courses
- `Topics.csv` and `Prerequisites.csv` define the shared topic graph
- `Lessons/<topic-id>` stores the normalized content for each topic
- `Lesson-Data/*.csv` turns lesson JSON into relational indexes
- `COURSES/.../GRAPH-*` and `COURSES/.../LESSONS/*` are course-specific views over that shared graph and lesson content

## Orchestration

Run the whole pipeline with:

```bash
python PIPELINE/Math-Academy/math-academy.py
```

Or start at a later stage with `--start`, which is parsed and passed down by `math-academy.py` and each stage runner.
