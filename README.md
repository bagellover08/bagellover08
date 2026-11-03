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

- Edit `index.html` for the home page and `about.md` for the about page. The About text is explicitly a placeholder.
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

It appears automatically in the garden, sorted by title. Its URL will be `/garden/my-new-note/`. Rename the file to change that URL. To remove a note, delete its file; check and update any links pointing to it. The home page displays the first three notes alphabetically.

## Change the colors

Open `assets/css/style.css`. The named color variables at the top control the palette. For example, change `--forest` for dark green and `--berry` for the red accent. Try different combinations, but check that text and links remain readable against their backgrounds. The site works without remote fonts, images, or JavaScript.

## Hosting and a future domain

Nothing here purchases a domain or configures hosting. When ready, choose a host that builds Jekyll or accepts the generated static `_site` directory. Run `bundle exec jekyll build` to generate it. Follow your host's current deployment and custom-domain instructions, and purchase or connect `bagellover08.com` only if you choose to. For a site hosted at a subpath, set `baseurl` in `_config.yml` (for example `/repository-name`); for a root domain leave it empty. Set `url` to the final origin when you know it, and rebuild. These settings alone do not connect a domain.
