const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync('assets/js/spotify.js', 'utf8');

async function render(endpoint, response) {
  const status = { textContent: 'Listening status is unavailable right now.' };
  const link = { hidden: true, href: 'https://open.spotify.com/' };
  const player = { dataset: { endpoint }, querySelector: selector => selector.includes('status') ? status : link };
  let calls = 0;
  const context = { URL, document: { hidden: false, querySelector: () => player }, setInterval() {}, fetch: async () => { calls++; if (response instanceof Error) throw response; return response; } };
  vm.runInNewContext(source, context);
  await new Promise(resolve => setImmediate(resolve));
  return { status, link, calls };
}

test('empty endpoint stays unavailable without a request', async () => {
  const r = await render('', null);
  assert.equal(r.calls, 0);
  assert.match(r.status.textContent, /unavailable/);
});
test('playing track is rendered as text and links to Spotify', async () => {
  const r = await render('https://example.com/playback', { ok: true, json: async () => ({ is_playing: true, item: { name: '<track>', artists: ['Artist'], url: 'https://open.spotify.com/track/123' } }) });
  assert.equal(r.status.textContent, '<track> — Artist');
  assert.equal(r.link.hidden, false);
});
test('inactive playback and failed requests have distinct messages', async () => {
  const inactive = await render('https://example.com/playback', { ok: true, json: async () => ({ is_playing: false }) });
  assert.match(inactive.status.textContent, /Nothing playing/);
  const failed = await render('https://example.com/playback', new Error('offline'));
  assert.match(failed.status.textContent, /unavailable/);
});
test('untrusted track links and insecure endpoints are rejected', async () => {
  const badLink = await render('https://example.com/playback', { ok: true, json: async () => ({ is_playing: true, item: { name: 'Track', artists: [], url: 'https://evil.example/' } }) });
  assert.equal(badLink.link.hidden, true);
  const badEndpoint = await render('http://example.com/playback', null);
  assert.equal(badEndpoint.calls, 0);
});
