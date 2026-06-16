#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);

function loadPlaywright() {
  const candidates = [
    "playwright",
    path.join(
      os.homedir(),
      ".cache",
      "codex-runtimes",
      "codex-primary-runtime",
      "dependencies",
      "node",
      "node_modules",
      ".pnpm",
      "playwright@1.60.0",
      "node_modules",
      "playwright"
    ),
    path.join(
      os.homedir(),
      ".cache",
      "codex-runtimes",
      "codex-primary-runtime",
      "dependencies",
      "node",
      "node_modules",
      "playwright"
    ),
  ];
  const errors = [];
  for (const candidate of candidates) {
    try {
      return require(candidate);
    } catch (error) {
      errors.push(`${candidate}: ${error.message}`);
    }
  }
  throw new Error(`Could not load Playwright.\n${errors.join("\n")}`);
}

const { chromium } = loadPlaywright();

const PDF_SELECTORS = [
  'a[href*=".pdf" i]',
  'a[href*="/pdf" i]',
  'a[href*="epdf" i]',
  'a[href*="/stamp/stamp.jsp" i]',
  'a[href*="arnumber=" i]',
  'a[aria-label*="PDF" i]',
  'button[aria-label*="PDF" i]',
  'a:has-text("PDF")',
  'a:has-text("Download PDF")',
  'a:has-text("Article PDF")',
  'a:has-text("Full Text PDF")',
  'a:has-text("View PDF")',
  'a:has-text("Texto completo")',
  'a:has-text("Baixar PDF")',
  'button:has-text("PDF")',
  'button:has-text("Download PDF")',
  'button:has-text("Article PDF")',
  'button:has-text("Full Text PDF")',
  'button:has-text("View PDF")',
];

const ACM_CAPES_SEARCH_TEMPLATE =
  "https://dl-acm-org.ez93.periodicos.capes.gov.br/action/doSearch?AllField={query}&expand=all";
const ACM_CAPES_HOME = "https://dl-acm-org.ez93.periodicos.capes.gov.br/";
const IEEE_CAPES_HOME = "https://ieeexplore-ieee-org.ez93.periodicos.capes.gov.br/Xplore/home.jsp";

const SEARCH_PROVIDERS = {
  acm: {
    home: ACM_CAPES_HOME,
    selectors: [
      'input[aria-label="Search"][name="AllField"]',
      'input[name="AllField"]',
      'input.quick-search__input',
      'input[type="search"]',
    ],
  },
  ieee: {
    home: IEEE_CAPES_HOME,
    selectors: [
      'input[aria-label="main"]',
      'input.Typeahead-input',
      'input[type="search"]',
    ],
  },
};

function usage() {
  return `Usage:
  node scripts/capes_download.mjs --from-artigos
  node scripts/capes_download.mjs --queue data/download_queue.csv
  node scripts/capes_download.mjs --login

Options:
  --from-artigos              Build the queue from artigos/**/info.md.
  --queue <file.csv>          CSV with title,url,out columns.
  --profile <dir>             Browser profile dir. Default: .capes-profile
  --out <dir>                 Base output dir. Default: artigos
  --portal <url>              URL opened by --login. Default: https://www-periodicos-capes-gov-br.ezl.periodicos.capes.gov.br/
  --search-url-template <url> URL template for missing links. Use {query}.
  --acm-capes-search          Search missing-link articles directly on ACM via CAPES.
  --search-provider <name>    Search missing-link articles from a home page. Values: acm, ieee.
  --headless                  Run without visible browser.
  --limit <n>                 Process only the first n queued articles.
  --delay-ms <n>              Delay between articles. Default: 2500
  --timeout-ms <n>            Page timeout. Default: 45000
  --dry-run                   Print queue only.
  --overwrite                 Replace existing artigo.pdf files.
  --interactive-missing       Pause when automation cannot find a PDF.
  --keep-open                 Keep the browser open until you press Enter.
`;
}

