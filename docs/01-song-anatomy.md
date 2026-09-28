# 01 — Song anatomy: "Sometimes I Rhyme Slow" (Nice & Smooth, 1991)

The original was our inspiration and the reference for writing the parody: its form, tempo, key, and feel. These notes
are that reference, measured once and summarized here (the numbers are also in `analysis/grid-original.json`,
`analysis/beats-original.json` and `analysis/vocal-lines.json`). Nothing downstream uses the original recording: the
song was generated fresh in Suno from our own lyrics and a style prompt, and everything after that is independent.

> **No original lyrics appear in this doc.** They're copyrighted. What a parody needs instead is here: sections, bar
> positions, entry points, syllable counts, rhyme placement, and a paraphrase of what each passage is about.

## The numbers

| | |
|---|---|
| Tempo | **108.35 BPM**, dead steady. 96.8% of beats sit within 30 ms of one fixed grid (8 ms residual). |
| Bar | 2.2152 s. Bar 1 starts at 0:00.270. 77 bars in total. |
| Key | **B major** (r = 0.86). |
| Groove | A **2-bar loop** runs the whole song: boom-bap drums, warm bass, and the replayed "Fast Car" riff. The riff was re-performed by session guitarist Jamie Propp, not sampled. |
| Mix | Almost mono (side/mid 0.04). The vocal sits about 5.7 dB under the beat by loudness. |
| Context | *Ain't a Damn Thing Changed* (Sept 1991). #1 on Hot Rap Singles (June 20, 1992), #44 on the Hot 100. See `research/song-and-cogsci-background.md`. |

## Form

| # | Section | Bars | Time | Voice | Shape |
|---|---|---|---|---|---|
| 1 | Intro | 1–2 | 0:00–0:04 | — | Loop only. The hook's pickup comes in on bar 2, beat 4. |
| 2 | **Hook 1** | 3–6 | 0:04–0:13 | group chant | Two call-and-echo units (see below). |
| 3 | Verse 1 | 7–23 | 0:13–0:50 | **Greg Nice**: high and bright (F0 ≈ 290 Hz), playful | 17 lines, one per bar. Opens by restating the hook as a variant. |
| 4 | **Hook 2** | 24–30 | 0:50–1:06 | group chant | Two call-and-echo units, then the chant splits into its halves. |
| 5 | Verse 2 | 31–56 | 1:06–2:04 | **Smooth B**: lower and silky (F0 ≈ 175 Hz), storyteller | 34 lines. Sparse, then two very dense lines, then mixed. **The beat cuts out twice.** |
| 6 | **Hook 3** | 57–65 | 2:04–2:22 | group chant | Five "slow" / "quick" pairs, one pair every 2 bars, with air around them. |
| 7 | Outro | 66–69 | 2:22–2:33 | a much lower voice (F0 ≈ 110–130 Hz, falling) | The hook phrase in a deep, pitched-down or slowed treatment, fading out. |
| 8 | Tail | 70–77 | 2:33–2:52 | — | Loop only. Fades out from bar 73. |

## The hook: what has to survive

```
bar 2, beat 4 ──── "Some-times I [rhyme] slow,"      pickup; the call is 10 syllables across bar 3
bar 3        ──── "some-times I [rhyme] quick"       lands late in bar 3
bar 3, beat 4.75 ─ ECHO: quick · quick · quick       3 hard hits: bar 4, beats 1, 2 and 3
(repeat the unit: bars 4.4 → 6)
```

- The call is **10 syllables**, split 5 + 5. Two words change in the parody: *rhyme→think*, and *quick→fast* if you want Kahneman's wording.
- The echo is three stressed monosyllables on beats 1-2-3. "Quick" is percussive, a short vowel plus a hard K. "Fast" works too but is softer, sibilant. Both fit.
- Hook 2 adds a split: the two 5-syllable halves come separately ("…slow" at x.3.2, "…quick" at x+1.2.2), then an echo.
- Hook 3 is only those split halves, five pairs with a bar of air after each one. It's the singalong part.
- Pitch detection finds **no single steady voice** in the hook. It reads as a gang chant, two or more voices together, not a solo line.

## Verse 1 (Greg Nice), bars 7–23: the "quick" flow

Each line starts with a **pickup on beat 4** and lands its stress on the next downbeat. That's one line per bar, about 9–13 syllables, with bright, bouncy delivery. Syllable counts are approximate (±1) for every line.

