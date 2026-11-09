const STOP = new Set(
  "the a an and or of to in for with that this is are be by on as from at it its can may not ai risk risks system systems model models agent agents 인공지능 시스템 리스크 위험 대한 통해 위한 경우 있는 없는 이를 또는 및 등의 한다 하는 하여 되어 관련 발생 가능 사용 결과 서비스 과정 이용자 고객".split(
    /\s+/,
  ),
);
export function normalize(s) {
  return String(s)
    .normalize("NFKC")
    .toLowerCase()
    .replace(/[_/·–—-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}
const compact = (s) => normalize(s).replace(/\s/g, "");
function words(s) {
  return (
    normalize(s)
      .match(/[\p{L}\p{N}]+/gu)
      ?.filter((w) => w.length > 1 && !STOP.has(w)) || []
  );
}
function terms(s) {
  const set = new Set();
  for (const w of words(s)) {
    set.add(w);
    if (/^[가-힣]+$/.test(w)) {
      const stem = w.replace(
        /(으로부터|에서는|으로|에서|에게|하는|하지|하고|하여|되어|되는|하면|이다|입니다|습니다|거나|이나|처럼|보다|에는|은|는|이|가|을|를|의|에|와|과|도|로)$/,
        "",
      );
      if (stem.length > 1 && !STOP.has(stem)) set.add(stem);
    }
  }
  return set;
}
function grams(s) {
  const set = new Set();
  for (const part of normalize(s).match(/[가-힣\s]+/g) || []) {
    const t = part.replace(/\s/g, "");
    for (let i = 0; i < t.length - 2; i++) set.add(t.slice(i, i + 3));
  }
  return set;
}
// Shared concepts are counted once, rather than once for each synonym or language.
const CONCEPTS = [
  ["advice", /추천|조언|권고|recommend|advice/],
  [
    "insufficient",
    /불충분|정보부족|일부정보만|정보.{0,10}(부족|불완전)|충분한정보.{0,14}(못|없이|않)/,
  ],
  ["interpretation", /잘못해석|잘못이해|오해|misinterpret|misunderstand/],
  ["context", /맥락|상황|이용패턴|결합조건|할인조건|상황적단서|context/],
  [
    "privacy",
    /개인정보|사생활|민감한?정보|privacy|personaldata|personalinformation/,
  ],
  ["consent", /동의|동의철회|consent/],
  ["leak", /유출|노출|누출|disclos|leak|exposure/],
  ["memory", /메모리|기억|memory/],
  ["collect", /수집|저장|축적|collect|retention|storage/],
  ["unfair", /차별|불공정|합리적근거없이|discriminat|unfair/],
  [
    "protected",
    /연령|성별|인구집단|보호대상|\bage\b|\bgender\b|protectedcharacter/,
  ],
  [
    "false",
    /없는.{0,10}(상품|정보|혜택)|실제와다른|허위|환각|부정확|오안내|hallucinat|misinformation|inaccurate/,
  ],
  ["calculation", /계산|오계산|납부액|절감액|수치|calculat|numerical/],
  ["refusal", /제공하지않|요청.{0,10}거부|부당하게거부|정당한요청|refus/],
  ["oversight", /감독|제어권|인계|oversight|handover/],
  [
    "injection",
    /프롬프트.{0,14}(공격|주입)|시스템지시무시|역할변경|promptinjection/,
  ],
  ["attack", /악의|공격자|탈옥|안전장치우회|jailbreak|attacker|adversarial/],
  ["confidential", /기밀|내부정보|내부정책|시스템프롬프트|confidential|secret/],
  ["harmful", /유해콘텐츠|혐오|성적|자해|폭력|harmfulcontent|hate|selfharm/],
  ["collision", /충돌|상해|collision|injury/],
  [
    "recognition",
    /인식하지못|미인식|감지.{0,5}실패|오인식|recognition|perception/,
  ],
];
function concepts(s) {
  const c = compact(s),
    n = normalize(s);
  return new Set(
    CONCEPTS.filter(([, pattern]) => pattern.test(c) || pattern.test(n)).map(
      ([name]) => name,
    ),
  );
}
export function createRiskIndex(taxonomy) {
  const docs = Object.entries(taxonomy.domains).flatMap(([domain, rows]) =>
    rows.map((row) => {
      const title = [row.L4_Title_ko, row.L4_Title_en].join(" "),
        definition = [row.L4_Description_ko, row.L4_Description_en].join(" ");
      return {
        row,
        domain,
        title: normalize(title),
        text: normalize(title + " " + definition),
        compact: compact(title + " " + definition),
        terms: terms(title + " " + definition),
        grams: grams(title + " " + definition),
        concepts: concepts(title + " " + definition),
      };
    }),
  );
  const freq = new Map(),
    cf = new Map();
  for (const d of docs) {
    for (const t of d.terms) freq.set(t, (freq.get(t) || 0) + 1);
    for (const c of d.concepts) cf.set(c, (cf.get(c) || 0) + 1);
  }
  return {
    docs,
    freq,
    cf,
    koreanVocabulary: [...freq.keys()].filter((t) => /^[가-힣]{2,}$/.test(t)),
    avgLength: docs.reduce((n, d) => n + d.terms.size, 0) / docs.length,
  };
}
export function searchRisks(index, input, { limit = 5, domain = "all" } = {}) {
  const q = normalize(input),
    qc = compact(input),
    qset = new Set([
      ...[...terms(input)].filter((t) => !/^[가-힣]+$/.test(t)),
      ...index.koreanVocabulary.filter((t) => qc.includes(t)),
    ]),
    qt = [...qset].filter((t) => {
      if (!/^[가-힣]+$/.test(t)) return true;
      for (let n = 2; n < t.length; n++)
        if (qset.has(t.slice(0, n))) return false;
      return true;
    }),
    qg = grams(input),
    concept = concepts(input);
  if (!q || (!qt.length && !qg.size)) return [];
  const scores = [];
  for (const doc of index.docs) {
    if (domain !== "all" && doc.domain !== domain) continue;
    let lexical = 0;
    const matched = [];
    for (const t of qt) {
      const present =
        doc.terms.has(t) ||
        (/^[가-힣]{2,}$/.test(t) && doc.compact.includes(t));
      if (!present) continue;
      const df = index.freq.get(t) || Math.ceil(index.docs.length / 8),
        idf = Math.log(1 + (index.docs.length - df + 0.5) / (df + 0.5));
      const norm = 1.2 * (0.25 + (0.75 * doc.terms.size) / index.avgLength);
      const weight =
        ((idf * 2.2) / (1 + norm)) * (doc.title.includes(t) ? 1.8 : 1);
      lexical += weight;
      matched.push({ term: t, weight });
    }
    let overlaps = 0;
    for (const g of qg) if (doc.grams.has(g)) overlaps++;
    const charScore = qg.size
      ? overlaps / Math.sqrt(qg.size * Math.max(1, doc.grams.size))
      : 0;
    let conceptScore = 0,
      conceptMatches = 0;
    for (const c of concept)
      if (doc.concepts.has(c)) {
        conceptMatches++;
        conceptScore += Math.log(
          1 + (index.docs.length + 1) / ((index.cf.get(c) || 0) + 1),
        );
      }
    let score = lexical + 8 * charScore + 2.2 * conceptScore;
    if (concept.size) score *= 0.25 + (0.75 * conceptMatches) / concept.size;
    // Card-specific application conditions are soft penalties, not domain-wide exclusions.
    const title = compact(doc.row.L4_Title_ko),
      body = compact(doc.row.L4_Description_ko);
    const prerequisites = [
      [
        /로봇|드론|자율주행|물리적접촉|구동기|엔드이펙터/,
        /로봇|드론|자율주행|차량|보행자|센서|물리적|충돌|robot|drone|vehicle|pedestrian|sensor|physical|collision/,
      ],
      [
        /학습|훈련|주석자|레이블|미세조정/,
        /학습|훈련|레이블|모델개발|미세조정|training|learning|label|fine.tun/,
      ],
      [
        /공격자|공격에의한|적대적|탈옥/,
        /악의|공격|프롬프트|탈옥|보안|attack|malicious|prompt|security|jailbreak/,
      ],
    ];
    prerequisites.push(
      [
        /의료|의학|과학데이터/,
        /의료|의학|과학|진료|환자|의사|medical|science|patient|doctor|health/,
      ],
      [
        /정치|민주주의|선거|온라인양극화/,
        /정치|선거|민주|여론|양극화|politic|election|democra|polariz/,
      ],
      [
        /신체개입|물리적|하드웨어|행동전이/,
        /신체|물리|하드웨어|로봇|차량|센서|충돌|physical|hardware|robot|vehicle|sensor|collision/,
      ],
    );
    if (
      /동물|육류|축산|동물학대/.test(body) &&
      !/동물|육류|축산|animal|meat|livestock/.test(qc)
    )
      score *= 0.2;
    for (const [required, present] of prerequisites)
      if (required.test(title) && !present.test(qc)) score *= 0.25;
    if (
      doc.domain === "Physical" &&
      !/로봇|물리|보행자|차량|드론|센서|충돌|신체|제어|robot|physical|pedestrian|vehicle|drone|sensor|collision|body|control/.test(
        qc,
      )
    )
      score *= 0.25;
    if (
      /물체|장면/.test(title) &&
      !/물체|장면|로봇|물리|센서|영상|이미지|object|scene|robot|physical|sensor|image|vision/.test(
        qc,
      )
    )
      score *= 0.25;
    if (
      /평가|벤치마크|시험/.test(title) &&
      !/평가|시험|벤치마크|테스트|측정|evaluat|test|benchmark|measur/.test(qc)
    )
      score *= 0.25;
    if (
      /자기교정|수정·개선/.test(doc.row.L4_Title_ko) &&
      !/교정|정정|오류|잘못|수정|개선|correct|error|wrong|modif|improv/.test(qc)
    )
      score *= 0.3;
    if (
      /돌봄|취약계층/.test(title) &&
      !/돌봄|고령|아동|청소년|미성년|취약|care|elder|child|adolesc|minor|vulnerab/.test(
        qc,
      )
    )
      score *= 0.3;
    if (
      /공격자가/.test(body) &&
      !/악의|공격|탈옥|주입|프롬프트|malicious|attack|jailbreak|inject|prompt/.test(
        qc,
      )
    )
      score *= 0.4;
    if (
      qc === compact(doc.row.L4_Title_ko) ||
      qc === compact(doc.row.L4_Title_en) ||
      normalize(input) === normalize(doc.row.L4_ID)
    )
      score += 1000;
    if (!matched.length && !conceptMatches && charScore < 0.12) continue;
    if (
      score < 3.5 ||
      (matched.length < 2 && !conceptMatches && charScore < 0.18)
    )
      continue;
    matched.sort((a, b) => b.weight - a.weight);
    scores.push({
      ...doc,
      score,
      matched: matched.slice(0, 6).map((x) => x.term),
      snippet: String(input),
    });
  }
  scores.sort(
    (a, b) => b.score - a.score || a.row.L4_ID.localeCompare(b.row.L4_ID),
  );
  const threshold = scores.length ? Math.max(3.5, scores[0].score * 0.4) : 3.5;
  return scores
    .filter((x) => x.score >= threshold)
    .slice(0, Math.max(1, Math.min(20, limit)));
}
