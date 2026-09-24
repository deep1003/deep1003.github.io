# Policy Commons contamination and country-attribution criteria

This register records error types that must be checked in every future dataset. Each new error must be added with a failing example and a counterexample that should remain included.

## Historical core rules

The rules below document the earlier protocol. Where they conflict, the 24 September 2026 amendment at the end of this register supersedes rules 1, 7 and 9 concerning country evidence, media exceptions and removal from active corpora. Historical results below are not new validation results.

1. Do not infer a country from `Published in` or place alone. Check the issuer, source, institutional hierarchy and policy jurisdiction. Where place and issuer conflict, issuer jurisdiction takes priority.
2. Aggregate HKG to CHN for country analysis, while preserving the original RIS and CSV values.
3. Do not treat the headquarters or repository location of an EU body, international organisation or regional network as a national issuer. Include a national office, commission or country-specific policy report only when the source provides supporting evidence.
4. Do not automatically remove a multinational private company. Exclude ordinary business, product and promotional documents from the national policy-interest analysis, but retain them in the source master. Include a private research unit where the source evidences government funding, commissioning or a national policy research project.
5. Exclude standalone logistical agendas, recruitment notices, theses and purely scholarly outputs. Retain official proceedings, workshops and agendas when they document policy inquiries, regulation, standards, public administration, testimony, recommendations or implementation. Retain substantive bundles such as minutes, policy documents, strategies, assessments and official records.
6. Absence of an AI term in the title, abstract or keywords is not evidence of Non-AI. Policy Commons may have matched the indexed full text. Exclude only clear alternative meanings supported by positive evidence.
7. Exclude video, image, audio, patent and dataset items when they are not policy documents. Confirm the document type on the original page.
8. Join RIS and CSV using normalised Policy Commons and artefact identifiers. Never join on title, row order or filename.
9. Preserve the source master. Record every exclusion, rule ID, evidence field and random seed in versioned audit outputs. Do not physically delete source observations.
10. The national AI policy-interest corpus includes government departments, public authorities, local government, publicly funded research institutes, government-funded research centres and private research units carrying out commissioned national research. A company’s headquarters or branch location alone is insufficient.

## Policy Commons source examples

