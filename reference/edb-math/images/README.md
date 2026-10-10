# Images

Supporting documentation is stored under `/home/jake/Developer/Course_Academy/reference/edb-math`. Database files, images, schema, seeds, and prepared transaction EDNs remain under `/media/jake/SSD/EDB/math`; relative data paths below refer to that database folder.

Image files are stored as `<first-two-sha256-characters>/<full-sha256>.<extension>`. The SHA-256 digest is calculated from the exact file bytes. Identical image bytes reuse one stored file. Images are copied without conversion or resizing.

Database content should reference `images/<prefix>/<hash>.<extension>`, relative to the math directory. The application resolves that path against the math directory; Markdown files exported elsewhere need their image links resolved for that destination.

`math-academy-map.json` maps original absolute image paths and topic-specific MA `src` references to the stored relative paths. Use it when rendering lesson JSON into database content. It also records counts and any missing references.

The import script is `../bin/import-ma-images.py`. Its default input is `/home/jake/Developer/MA/DATA/Lessons/*/Source/*.json`; it copies only referenced lesson images. Section screenshots, PDFs, JSON, and Markdown are not copied here. Original image files are retained. Rerunning the script verifies image content and reuses existing stored files.

No image entities or schema changes are required, and copying images does not transact lesson content.