| Line | Bar entry | Syl | Rhyme | What it's about (paraphrase) |
|---|---|---|---|---|
| 1 | 6.4 | 11 | A "-ick" | Restates the hook, with the slow half stretched |
| 2–5 | 7.4–10.4 | 10–11 | A ×4 | Whimsical everyday flexes: sweets, a movie, new footwear |
| 6–7 | 12.1, 12.4 | 9, 9 | B (slant) | Flirting, then leaving a party buzzed. **Line 6 starts on the downbeat, not a pickup.** |
| 8–12 | 13.4–17.4 | 9–13 | C "-ine" ×5 | Good-life flexes: mood, car, romance, fine dining, gossip |
| 13–14 | 19.1, 20.1 | 9, 11 | D "-atic" pair | A tough-guy boast, then a proverb about excess that foreshadows verse 2 |
| 15–16 | 21.1, 21.4 | 8, 9 | E "-easing/-eason" pair | A rhyming word list, then "don't ask why" |
| 17 | 22.4 | 7 | A "-ick" | Roll call of the duo's names, handing off to the hook |

The mood is a free-associative, playful flex: candy, dessert, sneakers, a car, gossip. Nothing heavy. **That's the "fast mind": associative, confident, fun.**

## Verse 2 (Smooth B), bars 31–56: the long story

Smooth isn't slower per syllable. He averages about **10.6 syllables per bar against Greg's 9.8**, and he simply goes on about twice as long, 27 bars to 17. *That's exactly how reasoning models "think slow": same speed per token, many more tokens.*

| Lines | Bars | Shape | Rhyme | Story (paraphrase) |
|---|---|---|---|---|
| 1–5 | 30.4–33.2 | **Sparse:** 2 short lines per bar, 4–7 syllables each | pairs | Scene-setting: alone uptown, heartsick |
| 6–8 | 33.4–34.4 | short | pair | Brooding about a woman who hurt him; a dark impulse… |
| 9 | 35.2 | **BEAT STOPS** (beats 2–4, silence under the vocal) | — | …which lands a cappella |
| 10–12 | 36–37 | short | triple "-ur" | Disbelief |
| 13–17 | 37.4–39.4 | short | pairs | Flashback: they were a close couple, or so he believed |
| 18 | 40.2 | **19 syllables** | "-ort" | Her drug habit enters the story |
| 19 | 41.4 | **24 syllables**, split in two with an internal rhyme | "-ends" | While he worked, she used |
| 20–21 | 43.4–44.4 | ~12 | "-ip" pair | Damage piles up; a friend warns him |
| 22–24 | 46–47 | mixed | "-oss/-orse" | He notices the signs and confronts her |
| 25–33 | 47.4–54.4 | mixed, 3–20 syllables | long **"-oh/-oke" run** (the "slow" vowel) | Denial, then admission; he refuses to enable her and sends her to rehab |
| 34 | 54.4 | 11 | "-in" | She comes back and he takes her back… |
| 35 | 56.1 | **BEAT STOPS** (beats 2–4) | "-in" | …punchline: relapse. The hook comes in. |

It's a cautionary tale told calmly over a sunny loop. The contrast between that vibe and the content is the point.

## Performance traits to copy

- **Two voices, two lanes.** Greg is bright, high and bouncy, and throws lines. Smooth is low, silky and conversational, and tells. The hook is both of them chanting together.
- **Pickups on beat 4.** Nearly every line enters just before the bar and lands on the downbeat.
- **Two beat stops** (bar 35 and bar 56) spotlight the two heaviest lines of the story. Keep them. They're the parody's two biggest punchlines.
- **The deep-voice outro.** The hook phrase comes back in a much lower, slowed-sounding voice. Our "thinking slow" can literally slow down here.
- **Near-mono, dry, upfront vocals** with little reverb. A 1991 NY mix.

## Structural gifts for the parody

1. **The duo is the metaphor.** Nice and Smooth are fast and slow, System One and System Two. Verse 1 is the fast mind's flex; verse 2 is the slow mind telling a long story. The hook is both of them.
2. **The "slow" MC isn't slower, he's longer.** That's the most accurate thing anyone can say about reasoning models, and it's already built into the song.
3. **Verse 2's late rhyme run is on the "slow" vowel** ("-oh/-oke"), so the parody gets a whole run of *low / slow / go / broke / joke* for free.
4. **Verse 1's excess-and-addiction proverb** foreshadows verse 2. The parody can foreshadow its own verse-2 twist the same way.
5. **The backing is a replayed "Fast Car".** A slow song built on a riff called *Fast Car*.