- [Government of Sweden AI regulation response](https://policycommons.net/artifacts/44770242/internetstiftelsens-response-to-ai-regulation-adaptations-sou-2025101/45669071/): government policy context and issuer jurisdiction support Sweden.
- [Government of Canada parliamentary evidence](https://policycommons.net/artifacts/4252309/evidence-standing-committee-on-canadian-heritage/5061382/): Government of Canada and parliamentary information take precedence over the place value Ottawa.
- [Canadian AI patent-landscape report](https://policycommons.net/artifacts/54150589/processing-artificial-intelligence/55048942/): a Canadian public research institution and Canadian policy context support inclusion.
- [Abbott (United States) document](https://policycommons.net/artifacts/14004974/beyond-intervention/): preserve the United States source evidence, but exclude the ordinary multinational-company document from the national policy-interest analysis unless government-research evidence is found.
- [European Union Fourth Framework Programme](https://policycommons.net/artifacts/294457/the-fourth-framework-programme-for-reserach-and-technological-development/1183995/): European Union authorship and rights indicate a supranational document, not a Belgian national document.
- [EUAA AI and robotics document](https://policycommons.net/artifacts/2024412/1/2776854/): `Published in Malta` does not by itself convert an EU agency document into a Maltese national document.

## Reproducible application order

1. Read the original Policy Commons page and capture issuer, Source, institutional level, Rights and `Published in`.
2. Classify the issuer as government/public, publicly funded research, private, international or supranational.
3. For a private issuer, search the source record for government commissioning, funding or a national research remit.
4. For an international or EU issuer, separate headquarters location from country-specific policy jurisdiction.
5. Record `issuer_country`, `country_scope_class`, `government_research_evidence` and `country_decision_source`.
6. If evidence is insufficient, retain the observation as `manual_review`, not as a silent exclusion.

## Regression checks

- Separate document counts from document-country row counts.
- Test Kosovo, Ottawa/Canada, HKG/China and EU/international-organisation conflicts.
- Test agenda substantive-bundle exceptions.
- Test international networks against national branches and commissions.
- Test that metadata-negative AI records remain included.
- Mark inaccessible pages as `unverifiable`; never count them as semantically validated.

### Round-5 findings (v7.6 census)

The latest full-census pass found 77 additional high-confidence form exclusions: 33 standalone vacancy or position-description records, 30 standalone user or product manuals, 10 thesis or thesis-administration records, 2 standalone datasets and 2 university syllabi. It also found 5 repository or commercial-platform records for manual country review. Twenty-six international or non-national cases remain in a manual-review queue. These categories must be tested before the next release; AI-term absence was not used as an exclusion rule.

## Human-review amendment, 24 September 2026

These criteria supersede conflicting historical rules. They distinguish metadata screening, original-text assessment and human adjudication; a completed metadata census is not evidence that every full text has been read.

1. **Videos and recordings.** Exclude by default. Include an explicitly labelled exception when the abstract substantively describes AI policy and the source metadata explicitly identifies a country. A proposed event, an AI token in a topic list or an institution's location alone is insufficient. Preserve format and exception evidence for sensitivity analysis.
2. **Blogs.** Exclude by default. Include an exception when the title, abstract or keywords explicitly establishes AI-policy relevance and source metadata states the country. Do not infer AI relevance solely from precision medicine or another adjacent field. Human review excludes `pcv3_cdff38557f69d23670d3f7fd` (`20.500.12592/b0tjxtf`) because direct AI content is absent, despite its United States publication metadata.
3. **AI-token integrity.** Match the acronym as a standalone token, allowing punctuation and compounds such as AI-powered. Do not match letters inside airport, airplane, availability, obtaining or explaining. Recognise full phrases and multilingual AI terminology. A boundary rule is a screening safeguard, not proof that a document without metadata matches is irrelevant. Indexed full-text AI evidence remains valid. Human adjudication confirms removal of `pcv3_237cb1fb6452ba66b6ba4ffa` (`20.500.12592/1p0r921`) and `042a2ba1c1ed659b95da` (`20.500.12592/5jbt2zn`).
4. **Country evidence roles.** Preserve source-reported publication country separately from issuer location, author affiliation and inferred target country. When publication-country evidence is missing, explicit national policy scope in the title or abstract can support target-country inference for up to three countries. Record the inference basis; do not label it verified publication place.
5. **International bodies.** Classify international organisations and coordination bodies separately from national publications. Store headquarters or secretariat country in the organisation dictionary without automatically assigning that country to documents. `79c246521fc639ce218e` (`20.500.12592/4w3qzvc`) belongs to CGMS, an international coordination body. Its German secretariat location is dictionary information, distinct from national analytical attribution.
6. **Substantive health and culture policy.** Sector-specific AI evidence is eligible. RHTP (`pcv3_530792066cd1fc7945efdd9c`, `20.500.12592/4znk86f`) concerns rural healthcare and must retain that topic alongside supported AI-powered clinical tools and cybersecurity labels. Do not reduce it to cybersecurity alone. Creative Australia (`c6565b6ec3aa05c6bcd2`, `20.500.12592/2yhb6rg`) explicitly covers AI within Australian arts participation and receives Australia (`AUS`).
7. **Deletion and exclusion propagation.** Delete user-confirmed exact false-positive records from active collected, deduplicated and final analytical corpora using stable identifiers. Record identifiers, affected files, reason, evidence and rule version in a deletion ledger. Preserve immutable archival evidence outside the active pipeline where required for reproducibility, and maintain tombstones to prevent re-ingestion. Ordinary format exclusions and unresolved candidates retain explicit status; absence of metadata terms alone does not justify permanent deletion.
8. **Audit reporting.** Record original format, AI evidence, policy evidence, country source, decision confidence, human override and exception status. Report classified records separately from unresolved candidates and full-text-verified records. Run structural consistency checks across all active stages and report actual execution counts separately from this protocol.

9. **Format evidence and enrichment.** A genre word in keywords alone does not establish that a record is a video, recording or blog. Confirm format using source metadata, the source URL or the original page. Where the collected abstract is truncated, a substantive official transcript or recap may support the media exception. Preserve the collected abstract and store source-backed enrichment separately. Neither a metadata census nor specialist metadata review is equivalent to full-text verification.

### Specialist candidate-review outcomes

All 238 initial exclusion candidates were reviewed, yielding 179 provisional exclusions and 59 holds. Of 22 exception candidates, 13 were approved and 9 were held. These are review-stage decisions; completion of updates to the collected, deduplicated and analytical masters must be established separately from execution manifests. A hold indicates insufficient evidence for a final disposition.

### Original-source evidence for the amendment

- **RHTP media exception.** The [official Alaska RHTP programme page](https://health.alaska.gov/en/education/rural-health-transformation-program/rhtp-impacts/) establishes rural-health policy context. Its [official Session 1 recap](https://health.alaska.gov/media/n5bfbqt2/260331-ak-rhtp-webinar-recap-rhtp-impacts-spark-technology-and-innovation-kickoff-session.pdf) describes clinical AI tools, cybersecurity and data protection. This source-backed content supports the video exception beyond the truncated collected abstract. Preserve the original abstract and store enrichment separately. If the recap is separately collected, link the two manifestations to avoid counting the same session twice.
- **CGMS institutional scope.** The [official CGMS description](https://cgms-info.org/about-cgms/) establishes its international coordination function. The [official contact page](https://cgms-info.org/contact-us/) identifies the secretariat location in Germany. Store `DEU` as secretariat-country evidence in the organisation dictionary, not as the publication's national analytical country.
- **Creative Australia sectoral relevance.** The [official Creative Transformations report page](https://creative.gov.au/research/creative-transformations-results-national-arts-participation-survey) and [special-focus chapter on AI for creative purposes](https://creative.gov.au/sites/creative-australia/files/documents/2026-06/Special%20Focus%20Chapter_AI%20for%20Creative%20Purposes.pdf) directly support AI relevance in Australian arts participation. This is substantive cultural-policy evidence, not inference from an adjacent sector.
