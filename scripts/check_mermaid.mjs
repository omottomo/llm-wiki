// wiki/ 안 모든 ```mermaid 블록을 실제 Mermaid 파서에 넣어본다 (phase-19).
//
// lint_wiki.py 의 check_diagrams 는 그림의 겉(캡션·인용·타입·개수·페이지 타입)만 본다 —
// 문법이 말이 되는지는 파이썬에 Mermaid 파서가 없어 검사하지 못한다(lint_wiki.py:443).
// 그 블록은 독자 브라우저에서 렌더되므로, 문법 오류는 아무 경고 없이 배포되고
// 사이트에서 빨간 에러 박스로 나타난다. 이 스크립트가 그 사이를 막는다.
//
// 검사 범위는 "파싱되는가"뿐이다. 라벨 겹침·글자 넘침·알아보기 힘든 배치는 잡지 못하며,
// 그건 여전히 PR에서 사람이 볼 몫이다. 품질 게이트가 아니라 문법 게이트다.
//
// 실행:
//   npm i --no-save mermaid@<pin> jsdom@<pin>
//   node scripts/check_mermaid.mjs [--root PATH]
// --root 는 lint_wiki.py 와 같은 뜻 — <PATH>/wiki 를 대신 검사한다 (테스트용).

import { readFileSync, readdirSync, statSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { JSDOM } from "jsdom";

const REPO = dirname(dirname(fileURLToPath(import.meta.url)));

// lint_wiki.py:59 의 MERMAID_FENCE_RE 와 같은 모양. 두 곳이 갈라지면 한쪽이 못 보는 블록이
// 생기므로, 펜스 규약을 바꾸면 둘 다 고친다.
const MERMAID_FENCE_RE = /^[ \t]*```mermaid[ \t]*\r?\n([\s\S]*?)^[ \t]*```[ \t]*$/gm;

// site/build.py 가 브라우저에 로드하는 그 버전으로 검사해야 게이트가 거짓말을 하지 않는다.
const PIN_RE = /^MERMAID_VERSION\s*=\s*"([^"]+)"/m;

function parseArgs(argv) {
  const i = argv.indexOf("--root");
  if (i === -1) return { root: REPO };
  const value = argv[i + 1];
  if (!value) {
    console.error("--root 에 경로가 없다");
    process.exit(2);
  }
  return { root: resolve(value) };
}

function markdownFiles(dir) {
  const found = [];
  for (const name of readdirSync(dir).sort()) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) found.push(...markdownFiles(path));
    else if (name.endsWith(".md")) found.push(path);
  }
  return found;
}

function mermaidBlocks(root) {
  const blocks = [];
  for (const file of markdownFiles(join(root, "wiki"))) {
    const text = readFileSync(file, "utf8");
    for (const match of text.matchAll(MERMAID_FENCE_RE)) {
      // 펜스 앞 줄 수 + 1 = 펜스 줄, 그 다음 줄부터가 그림 소스.
      const line = text.slice(0, match.index).split("\n").length;
      blocks.push({ where: `${relative(root, file)}:${line}`, source: match[1] });
    }
  }
  return blocks;
}

// dompurify 는 import 시점에 window 에 붙으므로, mermaid 를 부르기 전에 DOM 을 깔아둔다.
function installDom() {
  const dom = new JSDOM("<!doctype html><html><body></body></html>");
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  globalThis.Node = dom.window.Node;
  globalThis.Element = dom.window.Element;
  // node 24 의 globalThis.navigator 는 getter 라 대입이 안 된다.
  Object.defineProperty(globalThis, "navigator", {
    value: dom.window.navigator,
    configurable: true,
  });
}

function assertPinnedVersion() {
  const buildPy = readFileSync(join(REPO, "site", "build.py"), "utf8");
  const pinned = PIN_RE.exec(buildPy)?.[1];
  if (!pinned) {
    console.error("site/build.py 에서 MERMAID_VERSION 을 찾지 못했다");
    process.exit(2);
  }
  const require = createRequire(import.meta.url);
  const installed = require("mermaid/package.json").version;
  if (installed !== pinned) {
    console.error(
      `mermaid 버전 불일치 — site/build.py 핀은 ${pinned}, 설치된 건 ${installed}. ` +
        `다른 버전으로 검사하면 게이트가 양쪽으로 거짓말을 한다.`
    );
    process.exit(2);
  }
  return pinned;
}

const { root } = parseArgs(process.argv.slice(2));
const version = assertPinnedVersion();
const blocks = mermaidBlocks(root);

if (blocks.length === 0) {
  console.log(`그림 없음 — 검사할 mermaid 블록이 하나도 없다 (mermaid ${version})`);
  process.exit(0);
}

installDom();
const { default: mermaid } = await import("mermaid");

const failures = [];
for (const block of blocks) {
  try {
    await mermaid.parse(block.source);
  } catch (error) {
    failures.push({ where: block.where, message: String(error.message).split("\n")[0] });
  }
}

if (failures.length > 0) {
  for (const failure of failures) console.error(`FAIL ${failure.where} — ${failure.message}`);
  console.error(`\n${blocks.length}개 중 ${failures.length}개가 파싱되지 않는다 (mermaid ${version})`);
  process.exit(1);
}

console.log(`OK — mermaid 블록 ${blocks.length}개 모두 파싱됨 (mermaid ${version})`);
