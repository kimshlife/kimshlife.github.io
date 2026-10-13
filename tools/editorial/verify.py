"""Check published local targets, evidence controls, and case-page structure."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

ROOT = Path(__file__).resolve().parents[2]
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path, self.ids, self.links, self.controls = path, [], [], []
        self.h1 = 0
        self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'h1': self.h1 += 1
        if 'aria-controls' in attrs: self.controls.append(attrs['aria-controls'])
        if tag == 'img': assert attrs.get('alt'), (self.path, 'image without alt')
        for attr in ('src', 'href'):
            if attrs.get(attr): self.links.append(attrs[attr])

pages = [Page(path) for role in ('planning', 'qa') for path in (ROOT / role).rglob('index.html')]
by_path = {page.path.resolve():page for page in pages}
checked = 0
for page in pages:
    assert page.h1 == 1, (page.path, 'expected one page heading')
    assert len(page.ids) == len(set(page.ids)), (page.path, 'duplicate ids')
    assert set(page.controls) <= set(page.ids), (page.path, 'missing tab panel')
    base = '/' + page.path.relative_to(ROOT).parent.as_posix() + '/'
    for link in page.links:
        if urlsplit(link).scheme or link.startswith('//'): continue
        target = urlsplit(urljoin(base, link))
        local = ROOT / unquote(target.path.lstrip('/'))
        if target.path.endswith('/'): local /= 'index.html'
        assert local.is_file(), (page.path.relative_to(ROOT), link, 'missing local resource')
        if target.fragment and local.resolve() in by_path:
            assert target.fragment in by_path[local.resolve()].ids, (page.path, link, 'missing anchor')
        checked += 1
assert len(pages) == 10, 'Expected 2 role indexes and 8 case pages'
assert (ROOT/'index.html').read_bytes() == (ROOT/'404.html').read_bytes(), 'Archive entry and fallback differ'
print(f'PASS: {len(pages)} pages; {checked} local image, document, navigation and anchor targets.')
