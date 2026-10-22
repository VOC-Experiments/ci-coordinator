"""Sign the SDK-generated index, once, in the trusted publisher."""
import gzip
import json
import os
from pathlib import Path
import tempfile

from ci.repository import ROOT, digest, run


def sign(directory, info):
    info['unsigned_files'] = info['files'].copy()
    with tempfile.TemporaryDirectory() as temporary:
        key = Path(temporary) / 'key'
        if info['series'] == '24.10':
            key.write_text(os.environ['OPENWRT_USIGN_KEY'])
            key.chmod(0o600)
            index = directory / 'Packages'
            signature = directory / 'Packages.sig'
            run('usign', '-S', '-m', str(index), '-s', str(key), '-x', str(signature))
            run('usign', '-V', '-m', str(index), '-p', str(ROOT / 'keys/opkg.pub'), '-x', str(signature))
            info['files']['Packages.sig'] = digest(signature)
        else:
            key.write_text(os.environ['OPENWRT_APK_KEY'])
            key.chmod(0o600)
            index = directory / 'packages.adb'
            run('apk', 'adbsign', '--allow-untrusted', '--sign-key', str(key), str(index))
            run('apk', 'verify', '--keys-dir', str(ROOT / 'keys'), str(index))
            info['files']['packages.adb'] = digest(index)
    (directory / 'build.json').write_text(json.dumps(info, indent=2) + '\n')


def reindex(directory, previous, info):
    """Rebase retained products without recompiling or changing captured dependencies."""
    if info['series'] == '24.10':
        paragraphs = {}
        for path in (directory / 'Packages', previous / 'Packages'):
            if path.exists():
                for paragraph in path.read_text().strip().split('\n\n'):
                    fields = dict(line.split(': ', 1) for line in paragraph.splitlines() if ': ' in line)
                    filename = fields.get('Filename', '').removeprefix('./')
                    if filename in info['files']:
                        paragraphs.setdefault(filename, paragraph)
        data = ('\n\n'.join(paragraphs[name] for name in sorted(paragraphs)) + '\n\n').encode()
        (directory / 'Packages').write_bytes(data)
        (directory / 'Packages.gz').write_bytes(gzip.compress(data, mtime=0))
        indexes = ['Packages', 'Packages.gz']
    else:
        run('apk', 'mkndx', '--allow-untrusted', '--output', str(directory / 'packages.adb'),
            *(str(path) for path in sorted(directory.glob('*.apk'))))
        indexes = ['packages.adb']
    for name in indexes:
        info['files'][name] = digest(directory / name)
    return None
