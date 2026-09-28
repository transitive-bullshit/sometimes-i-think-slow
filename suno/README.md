# Suno package v1: "Sometimes I Think Slow"

This makes a new, copyright-clean song from scratch in Suno: close in feel to the 1991 original, not a one-to-one copy.
Nothing here names the original artist, song or sample, and nothing reuses its lyrics or audio. Suno blocks all of those.

## How to use it

1. **Create → Custom mode.** Model: **v6**. If your plan has **v6-wild**, run each style on it too, since v6's groove is getting mixed reviews.
2. **Lyrics:** paste all of [`lyrics-v3-suno.txt`](lyrics-v3-suno.txt).
   - Bracketed tags are section and delivery cues.
   - Parentheses are the chanted echoes and ad-libs.
   - Some names are spelled phonetically on purpose so Suno pronounces them right: *Ahn-dray, Kah-nuh-mun, Nav-yay Stokes, R-L*.
   - Every hook is written out in full; never use `[Chorus x2]`.
   - Stretched vowels ("slooow") and "..." shape phrasing, and CAPS are used sparingly for punch.
3. **Styles:** paste one of the four style prompts below. **Exclude styles:** paste the exclude line.
4. **Title:** "Sometimes I Think Slow". If Suno ever flags it, use "Think Slow, Think Fast".
5. **Settings:** vocal gender **Male**; **Weirdness 30%**; **Style Influence 75%**. For C, Weirdness 40%.
6. **Generate 2–3 times per style**, which gives 4–6 takes each. Keep the lyrics identical across styles, so you're comparing styles and not words.
7. **Once a voice feels right, save it as a Persona** and reuse it for every later iteration, so the voice stays consistent.

## Style prompts (each under Suno's 1,000-character limit)

**A. "1991 faithful": closest to the original's feel**
```
1991 New York golden-era hip-hop, laid-back and sunny, boom-bap at 108 BPM in B major. Dusty crisp drum break with a fat snare on 2 and 4, warm round bass, and a mellow looped clean electric guitar arpeggio with a fingerpicked folk-pop feel. Male MC with a smooth, mellow, warm mid-low voice; relaxed, conversational, half-sung rap that sits slightly behind the beat. The hook is a chanted gang-vocal call-and-response with two voices and a punchy echo. The hook: the MCs chant "sometimes I think slow, sometimes I think fast" and the crew answers "fast, fast, fast". Dry, upfront, near-mono vocals, vinyl warmth, sampler grit, early-90s radio mix.
```

