# Policy Commons contamination and country-attribution criteria

This register records error types that must be checked in every future dataset. Each new error must be added with a failing example and a counterexample that should remain included.

## Core rules

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
