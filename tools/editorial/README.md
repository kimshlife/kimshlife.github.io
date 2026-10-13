# Editorial portfolio

The two role indexes and eight case pages are static HTML, so each case can be linked directly on GitHub Pages. Full source records, images, PDFs, contribution boundaries, and former hash links are retained.

Edit `portfolio.json` to change case copy or detailed records, then run:

```sh
python tools/editorial/build.py
```

Styling is in `assets/css/editorial.css`. `assets/js/editorial.js` enhances evidence tabs and redirects former case anchors. All case copy is readable without JavaScript. The entry-page markup is in `viewSelect()` in `assets/js/app.js`; profile facts still come from `SELECT.sheet` in `assets/js/data.js`.

After updating root metadata or asset versions, copy `index.html` to `404.html`, as required by the existing archive router.

`import-content.cjs` and `import-records.py` were used once to migrate the reviewed prototype and the former detailed case copy. Do not run them against the new indexes. Future builds use only `portfolio.json`.

Local backups live in `backups/`, which is ignored by Git. Before a future migration, `python tools/editorial/backup.py` saves and verifies a new snapshot of the current tracked site files. It never changes the site or the Git history.
