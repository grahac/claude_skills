---
name: product-naming
description: Generate creative, memorable product and company names with available .com or .ai domains. Use when users need naming help for products, companies, apps, or services. Specializes in portmanteaus, puns, alliteration, and unique brandable names under 10 letters with domain availability checking.
---

# Product Naming Skill

Generate creative, memorable, and brandable product/company names with verified domain availability.

## Process Overview

1. Gather product context and industry information
2. Generate 20 initial name suggestions categorized by style
3. Check domain availability in real-time using whois
4. Collect feedback on liked/disliked names
5. Iterate with refined suggestions based on preferences
6. Provide trademark checking guidance for final selection

## Step 1: Gather Context

Ask the user for:
- **Product/company description**: What does it do? What problem does it solve?
- **Target audience**: Who will use it?
- **Industry/category**: What sector (tech, healthcare, finance, etc.)?
- **Brand personality**: How should it feel? (playful, professional, innovative, trustworthy, etc.)
- **Any specific requirements**: Words to include/avoid, specific themes, cultural considerations

Keep questions natural and conversational. Don't ask all at once—start with the most important.

## Step 2: Generate Initial Name Suggestions

Generate exactly 20 name suggestions, categorized by creative style:

**Portmanteaus** (blend two words):
- [5 names combining relevant words]

**Puns & Wordplay** (double meanings, homophones):
- [5 names with clever linguistic twists]

**Creative Alliteration** (memorable repeated sounds):
- [5 alliterative names]

**Metaphorical/Abstract** (evocative or invented words):
- [5 names using metaphors or unique constructions]

For each name suggestion, provide:
- The name itself
- Brief meaning/etymology (what words it comes from or what it evokes)
- Why it fits the product

### Naming Constraints
- Maximum 10 letters (strict)
- Easy to pronounce and spell unambiguously
- No hyphens
- Numbers only if genuinely relevant to the product
- Prioritize names likely to have .com availability

## Step 3: Check Domain Availability

> **Caveat:** Domain checks use the `whois` command, which requires a shell — so this step only runs in Claude Code, not on claude.ai or Cowork. Results are best-effort: registrar rate-limiting, WHOIS privacy, and some TLDs mean "no match" doesn't guarantee a name is actually registrable. Always confirm with a registrar before committing. If `whois` is unavailable, still suggest names but tell the user domains are unverified.

For EVERY suggested name, immediately check domain availability using the whois tool:

1. First try: `[name].com` (highest priority)
2. If unavailable, try: `get[name].com` (only if total ≤ 10 chars)
3. If unavailable, try: `try[name].com` (only if total ≤ 10 chars)
4. If still unavailable, try: `[name].ai` (fallback)

Present results in this format:

**Name Category**
- **NameSuggestion** - [brief meaning]
  - ✅ Available: namesuggestion.com
  - OR
  - ❌ .com taken | ✅ Available: getnamesuggestion.com
  - OR
  - ❌ All primary options taken | ✅ Available: namesuggestion.ai

Only suggest names with at least one available domain option from the patterns above.

## Step 4: Gather Feedback

After presenting all 20 names with availability, ask:

"Which names do you like or dislike? What appeals to you about the ones you like, and what doesn't work about the ones you dislike?"

Listen for:
- Specific names they prefer
- Style preferences (prefer puns over metaphors?)
- Sound/feel preferences (wants something more professional/playful?)
- Meaning preferences (wants clarity vs. intrigue?)

## Step 5: Iterate and Refine

Based on feedback, generate 10-15 new suggestions that align with their preferences. Apply the same domain checking process.

Continue iterating until the user finds options they love.

## Step 6: Trademark Checking (Final Stage Only)

ONLY after the user has selected 1-3 final name candidates they want to pursue, offer trademark checking:

"I can help you do a preliminary trademark check on your final choices. Would you like me to search for potential conflicts?"

If yes, use web_search to check:
- USPTO database (for US trademarks)
- Similar names in their industry
- Common law trademarks (existing businesses)

Explain that this is preliminary only and recommend consulting a trademark attorney for official clearance.

## Reference Materials

For detailed information about naming strategies and patterns, consult:
- **references/naming-patterns.md**: Comprehensive guide to naming categories, domain strategies, and pitfalls to avoid

## Best Practices

- Always check domain availability before suggesting names
- Prioritize .com over .ai or prefixed versions
- Be creative but ensure names are easy to spell from hearing them
- Consider how names will appear in various contexts (logo, URL, speech)
- Avoid names too similar to major existing brands in the same space
- Test pronunciation by saying names out loud mentally
- Think about longevity—will this age well?
