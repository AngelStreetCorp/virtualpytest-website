"""Lane test for the website repo (run: python3 -m pytest tests -q). The lane runs it on the merged tree before it
pushes master, and Vercel deploys master, so this is the last gate before the live site."""
import json, pathlib, shutil, subprocess, sys
import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import learn_fit  # noqa: E402


def test_json_files_parse():
    for p in [ROOT / 'locales.json', ROOT / 'vercel.json', *(ROOT / 'learn' / 'i18n').glob('*.json')]:
        json.loads(p.read_text(encoding='utf-8'))


def test_tools_compile():
    subprocess.run([sys.executable, '-m', 'py_compile', str(ROOT / 'tools' / 'learn_fit.py')], check=True)


def test_every_lesson_fits_a_phone():
    ids, tall, wrap, broken, errs = learn_fit.check(str(ROOT))
    assert len(ids) >= 50
    assert not tall, f'lessons too tall for 390x740 (px over): {tall}'
    assert not wrap, f'titles on two lines: {wrap}'
    assert not broken and not errs, f'card errors: {broken} {errs}'


def test_too_tall_lesson_fails(tmp_path):
    """The check must be able to fail: one lesson gets 400 px of extra text, only that one is reported."""
    site = tmp_path / 'site'
    shutil.copytree(ROOT, site, ignore=shutil.ignore_patterns('.git', 'node_modules', '__pycache__', '.pytest_cache'))
    page = site / 'learn' / 'index.html'
    inject = ("<script>addEventListener('hashchange',()=>setTimeout(()=>{"
              "document.querySelectorAll('.xtall').forEach(e=>e.remove());if(location.hash==='#3.5'){"
              "const d=document.createElement('div');d.className='xtall';d.style.height='400px';"
              "document.querySelector('aside.panel .body').appendChild(d)}},50))</script></body>")
    html = page.read_text(encoding='utf-8')
    assert '</body>' in html
    page.write_text(html.replace('</body>', inject, 1), encoding='utf-8')
    ids, tall, wrap, broken, errs = learn_fit.check(str(site))
    assert list(tall) == ['3.5'], tall
    assert tall['3.5'] > 300
    assert learn_fit.main([str(site)]) == 1


def test_short_viewport_fails_everything():
    ids, tall, *_ = learn_fit.check(str(ROOT), vh=500)
    assert len(tall) == len(ids)
