// Builds dist/trophies.svg from real GitHub stats (no third-party service).
// Usage in CI: GITHUB_TOKEN=... USERNAME=jieponk node scripts/trophy.mjs
// Local test:  node scripts/trophy.mjs --data stats.json
import fs from 'node:fs';
import path from 'node:path';

const QUERY = `query($login:String!){user(login:$login){
  createdAt followers{totalCount}
  repositories(ownerAffiliations:OWNER,privacy:PUBLIC,first:100){totalCount nodes{stargazerCount}}
  pullRequests{totalCount} issues{totalCount}
  repositoriesContributedTo(contributionTypes:[COMMIT,PULL_REQUEST,ISSUE,REPOSITORY]){totalCount}
  contributionsCollection{totalCommitContributions restrictedContributionsCount contributionCalendar{totalContributions}}
}}`;

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
  return json;
}

const RANKS = ['C', 'B', 'A', 'AA', 'S', 'SS', 'SSS'];
const COLORS = { C: '#8b949e', B: '#4ec9b0', A: '#58a6ff', AA: '#bf91f3', S: '#ffa657', SS: '#ffd166', SSS: '#ffe599' };

function rankOf(value, steps) {
  let r = -1;
  steps.forEach((s, i) => { if (value >= s) r = i; });
  const next = steps[r + 1];
  const prev = r >= 0 ? steps[r] : 0;
  const progress = next === undefined ? 1 : Math.max(0, Math.min(1, (value - prev) / (next - prev)));
  return { rank: r >= 0 ? RANKS[r] : null, next, progress };
}

const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const fmt = n => n >= 1000 ? (n / 1000).toFixed(n >= 10000 ? 0 : 1) + 'k' : String(n);

function cup(x, y, color, locked) {
  const c = locked ? '#30363d' : color;
  return `<g transform="translate(${x},${y})" fill="${c}">
    <path d="M10 2h24v10c0 7-5 12-12 12S10 19 10 12z"/>
    <path d="M10 5H4v4c0 5 3 8 7 8v-3c-2 0-4-2-4-5V8h3zM34 5h6v4c0 5-3 8-7 8v-3c2 0 4-2 4-5V8h-3z"/>
    <rect x="19" y="24" width="6" height="6"/><rect x="13" y="30" width="18" height="5" rx="1.5"/>
    ${locked ? '' : '<path d="M22 7l1.6 3.3 3.6.5-2.6 2.5.6 3.6-3.2-1.7-3.2 1.7.6-3.6-2.6-2.5 3.6-.5z" fill="#0d1117" opacity=".55"/>'}
  </g>`;
}

