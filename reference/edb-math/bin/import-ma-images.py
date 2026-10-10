#!/usr/bin/env python3
"""Copy referenced MA lesson images into byte-preserving SHA-256 storage."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp', '.avif'}


def image_sources(value):
    if isinstance(value, dict):
        if isinstance(value.get('src'), str):
            yield value['src']
        for item in value.values():
            yield from image_sources(item)
    elif isinstance(value, list):
        for item in value:
            yield from image_sources(item)


def image_lookup(image_dir):
    result = {}
    metadata = image_dir / '_image_meta.json'
    if metadata.is_file():
        for row in json.loads(metadata.read_text()).get('images', []):
            if isinstance(row, dict) and row.get('img_src') and row.get('filename'):
                path = image_dir / row['filename']
                if not path.resolve().is_relative_to(image_dir.resolve()):
                    raise ValueError(f'Image metadata points outside its image directory: {path}')
                if path.is_file():
                    result[row['img_src']] = path
    return result


def resolve_source(src, image_dir, lookup):
    if src in lookup:
        return lookup[src]
    stem = Path(src).name
    if not stem:
        return None
    candidates = sorted(path for path in image_dir.iterdir()
                        if path.is_file() and path.name.startswith(stem + '.')
                        and path.suffix.lower() in IMAGE_EXTENSIONS) if image_dir.is_dir() else []
    if not candidates:
        return None
    if len(candidates) > 1:
        raise ValueError(f'Ambiguous image reference: {image_dir} / {src}')
    return candidates[0]


def write_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def import_images(lessons_root, math_root):
    image_root = math_root / 'images'
    image_root.mkdir(parents=True, exist_ok=True)
    by_source_path = {}
    by_topic = {}
    unique_images = {}
    missing = []
    copied = 0
    source_bytes = 0
    json_files = sorted(lessons_root.glob('*/Source/*.json'), key=lambda path: int(path.stem))
    for number, json_path in enumerate(json_files, 1):
        data = json.loads(json_path.read_text())
        topic_id = str(data['topic_id'])
        assert topic_id == json_path.stem
        image_dir = json_path.parent / 'Images'
        lookup = image_lookup(image_dir)
        references = {}
        for src in sorted(set(image_sources(data['lesson']))):
            source = resolve_source(src, image_dir, lookup)
            if source is None:
                missing.append({'topic_id': topic_id, 'src': src})
                continue
            original_path = str(source.resolve())
            if original_path in by_source_path:
                references[src] = by_source_path[original_path]
                continue
            content = source.read_bytes()
            if source.suffix.lower() == '.png' and not content.startswith(b'\x89PNG\r\n\x1a\n'):
                raise ValueError(f'PNG filename contains non-PNG bytes: {source}')
            digest = hashlib.sha256(content).hexdigest()
            extension = source.suffix.lower()
            if extension == '.jpeg':
                extension = '.jpg'
            relative = Path('images') / digest[:2] / (digest + extension)
            destination = math_root / relative
            if destination.exists():
                if destination.read_bytes() != content:
                    raise ValueError(f'Existing hashed file has different bytes: {destination}')
            else:
                write_atomic(destination, content)
                copied += 1
            by_source_path[original_path] = relative.as_posix()
            references[src] = relative.as_posix()
            unique_images[relative.as_posix()] = len(content)
            source_bytes += len(content)
        if references:
            by_topic[topic_id] = references
        if number % 500 == 0:
            print(f'Processed {number}/{len(json_files)} lesson JSON files; {len(unique_images)} unique images.', flush=True)
    counts = {'lesson_json_files': len(json_files),
              'references': sum(len(items) for items in by_topic.values()),
              'source_files': len(by_source_path), 'unique_images': len(unique_images),
              'copied_this_run': copied, 'source_bytes': source_bytes,
              'stored_bytes': sum(unique_images.values()), 'missing_references': len(missing)}
    mapping = {'format_version': 1, 'hash_algorithm': 'sha256',
               'lessons_root': str(lessons_root), 'math_root': str(math_root),
               'counts': counts, 'by_source_path': by_source_path,
               'by_topic': by_topic, 'missing': missing}
    map_path = image_root / 'math-academy-map.json'
    write_atomic(map_path, (json.dumps(mapping, indent=2, ensure_ascii=False) + '\n').encode())
    print(json.dumps(counts), flush=True)
    print(f'Mapping: {map_path}', flush=True)
    if missing:
        raise SystemExit('Some referenced images are missing; see the mapping before importing lessons.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lessons-root', type=Path, default=Path('/home/jake/Developer/MA/DATA/Lessons'))
    parser.add_argument('--math-root', type=Path, default=Path('/media/jake/SSD/EDB/math'))
    args = parser.parse_args()
    import_images(args.lessons_root.resolve(), args.math_root.resolve())


if __name__ == '__main__':
    main()
