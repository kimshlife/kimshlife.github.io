// One-time import of the reviewed editorial copy. Subsequent edits use portfolio.json.
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(process.argv[2], 'utf8');
const match = source.match(/const work=(\{[\s\S]*?\});\s*let ui=/);
if (!match) throw new Error('Reviewed portfolio data not found');
const work = vm.runInNewContext(`(${match[1]})`, Object.create(null), {timeout:1000});
fs.writeFileSync(path.join(__dirname, 'portfolio.json'), JSON.stringify(work, null, 2) + '\n');