function parseArgs(argv) {
  const args = {
    profile: ".capes-profile",
    out: "artigos",
    portal:
      "https://www-periodicos-capes-gov-br.ezl.periodicos.capes.gov.br/",
    delayMs: 2500,
    timeoutMs: 45000,
    fromArtigos: false,
    headless: false,
    dryRun: false,
    overwrite: false,
    interactiveMissing: false,
    keepOpen: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      const value = argv[++i];
      if (!value) throw new Error(`Missing value for ${arg}`);
      return value;
    };
    if (arg === "--help" || arg === "-h") args.help = true;
    else if (arg === "--from-artigos") args.fromArtigos = true;
    else if (arg === "--queue") args.queue = next();
    else if (arg === "--profile") args.profile = next();
    else if (arg === "--out") args.out = next();
    else if (arg === "--portal") args.portal = next();
    else if (arg === "--search-url-template") args.searchUrlTemplate = next();
    else if (arg === "--acm-capes-search") args.searchUrlTemplate = ACM_CAPES_SEARCH_TEMPLATE;
    else if (arg === "--search-provider") args.searchProvider = next().toLowerCase();
    else if (arg === "--limit") args.limit = Number.parseInt(next(), 10);
    else if (arg === "--delay-ms") args.delayMs = Number.parseInt(next(), 10);
    else if (arg === "--timeout-ms") args.timeoutMs = Number.parseInt(next(), 10);
    else if (arg === "--headless") args.headless = true;
    else if (arg === "--login") args.login = true;
    else if (arg === "--dry-run") args.dryRun = true;
    else if (arg === "--overwrite") args.overwrite = true;
    else if (arg === "--interactive-missing") args.interactiveMissing = true;
    else if (arg === "--keep-open") args.keepOpen = true;
    else throw new Error(`Unknown option: ${arg}`);
  }
  return args;
}

function slug(value, maxLen = 95) {
  return (value || "sem-titulo")
    .replace(/[\\/:*?"<>|]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .replace(/[. ]+$/g, "")
    .slice(0, maxLen)
    .trim() || "sem-titulo";
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;

  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted && ch === '"' && next === '"') {
      cell += '"';
      i += 1;
    } else if (ch === '"') {
      quoted = !quoted;
    } else if (!quoted && ch === ",") {
      row.push(cell);
      cell = "";
    } else if (!quoted && (ch === "\n" || ch === "\r")) {
      if (ch === "\r" && next === "\n") i += 1;
      row.push(cell);
      if (row.some((part) => part.trim())) rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += ch;
    }
  }
  row.push(cell);
  if (row.some((part) => part.trim())) rows.push(row);
  return rows;
}

function readQueueCsv(filePath, outBase) {
  const rows = parseCsv(fs.readFileSync(filePath, "utf8"));
  if (rows.length === 0) return [];
  const headers = rows[0].map((h) => h.trim().toLowerCase());
  const idx = (name) => headers.indexOf(name);
  const titleIdx = idx("title");
  const urlIdx = idx("url");
  const outIdx = idx("out");
  if (titleIdx < 0) throw new Error("CSV must include a title column");

  return rows.slice(1).map((row, index) => {
    const title = row[titleIdx]?.trim() || `artigo-${index + 1}`;
    const out =
      row[outIdx]?.trim() ||
      path.join(outBase, `${String(index + 1).padStart(2, "0")} - ${slug(title)}`);
    return {
      id: String(index + 1).padStart(2, "0"),
      title,
      url: row[urlIdx]?.trim() || "",
      outDir: out,
      source: filePath,
    };
  });
}

function walkInfoFiles(root) {
  const found = [];
  if (!fs.existsSync(root)) return found;
  for (const entry of fs.readdirSync(root, { withFileTypes: true })) {
    const fullPath = path.join(root, entry.name);
    if (entry.isDirectory()) found.push(...walkInfoFiles(fullPath));
    else if (entry.isFile() && entry.name.toLowerCase() === "info.md") found.push(fullPath);
  }
  return found;
}

