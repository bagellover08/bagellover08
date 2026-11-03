# bagellover08

A small Jekyll website and digital garden. The text and notes are examples: make them yours!

## Run locally

You need Ruby, RubyGems, and Bundler. From a terminal:

```sh
cd /Users/masonmiller/code/bagellover08
bundle install
bundle exec jekyll serve
```

Open the local address printed by Jekyll, usually <http://localhost:4000>. Stop the server with Ctrl+C. `bundle install` installs project dependencies; it does not deploy your site. If your system Ruby is too old for a dependency or your system gem directory is not writable, use a current Ruby managed in your user account and try again. Jekyll 3.9 is selected for compatibility with older Ruby; your Ruby installation may still require additional setup. Restart the server after editing `_config.yml`.

## Make it yours

- The main editable pages are grouped in `pages/`: edit `pages/index.html` for the home page, `pages/about.md` for the About page, and `pages/writings.html` for the Writings page. The old `/garden/` page redirects to `/writings/`.
- Edit `title` and `description` in `_config.yml` for the site name and default browser description.
- Notes are ordinary Markdown files in `_notes/`. To add one, create a file such as `_notes/my-new-note.md`:

```markdown
---
title: My new note
description: A sentence about this note.
category: Ideas
---

Write your note here. **Markdown** works!
```

It appears automatically on the Writings page, sorted by title. Its URL will be `/garden/my-new-note/`. Rename the file to change that URL. To remove a note, delete its file; check and update any links pointing to it. The home page displays the first three notes alphabetically.

## Change the colors

Open `assets/css/style.css`. The named color variables at the top control the palette. For example, change `--forest` for dark green and `--berry` for the red accent. Try different combinations, but check that text and links remain readable against their backgrounds. The site uses JetBrains Mono from Google Fonts and JavaScript for the Spotify widget; the rest of the content remains available if they cannot load.

## Monkeytype stats

The home page works offline and shows a disconnected message until the first successful update. The updater requests your personal bests for 15-second and 10-word tests, and averages WPM and accuracy equally across matching saved results. Personal bests can cover more tests than the retrieved results. It publishes only the aggregates and counts in `_data/monkeytype.json`, not individual tests or the key. Do not put the key in a file or commit it.

To enable automatic updates after publishing this repository:

1. Create a Monkeytype ApeKey with permission to read personal bests and results. In your GitHub repository settings, add it as the Actions secret `MONKEYTYPE_API_KEY` (never as a variable or in source control).
2. Ensure Actions is enabled and workflows have permission to write repository contents. If the default branch is protected against the Actions bot, allow its push or use a separate approved update process.
3. Run **Update Monkeytype aggregates** from the Actions tab with the manual dispatch, or wait for its daily 06:17 UTC schedule. Schedules can be delayed. The workflow commits only `_data/monkeytype.json` to the default branch; failed fetches leave the previous file untouched. Concurrent branch changes may reject a push; rerun the workflow.

The updater pages through the API's saved results until a short page proves completeness or the account's API cap is reached (currently 1,000 free / 10,000 premium). At a cap it labels the figures “retrieved saved tests,” not all-time; the displayed counts show the total fetched and the subset in each category. Failed requests or malformed relevant data fail the update rather than replacing earlier data. The API may not include unsaved or deleted tests.

GitHub's default `GITHUB_TOKEN` pushes do not trigger most other workflows, so this scheduled commit cannot create a push-workflow loop. If your site deploys via a separate push-triggered Actions workflow, that deployment may not run for the bot's commit; configure an appropriate deployment trigger separately if needed. This integration does not change deployment settings.

For a local refresh, set `MONKEYTYPE_API_KEY` in your environment securely and run `python3 scripts/update_monkeytype.py`; the generated aggregate file is public. Run `python3 -m unittest discover -s tests` for the mocked tests.

## Hosting and a future domain

Nothing here purchases a domain or configures hosting. When ready, choose a host that builds Jekyll or accepts the generated static `_site` directory. Run `bundle exec jekyll build` to generate it. Follow your host's current deployment and custom-domain instructions, and purchase or connect `bagellover08.com` only if you choose to. For a site hosted at a subpath, set `baseurl` in `_config.yml` (for example `/repository-name`); for a root domain leave it empty. Set `url` to the final origin when you know it, and rebuild. These settings alone do not connect a domain.