function render(user) {
  const cc = user.contributionsCollection;
  const stars = user.repositories.nodes.reduce((a, r) => a + r.stargazerCount, 0);
  const years = (Date.now() - new Date(user.createdAt)) / (365.25 * 864e5);
  const items = [
    ['Commits', 'last 12 months', cc.totalCommitContributions + cc.restrictedContributionsCount, [1, 10, 50, 100, 250, 500, 1000]],
    ['Contributions', 'last 12 months', cc.contributionCalendar.totalContributions, [1, 50, 100, 250, 500, 1000, 2000]],
    ['Repositories', 'public', user.repositories.totalCount, [1, 5, 10, 20, 30, 50, 100]],
    ['Stars', 'earned', stars, [1, 5, 10, 30, 50, 100, 200]],
    ['Pull Requests', 'opened', user.pullRequests.totalCount, [1, 5, 10, 20, 50, 100, 200]],
    ['Issues', 'opened', user.issues.totalCount, [1, 5, 10, 20, 50, 100, 200]],
    ['Followers', 'on GitHub', user.followers.totalCount, [1, 5, 10, 20, 50, 100, 200]],
    ['Experience', 'years on GitHub', Math.floor(years * 10) / 10, [1, 2, 3, 4, 5, 7, 10]]
  ];
  const W = 205, H = 118, GAP = 12, COLS = 4;
  const width = COLS * W + (COLS - 1) * GAP, height = 2 * H + GAP;
  const cards = items.map(([title, sub, value, steps], i) => {
    const { rank, next, progress } = rankOf(value, steps);
    const color = rank ? COLORS[rank] : '#484f58';
    const x = (i % COLS) * (W + GAP), y = Math.floor(i / COLS) * (H + GAP);
    const val = title === 'Experience' ? value.toFixed(1) : fmt(value);
    const nextTxt = next === undefined ? 'max rank' : `next: ${fmt(next)}`;
    return `<g transform="translate(${x},${y})" class="card" style="animation-delay:${i * 90}ms">
      <rect width="${W}" height="${H}" rx="10" fill="#0d1117" stroke="#30363d"/>
      ${cup(14, 16, color, !rank)}
      <text x="66" y="30" class="t">${esc(title)}</text>
      <text x="66" y="47" class="s">${esc(sub)}</text>
      <text x="66" y="78" class="v" fill="${color}">${esc(val)}</text>
      <text x="${W - 14}" y="30" class="r" fill="${color}" text-anchor="end">${rank || '?'}</text>
      <rect x="14" y="${H - 24}" width="${W - 28}" height="5" rx="2.5" fill="#21262d"/>
      <rect x="14" y="${H - 24}" width="${((W - 28) * progress).toFixed(1)}" height="5" rx="2.5" fill="${color}" class="bar"/>
      <text x="${W - 14}" y="${H - 6}" class="n" text-anchor="end">${esc(nextTxt)}</text>
    </g>`;
  }).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-label="GitHub trophies">
<style>
  text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
  .t{font-size:14px;font-weight:700;fill:#e6edf3}.s{font-size:11px;fill:#8b949e}
  .v{font-size:24px;font-weight:800}.r{font-size:20px;font-weight:900}.n{font-size:10px;fill:#8b949e}
  .card{opacity:0;animation:in .5s ease forwards}
  @keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1}}
</style>
${cards}
</svg>`;
}

function renderStats(user) {
  const cc = user.contributionsCollection;
  const stars = user.repositories.nodes.reduce((a, r) => a + r.stargazerCount, 0);
  const m = [
    ['commits', cc.totalCommitContributions + cc.restrictedContributionsCount, '#39d353', 'last 12 months'],
    ['contributions', cc.contributionCalendar.totalContributions, '#58a6ff', 'last 12 months'],
    ['pull requests', user.pullRequests.totalCount, '#bf91f3', 'all time'],
    ['issues', user.issues.totalCount, '#ffa657', 'all time'],
    ['stars', stars, '#ffd166', 'earned'],
    ['contributed to', user.repositoriesContributedTo.totalCount, '#4ec9b0', 'repositories']
  ];
  const cols = m.map(([k, v, c, sub], i) => {
    const x = 40 + i * 188;
    return `<g class="col" style="animation-delay:${i * 120}ms">
      <text x="${x}" y="108" class="v" fill="${c}">${esc(fmt(v))}</text>
      <text x="${x}" y="134" class="k">${esc(k)}</text>
      <text x="${x}" y="152" class="s">${esc(sub)}</text>
      <rect x="${x}" y="166" width="150" height="3" rx="1.5" fill="#21262d"/>
      <rect x="${x}" y="166" width="150" height="3" rx="1.5" fill="${c}" class="bar" style="animation-delay:${i * 120}ms"/>
    </g>`;
  }).join('');
  const L = `<circle cx="22" cy="17" r="6" fill="#ff5f57"/><circle cx="42" cy="17" r="6" fill="#febc2e"/><circle cx="62" cy="17" r="6" fill="#28c840"/>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="196" viewBox="0 0 1200 196" role="img" aria-label="GitHub stats">
<style>
  text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}
  .v{font-size:38px;font-weight:800}.k{font-size:14px;font-weight:700;fill:#e6edf3}.s{font-size:11.5px;fill:#8b949e}
  .bar{transform-box:fill-box;transform-origin:left;animation:grow 1.2s ease-out both}
  @keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
  .blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>
<rect x=".5" y=".5" width="1199" height="195" rx="14" fill="#0d1117" stroke="#30363d"/>
<path d="M14.5 .5h1171a14 14 0 0 1 14 14V34H.5V14.5a14 14 0 0 1 14-14z" fill="#161b22"/>
<line x1="0" y1="34" x2="1200" y2="34" stroke="#30363d"/>${L}
<text x="600" y="22" text-anchor="middle" font-size="12.5" fill="#8b949e">gh api users/${esc(process.env.USERNAME || 'jieponk')} — live stats</text>
<text x="1176" y="22" text-anchor="end" font-size="11" fill="#6a9955">updated ${new Date().toISOString().slice(0, 10)}</text>
<text x="40" y="62" font-size="13"><tspan fill="#39d353">❯</tspan><tspan fill="#e6edf3"> stats --summary</tspan></text>
<rect class="blink" x="180" y="51" width="8" height="15" fill="#39d353"/>
${cols}
</svg>`;
}

const json = await load();
const out = path.resolve('dist/trophies.svg');
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, render(json.data.user));
fs.writeFileSync(path.resolve('dist/stats.svg'), renderStats(json.data.user));
console.log('Wrote', out);