**B. "The duo": two MCs, one bright and fast, one smooth and slow (the song's whole metaphor)**
```
Early-90s East Coast hip-hop duo, playful and laid-back, 108 BPM boom-bap. Two contrasting male MCs: a bright, high-pitched, bouncy, comedic MC raps the first verse with quick punchlines; a smooth, low, silky storyteller half-sings the second verse behind the beat. Both chant the hook together as a call-and-response with echoes. The hook: the MCs chant "sometimes I think slow, sometimes I think fast" and the crew answers "fast, fast, fast". Mellow looped clean electric guitar riff, dusty drums, warm bass, a few turntable scratches between sections. Dry upfront vocals, sampler grit, feel-good block-party vibe.
```

**C. "Modern lo-fi": cleaner, cozier, more modern sound quality**
```
Chill jazzy lo-fi hip-hop with golden-era boom-bap bones, 106 BPM, warm and cozy. Clean fingerpicked electric guitar loop, soft Rhodes chords, round upright-style bass, dusty swung drums with a crisp rimshot snare, light tape hiss and vinyl crackle. Smooth, mellow, laid-back male rapper with a conversational half-sung flow, relaxed and witty, slightly behind the beat. Catchy chanted hook with stacked doubles. The hook: the MCs chant "sometimes I think slow, sometimes I think fast" and the crew answers "fast, fast, fast". Modern clean mix, intimate close-mic vocal, late-night coding vibe.
```

**D. "Live band": organic groove, jazz-rap**
```
Live-band jazz-rap with early-90s New York soul, 108 BPM. Tight live drummer with a dry snare and ghost notes, warm fingered electric bass, clean jazzy guitar riff looping in the pocket, light Rhodes stabs, hand claps on the hook. Charismatic smooth male MC, relaxed and conversational, playful in the first verse and storytelling in the second; half-sung flow behind the beat. Gang-vocal chant on the hook with call-and-response echoes. The hook: the MCs chant "sometimes I think slow, sometimes I think fast" and the crew answers "fast, fast, fast". Warm analog, organic, feel-good.
```

**Exclude styles (use with all four)**
```
trap, 808 slides, trap hi-hats, hi-hat rolls, ticking, clock, metronome, double-time, autotune, drill, EDM, dubstep, rock, metal, pop punk, orchestral, screaming, heavy reverb, female lead vocal
```

## Iteration playbook: symptom → fix

| If… | Try… |
|---|---|
| Verse 1 rushes or crams words | Cut 2–3 lines (the easiest to drop are the date line and the glazing line), or change the tag to `[Verse 1: bright playful rap, relaxed, room to breathe]` |
| The hook isn't chanted or punchy | Change its tag to `[Hook: crowd chant, gang vocals, call-and-response]`. Keep all hooks word-for-word identical. |
| Suno sings the verses instead of rapping them | Add "rapped verses, no singing on verses" to the style prompt. Put "rap" in every verse tag. |
| Verse 2 isn't laid back enough | Retag it `[Verse 2: slow, smooth, spoken-word storytelling, lots of space]`. B's two-MC contrast usually helps. |
| The a cappella drops (`[Break: beat drops out]`) are ignored | Keep going. We can cut the beat in post under "…to an old checkpoint" and "…guessing again". |
| One line is garbled or mispronounced | Use **Replace Section / Edit Lyrics** on just that line. Spell it more phonetically if needed. |
| It ends before the outro | Use **Extend** from the last good bar with only the Hook 3 + Outro lyrics. |
| A take has the right beat but the wrong voice, or the reverse | Save the good voice as a **Persona**, then regenerate or **Cover** the take with that Persona. |
| You get a "matches existing work" or lyric flag | Unlikely, since only the hook echoes the original, loosely. If it happens, change the hook echo to "(I'm fast, I'm fast)" and tell me. |

## After you have a take you love

1. Download the **stems** (vocals + instrumental) and the full mix.
2. I'll time-map the lyrics to the audio and build the lyric/beat grid for the music video pass.
   - Do the beat-drops in post if Suno didn't.
   - The final spoken tag, "Thought for three minutes.", can be re-recorded to match the real song length.

## Lessons carried over from Slow It Down

Its final track was a V6 take, picked mainly for lyric accuracy.

- **No artist names, song titles or samples anywhere.** Suno rejects them. It also fingerprints uploads and checks lyrics against a lyrics database.
- **Describe measured facts:** era, tempo, key, instruments, vocal character. Spell out the hook's call-and-response in the style text.
- **Put delivery cues inside section tags**; that's what switched the rap voice.
- **Parentheses mean backing vocals.** Put each answer on its own line.
- **Settings:** V6, Male, Style Influence ~70–80%, Weirdness ~20–30%.
  - Generate 4–8 takes and save a Persona when the voice is right.
  - Fix single lines with Replace Section instead of rerolling.
- **Avoid "ticking", "double-time", and hi-hat-roll wording.** Suno took them literally and put a ticking sound in every take. They're in the excludes.
- **Pick by lyric accuracy as well as by ear.** Send me your favorite takes and I'll Whisper-score them against the lyrics, the same check the Slow It Down final passed with 77% of script words heard in order.

## Why these choices

- **Hook:** keeps the original's meter exactly ("rhyme" → "think" and "quick" → "fast" are both one syllable) and uses "fast, fast, fast" as the echo, per your call.
- **Voice brief:** follows the Lyria 3.5 "smooth" voice you liked: mellow, warm, mid-low, half-sung, behind the beat.
- **Lyrics v3 = v2 made easier for Suno to perform:**
  - The 24-syllable Navier–Stokes line is split in two; every earlier take swallowed it.
  - The AI product-name roll calls are gone. Filters balked at them, and plain words carry the joke.
  - Phonetic spellings for names.
  - A new outro line: models went from *sometimes* thinking to thinking *always*. In Sept 2026, Opus 5.5 can't switch thinking off.
- **Structure:** the original's arc is kept, so fans still feel it: hook → bright verse → hook → long slow story with two a cappella punchlines → chanted pairs → slowed outro.
