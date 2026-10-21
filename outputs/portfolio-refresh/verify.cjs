const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const cp = require('node:child_process');
const root = path.resolve(__dirname, '../..');
const errors = [];
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
// /portfolio/ is being reviewed by others: keep its page and shared inputs intact.
const protectedCheck = cp.spawnSync('git', ['-c','core.autocrlf=false','diff','--quiet','HEAD','--','portfolio','assets/js/data.js','assets/img/og.png','assets/img/profile.jpg','assets/brand'], { cwd:root });
if (protectedCheck.status !== 0) errors.push('Protected /portfolio/ page or its shared inputs have changed.');
const data = vm.runInNewContext(read('assets/js/data.js') + '\n' + read('assets/js/journal-data.js') + '\n({ JOURNAL, JOURNAL_ORDER, JOURNAL_AWARDS })');
let checkedAssets = 0;
function checkAsset(ref, origin = 'index.html') {
  if (/^(https?:|mailto:|tel:|data:)/.test(ref) || ref.startsWith('#')) return;
  const url = new URL(ref, 'https://portfolio.local/' + origin);
  const file = path.join(root, decodeURIComponent(url.pathname));
  if (!fs.existsSync(file)) errors.push('Missing local reference: ' + ref + ' in ' + origin);
  checkedAssets++;
}
const html = read('index.html');
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
if (new Set(ids).size !== ids.length) errors.push('Duplicate HTML IDs');
if (html !== read('404.html')) errors.push('index.html and 404.html differ');
for (const file of ['index.html','404.html','portfolio/index.html','planning/index.html','qa/index.html','funqa/index.html']) {
  for (const [,ref] of read(file).matchAll(/(?:src|href)="([^"]+)"/g)) checkAsset(ref, file);
}
for (const [,href] of html.matchAll(/href="(#[^"]+)"/g)) {
  if (href.startsWith('#/works/')) {
    if (!Object.hasOwn(data.JOURNAL, href.split('/')[2])) errors.push('Missing project: ' + href);
  } else if (!ids.includes(href.slice(1))) errors.push('Missing section: ' + href);
}
for (const [key,project] of Object.entries(data.JOURNAL)) {
  if (!project.intro || !project.tasks.length || !project.stories.length) errors.push('Incomplete project: ' + key);
  if (project.cover) checkAsset(project.cover);
  for (const story of project.stories) if (story.image) checkAsset(story.image);
  for (const link of project.links || []) if (link.href) checkAsset(link.href);
}
for (const key of data.JOURNAL_ORDER) if (!Object.hasOwn(data.JOURNAL,key)) errors.push('Missing navigation project: ' + key);
if (errors.length) { console.error(errors.join('\n')); process.exitCode = 1; }
else console.log(JSON.stringify({ projects:Object.keys(data.JOURNAL).length, awards:data.JOURNAL_AWARDS.length, localReferences:checkedAssets, identical404:true, status:'passed' }));
