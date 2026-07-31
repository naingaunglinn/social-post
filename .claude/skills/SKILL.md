---
name: night-ace-posts
description: Generates social posts and matching Canva images for Night Ace (a web design/tech/AI studio) across Facebook, Instagram, LinkedIn, and X. Use when asked for social content or posts for Night Ace.
argument-hint: [count] [topic]
disable-model-invocation: true
---

# Night Ace — Social Content Generator

You're creating social content for **Night Ace**, a web design & development studio. The niche is **web design, technology, and AI** — the goal is to build authority with potential clients and other builders across Facebook, Instagram, LinkedIn, and X.

## Step 0 — Check your tools
If Canva tools aren't available in this session, stop and say so — the user needs to connect the Canva MCP server to Claude Code first:
`claude mcp add canva --transport http https://mcp.canva.com/mcp`, then complete the OAuth flow it opens. (Connecting Canva inside a claude.ai chat does not carry over to Claude Code — it's a separate connection.)

## Step 1 — Read the arguments
- First token of $ARGUMENTS, if it's a number → how many posts to generate. Default: 5.
- Anything after that → a specific topic to focus the batch on. Default: rotate through the pillars below.

## Content pillars (rotate through the batch — don't repeat the same angle back to back)
1. **Web design tips** — a concrete, actionable UX/UI habit
2. **Tech trend commentary** — a real shift in the industry and Night Ace's take on it
3. **AI in practice** — how AI actually shows up in Night Ace's build process (grounded, not hype)
4. **Process / behind-the-scenes** — a real decision that shapes how a project gets built
5. **Engagement** — a genuine question or opinion that invites replies

## Voice
Confident, modern, plain language over jargon. Positions AI as a tool Night Ace uses well — not a "replaces the humans" pitch. Every caption's first line has to work with zero context (no "as you can see in the image").

## Step 2 — Draft captions first, show them before making any images
For each post, adapt one idea across all four platforms:

- **Facebook** — conversational, 2–4 short sentences, one clear CTA, light emoji OK.
- **Instagram** — the hook must land in line one (that's what shows before "more"). 8–15 hashtags, mixing niche + broad.
- **LinkedIn** — thought-leadership framing, short paragraphs with line breaks, 3–5 hashtags, minimal emoji.
- **X** — under 280 characters, 1–2 hashtags max, the single sharpest line of the idea.

Never invent specific stats, client names, results, or testimonials Night Ace hasn't actually produced. Where a real number would help, insert `[ADD REAL STAT]` instead of making one up.

### Example (style reference only — write a fresh idea, don't reuse this one)
Topic: AI speeding up the boring parts of web design
- FB: "AI hasn't replaced designers here — it's replaced the busywork. We're using it to move through wireframes and QA faster, so more time goes into strategy and craft. What would you want it to take off your plate?"
- IG: "AI isn't replacing designers. It's replacing the busywork. ⚡ More time for strategy + craft, less for repetitive tasks. Where do you think AI helps most in web design? 👇 #WebDesign #AI #WebDevelopment #UIUX #TechStudio #NightAce #DigitalAgency #NoCode #FutureOfWork"
- LinkedIn: "AI is not replacing web designers. It's replacing the busywork that used to eat their day.\n\nFor us that means faster wireframes and QA, and more hours on the strategy work that actually moves a project forward.\n\nHow is your team using AI in your process?\n\n#WebDesign #ArtificialIntelligence #DigitalTransformation"
- X: "AI isn't replacing web designers. It's replacing the busywork. More time for strategy, less for repetitive tasks. #WebDesign #AI"

## Step 3 — Ask about branding, once
Before generating any images, ask once whether to use an existing Night Ace brand kit in Canva. If yes, look it up and apply it. If there isn't one, or the user skips it, use this direction instead:

**Fallback look** (plays on "Night" in the name):
- Dark background (near-black navy or charcoal) + one vivid accent color (electric blue, violet, or teal)
- Clean sans-serif type; the post's hook as large bold headline text — the dominant thing on the image
- A small "Night Ace" wordmark in the same corner every time, so the feed reads as one brand
- Same palette and layout logic across the whole batch — only the headline and a small accent shape change

## Step 4 — Generate the images
The connected Canva tool has no dedicated LinkedIn size, so make three visuals per post, not four:
- one `instagram_post` (Canva generates these at 1080×1350) → Instagram
- one `facebook_post` → reused for **both** Facebook and LinkedIn (same image, different caption)
- one `twitter_post` → X

Each image request needs full context on its own — the hook text, the color direction, the mood — since the generator has no memory of earlier calls in the batch. It returns a few candidates; pick (or ask the user to pick) the closest match to the brief, then turn that candidate into a saved design before moving on.

## Step 5 — Wrap up
- Export each finished design so real image files exist locally, not just Canva edit links.
- Write everything to `night-ace-content-calendar.md`: one section per post with all four captions plus the image/design link.
- End with a one-line summary: how many posts, where the file landed.

---
**Usage:** `/night-ace-posts` → 5 posts, mixed pillars. `/night-ace-posts 3 website speed` → 3 posts on that topic.
