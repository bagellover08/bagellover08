(() => {
  const player = document.querySelector('[data-spotify-player]');
  if (!player) return;
  const status = player.querySelector('[data-spotify-status]');
  const link = player.querySelector('[data-spotify-link]');
  const endpoint = player.dataset.endpoint;
  if (!endpoint) return;

  let url;
  try {
    url = new URL(endpoint);
    if (url.protocol !== 'https:') return;
  } catch { return; }

  async function update() {
    try {
      const response = await fetch(url, { credentials: 'omit', cache: 'no-store' });
      if (!response.ok) throw new Error('Playback unavailable');
      const data = await response.json();
      link.hidden = true;
      if (!data.is_playing || !data.item) {
        status.textContent = 'Nothing playing right now.';
        return;
      }
      const artists = Array.isArray(data.item.artists) ? data.item.artists.filter(a => typeof a === 'string').join(', ') : '';
      status.textContent = [data.item.name, artists].filter(Boolean).join(' — ');
      try {
        const track = new URL(data.item.url);
        if (track.protocol === 'https:' && track.hostname === 'open.spotify.com') {
          link.href = track.href;
          link.hidden = false;
        }
      } catch { /* A track link is optional. */ }
    } catch {
      status.textContent = 'Listening status is unavailable right now.';
      link.hidden = true;
    }
  }
  update();
  setInterval(() => { if (!document.hidden) update(); }, 60000);
})();
