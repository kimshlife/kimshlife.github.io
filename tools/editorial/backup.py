"""Back up the current site files before the editorial migration."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import subprocess
import zipfile

root = Path(__file__).resolve().parents[2]
stamp = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y%m%d-%H%M%S")
destination = root / "backups" / f"portfolio-before-editorial-{stamp}.zip"
destination.parent.mkdir(exist_ok=True)
tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
paths = sorted(set(p for p in tracked if p) | {"README.md"})
manifest = {"created_at_kst": stamp, "git_head": subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=root).decode().strip(), "files": {}}
with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED) as archive:
    for name in paths:
        path = root / name
        if not path.is_file():
            continue
        content = path.read_bytes()
        archive.writestr(name, content)
        manifest["files"][name] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
    archive.writestr("BACKUP-MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))
with zipfile.ZipFile(destination) as archive:
    assert archive.testzip() is None
    for name, info in manifest["files"].items():
        assert hashlib.sha256(archive.read(name)).hexdigest() == info["sha256"]
(destination.parent / "복원-안내.txt").write_text(
    f"에디토리얼 디자인 적용 전 백업\n파일: {destination.name}\n"
    f"기존 사이트 파일 {len(manifest['files'])}개를 저장하고 내용의 일치 여부를 검증했습니다.\n\n"
    "복원: ZIP을 별도 폴더에 풀고, BACKUP-MANIFEST.json을 제외한 파일을 사이트 폴더에 덮어씁니다.\n"
    "기존 사이트 파일이 원래 상태로 돌아갑니다. 새로 추가된 상세 페이지는 기존 페이지에서 연결되지 않습니다.\n"
    "백업에는 Git 저장소 내부, 비공개 원본 자료, 이전 작업 결과 폴더는 포함하지 않습니다.\n",
    encoding="utf-8")
print(json.dumps({"path": str(destination), "files": len(manifest["files"]), "bytes": destination.stat().st_size, "verified": True}, ensure_ascii=False))
