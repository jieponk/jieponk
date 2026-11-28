// Builds dist/activity.svg: contributions per day for the last 30 days (no third-party service).
// Replaces github-readme-activity-graph.vercel.app, which often fails to render on the profile.
// Usage in CI: GITHUB_TOKEN=... USERNAME=jieponk node scripts/activity.mjs
// Local test:  node scripts/activity.mjs --data calendar.json
import fs from 'node:fs';
import path from 'node:path';

const QUERY = `query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
  weeks{contributionDays{date contributionCount}}}}}}`;

async function load() {
  const i = process.argv.indexOf('--data');
  if (i > -1) return JSON.parse(fs.readFileSync(process.argv[i + 1], 'utf8'));
  const res = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: { Authorization: `bearer ${process.env.GITHUB_TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: QUERY, variables: { login: process.env.USERNAME } })
  });
  const json = await res.json();
  if (!json.data?.user) throw new Error('GitHub API error: ' + JSON.stringify(json.errors || json));
  return json.data.user;
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const label = d => `${Number(d.slice(8, 10))} ${MONTHS[Number(d.slice(5, 7)) - 1]}`;

function render(days) {
  const W = 1200, H = 300, L = 64, R = 28, T = 64, B = 48;
  const max = Math.max(4, ...days.map(d => d.contributionCount));
  const top = Math.ceil(max / 4) * 4;
  const x = i => L + (i * (W - L - R)) / (days.length - 1);
  const y = v => T + (H - T - B) * (1 - v / top);
  const pts = days.map((d, i) => [x(i), y(d.contributionCount)]);
  const line = pts.map(([px, py], i) => `${i ? 'L' : 'M'}${px.toFixed(1)} ${py.toFixed(1)}`).join('');
  const area = `${line}L${x(days.length - 1).toFixed(1)} ${y(0)}L${L} ${y(0)}Z`;
  const total = days.reduce((a, d) => a + d.contributionCount, 0);
  const active = days.filter(d => d.contributionCount > 0).length;
  const grid = [0, 1, 2, 3, 4].map(k => {
    const v = (top / 4) * k, gy = y(v).toFixed(1);
    return `<line x1="${L}" y1="${gy}" x2="${W - R}" y2="${gy}" stroke="#21262d"/><text x="${L - 12}" y="${(+gy + 4).toFixed(1)}" text-anchor="end" class="a">${v}</text>`;
  }).join('');
  const ticks = days.map((d, i) => (i % 5 === 0 || i === days.length - 1)
    ? `<text x="${x(i).toFixed(1)}" y="${H - 20}" text-anchor="middle" class="a">${label(d.date)}</text>` : '').join('');
  const dots = pts.map(([px, py], i) => `<circle cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="3.5" fill="#e6edf3" stroke="#39d353" stroke-width="2"><title>${label(days[i].date)}: ${days[i].contributionCount}</title></circle>`).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="Contributions in the last 30 days: ${total}">
<style>.t{font:700 17px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#e6edf3}.s{font:13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8b949e}.a{font:11px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8b949e}
.draw{stroke-dasharray:4000;stroke-dashoffset:4000;animation:d 2.2s ease-out forwards}@keyframes d{to{stroke-dashoffset:0}}@media (prefers-reduced-motion:reduce){.draw{animation:none;stroke-dashoffset:0}}</style>
<defs><linearGradient id="f" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#39d353" stop-opacity=".35"/><stop offset="1" stop-color="#39d353" stop-opacity="0"/></linearGradient></defs>
<rect x=".5" y=".5" width="${W - 1}" height="${H - 1}" rx="14" fill="#0d1117" stroke="#30363d"/>
<text x="24" y="36" class="t">last 30 days</text>
<text x="${W - 24}" y="36" text-anchor="end" class="s">${total} contributions · ${active}/${days.length} active days</text>
${grid}${ticks}
<path d="${area}" fill="url(#f)"/>
<path d="${line}" class="draw" fill="none" stroke="#39d353" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
${dots}
</svg>`;
}

const user = await load();
const all = user.contributionsCollection.contributionCalendar.weeks.flatMap(w => w.contributionDays);
const days = all.slice(-30);
fs.mkdirSync('dist', { recursive: true });
fs.writeFileSync(path.join('dist', 'activity.svg'), render(days));
console.log('activity.svg:', days.length, 'days');
