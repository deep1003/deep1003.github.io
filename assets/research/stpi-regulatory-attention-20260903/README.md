# STPI regulatory-attention figures and derived data

Snapshot: 3 September 2026

This directory contains slide-ready figures and derived data for the study of the
science-technology-policy interface (STPI) in AI regulatory attention.

## Measurement

- Policy activity is reconstructed from Digital Policy Alert lifecycle events.
- An intervention counts at most once in each jurisdiction-year and is weighted for
  jurisdictional scope.
- Topic shares use positive relevance-weighted mass in the common AI policy L3 space.
- The early and recent comparison uses 2020-21 and 2025-26. The 2026 observation is
  partial through 3 September 2026.
- Group values are unweighted means over a fixed set of countries observed in both
  periods. The available-country coverage is OECD 11 and EU members 4.
- “OECD observed” and “EU members observed” are sample estimates;
  they are not official OECD or EU aggregates.
- Science and technology source records come from the local Web of Science and
  PATSTAT research corpora. Recent patent counts are right-truncated.
- Semantic maps are two-dimensional PCA projections of L3 topic embeddings. They
  represent descriptive semantic proximity, not causal effects.

## Sources

- Digital Policy Alert: https://digitalpolicyalert.org/
- OECD membership: https://www.oecd.org/en/about/legal/privileges-and-immunities-agreements.html
- EU membership: https://european-union.europa.eu/principles-countries-history/eu-countries_en
- OECD visual identity: https://www.oecd.org/en/about/the-oecd-visual-identity.html

## Reproduction

The plotting and derivation script is `code/make_stpi_oecd_deck_figures.py`.
It expects the research-only source arrays and event panel documented in the manuscript
workspace. Public CSV files here are the complete derived inputs behind the displayed
figures, but do not redistribute licensed document text or embedding arrays.
