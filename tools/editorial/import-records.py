"""One-time import of the existing, detailed source records, with neutral markup."""
from html.parser import HTMLParser
from html import escape
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import json

ROOT = Path(__file__).resolve().parents[2]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
ALIASES = {"planning": {"ssketch": "ssketch", "workshop": "bodybuilder", "projectrg": "projectrg", "neontetris": "neontetris"},
           "qa": {"ssketch": "ssketch", "bodybuilder": "bodybuilder", "reference": "reference", "counterside": "counterside"}}

class Element:
    def __init__(self, tag, attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []
    def find(self, predicate):
        return next((n for n in self.all() if predicate(n)), None)
    def all(self):
        for child in self.children:
            if isinstance(child, Element):
                yield child
                yield from child.all()
    def has(self, name):
        return name in self.attrs.get("class", "").split()
    def text(self):
        return "".join(c.text() if isinstance(c, Element) else c for c in self.children)

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Element("root")
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        n = Element(tag, attrs)
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.stack.pop()
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                return
    def handle_data(self, data):
        self.stack[-1].children.append(data)

def internal_url(value, role):
    if value.startswith(("https:", "http:", "mailto:", "data:")):
        return value
    parsed = urlsplit(urljoin(f"https://kimshlife.github.io/{role}/", value))
    if parsed.path.strip("/") in ALIASES and parsed.fragment in ALIASES[parsed.path.strip("/")]:
        job = parsed.path.strip("/")
        return f"/{job}/{ALIASES[job][parsed.fragment]}/"
    return parsed.path + ("?" + parsed.query if parsed.query else "") + ("#" + parsed.fragment if parsed.fragment else "")

def markup(node, role):
    if isinstance(node, str):
        return escape(node)
    attrs = {k:v for k,v in node.attrs.items() if k not in {"style", "class", "id"}}
    for field in ("href", "src"):
        if field in attrs:
            attrs[field] = internal_url(attrs[field], role)
    mapping = {"thumbs":"ed-gallery", "docs":"ed-doc-links", "src":"ed-caption", "muted":"ed-muted", "t":"ed-table"}
    classes = [new for old,new in mapping.items() if node.has(old)]
    if classes:
        attrs["class"] = " ".join(classes)
    if node.tag == "img":
        attrs["loading"] = "lazy"
    if node.tag == "a" and attrs.get("target") == "_blank":
        attrs["rel"] = "noopener noreferrer"
    attr = "".join(f' {k}="{escape(v or "", quote=True)}"' for k,v in attrs.items())
    inner = "".join(markup(c, role) for c in node.children)
    return f"<{node.tag}{attr}>" + ("" if node.tag in VOID else inner + f"</{node.tag}>")

data_path = Path(__file__).with_name("portfolio.json")
data = json.loads(data_path.read_text(encoding="utf-8"))
for role in ("planning", "qa"):
    parser = Parser()
    parser.feed((ROOT / role / "index.html").read_text(encoding="utf-8"))
    for case in data[role]:
        alias = next(old for old,new in ALIASES[role].items() if new == case["id"])
        article = parser.root.find(lambda n: n.tag == "article" and n.attrs.get("id") == alias)
        assert article, (role, alias)
        case["records"] = []
        for step in (n for n in article.all() if n.has("d-step")):
            title = step.find(lambda n: n.tag == "h4")
            heading = "".join(c.text() if isinstance(c, Element) else c for c in title.children if not (isinstance(c, Element) and c.tag == "small")).strip()
            content = "".join(markup(c, role) for c in step.children if c is not title)
            case["records"].append({"title": heading, "html": content})
        body = article.find(lambda n: n.has("more-body"))
        case["resourceHtml"] = "".join(markup(c, role) for c in body.children if isinstance(c, Element) and c.tag == "p")
        # Tables that carry evidence before the expanded source records.
        grid = article.find(lambda n: n.has("case-grid"))
        case["overviewTables"] = [markup(n, role) for n in grid.all() if n.tag == "table"] if grid else []
data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Imported detailed records:", sum(len(c["records"]) for cases in data.values() for c in cases))