function readQueueFromArtigos(root) {
  return walkInfoFiles(root).map((infoPath, index) => {
    const text = fs.readFileSync(infoPath, "utf8");
    const title = /^#\s+(.+)$/m.exec(text)?.[1]?.trim() || path.basename(path.dirname(infoPath));
    const link = /^- Link original:\s*(.+)$/m.exec(text)?.[1]?.trim() || "";
    const normalizedLink = /nao informado|não informado|sem link|link nao informado|link não informado/i.test(link)
      ? ""
      : link.replace(/&amp;/g, "&");
    return {
      id: String(index + 1).padStart(2, "0"),
      title,
      url: normalizedLink,
      outDir: path.dirname(infoPath),
      source: infoPath,
    };
  });
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function isPdfBytes(buffer) {
  return buffer.subarray(0, 4).toString("latin1") === "%PDF";
}

function destinationFor(item) {
  return path.join(item.outDir, "artigo.pdf");
}

function normalizeForMatch(value) {
  return (value || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

function titleScore(expected, candidate) {
  const expectedWords = new Set(
    normalizeForMatch(expected)
      .split(/\s+/)
      .filter((word) => word.length > 2 && !/^\d+$/.test(word))
  );
  const candidateWords = new Set(
    normalizeForMatch(candidate)
      .split(/\s+/)
      .filter((word) => word.length > 2 && !/^\d+$/.test(word))
  );
  if (expectedWords.size === 0 || candidateWords.size === 0) return 0;
  let matches = 0;
  for (const word of expectedWords) {
    if (candidateWords.has(word)) matches += 1;
  }
  return matches / expectedWords.size;
}

function isGenericPortalPdf(url) {
  return /periodicos\.capes\.gov\.br\/images\/documents\//i.test(url);
}

async function openBestSearchResult(page, item, timeoutMs) {
  const pageUrl = page.url();
  const isAcm = /dl-acm-org\.ez93\.periodicos\.capes\.gov\.br/i.test(pageUrl);
  const isIeee = /ieeexplore-ieee-org\.ez93\.periodicos\.capes\.gov\.br/i.test(pageUrl);
  if (!isAcm && !isIeee) {
    return { opened: false, reason: "not an ACM/IEEE search page" };
  }

  const candidates = await page.evaluate(() =>
    [...document.querySelectorAll("a[href]")]
      .map((link) => ({
        text: (link.textContent || "").replace(/\s+/g, " ").trim(),
        href: new URL(link.getAttribute("href") || "", window.location.href).href,
      }))
      .filter((link) => link.text)
  );

  let best = null;
  for (const candidate of candidates) {
    if (isAcm && !/\/doi\/|\/book\//i.test(candidate.href)) continue;
    if (isIeee && !/\/document\/\d+/i.test(candidate.href)) continue;
    const score = titleScore(item.title, candidate.text);
    if (!best || score > best.score) best = { ...candidate, score };
  }

  if (!best || best.score < 0.45) {
    return {
      opened: false,
      reason: `no confident ${isAcm ? "ACM" : "IEEE"} result match${
        best ? ` (best score ${best.score.toFixed(2)}: ${best.text})` : ""
      }`,
    };
  }

  await page.goto(best.href, { waitUntil: "domcontentloaded", timeout: timeoutMs });
  return {
    opened: true,
    reason: `opened ${isAcm ? "ACM" : "IEEE"} result (${best.score.toFixed(2)}): ${best.text}`,
  };
}

async function searchFromProviderHome(page, providerName, query, timeoutMs) {
  const provider = SEARCH_PROVIDERS[providerName];
  if (!provider) {
    throw new Error(
      `Unknown search provider "${providerName}". Use one of: ${Object.keys(SEARCH_PROVIDERS).join(", ")}`
    );
  }

  await page.goto(provider.home, { waitUntil: "domcontentloaded", timeout: timeoutMs });

  let searchBox = null;
  for (const selector of provider.selectors) {
    const locator = page.locator(selector).first();
    if ((await locator.count().catch(() => 0)) > 0) {
      searchBox = locator;
      break;
    }
  }
  if (!searchBox) {
    throw new Error(`Could not find search input for provider "${providerName}"`);
  }

  await searchBox.fill(query, { timeout: timeoutMs });
  await Promise.all([
    page.waitForLoadState("domcontentloaded", { timeout: timeoutMs }).catch(() => null),
    searchBox.press("Enter"),
  ]);

  return { opened: true, reason: `searched ${providerName} home page for title` };
}

function existingBrowserExecutable() {
  const candidates = [
    process.env.CHROME_PATH,
    process.env.EDGE_PATH,
    path.join(process.env.PROGRAMFILES || "", "Google", "Chrome", "Application", "chrome.exe"),
    path.join(process.env["PROGRAMFILES(X86)"] || "", "Google", "Chrome", "Application", "chrome.exe"),
    path.join(process.env.LOCALAPPDATA || "", "Google", "Chrome", "Application", "chrome.exe"),
    path.join(process.env.PROGRAMFILES || "", "Microsoft", "Edge", "Application", "msedge.exe"),
    path.join(process.env["PROGRAMFILES(X86)"] || "", "Microsoft", "Edge", "Application", "msedge.exe"),
    path.join(process.env.LOCALAPPDATA || "", "Microsoft", "Edge", "Application", "msedge.exe"),
  ].filter(Boolean);

  return candidates.find((candidate) => fs.existsSync(candidate));
}

async function launchBrowserContext(args) {
  const options = {
    acceptDownloads: true,
    headless: args.headless,
    viewport: { width: 1366, height: 900 },
  };
  const executablePath = existingBrowserExecutable();
  if (executablePath) options.executablePath = executablePath;

  try {
    return await chromium.launchPersistentContext(path.resolve(args.profile), options);
  } catch (error) {
    if (executablePath) throw error;
    throw new Error(
      `${error.message}\n\nNo Chrome/Edge executable was found in the standard Windows paths. ` +
        `Install a browser with "npx playwright install chromium" or set CHROME_PATH to chrome.exe.`
    );
  }
}

async function waitForExplicitClose(message) {
  const rl = readline.createInterface({ input, output });
  try {
    while (true) {
      const answer = await rl.question(message);
      if (answer.trim().toUpperCase() === "FECHAR") return;
      message = 'Digite FECHAR para fechar o navegador. Enter sozinho mantem aberto: ';
    }
  } finally {
    rl.close();
  }
}

async function saveIfPdf(response, dest) {
  if (!response) return { ok: false, reason: "no response" };
  const headers = response.headers();
  const contentType = headers["content-type"] || "";
  const url = response.url();
  if (isGenericPortalPdf(url)) {
    return { ok: false, reason: `ignored generic CAPES PDF: ${url}` };
  }
  if (!/pdf/i.test(contentType) && !/\.pdf(?:$|[?#])/i.test(url)) {
    return { ok: false, reason: `not a pdf response: ${contentType || "unknown"}` };
  }

  const body = await response.body();
  if (!isPdfBytes(body) && !/pdf/i.test(contentType)) {
    return { ok: false, reason: "response did not look like a PDF" };
  }
  ensureDir(path.dirname(dest));
  fs.writeFileSync(dest, body);
  return { ok: true, reason: `saved direct PDF from ${url}` };
}

async function requestPdf(context, url, dest) {
  if (isGenericPortalPdf(url)) {
    return { ok: false, reason: `ignored generic CAPES PDF: ${url}` };
  }
  const response = await context.request.get(url, {
    headers: {
      Accept: "application/pdf,text/html;q=0.9,*/*;q=0.8",
      "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    },
    timeout: 30000,
  });
  const contentType = response.headers()["content-type"] || "";
  const body = await response.body();
  if (!response.ok()) return { ok: false, reason: `HTTP ${response.status()}` };
  if (!isPdfBytes(body) && !/pdf/i.test(contentType)) {
    return { ok: false, reason: `not PDF: ${contentType || "unknown"}` };
  }
  ensureDir(path.dirname(dest));
  fs.writeFileSync(dest, body);
  return { ok: true, reason: `saved PDF from ${url}` };
}

async function collectPdfUrls(page) {
  return page.evaluate(() => {
    const urls = new Set();
    for (const meta of document.querySelectorAll("meta")) {
      const name = `${meta.getAttribute("name") || ""} ${meta.getAttribute("property") || ""}`;
      const content = meta.getAttribute("content") || "";
      if (/citation_pdf_url|pdf/i.test(name) && content) urls.add(content);
    }
    for (const link of document.querySelectorAll("a[href]")) {
      const href = link.getAttribute("href") || "";
      const text = link.textContent || "";
      if (/\.pdf(?:$|[?#])|\/pdf|epdf/i.test(href) || /\bpdf\b/i.test(text)) {
        urls.add(new URL(href, window.location.href).href);
      }
    }
    return [...urls];
  });
}

async function clickPdfControls(page, dest, timeoutMs) {
  for (const selector of PDF_SELECTORS) {
    const elements = await page.locator(selector).elementHandles().catch(() => []);
    for (const element of elements.slice(0, 4)) {
      const downloadPromise = page.waitForEvent("download", { timeout: 7000 }).catch(() => null);
      const popupPromise = page.waitForEvent("popup", { timeout: 7000 }).catch(() => null);
      const navPromise = page.waitForNavigation({ timeout: 7000, waitUntil: "domcontentloaded" }).catch(() => null);

      await element.click({ timeout: 5000 }).catch(() => null);

      const download = await downloadPromise;
      if (download) {
        ensureDir(path.dirname(dest));
        await download.saveAs(dest);
        return { ok: true, reason: `saved browser download from ${selector}` };
      }

      const popup = await popupPromise;
      if (popup) {
        await popup.waitForLoadState("domcontentloaded", { timeout: timeoutMs }).catch(() => null);
        const direct = await saveIfPdf(await popup.waitForResponse((r) => /pdf/i.test(r.headers()["content-type"] || ""), { timeout: 5000 }).catch(() => null), dest);
        if (direct.ok) {
          await popup.close().catch(() => null);
          return direct;
        }
        const urls = await collectPdfUrls(popup).catch(() => []);
        await popup.close().catch(() => null);
        if (urls.length > 0) return { ok: false, reason: `popup exposed PDF candidate: ${urls[0]}` };
      }

      await navPromise;
      const currentResponse = await page
        .waitForResponse((r) => /pdf/i.test(r.headers()["content-type"] || ""), { timeout: 3000 })
        .catch(() => null);
      const direct = await saveIfPdf(currentResponse, dest);
      if (direct.ok) return direct;
    }
  }
  return { ok: false, reason: "no clickable PDF control succeeded" };
}

async function processItem(context, page, item, args) {
  const dest = destinationFor(item);
  if (!args.overwrite && fs.existsSync(dest)) {
    const existing = fs.readFileSync(dest);
    if (isPdfBytes(existing)) return { status: "skipped", note: "artigo.pdf already exists" };
  }

  ensureDir(item.outDir);
  let targetUrl = item.url;
  if (!targetUrl && args.searchProvider) {
    await searchFromProviderHome(page, args.searchProvider, item.title, args.timeoutMs);
  } else if (!targetUrl && args.searchUrlTemplate) {
    targetUrl = args.searchUrlTemplate.replace("{query}", encodeURIComponent(item.title));
  }
  if (!targetUrl && !args.searchProvider) return { status: "missing", note: "no URL and no search template/provider" };

  let response = null;
  if (targetUrl) {
    response = await page.goto(targetUrl, {
      waitUntil: "domcontentloaded",
      timeout: args.timeoutMs,
    }).catch((error) => ({ error }));
    if (response?.error) return { status: "failed", note: response.error.message };
  }

  if (response) {
    const direct = await saveIfPdf(response, dest);
    if (direct.ok) return { status: "downloaded", note: direct.reason };
  }

  const searchResult = await openBestSearchResult(page, item, args.timeoutMs).catch((error) => ({
    opened: false,
    reason: error.message,
  }));
  if (searchResult.opened) {
    const articleDirect = await saveIfPdf(await page.waitForResponse((r) => /pdf/i.test(r.headers()["content-type"] || ""), { timeout: 2500 }).catch(() => null), dest);
    if (articleDirect.ok) return { status: "downloaded", note: `${searchResult.reason}; ${articleDirect.reason}` };
  }

  const pdfUrls = await collectPdfUrls(page).catch(() => []);
  for (const pdfUrl of pdfUrls.slice(0, 8)) {
    const result = await requestPdf(context, pdfUrl, dest).catch((error) => ({
      ok: false,
      reason: error.message,
    }));
    if (result.ok) return { status: "downloaded", note: result.reason };
  }

  const clicked = await clickPdfControls(page, dest, args.timeoutMs);
  if (clicked.ok) return { status: "downloaded", note: clicked.reason };

  if (args.interactiveMissing) {
    const rl = readline.createInterface({ input, output });
    await rl.question(
      `Nao achei o PDF para "${item.title}". Baixe manualmente nessa janela ou navegue ate o PDF, depois pressione Enter...`
    );
    rl.close();
    if (fs.existsSync(dest) && isPdfBytes(fs.readFileSync(dest))) {
      return { status: "downloaded", note: "saved during interactive pause" };
    }
    const afterPause = await saveIfPdf(await page.waitForResponse((r) => /pdf/i.test(r.headers()["content-type"] || ""), { timeout: 3000 }).catch(() => null), dest);
    if (afterPause.ok) return { status: "downloaded", note: afterPause.reason };
  }

  return {
    status: "failed",
    note: `${clicked.reason}; ${pdfUrls.length} PDF candidate(s) found`,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(usage());
    return;
  }

  let queue = [];
  if (args.queue) queue = readQueueCsv(args.queue, args.out);
  else if (args.fromArtigos) queue = readQueueFromArtigos(args.out);
  else if (!args.login) throw new Error("Use --from-artigos, --queue, or --login");
  if (args.limit) queue = queue.slice(0, args.limit);

  if (args.dryRun) {
    for (const item of queue) {
      const targetUrl =
        item.url ||
        args.searchUrlTemplate?.replace("{query}", encodeURIComponent(item.title)) ||
        (args.searchProvider ? `${args.searchProvider}: search home page for "${item.title}"` : null) ||
        "(search only)";
      console.log(`${item.id}\t${item.title}\t${targetUrl}\t${destinationFor(item)}`);
    }
    return;
  }

  ensureDir(args.profile);
  const context = await launchBrowserContext(args);
  const page = context.pages()[0] || (await context.newPage());
  page.setDefaultTimeout(args.timeoutMs);

  if (args.login) {
    await page.goto(args.portal, { waitUntil: "domcontentloaded", timeout: args.timeoutMs }).catch(() => null);
    const rl = readline.createInterface({ input, output });
    await rl.question("Faca login no portal aberto. Quando terminar, pressione Enter aqui para continuar...");
    rl.close();
  }

  const logPath = path.join(args.out, "capes_download_log.jsonl");
  ensureDir(args.out);
  let downloaded = 0;
  let failed = 0;
  let skipped = 0;

  for (const item of queue) {
    const startedAt = new Date().toISOString();
    console.log(`[${item.id}] ${item.title}`);
    const result = await processItem(context, page, item, args).catch((error) => ({
      status: "failed",
      note: error.stack || error.message,
    }));
    if (result.status === "downloaded") downloaded += 1;
    else if (result.status === "skipped") skipped += 1;
    else failed += 1;
    const row = {
      startedAt,
      finishedAt: new Date().toISOString(),
      ...item,
      dest: destinationFor(item),
      ...result,
    };
    fs.appendFileSync(logPath, `${JSON.stringify(row)}\n`, "utf8");
    console.log(`  ${result.status}: ${result.note}`);
    await page.waitForTimeout(args.delayMs);
  }

  if (args.keepOpen) {
    await waitForExplicitClose(
      "Navegador mantido aberto. NAO aperte Enter para fechar; digite FECHAR somente quando quiser encerrar: "
    );
  }

  await context.close();
  console.log(`Done. downloaded=${downloaded} skipped=${skipped} failed=${failed}`);
  console.log(`Log: ${logPath}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
