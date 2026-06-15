# CAPES article downloader

This script uses a normal authenticated browser session. It does not bypass paywalls or authentication. On the first run, log in through CAPES in the Playwright window; later runs reuse `.capes-profile`.

## 1. Prepare the folders

If the article folders do not exist yet, run the existing organizer first:

```powershell
python organize_articles.py
```

## 2. Log in once

```powershell
& "C:\Users\isaac\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\capes_download.mjs --login
```

Finish the CAPES login in the opened browser window, then press Enter in the terminal. The session is saved in `.capes-profile`.

## 3. Download from existing `artigos/**/info.md`

```powershell
& "C:\Users\isaac\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\capes_download.mjs --from-artigos
```

To use ACM through CAPES as the search base for articles that have no direct link:

```powershell
& "C:\Users\isaac\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\capes_download.mjs --from-artigos --acm-capes-search
```

Useful options:

```powershell
# See what it would process.
& "C:\Users\isaac\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\capes_download.mjs --from-artigos --dry-run

# Test only the first 5.
& "C:\Users\isaac\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\capes_download.mjs --from-artigos --limit 5

# Pause for manual help only when it cannot find a PDF button/link.
& "C:\Users\isaac\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\capes_download.mjs --from-artigos --interactive-missing
```

The script writes `artigo.pdf` inside each article folder and logs each attempt to `artigos/capes_download_log.jsonl`.

## CSV queue

You can also use a CSV:

```csv
title,url,out
"Article title","https://publisher.example/article","artigos/01 - Article title"
```

Run:

```powershell
& "C:\Users\isaac\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\capes_download.mjs --queue data\download_queue.csv
```

For rows without `url`, provide a search template:

```powershell
& "C:\Users\isaac\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" scripts\capes_download.mjs --queue data\download_queue.csv --search-url-template "https://example.edu/search?q={query}"
```
