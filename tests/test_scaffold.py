"""Run: python tests/test_scaffold.py <scratch directory>. No cloud access. Repo-level test, not shipped inside the skill."""
import json
import os
GIT = os.environ.get('GIT_EXE', 'git')
import subprocess
import sys
import tempfile
from pathlib import Path

script = Path(__file__).resolve().parents[1] / 'skills' / 'company-brain-starter' / 'scripts' / 'scaffold_brain.py'
base = Path(sys.argv[1]).resolve()
with tempfile.TemporaryDirectory(prefix='brain-test-', dir=base) as temp:
    root = Path(temp)
    answers = root / 'answers.json'
    answers.write_text(json.dumps(dict(business_name='Sunny Day Landscaping', what_sells='Lawn care', serves='Homeowners', clients=['Maple HOA', 'Rivera Family'], personal=True, cloud='google-drive', users='just-me', goals=['Spring campaign', 'Referral offer', 'Hire crew'], tools={'email':'Gmail'})))
    parent = root / 'Documents'
    def cmd(*args):
        return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)
    args = ['--answers', str(answers), '--parent', str(parent)]
    assert cmd('plan', *args).returncode == 0
    assert not parent.exists(), 'Plan created folders'
    assert cmd('build', *args).returncode != 0
    assert not parent.exists(), 'Unapproved build created folders'
    assert cmd('build', *args, '--approved').returncode == 0
    brain = parent / 'Company Brain'
    subprocess.run([GIT, 'init', '-q', str(brain)], check=True)
    for name in ['dummy.mp4', 'dummy.pdf', '.env']:
        (brain / name).write_text('dummy')
        r = subprocess.run([GIT, '-C', str(brain), 'check-ignore', '-v', name], capture_output=True, text=True)
        assert r.returncode == 0
        print(r.stdout.strip())
    (brain / 'oversized.md').write_bytes(b'x' * (6 * 1024 * 1024))
    assert cmd('check', '--brain', str(brain)).returncode != 0
    export = root / 'snapshot'
    assert cmd('export', '--brain', str(brain), '--destination', str(export)).returncode == 0
    assert not any((export / n).exists() for n in ['dummy.mp4', 'dummy.pdf', '.env', 'oversized.md'])
    assert (export / 'brain/business/overview.md').exists()
    pointers = list((brain / 'workspace').rglob('README.md'))
    assert len(pointers) == 8
    for p in pointers:
        rel = p.parent.relative_to(brain / 'workspace')
        assert f'Deliverables/{rel.as_posix()}/' in p.read_text()
        assert (parent / 'Deliverables' / rel).is_dir()
    print('PASS: plan writes nothing; unapproved build blocked; 8 pointers; Git ignores; export excludes media, secrets and 6 MB note.')
print('PASS: scratch test deleted.')
