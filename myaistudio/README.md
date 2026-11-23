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
