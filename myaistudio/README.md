# Studio test build

Fresh product source lives here. The repository's original root README is unchanged. Node.js 22.13 or newer is required. No frontend dependencies, remote fonts, analytics or CDNs.

## Install, run, test

From this directory: `npm install` (no dependencies), `npm start`, `npm test`. The dynamic server uses port 3000. This is a test build, not deployment authorization.

## First-page checkpoint

Working: public page, navigation, honest Stories empty state, one brief layout with expandable controls and field help, prototype brand enquiry (does not save/send).

Missing at this checkpoint: configured owner authentication, persistent films, pipeline execution, playable demos, generation backend and Stripe integration. Owner routes do not bypass sign-in. Mode is DEMO; storage and generation capabilities are separate.

Brand, defaults and provisional `brand_enquiries` purpose are in `src/config.mjs`. Public form audience and future commercial/payment rules remain undecided. No public pricing, posting or live collection.

## Storage, restart, backup and restore

No private persistence is enabled at this first checkpoint. Restart with `npm start`; no private save claim is made. Backup/restore will be documented with the persistent storage milestone. Do not commit secrets or private data.

## Assets and capabilities

The aperture illustration is original CSS made for this build. No external image, font, voice or music assets. All eight requested picker labels are preserved as labels only; no native app-runtime API or independent role assignment has been verified. Demo controls must not claim live generation.

## Pipeline checkpoint

Implemented: one server-validated shared brief, saved sample role outputs, source/translation-review scope, written boards, composable sound planning, producer handoff, honest blocked edit/review, draft marketing, optional one-time consolidated review, versioned settings-impact/returns, notes, restore-as-new-revision, manual retry and error history. Automatic mode reaches a sample planning result, not a brief-specific final cut. No owner approval is fabricated.

Private storage is SQLite with WAL, FULL synchronous transactions, read-back checks, opaque private PNG assets and server-side sessions. Set `STUDIO_DATA_DIR` to a protected directory **outside this Git repository**. The preview's local disk survives server restart only; it is not verified cloud durability and will not survive destruction of the sandbox. Set `OWNER_PASSWORD_HASH` through secure host environment configuration; no owner password or shared demo login is bundled. Hash format is 32 lowercase hex salt characters, a colon, then a 128 lowercase hex scrypt digest (64 bytes). Authentication requires both the hash and storage. Session cookies are HttpOnly, Secure and SameSite=Strict. Only offline tests permit insecure cookies with `NODE_ENV=test` and `TEST_INSECURE_COOKIE=true`.

Stop the server before backup. Copy the entire private directory (database and assets) to protected durable storage outside Git, retaining permissions. Restore that directory, point `STUDIO_DATA_DIR` to it, and restart. Sessions remain server-side but expire after eight hours; remove the `sessions` table's rows when restoring a backup if revocation is needed. Interrupted running stages recover as failed and require manual retry; previous errors/outputs remain. A cloud backup target is not configured in this build. Never put a private backup into a source commit.

Upload support is intentionally narrow: verified noninterlaced, 8-bit PNG with checked chunk structure, CRC, decompression size and restricted metadata. Other files are rejected, not trusted by extension. Uploading does not supply a production backend or make a cut.

## Stripe test-only integration

Uses the official server SDK and hosted Checkout in payment mode, restricted to `sk_test_` credentials and non-live objects/events. No public customer pricing. Required server-only fixtures: `STRIPE_SECRET_KEY`, `STRIPE_TEST_AMOUNT` (positive minor units), `STRIPE_TEST_CURRENCY`, `STRIPE_TEST_PRODUCT`, `STRIPE_RETURN_ORIGIN` (verified HTTPS native-preview origin). None has a production default. Optional signed test events require `STRIPE_WEBHOOK_SECRET`. Do not paste secrets into chat, public browser configuration or Git.

