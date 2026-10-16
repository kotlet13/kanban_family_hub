#!/usr/bin/env python3
"""Build a source-only installation ZIP from the explicitly reviewed manifest."""
import argparse
import hashlib
import json
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name('runtime-manifest.json')


def collect():
    names = json.loads(MANIFEST.read_text())
    if not isinstance(names, list) or len(names) != len(set(names)):
        raise ValueError('Invalid runtime manifest')
    entries = {}
    for name in names:
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or str(relative) != name:
            raise ValueError('Invalid runtime path')
        if name not in ['Plugin.php', 'LICENSE', 'README.md', 'NOTICE.md', 'CHANGELOG.md', 'DOCUMENTS_API.md'] and not name.startswith(('Api/', 'Controller/', 'Model/', 'Schema/', 'Template/', 'cli/', 'docs/')):
            raise ValueError('Unapproved runtime path')
        path = ROOT / name
        if path.is_symlink() or not stat.S_ISREG(path.stat().st_mode) or path.stat().st_size > 2 * 1024 * 1024:
            raise ValueError('Runtime input must be a bounded regular file')
        if ROOT not in path.resolve().parents:
            raise ValueError('Runtime input outside repository')
        data = path.read_bytes()
        text = data.decode('utf-8')
        if '\x00' in text or re.search(r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|"type"\s*:\s*"service_account"|\b(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_]{20,}', text):
            raise ValueError('Credential-like input refused; no value printed')
        entries[name] = data
    expected_php = {n for n in names if n.endswith('.php')}
    actual_php = {p.relative_to(ROOT).as_posix() for prefix in ['Api','Controller','Model','Schema','Template','cli'] for p in (ROOT/prefix).rglob('*.php')}
    actual_php.add('Plugin.php')
    if actual_php != expected_php:
        raise ValueError('Review added or missing PHP files in the manifest')
    license_text = entries['LICENSE'].decode('utf-8')
    if not all(s in license_text for s in ['MIT License','Copyright (c)','Permission is hereby granted, free of charge','THE SOFTWARE IS PROVIDED "AS IS"']):
        raise ValueError('Confirmed MIT license required')
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'dist/FamilyHub-0.15.0.zip')
    args = parser.parse_args()
    entries = collect()
    destination = args.output.absolute()
    if destination.exists() or destination.with_suffix(destination.suffix+'.sha256').exists():
        raise ValueError('Existing outputs are never overwritten')
    destination.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(destination,'x',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(entries.items()):
            info=zipfile.ZipInfo('FamilyHub/'+name,(2026,10,16,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,data)
    with zipfile.ZipFile(destination) as z:
        if z.testzip() is not None or len(z.namelist()) != len(entries):
            raise ValueError('Archive verification failed')
        for name,data in entries.items():
            if z.read('FamilyHub/'+name) != data:
                raise ValueError('Archive bytes differ from reviewed source')
    digest=hashlib.sha256(destination.read_bytes()).hexdigest()
    destination.with_suffix(destination.suffix+'.sha256').write_text(digest+'  '+destination.name+'\n')
    print(f'Verified {len(entries)} public runtime files. SHA256 {digest}')


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError,UnicodeError,KeyError,TypeError) as e:
        print('Package refused: '+str(e))
        raise SystemExit(1)
