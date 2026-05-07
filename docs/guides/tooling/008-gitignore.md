# .gitignore

## What It Does

`.gitignore` tells Git which files and folders to never track and never commit.
Every line is a pattern. Git checks each untracked file against these patterns — if it matches, the file is invisible to Git.

---

## Pattern Syntax

```
node_modules/            # a folder (trailing / is convention, not required)
*.log                    # any file ending in .log
.env                     # exact filename
apps/frontend/.vite/     # specific path inside the repo
```

- `*` = any characters
- `/` at the end = directory
- Leading `/` = root of the repo only
- Full path without leading `/` = matched anywhere in the repo

## How to Add an Entry

Open the file, add a line. No compilation, no special command — that is all.

---

## Important: Already-Tracked Files

`.gitignore` only works for **untracked** files. If a file was already committed, adding it to `.gitignore` does nothing — Git keeps tracking it.

To stop tracking a file that was already committed:

```bash
git rm --cached <file>
git rm --cached -r <folder>   # for a directory
```

This removes the file from Git's index (stops tracking it) without deleting it from disk.
After that, commit the removal and `.gitignore` takes effect going forward.

---

## Why we added `apps/frontend/.vite/`

Vite creates a `.vite/` cache directory when it runs — dependency pre-bundling output.
It is generated automatically and changes frequently. Committing it would add noise to every `git status` and `git diff`.

The directory was untracked when we added it, so `git rm --cached` was not needed.
