from pathlib import Path
import importlib.util, os, sys, shutil, tempfile

qa=Path(__file__).resolve().parent
renderer=Path('C:/Users/SSAFY/.codex/plugins/cache/openai-primary-runtime/documents/26.1011.11113/skills/documents/render_docx.py')
spec=importlib.util.spec_from_file_location('packaged_render_docx',renderer)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# The supplied renderer does not bundle LibreOffice on Windows. Use the PDF
# exported by native Word, then retain its canonical DPI, PNG and page pipeline.
docx=qa.parent/'KOG_입사지원서_인쇄용.docx'
pdf=qa/'word-preview-filled.pdf'
assert pdf.exists() and pdf.stat().st_size>0
module.convert_to_pdf=lambda *args,**kwargs:(str(pdf),'Native Word PDF export used on Windows')
tmp=qa/'renderer-temp'
tmp.mkdir(exist_ok=True)
tempfile.tempdir=str(tmp)
os.environ['PATH']='C:/Users/SSAFY/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin'+os.pathsep+os.environ['PATH']
sys.argv=[str(renderer),str(docx),'--output_dir',str(qa/'rendered-filled'),'--verbose']
module.main()