Checkout is separate from Films. Browser return flags do not determine state; session retrieval, verified session expiration or signature-verified test events do. Request and event deduplication are persistent; no film, release approval or entitlement is unlocked. No external Stripe test was run: credentials, technical fixture values and verified return/event-delivery access are missing. Declines inside synchronous hosted card checkout can leave a session open; this is pending, not falsely marked failed. API operation errors and asynchronous failure events have a distinct failed state. No public tunnel is created.

Official documentation fetched during this build on 2026-11-23: https://docs.stripe.com/testing ; https://docs.stripe.com/api/checkout/sessions/create ; https://docs.stripe.com/api/checkout/sessions/retrieve ; https://docs.stripe.com/api/checkout/sessions/expire ; https://docs.stripe.com/webhooks ; https://docs.stripe.com/api/idempotent_requests . SDK package version is locked in `package-lock.json`. Offline fixtures test mechanics, not a successful real Stripe integration.

## Complete prerecorded demo assets

`public/demos/story.mp4` is an 18-second miniature story, with beginning, reflected turn and resolved ending. `loop.mp4` is an 8-second original bead action loop. `story-v2.mp4` is a prepared private-reference alternative, not publicly served: amber ending instead of blue, with three louder closing notes instead of one. Only the first story and loop appear in the signed-out gallery. None belongs to Films or published Stories, and none was made from a later private brief.

All drawings/animation, story, captions, synthesized tones and assembly code are original for this project in `scripts/make-demos.py`. Narration uses the generic installed eSpeak NG English synthetic voice, not a real person's cloned voice or likeness. No music track or stock visual was obtained; no licensed-music claim is made. DejaVu Sans rasterized caption glyphs use the installed redistributable DejaVu font. Required credits are this provenance section and the “original local animation / prerecorded” player captions. Rebuilding demos requires Python 3, Pillow, NumPy, ffmpeg (H264/AAC encoder) and eSpeak NG, plus the DejaVu font at the path in the render script. Existing bundled MP4s need none of those tools at runtime.

The story has readable burned-in speech captions and explicit English VTT/SRT files. The optional player caption track is off by default to avoid duplicating burned text. Sample draft and sample-approved VTT exports name the same exact reference version as their MP4. Live subtitle timing/rendering/export is not configured. Public playback is local, user-initiated and has no model call, account, email or payment requirement. Missing media has an error message; no autoplay.

Audio/video automated checks decode all bundled assets, measure their true durations, check narration-window audio energy and the loop marker pulse timing, and distinguish the alternate ending. Browser tests exercise playback, seek and replay. **No manual listening pass has been performed by the assistant**; signal measurements and screenshots do not prove perceived audio quality. Human viewing/listening is still needed. Sample approval is explicitly not real release approval.

## Test evidence and current limits

`npm test` runs bounded Node tests for validation, dependencies, multilingual tracks, sound, storage failures/restart recovery, auth/private routes, deceptive uploads and offline Stripe signatures/state/deduplication. `npm run test:browser` runs Playwright against an isolated server with clearly fictional fixture credentials and briefs; these are never the preview owner login. Install Playwright Chromium for browser tests. `PLAYWRIGHT_CHROMIUM_EXECUTABLE` can point to an already installed Chromium. `EVIDENCE_DIR` sends screenshots outside Git (defaults to temporary storage). All private fixture directories are cleaned after testing. Do not add screenshot/evidence archives containing real private data to Git.

Known gaps: owner authentication is not configured in the native preview; no secure host secret-entry route was exposed in this task. Cloud durability/backup is unverified; preview persistence is limited to sandbox lifetime. All real native model runtime, generation, exact-language translation/voice/timing/rendering and media critique remain unverified. Text plans are samples, written boards are not images, sound plans are not audio, and a playable unrelated demo is not a cut for a brief. Stripe external tests (success, decline, cancellation, interrupted return and event delivery) remain unrun. Local/offline tests are not integration success. Arbitrary change notes are saved to a named stage but cannot alter prerecorded footage; only settings-impact sample reruns and prepared sample cuts are implemented. The build therefore delivers a tested **prototype**, not a complete live brief-to-film studio.
