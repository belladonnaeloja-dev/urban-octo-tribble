# Ad-Variations extension — scale a discovered winner into ~50 creatives

This is the second capability bundled into `find-winning-products-2.0`: once the discovery
engine ([discovery-engine.md](discovery-engine.md)) has surfaced and confirmed a Pinterest
winner, this workflow turns that ONE winning creative into ~50 fresh ad variations bundled
into a single Pinterest "Mixed P+" creative-test campaign — the way a paid-media buyer
scales a proven winner.

**What it needs to run:** the downloaded winning video + product name, Shopify MCP
connected, Higgsfield MCP connected, Vmake API connected, and the Pinterest Bulk Editor to
upload the finished campaign. Reference walkthrough:
https://www.loom.com/share/decd2af2952447c98508708d2214670e

Five stages: (0) SOURCE the winner + exact-match competitor footage; (1) DECONSTRUCT the
winner into a preserve/vary brief BEFORE generating anything; (2) GENERATE the variations via
the levers — cv2 colorway recolors, PIL hook overlays, cv2 stitching, Higgsfield Marketing
Studio person/CGI clips; (3) add AUDIO (ffmpeg remux the winner's music onto silent cv2
outputs); (4) OUTPUT the Pinterest 163/165-column bulk-upload sheet. The engine is
**Higgsfield Marketing Studio + local cv2/PIL/ffmpeg**, NOT Creatomate.

Use this extension whenever the user wants to scale a winning ad this skill just found (or
any winning ad), "make ~50 creatives," build ad variations, spin a winner into a creative
test, or produce a Pinterest creative-test campaign — even if they don't say the word
"skill." Works on any store (Solundi = NL, Zanaro = DE); ask for store + language up front.

---

## Before you start — confirm two things

1. **Store + language.** Solundi = Dutch (NL), Zanaro = German (DE). This sets hook
   language and the destination product URLs. Never call `switch-shop`; work on whatever
   store is connected and ask the user to switch if it's the wrong one.
2. **The winner. ⛔ HARD STOP — ASK THE USER, AND WAIT, BEFORE DOING ANYTHING ELSE.**
   The whole workflow hinges on deconstructing the *right* winner, so confirming it is a
   BLOCKING first step, not a formality you resolve later. Before you source, mine ad
   libraries, download ffmpeg, extract store media, or run ANY tool: ask the user which
   creative is the proven winner and where the file/ad is, then STOP and wait for their
   answer. The best hand-off is the user dropping the winning `.mp4` locally (or a path
   like `~/Downloads/…`).
   - **NEVER infer the winner and run ahead on the guess** — even a confident, correct
     guess. A winning-looking clip in the product media (hook overlay + real creator +
     trendy aesthetic) is a strong *hypothesis*, not a confirmed winner with spend data.
     Name your hypothesis to the user if you have one, but make them confirm it. (Learned
     2026-07-24 on Zanaro VoluComb: the inferred pink-lit UGC clip WAS the real winner,
     but the user rightly flagged that guessing-then-building is the wrong order — the ask
     is cheap, a wrong-base 45-creative build is not.)
   - This ask is the point of no return for scope: only after the winner is confirmed do
     you spend tokens/tool-calls on Stage 0 sourcing and setup.

Copy rules apply throughout: no em-dashes; never state a delivery time; never claim free
returns (use "30 dagen geld-terug" / "retourrecht" or the German equivalent).

## Deliverable — ALWAYS one folder, all 50 together

Bundle the finished set into a SINGLE folder in the user's Downloads, named
`<Product>_Ad_Variations/` (e.g. `~/Downloads/Leona_Ad_Variations/`; keep the name
count-agnostic — the set often grows past 50). Create it at the start of Stage 2. EVERY one
of the ~50 finished creatives lands there and nowhere else, named by batch so they sort
(`A01_…`, `B01_…`, `H01_…`). Each file is fully finalized before it goes in: audio muxed
(Stage 3), transcoded to **H.264 + AAC**, and upscaled to **1080×1920** (Lanczos + light
unsharp; the winner is usually only 720p). Do all recolor / overlay / stitch scratch work in
the scratchpad — only the final creatives go in the folder. This folder IS the single
deliverable the user opens and feeds to the bulk sheet (Stage 4).

## The golden rule

**Preserve the winning DNA; vary only the surface.** Random variation is wasted ad spend.
Stage 1 (deconstruct) is not optional and must happen before any generation — the first
attempts on past products failed precisely because they skipped it (slim avatar + studio
setting on a product whose whole winning angle was a real plus-size woman in the street).

---

## Stage 0 — Source material

