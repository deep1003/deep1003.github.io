# Row-level scenario risk search

The unchanged v10 taxonomy contains 55 L3 categories and 592 active L4 cards. Each confirmed scenario is searched independently. Number and title identify an input row; all other source columns are excluded from the query.

Markdown and CSV readers select tables by their scenario-column header. PDF text coordinates are used to select that column and continue rows across pages. Other impact-assessment tables are ignored. Flattened text whose columns cannot be recovered enters a manual correction preview and cannot be searched until scenario-only rows are supplied. The preview remains editable.

Output is a flat L4 list per input scenario, sorted by the internal retrieval score, with the parent L3 and canonical IDs. No domain regrouping is applied. The ranking combines length-normalized lexical weights, concept matches, character overlap and soft application-condition penalties. It is not a sentence-embedding model, a calibrated percentage or a measure of risk probability or severity. Its relevance quality requires separate human evaluation.

Browser tests cover the actual uploaded Markdown and PDF, a CSV, and flattened copied text. Automated tests verify column isolation, blank row preservation, PDF continuation, mixed-input review, payload preservation, language consistency and existing anonymous comments.
