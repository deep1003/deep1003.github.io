# HEART anonymous risk comments

The existing pai-risk-survey-api Cloudflare Worker serves comments for all 55 L3 and 592 L4 identifiers. Existing survey routes are preserved.

Comments are stored in deep1003/Physical-AI-Risk-Survey-Responses under heart-comments/risks/<riskId>.json. The existing GH_TOKEN binding remains server-side. Browser clients receive no GitHub credentials.

Visitors do not sign in. A random 256-bit edit key stays in the author browser local storage. The server stores its SHA-256 hash and requires the matching key to edit. Clearing browser storage removes that browser's ability to edit previous comments. Comments and their revision history are public in GitHub. No name, email, or IP is stored by this application.

The Worker validates all risk IDs and input lengths, uses GitHub SHA conflict retries, and preserves comment IDs for safe retries. The UI renders comment text with textContent, loads threads on demand, and polls visible open threads every 30 seconds.

Run verification with `node --test tests/comments.test.mjs tests/comments-ui.test.mjs`. UI tests use jsdom from the local test dependencies. Deploy worker-with-comments.mjs through the existing Cloudflare Worker editor. original-live-worker.js is the pre-change backup.