**MANDATORY: build a POOL of base clips, never work off the single winner alone.** Sourcing
is not just "get the winner" — it is "mine the ad libraries for every usable exact-match
competitor clip you can download," because each on-DNA clip is another A-style remix base
(more real base footage = more variations that aren't just the one winner re-hooked). Do this
every run, show the user a contact sheet of what you found, and let them cull. Skipping this
step (jumping straight to generation on one clip) is the #1 way this workflow under-delivers.

**HARD-FILTER every clip against the winner's audience AND the exact product model before it
goes in a montage** — this is not optional and the user should not have to catch it. If the
winner sells to women, DROP male-creator clips even when they're perfectly on-theme. If a clip
shows a visibly DIFFERENT product model (different frame shape/style than the store's actual
SKU), drop it or treat as inspiration only. "On-theme" is not enough; it must match WHO the
winner targets and WHAT the store actually sells. Re-check the Stage 1 audience/product signals
at cull time, not just at brief time.

**FB Ad Library is the workhorse and must always be mined** (public + downloadable):
navigate the in-app browser to
`facebook.com/ads/library/?active_status=all&ad_type=all&country=<GEO>&q=<term>&media_type=video`,
then read every `<video>`'s `currentSrc` in one `javascript_tool` sweep → tokenized fbcdn
`.mp4`s → download with a browser UA (use Python `urllib` with a UA header; the zsh shell
chokes on bash associative arrays). Dedupe by asset id, sample 2 frames/clip into a contact
sheet, and keep only the on-DNA ones. **Caveat: Ad Library serves ~360×640 previews** — fine
for Pinterest muted-autoplay after upscaling, but the sharpest base is still a higher-res
winner the user attached, so treat FB clips as volume, not hero.

- **BEST path for the winner: have the user attach it as a local file.** The simplest,
  most reliable way to hand off the proven winner is for the user to download the winning
  pin/ad themselves (on Pinterest: open the pin → download the video) and drop the local
  `.mp4` into the chat / point to its path (e.g. `~/Downloads/…VisionFit Video 3.mp4`).
  This sidesteps every login wall and tokenized-CDN hassle — go straight to Stage 1 on the
  file. It does NOT replace the pool-mining above; the attached winner is the hero clip, the
  FB Ad Library pool is the volume around it.
- **Iterate keywords per product.** Name the product the way its market names it. A
  bib-front dungaree romper is an "overall"/"dungaree," not a "jumpsuit" — the wrong word
  returns the wrong products. Try several.
- **Verify EXACT product match.** For gadgets/generic items, competitor clips are freely
  remixable. For **apparel or any variant product the customer would notice as different**,
  competitor footage is INSPIRATION ONLY — only reuse footage that is the exact product (or
  imperceptibly close).
- **Strip-text is two parts:** (1) remove the original baked-in text (Vmake), then (2) add
  text back in the store's native language. Erasing alone is not enough.
- **Sources & access:**
  - **FB Ad Library** — best: public, videos downloadable. Open the ad, play it, read the
    `<video>` element's `currentSrc` via javascript_tool → tokenized fbcdn `.mp4` → curl
    with a browser UA.
  - **Pinterest** — the IN-APP browser blanks/hangs on `/search/pins/` (bot-blocked), and a
    plain WebFetch returns an empty JS shell. The **user's logged-in real Chrome**
    (`claude-in-chrome`) DOES render search fine — drive it, `setTimeout`-wait ~3s, then scrape
    `a[href*="/pin/"]` for pin IDs (keep scroll loops SHORT — long CDP `Runtime.evaluate` loops
    time out at 45s on Pinterest's heavy renderer). Resolve each ID via the no-login pidgets API
    `widgets.pinterest.com/v3/pidgets/pins/info/?pin_ids=<comma-list>` and read
    `videos.video_list.V_720P.url` → curl. **Reality check for this niche:** Pinterest keyword
    search skews HARD to static product-listing image pins; usable on-DNA VIDEO pins are rare
    (a fit-over search returned ~19 pins, 1 video, and that one was off-DNA fashion eyewear).
    So Pinterest is where the user hand-picks a known winner (the BEST-path attach), NOT a bulk
    video mine. FB Ad Library is the bulk video source.
  - **TikTok — BEST method is Google short-video search → tikwm download (WORKS, gives 1080p
    no-watermark).** Do NOT rely on TikTok's own surfaces (see below). Instead: run a Google
    **short-video** search — `google.com/search?q=<niche terms>&udm=39` (udm=39 = "Korte video's"
    /Short videos) — in the user's real Chrome, scrape `a[href*="tiktok.com/"]` for
    `https://www.tiktok.com/@user/video/<id>` links, then download each no-login, no-watermark via
    the **tikwm API**: `https://www.tikwm.com/api/?hd=1&url=<url-encoded tiktok url>` → JSON
    `data.hdplay` (fallback `data.play`) → curl with a browser UA. This reliably returns **1080×1920**
    clips (higher-res than FB's 360p OR a typical winner), and Google's video index surfaces the
    exact niche UGC. **Run it as a SYSTEM, not one query:** each Google short-video query only
    trickles ~5-8 links, so ONE query is a peek — iterate **5+ angle/language-varied queries**
    (e.g. "<product> over glasses", "over prescription glasses", "<product> review", "<product>
    driving", plus the STORE-LANGUAGE term like "overzet zonnebril over bril"), scroll each ~5x,
    and **union + dedupe** across all queries (one real run → ~17 unique fit-over clips, incl.
    store-language ones). Skip near-dupes from the same creator. Baked-in TikTok captions →
    Vmake-strip then re-caption. First-class base-clip mine, second only to FB Ad Library.
  - **TikTok native surfaces (weaker, know the difference).** `library.tiktok.com/ads` (DSA
    Commercial Content Library) searches by **advertiser name only** — useless for creative
    discovery. `ads.tiktok.com/business/creativecenter` **Top Ads** does real content-keyword
    search (drive via the user's real Chrome; dismiss the Dreamina popup first) but returns the
    broad category (Ray-Ban / fashion / "$9 sunglasses"), not the narrow niche, and its videos are
    player-gated (not cleanly downloadable). Use Creative Center only for inspiration; use the
    Google→tikwm path above to actually GET TikTok base clips.
  - **Minea / WinningHunter** — no API; drive via the user's logged-in browser.

**⚠️ The store's OWN product-media clips (gallery "GIF" loops) are a LOW-QUALITY trap — do NOT
lean on them.** These animated webp/GIF loops in a Shopify product gallery are almost always
made FROM a real video found online (often ezgif-converted, e.g. `*-ezgif.com-video-to-webp*`),
downsampled to ~360-400px and a few fps — so they look soft/choppy next to real footage and drag
the whole set down. Before using ANY store gallery loop: (1) **try to source the ORIGINAL video**
it was cut from (it's usually one of the competitor clips you're already mining — the same demo
at full res; the FB Ad Library / tikwm pool typically SUPERSEDES the store loop outright), and
(2) if you can't find the original, **upscale it** (Higgsfield `upscale_video`, or at minimum a
Lanczos + unsharp ffmpeg pass) and eyeball whether it's acceptable. If neither yields a clip that
holds up at 1080×1920, DROP it — the competitor pool covers the same money-moment better.
**BANNED by Astrid (2026-07-24): do NOT use store-gallery GIF loops as source at all.** On
VoluComb the 400×400 loops stayed soft even upscaled while the competitor pool covered the same
barber-POV money-moment at native 1080p, so she ruled them out entirely. Treat "the store already
has demo clips" as a non-reason. (The only store asset you still use is a winner the user
explicitly confirms and hands over as a clean file.)

**Name every source clip with its VIEW/PLAY count in the filename, always** (e.g.
`pool_01_luxe_844k.mp4`, ranked highest-first). The count is used to judge each clip and to see
the ranking at a glance in the `_SOURCE/` folder. A source file without its view count in the
name is a bug.

## Stage 1 — Deconstruct the winner (mandatory, before any generation)

Extract WHY the winner works. That output IS the creative brief.

Method (no ffmpeg needed): use cv2 to sample frames — dense in the first 3 seconds (to
catch the hook), then roughly every 1.5s. Read the jpgs. Sort everything you see into two
buckets:

- **PRESERVE — the winning DNA, held constant across all 50:** hook mechanic, emotional
  driver/angle, target-audience signal (who is on camera), format/structure, setting type,
  visual style, sound/VO, social proof.
- **VARY — the test surface:** hook opener, colorway, setting, creator face/body, format,
  on-screen text.

Write this out explicitly and get the user's nod before generating. If the winner's driver
is "the creator IS the customer" (e.g. a real plus-size woman), that is the #1 thing to
hold constant — a clean but generic studio clip that loses it is a miss, not a variation.

## Stage 1.5 — Structure sign-off (MANDATORY, before any generation)

Before generating anything, present the user a **quick table of the batch mix** that will
make up the set (target ~45, hard cap 45 — see The blueprint below), then get their explicit
OK. This is the last cheap moment to change the plan; after generation it is not.

**⛔ THE SOURCE FOLDER MUST ALREADY EXIST AND BE HANDED TO THE USER AS PART OF THIS APPROVAL —
contact-sheet JPGs alone are NOT enough.** The user cannot judge whether the sourced material
is good from thumbnails; they need to open and WATCH the actual clips. So BEFORE (or in the same
turn as) presenting the mix table, assemble every kept source clip into a review folder and give
the user its path:
- Create `~/Downloads/<Product>_Ad_Variations/` now (do not wait for Stage 2) with a
  **`_SOURCE/` subfolder** inside it.
- Copy in: the **confirmed winner** (`winner_…mp4`), every **culled competitor clip** (named so
  they sort by value, e.g. `pool_01_luxe_844k.mp4`), and the **store's own gallery demo clips**
  (`store_demo_…mp4`). Transcode any webp/odd sources to normal H.264 mp4 so they play on
  double-click. Drop a one-line `_SOURCE/README.txt` mapping each file to its role
  (winner / competitor-plays / store-demo) and noting what was dropped and why.
- In the approval message, state the folder path explicitly (e.g. "open
  `~/Downloads/VoluComb_Ad_Variations/_SOURCE/` to watch the 14 source clips") and present it
  TOGETHER with the winner deconstruction + the mix table.
- Only after the user has the folder AND signs off on the table do you start Stage 2. If the
  user says the source material is weak, re-mine before generating — never build on a pool they
  haven't been able to inspect.

The table has one row per batch and MUST sum to **~45 (HARD CAP 45 — see The blueprint
section below; never exceed it, upload the complete set once)**. Columns: **Code · Batch ·
Type · Count · How it's made (lever) · VO / localization**. Tailor the mix to THIS product:
- Colorway/recolor batch → only for multi-variant apparel whose winner shows one colour;
  skip for single-variant products AND for winners that already show every colour.
- Plus-size / specific-persona person batch → only where the winner's DNA depends on it.
- Weight the count to the high-value batches (CRO stacks, combos); trim the filler
  (bare colorways, hooks) first.

**⛔ BOTH sign-offs are POP-UP PROMPTS (AskUserQuestion), NOT chat text, and they happen
ONE AT A TIME, in order.** Not every user reads long chat messages carefully — a prompt with
explicit options is what actually gets read and answered. So:

- **GATE 1 — SOURCE review (do this first, resolve it fully before the table).** After the
  `_SOURCE/` folder exists (see above), fire an **AskUserQuestion** asking the user to open the
  folder, watch the clips, and tell you whether the source material is good. Options along the
  lines of: *"All good, proceed"* · *"Remove some clips (tell me which)"* · *"Keep searching for
  more/better footage"*. If they name clips to remove, delete those from `_SOURCE/` and, if they
  ask, mine more; then re-confirm. Do NOT show the table yet.
- **GATE 2 — TABLE review (only after Gate 1 is settled).** Then fire a SECOND, SEPARATE
  **AskUserQuestion** with the batch-mix table, options like *"Approve, start generating"* ·
  *"Change counts / batches"*. Restate the revised table if they change it. Only start Stage 2
  after this second prompt is approved.

Never collapse the two gates into one prompt and never rely on chat-text alone for either.

Example (apparel winner, Solundi/NL) — matches The blueprint, sums to 45:

| Code | Batch | Type | Count | How it's made | VO/loc |
|------|-------|------|------:|---------------|--------|
| A | Winner-remix hooks | Video | 8 | real winner (Vmake-cleaned) + Dutch hook swaps + winner music; **A01/A02 = the winner's OWN hook translated literally** | NL captions |
| R | Colorway recolors (bare) | Video | 4 | cv2 HSV recolor to the store's real variants | NL text |
| M | Colour montages | Video | 2 | quick-cut colour / "welke kies jij" montage + music | NL captions |
| X | Multi-scene combos | Video | 9 | winner+hook opener → pool scenes (gens / CGI / UGC / detail) | NL captions |
| I | CRO conversion stacks | Video | 11 | 20-30s funnel: hook → proof → social → variety → CTA | NL captions |
| E | Person UGC gens | Video | 4 | Higgsfield product-locked × real-ref avatars/settings | **EN VO + NL captions (no dub)** |
| C | CGI / product motion | Video | 3 | Higgsfield showcase / hypermotion / camera-POV, silent | none |
| P | Cleaned-pin hooks | Video | 4 | 2nd exact-match base + Dutch hooks | NL captions |
| | **TOTAL** | | **45** | | |

## Stage 2 — Generate the variations (the levers)

Pick the levers that fit the product. Colorway recolor is powerful for apparel but
meaningless for a single-variant gadget/skincare/tool — skip it there.

**⛔⛔ NEVER COVER OR MASK BAKED-IN TEXT WITH A BOX, BAR, OR SCRIM. This is an absolute,
non-negotiable rule and violating it is the single worst recurring failure of this workflow.**
A dark/opaque rectangle placed over the original text — whether to "cover" a competitor's
English caption or to hide the winner's own baked-in hook — is FORBIDDEN. It looks cheap and
AI-made, it is exactly the "hard dark box" the hook-style rule already bans, and putting a
German line half over an English one is not localization. The ONLY correct way to change or
remove baked-in text is:

1. **REMOVE it cleanly with Vmake `videoscreenclear`** (the text-removal/background-correction
   pipeline in Stage 3 / Stage 0). This erases the original text and reconstructs the background
   underneath. Do this to the winner (to strip its own English hook before batch A), to every
   English competitor clip (batch P and any scene reused in M/X/I), and to any scene whose
   original text would otherwise show.
2. **THEN add the new German/store-language text in Style A** (white Avenir Next Bold + soft
   blurred drop shadow + thin dark outline, NO box) on the now-clean footage.

If Vmake is not available (no `MT_AK`/`MT_SK` credentials this session), STOP and ask the user
for them — do NOT fall back to bars/boxes. Clean removal is a hard requirement, not a nicety.
The winner's own hook counts: strip it with Vmake before overlaying a German hook; never let the
English show through and never black-box it.

**⛔ APPROVE EACH BATCH BEFORE STARTING THE NEXT — batch-by-batch pop-up prompts.** Do not
generate all of A, P, M, X, I and only then show them. Build ONE batch, render it fully into
the folder, then fire an AskUserQuestion for that batch (approve / fix specific ones / redo).
Only move to the next batch after the current one is approved.

**PRESENT EACH BATCH AS A PLAYABLE ARTIFACT, not "go check the folder."** Build a
self-contained HTML artifact that plays the batch's clips inline (a simple responsive grid of
`<video controls>` elements), so the user watches them in the browser and presses play. Since
artifacts must be self-contained (strict CSP, no external/local file access), **embed
COMPRESSED previews as `data:video/mp4;base64,...`**: transcode each clip to a small preview
first (`scale=-2:640`, `crf 30`, `-an` or low audio, aim <400KB each) so the page stays small
enough to publish. Label each with its code (A01…). The full-res deliverables still live in
the folder; the artifact is just the review surface. Then the AskUserQuestion references the
artifact. (Load the `artifact-design` skill before writing the page.) This catches a systemic
mistake (like a bad text-removal or a wrong cut) on batch A before it is repeated across 45
clips. The final Stage-3.5 whole-folder review still happens, but the per-batch gates come
first.

### Colorway RECOLOR (cv2) — exact-match multiplier for apparel
Per frame: convert to HSV, `inRange` mask the garment hue, `MORPH_CLOSE` + `dilate` to eat
the edge halo, Gaussian-blur the mask to feather. Within the mask, shift to the store's
REAL colors: for a new hue keep S/V and set H; for **black** multiply S≈0.18, V≈0.14; for
**white** S≈0.08, V≈0.40 then +160. Write with `cv2.VideoWriter('mp4v')`. Roughly 380
frames × 3 colors ≈ 12s of compute. Output is SILENT (see Stage 3). Recolor to the store's
actual variant list, not arbitrary colors.

### HOOK overlay (PIL + cv2)
Keep it PROFESSIONAL — do NOT use Arial and do NOT use a hard dark-gray box (both read as
cheap/AI). Use **Avenir Next Bold** (`/System/Library/Fonts/Avenir Next.ttc`, size ≈
frame-width × 0.056). **Default = style A (proven on Leona): clean white text + a soft
blurred drop shadow + a thin dark outline (`stroke_width≈fs/22`), NO box.** Alternatives if
the user prefers: (B) a branded rounded pill in the store's brand colour (Solundi mint-green
`(9,182,120)`, white text), or (C) white text over a subtle top gradient scrim. Use A unless
the user asks otherwise. Build the RGBA layer once, alpha-composite onto the first ~4s of
frames, fade out over the last 0.6s. Render at the 1080×1920 output size, not the 720p
source. 1 base × N hooks = N variations. Write hooks in the store's language, copy-rule-
compliant.

### STITCHING / multi-scene (cv2 or ffmpeg concat)
Normalize every clip to the 1080×1920 output @ 30fps, then write segments sequentially (ffmpeg
concat demuxer is more robust than cv2 for mixed sources) — hard cuts read fine. Shapes: (1)
**colorway montage** — the same ~3s hero shot across all recolors + a hook on scene 1; (2)
**multi-scene combo** — the opener MUST show the product + a hook.

### UGC-COMPILATION MONTAGE (the #1 way to scale a UGC winner) — full recipe
When the winner is a multi-creator UGC compilation (quick cuts of real people using the product,
persistent caption, music), THIS is the format you replicate from the sourced pool — not a single
talking clip. **Why:** ~85% of social video is watched muted and Pinterest autoplays silent, so a
whole talking-head clip is wasted; a montage of quick visual "money-moments" + music bed + native
on-screen text carries the message with the sound off. **Corollary: the spoken LANGUAGE in the
source clips is irrelevant** (Dutch, English, Finnish — doesn't matter, it's muted) — select clips
for the VISUAL demo moment, not the audio. Build it:
1. **Cull to audience + product model first** (see Stage 0 hard-filter): women-only if the winner
   is, matching frame style only. Drop off-persona / different-SKU clips even if on-theme.
2. **Vmake-strip baked captions BEFORE cutting** (`videoscreenclear`) — every TikTok/FB UGC clip
   has burned-in captions at varying heights; cropping can't remove them reliably and foreign text
   clashes with your native overlay. Strip first, then you have clean footage to caption. (Once
   stripped you do NOT need the zoom-crop; use the full clean frame.)
3. **Find the money-moment window per clip** — filmstrip each clip (6 thumbs w/ timestamps), pick
   a ~2.0-2.5s window showing the hook action (holding the product up, putting it on, the reaction).
4. **Normalize fps to 30** — some TikToks are 60fps; if you copy frames 1:1 they play 2x too long.
   Subsample by `round(src_fps/30)`, and `cv2.resize` every frame to 1080×1920.
5. **Hard-cut concat ~8 clips ≈ 16-18s** (match the winner's length/pace).
6. **Overlay (Style A):** persistent native value-prop bottom + a top hook on the first ~4s (fade
   out last 0.6s). cv2 output is SILENT.
7. **Music bed (ffmpeg):** extract the WINNER's own audio once (`-vn -c:a aac`), then loop it under
   the silent montage and finalize in one pass:
   `ffmpeg -stream_loop -1 -i winner_music.m4a -i montage.mp4 -map 1:v:0 -map 0:a:0 -shortest
   -c:v libx264 -crf 23 -pix_fmt yuv420p -vf unsharp=5:5:0.4 -c:a aac -b:a 128k -movflags +faststart out.mp4`.
   (Don't mux the winner's TALKING VO onto a montage of different faces — extract its music/trending
   sound; if the winner audio is VO-heavy, use a different clip's trending audio. `generate_audio`
   is speech-only — it canNOT make music.)

**APPAREL COMBOS — QC the garment on every segment.** A long winner is a GOLDMINE: it usually
holds 3-5 distinct real-dress scenes (different colourways / couples / rooms) — a reliable,
zero-drift source, so cut freely from those: `[scene A + hook] → [scene B, different colour] →
[scene C]`. Generated clips (Higgsfield UGC, image-to-video) are ALSO welcome in combos — the
rule is not "no generation," it is **look at each generated clip and only use it if its garment
actually matches the real product.** Higgsfield person-gen sometimes drifts into a
similar-but-DIFFERENT dress; that mismatch is glaring next to real scenes. So sample a frame of
every generated clip, compare it to the product, and drop/regenerate the drifters — never stitch
a wrong-dress segment in. When you need a guaranteed-match generated clip, **image-to-video from
the real product photo** (`kling3_0_turbo`/`seedance_2_0`, photo as start_image/reference) holds
the garment best.

### Higgsfield Marketing Studio (net-new clips)
`generate_video model=marketing_studio_video`, one MCP call per clip. Register the product
once (`show_marketing_studio action=create type=product` → product_id). Formats:
- **Person-based** (`ugc_virtual_try_on`, `ugc_before_and_after`, `ugc_selfie_testimonial`):
  force an on-camera creator + spoken VO. **ALWAYS generate the VO in ENGLISH** — Higgsfield
  cannot produce flawless Dutch/German (or any non-English) voiceover; the mouth-sync and
  pronunciation come out wrong. Write the whole prompt/script in English. **Then LOCALIZE with
  Dutch/German on-screen captions, NOT an audio dub** — Pinterest autoplays muted, so the English
  VO is a non-issue and a Dutch caption carries the message cleanly (add it with the same
  timed_caption white-box tool; keep the English audio underneath for the unmuted minority).
  Audio dubbing to NL is NOT available in our stack: Vmake does watermark/text removal + enhance
  only (no dubbing), and Higgsfield `dubbing` supports German (`deu`) but NOT Dutch (`nld`). So
  for Solundi/NL, caption; for Zanaro/DE, Higgsfield `dubbing target_language=deu` is an option.
  Never hand Higgsfield a Dutch/German VO line and expect clean output.
- **CGI garment-only** (`product_showcase`, `hypermotion_oj`): no person, genuinely silent
  → best for muted autoplay and zero localization.
- Levers: mode/preset, `hook_id`, `setting_id` (hook/setting only apply to UGC / Tutorial /
  Unboxing / Product-Review / UGC-Try-On), avatar, `ad_reference_id`, aspect_ratio,
  generate_audio.

**Plus-size (or any body/persona the winner depends on) custom avatars:** Marketing Studio
has no curvy preset. Source a REAL free-license portrait (Pexels/Unsplash) → `media_import_url`
→ get its Higgsfield CDN url via `show_medias` → `show_marketing_studio action=create
type=avatar` with `medias:[{value:<media_id>, type:media_input, role:image, url:<CDN url —
the cloudfront/cdn.higgsfield host, NOT the Pexels url>}]`. Never scratch-generate a body;
it looks fake. Ground on a real reference.

### Higgsfield generate_image gotchas
The full prompt goes in `params.prompt` (a top-level `prompt` is ignored); set `model` in
both places; media role is `"image"`; `nano_banana_pro` renders text best.

## Stage 3 — Audio (needs ffmpeg)

All cv2 outputs are SILENT (OpenCV strips audio); only true originals keep sound. Needs
ffmpeg. **`brew install ffmpeg` usually can't run headless** (Homebrew often isn't installed
and installing it wants an admin password you can't supply) — so grab a **static ffmpeg
binary** instead: on Apple Silicon use an arm64 build (`https://www.osxexperts.net/ffmpeg71arm.zip`;
evermeet.cx builds are Intel-only and fail with "bad CPU type"), unzip, `chmod +x`, and call
it by path. Do: extract the winner's audio once to a reusable file; (1) mux the winner's own
music onto the winner-aligned clips (recolors, hooks, montages) with `-map 0:v -map 1:a`; (2)
for non-aligned clips (Higgsfield gens, CGI, the pin) loop that track as a music bed
(`-stream_loop -1 -i music -i video -map 1:v -map 0:a -shortest`). Do the audio mux and the
1080×1920 upscale (`-vf scale=1080:1920:flags=lanczos`, unsharp) in the SAME ffmpeg pass that
transcodes to H.264 + AAC (**crf 23**, see the export-spec note in Stage 4) and writes the file into the output folder. Nothing ships
silent or below 1080p.

**Vmake text-removal (Stage 0 strip step) is SDK-based, working:** the user's Vmake dashboard
(`vmake.ai/developers` → Doc) links a Python SDK zip; download it, `pip install --user
alibabacloud_oss_v2`, import as `sdk`. Auth = SDK-HMAC-SHA256 via env `MT_AK`/`MT_SK`.

**⭐ CREDS LIVE IN macOS KEYCHAIN — never ask the user for them if they are already stored,
and never treat them as session-only.** The keys were being lost because past runs only set
them as shell env vars, which die with the session. Fixed by persisting them in Keychain ONCE.
Every run: load them from Keychain into env before using the SDK —
`export MT_AK="$(security find-generic-password -s vmake_mt_ak -w 2>/dev/null)"` and
`export MT_SK="$(security find-generic-password -s vmake_mt_sk -w 2>/dev/null)"`. Only if BOTH
come back empty do you ask the user, and then you store them so it never happens again:
`security add-generic-password -a vmake -s vmake_mt_ak -w '<AK>' -U` (and `vmake_mt_sk`). Prefer
having the USER run the `add-generic-password` command themselves so the secret never enters the
chat transcript. The secret never goes in a skill file, memory, or committed file — Keychain
only. `SkillClient().run_task(task,
<file-or-url>)`; video task = **`videoscreenclear`** (async → if it poll-times-out it returns
a `task_id`, resume with `poll_task_status(task_id)` and set `MT_AI_POLL_MIN_TOTAL_MS≈600000`,
`MT_AI_POLL_EXTEND_STEP_MS=8000`; never 0). Result `output_urls[0]` = de-texted mp4.

## Stage 3.5 — Video review sign-off (MANDATORY POP-UP PROMPT, before Stage 4)

**⛔ Once ALL creatives are finalized in the `~/Downloads/<Product>_Ad_Variations/` folder,
STOP and fire an AskUserQuestion asking the user to open the folder, watch the videos, and
confirm they are all okay BEFORE you build or finalize the Pinterest bulk sheet.** The
finished videos are the real deliverable; the user must be able to eyeball the actual files
(not a contact sheet) and catch anything wrong — English text bleeding through, a bad cut, a
wrong caption — while it is still cheap to re-render. Wait for all 45 to exist and be final
(audio muxed, upscaled), THEN prompt with options like *"All good, build the sheet"* ·
*"Some need fixing (I'll say which)"* · *"Re-do a batch"*. Do NOT start Stage 4 until the
user approves the videos. If they flag specific files, re-render just those and re-prompt.
(Same spirit as the Stage-1.5 source gate: real files in a folder + a prompt, never chat text
alone, never skip ahead to the sheet.)

## Stage 4 — Output: Pinterest bulk sheet

**BUILD BY CLONING THE LAST KNOWN-GOOD UPLOADED SHEET — never hand-author the campaign/ad-group
config.** This is the #1 reliability rule: a past upload failed purely because the config was
re-derived from scratch and "improved" (added conversion windows, DAILY budget, no brackets).
The safe method: open a proven sheet that already uploaded clean, keep its header + `#` rows,
take ONE data row's full config **VERBATIM**, and per creative override ONLY: `Media File Name`,
`Ad Format`, `Pin Title`, `Pin Description`, `Organic Pin URL`, `Promoted Pin URL`,
`Promoted Pin Name` — plus once at campaign level: `Campaign Name`, `Campaign Start Date`,
`Ad Group Name`. Do NOT touch bidding / budget / targeting / conversion cells.

**⭐ `Pin Title` = the WINNER's own hook, translated to the store language, on EVERY pin
(default rule).** The winning video's hook is proven copy, so it becomes the constant Pin-title
anchor across all pins while the on-VIDEO hook is the thing that varies (batch A swaps, batch P
keeps each clip's localized text). Read the winner's baked-in hook in Stage 1, translate it to
the store language, and drop that one line into `Pin Title` for all 45 rows. Only deviate if the
user gives a different title.

**⭐ The winner's own hook, translated literally, is ALSO a Batch-A on-video variation — always,
by default, without being asked.** The proven hook is the strongest line in the whole set, so it
must appear ON the video (Style A, on the Vmake-cleaned winner footage) as A01 or A02 — do not
fill batch A with only paraphrases and leave the literal winning line out. The remaining A slots
are fresh hook angles around it.

If no known-good sheet exists yet, match this proven config EXACTLY:
`Campaign Objective=SALES` · `Creative Source=STANDARD_AD` · `Campaign Status=PAUSED` ·
`Campaign Budget=YES` + `Daily Spend Limit=10.00` + `Performance+ daily budget=YES` +
`Campaign Start Date=[YYYY-MM-DD]` + `Campaign Start Time=[00:01]` · `Ad Group Budget Type=CBO` ·
`Ad Group Pacing Type=STANDARD` · `Ad Group Status=ACTIVE` · `Is Creative Optimization=NO` ·
`Performance+ Targeting=YES` · `Ad Placement=ALL` · `Conversion Tag ID=CT<id>` ·
`Conversion Event=CHECKOUT` · `Conversion Optimization=CONVERSION_VALUE` · `Bid strategy type=AUTOMATIC` ·
**Click/Engagement/View Window Days = ALL BLANK** · `Locations=[NL]` · `Genders=[female,unspecified]` ·
`AgeBuckets=[25-34,35-44,45-49,50-54,55-64,65+]` · `Languages=All` ·
`Devices=[web,ipad,web_mobile,iphone,android_mobile,android_tablet]` · `Interests=[]` ·
`Grid Click Type=DIRECT_TO_DESTINATION` · `CTA Selection=SHOP_NOW`. CBO = budget lives at CAMPAIGN
level (no per-ad-group budget, no ad-group start date). Map every column by header NAME, not index.

**Campaign-level Performance+ is NOT settable from a bulk sheet — accept it, and NEVER propose
mixing manual UI creation with the sheet.** Verified across all 165 V2 columns: there is no P+
master-toggle column. The only P+ fields are `Performance+ daily budget` (campaign, CBO) and
`Performance+ Targeting` (ad group) — both of which we DO set to `YES`. So a sheet-built campaign
runs with **P+ bidding + P+ targeting ON but the campaign P+ toggle OFF**, and that is fine. Keep
the campaign 100% bulk-sheet — do not create a shell in the UI and upload ads-only; mixing manual
creation with a bulk sheet is a recipe for disaster. Keep the `Mixed P+` campaign name, build the
whole campaign from the sheet via the clone method above, and move on.

**DOWNLOAD a FRESH sample sheet from the bulk editor each campaign** — Pinterest changes the
template over time (it moved from a 163-col to a **165-col V2** template in 2026-07; old sheets
built on the previous template get REJECTED). Build on the CURRENT sample's exact header, never
a saved one. Key current values: **Objective = `SALES`** (not the dead `WEB_CONVERSION`), new
required **`Creative Source` = `STANDARD_AD`**, **`Conversion Tag ID` = `CT<id>`** (CT prefix),
**`Ad Format` = `VIDEO`** (every creative is a video — this workflow does not produce statics),
keep BOTH `#` instruction rows. Never hand-trim columns; one row per ad; bracket lists/dates like
`[NL]` / `[2026-07-23]`. Only Media File Name / Pin Title / Pin Description / Promoted Pin Name
change per row.

**⚠️ #1 CAUSE OF A FAILED SALES UPLOAD — error 2374 (leave conversion windows BLANK).** For a
SALES + `Bid strategy type=AUTOMATIC` campaign you MUST leave `Click Window Days`,
`Engagement Window Days`, `View Window Days` **empty**. Filling any of them →
`2374: Conversion windows are not available for ad groups with automatic bidding`, which is a
PARENT ad-group error that **cascades**: every child ad then shows `2019: error in one of the
parents`, and every VIDEO row ALSO shows `2897: Error processing creative ad`. So `2897` on all
your videos is a RED HERRING — the videos are fine, the ad group is invalid. Fix the parent, do
NOT touch the creatives. Valid SALES ad group = `Conversion Tag ID=CT<id>`,
`Conversion Event=CHECKOUT`, `Conversion Optimization=CONVERSIONS` (or CONVERSION_VALUE),
`Bid strategy type=AUTOMATIC`, and NO windows.

**⚠️ #2 CAUSE OF A FAILED UPLOAD — `Interests=[]` (must be BLANK, not bracket-empty).**
Every other list field uses the bracket format (`Locations=[NL]`, `Genders=[female,unspecified]`,
`Devices=[...]`), but **`Interests` must be left completely EMPTY**. Writing `[]` there is a
parent-level error and cascades exactly like 2374: every child ad returns
`2019: There is an error in one of the parents`. Proven correlation in a past results CSV: rows
with `Interests=''` → SUCCESS; rows with `Interests='[]'` → failed 2019 across the board. So:
bracket-empty is NOT a safe default; leave `Interests` blank.

**⚠️ WHEN CLONING A KNOWN-GOOD SHEET, CLONE A ROW WHOSE `Status` IS `SUCCESS`.** Do not grab
the first data row — a results CSV interleaves succeeded and failed rows, and the first row may
be a FAILED one carrying exactly the poison value (this is how an `Interests=[]` bug propagated
into a later sheet). Load the previous `bulk_results*.csv`, filter to `Status == SUCCESS`, and
use that row as the template. Then diff your new sheet's parent-level columns against that
SUCCESS row before uploading — any difference is a suspect.

**Status hierarchy (one-switch launch):** `Campaign Status=PAUSED`, `Ad Group Status=ACTIVE`,
`Promoted Pin Status=ACTIVE`. A paused campaign overrides all children (nothing serves), so the
whole thing is armed and the user goes live with ONE campaign-level toggle. Never set the ad
group or ads to PAUSED.

**⚠️ #3 CAUSE OF A FAILED UPLOAD — REUSING MEDIA FILENAMES ON A RETRY (CONFIRMED).**
When an upload fails, Pinterest has usually STILL ingested the video files and created organic
pins for them (you can see `Existing Pin ID` populated on failed rows). Retrying with the SAME
filenames then collides with those pins and the whole thing dies — two consecutive uploads
returned `2019` on EVERY row and created no ad group at all. The moment the files got a new
suffix (`_x`) AND were re-muxed so the bytes/hash changed, the identical sheet created the
campaign, the P+ ad group, and the ads. **So on ANY retry after a failure: give every file a
new suffix, change its bytes (`ffmpeg -i in.mp4 -c copy -metadata comment=<stamp>` suffices), and
give the promoted pins new names.** Suspect this FIRST when a re-upload fails wholesale — do not
burn time diffing config columns. (Beware the false leads: `Interests=[]` and the Performance+
block both look guilty in a results-diff and are both innocent; a P+ ad group creates fine via CSV.)

**EXPORT + UPLOAD SPEC that prevents the `2897` "Error processing creative ad" timeouts.**
`2897` on a SUBSET of rows (ad group valid, other rows SUCCESS) is Pinterest's async video
processor overloading — NOT a bad file. Size/duration/bitrate does not predict it; it behaves
like a concurrency ceiling. So:
- **Export at `-crf 23`, never 18.** crf 18 gives 7-11 Mbps / 15-25 MB per clip — wasted bytes,
  Pinterest re-encodes anyway. crf 23 is ~45% smaller with no visible loss at mobile 1080×1920,
  and lightens the processor.
- **Still upload the whole set (≤45) in ONE pass** — do NOT split it into small batches. One
  upload plus, at worst, one recovery pass beats several manual uploads. crf 23 is the lever
  that reduces processor load; batching is not.
- **Treat `2897` stragglers as a NORMAL, cheap second pass, not a failure.** If a subset returns
  `2897`, generate the fixup sheet straight from the results CSV: only the failed rows,
  `Campaign ID` + `Ad Group ID` from any SUCCESS row filled in, `Campaign Objective` +
  `Creative Source` blanked, and — critically — **renamed + re-encoded media** per the retry rule
  above. Worst case is two uploads total.

**Fixup for TRANSIENT stragglers (only if a SUBSET of videos fail while the ad group is valid).**
Distinguish from 2374: if ALL videos fail → it's the parent (2374), fix the ad group. If only
SOME fail `2897` (others SUCCESS) → Pinterest's async video processor just timed out. Read the
results CSV `Status` column; grab the created `Campaign ID` + `Ad Group ID` from any SUCCESS row;
build a fixup sheet with ONLY the failed rows, set those two IDs, BLANK `Campaign Objective` +
`Creative Source` (unavailable on EDIT), and re-upload the fixup + just those media files. This
attaches them to the existing campaign/ad group (no duplicates). Re-run if a couple still
straggle. But per the cap rule above, prefer a clean ≤45 single upload.

- Campaign name pattern: `Mixed P+ | <GEO> | Creative Test - <Product> | DD-MM-YYYY | Conversions`
- Start time: 00:01 the next day.
- Upload leg is DECIDED: **bulk sheet, no Zapier** (Zapier can post organic image pins, but
  not video pins or campaigns).

---

## The blueprint (proven mix) — TARGET ~45, HARD CAP 45

**CAP the set at 45 creatives and upload it ONCE, complete, before the campaign goes live.**
Do NOT plan to append creatives to an already-live campaign later — the Pinterest bulk editor
is very error-prone for adds-to-live. Build the whole ≤45 set, upload in one clean pass (chunk
the *video* upload into ~30s if the processor drops stragglers), verify every row = SUCCESS
(auto-build a fixup sheet referencing the created Campaign/Ad Group IDs for any that fail),
THEN the user flips the campaign live. One campaign, one upload, done.

A balanced ~45 — do NOT let bare colorways dominate the count (a no-text recolor is a weak
standalone ad; the colours earn their keep inside hooks/montages/combos). Weight the count to
the high-value batches (CRO stacks, combos, gens); trim the filler (bare colorways, hooks) first:
- **Colorway recolors (bare, no text): CAP at ~4.** Only the hero colours as standalone ads.
  The full colour range still appears via hooks + montages + combos.
- **Hook × colour: ~8.** Colourways with a Dutch/localized text hook.
- **Colour montages: ~2.** "in N kleuren" / "welke kies jij" / "S–5XL".
- **Multi-scene combos: ~9–10 (aim high here).** Combos are the richest, most varied
  format and should carry real volume — winner+hook opener → different second/third scenes
  pulled from the whole pool (detail/rear shots, plus-size gens, CGI showcase, selfie, colour
  flashes). Vary the structure across the ten, not just the hook.
  **⭐ Combos (X) BEAT fast quick-cut montages (M) — weight X higher than M.** Default split ≈
  **X 10 : M 6** (the winner-led narrative build with fuller ~4.5s scenes reads far better than a
  7-cut blur). On a single-variant product (no colourway montage angle at all), lean even harder
  on X and keep M small.
- **CRO CONVERSION STACKS: ~11 (the highest-value batch — protect this count when trimming to
  45; build these as a senior CRO e-commerce video editor, not a lazy "winner + 1 clip").** Winner
  leads (as its 3s hook, OR the full winner, OR winner+text-hook), then a DEEP stack of new
  evidence pulled from the WHOLE pool, arranged as a real conversion narrative:
  **HOOK → product/demo → fit proof (detail/rear, close-up) → transformation or testimonial
  (before-after, selfie/UGC) → social proof (duo, "S–5XL") → variety (colour flashes / "in N
  kleuren") → CTA ("Shop nu op <store>").**
  Rules that make these convert: (1) **length ~20–30s** (Pinterest allows it — do NOT ship
  thin 7–16s cuts); (2) **stack 5–8 scenes**, endless combinations of the found + generated
  clips — the winner is the HOOK, the stack is the value, so never let the winner dominate the
  runtime (a 3s hook wants a ~25s tail; even a full-winner lead still needs a substantial tail,
  not +3s); (3) **native-language captions at the beats** (hook, one benefit, CTA), copy-rule
  compliant; (4) **winner music bed across the whole thing**; (5) vary the NARRATIVE across the
  ten (ugc-stack, transformation, why-everyone, detail-quality, problem→solution, testimonial-led,
  colourway-showcase, max-stack, etc.), not just the hook.
  **Always evaluate after building** — contact-sheet 5 frames/clip, read them, and RE-CUT any
  that lean too hard on the winner or where a beat (e.g. colour flashes) is too brief to read.
  Colour note: the winner colour and the gens' colour may differ across scenes — that reads as
  authentic multi-customer/multi-colour social proof (fine, often good); only force a single
  colour if the user wants ultra-clean hero cuts.
- **Person UGC gens (Higgsfield) + CGI product-motion: NOT standalone ad batches — they are
  INGREDIENTS, generated ONLY as scenes/b-roll to drop into combos and CRO stacks, and ONLY when
  you lack real material.** If the exact-match competitor pool is strong, generate ZERO
  person-UGC — real footage always beats a gen, and a gen only earns its place when there's a
  demo moment you genuinely can't source. Likewise CGI: make a couple of silent product-motion
  clips only if a stack needs a slick b-roll beat, never as its own ad. Do not pad the count with
  gens when real clips exist.
- **Competitor-clip ads (batch P): LOCALIZE the clip's OWN on-screen text, do NOT strip-and-
  replace with your own hook.** The competitor's baked-in caption is proven copy for that exact
  footage, so keep its message and placement and just TRANSLATE it into the store language
  (English "from flat to full of texture" → German "von platt zu voller Textur"); clips already
  in the store language stay untouched. One localized ad per strong competitor clip — each is
  its own variation. Only fall back to the strip-then-new-hook method (Stage 0) when a clip's
  original text is off-message or unreadable.

That sums to ~45. EVERY creative is a video: this workflow does not produce static image ads.
The apparel math still holds (many real colorways × hooks = lots of exact-match remixes), but
spend the colour depth on hooks/montages/combos, not on bare recolors — and never exceed 45 to
keep the one-shot upload clean.

## Core principles

- Preserve DNA, vary surface (Stage 1) — this is the whole game.
- Ground person avatars on real references; never scratch-generate a body.
- **Garment fidelity: QC every generated apparel clip with a SIDE-BY-SIDE vs the product photo,
  against a per-product feature CHECKLIST.** Generated clips are fine (great, even) WHEN the
  garment matches; the failure is Higgsfield drifting into a DIFFERENT dress. Eyeballing a lone
  frame is NOT enough — a clip can category-match ("cream backless maxi") while actually being the
  wrong dress. So: (1) at Stage 1 write the garment's **distinguishing features** — silhouette,
  fabric, the exact back treatment, straps; (2) build a hstack montage `[product photo | winner
  frame | each generated frame]` (PIL) and LOOK — drift is invisible solo, obvious side-by-side;
  (3) fail a clip if ANY feature differs. Note: couple/date presets tend to drift apparel into
  fancy eveningwear; try-on/showcase presets hold shape better. Guaranteed-match sources: the
  winner's own scenes, an exact-match ad-library pool, or image-to-video from the real product
  photo.
- Colorway recolor is product-dependent: clothing yes, single-variant no.
- **Never write "cinematic" (or "film/movie/widescreen") in a generation prompt** — it biases
  the model toward a letterboxed, widescreen, film-bar look. Always want full-frame **tall
  9:16 vertical**, phone/UGC framing edge-to-edge. Say "vertical 9:16, full-frame, phone-shot,
  no black bars" instead.
- Copy rules: no em-dashes; no delivery-time claims; no free-returns claims.
- One canonical thread per product — don't run two builds in parallel; they clobber the
  same files.

## Security

Never type or store third-party passwords (Higgsfield etc.). Rely on the user staying logged
in or on existing browser sessions.
