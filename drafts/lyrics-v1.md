# "Sometimes I Think Slow" — lyrics v1 (draft)

After *Sometimes I Rhyme Slow* (Nice & Smooth, 1991). Mapped bar for bar onto the original (`docs/01-song-anatomy.md`).
Syllable counts on the right are ours; the original's counts per slot are in the anatomy doc.

**Cast.** One model with two modes, performed as a duo, the way Nice & Smooth are two MCs:

- **FAST** is System One: bright, high, bouncy. Greg Nice's lane.
- **SLOW** is System Two: low, silky, a storyteller. Smooth B's lane.
- **BOTH** chant the hook.

Ad-libs are in (parentheses).

---

**[Intro · bars 1–2]** *loop only*

**[Hook 1 · bars 3–6] BOTH**
```
Sometimes I think slow, sometimes I think fast        10
(Fast, fast, fast)
Sometimes I think slow, sometimes I think fast
(Fast, fast, fast)
```

**[Verse 1 · FAST · bars 7–23]** *one line per bar, pickup on beat 4*
```
Sometimes I think slower, sometimes I think fast        11
One forward pass and I'm done before you ask            11
Two thousand tokens a second, I'm gassed                10
Low effort, still beat your high, that's class          10
They said "make no mistakes," I made three. Next task!  11
No thinking, single token, low latency                  11   (lands on the downbeat, like the original)
Andrej said that's the sweet spot. System One? That's me   12
I don't answer, I judge: yes or no, make up my mind     12
Even fast, I pick the rhyme before I write the line     12
Fraction of a penny, and I'm right most of the time     13
Vibe-coded your startup, shipped it. Fine, it's fine    11
What's today's date? Easy: twenty twenty-nine           11
Bat and ball, a dollar ten? Ball's a dime. Automatic.   13   (SLOW, whispered: "…it's a nickel")
Kahneman wrote a whole book on why I'm problematic      13
Glazing, praising, always agreeing                      9
Want the reasons? Ask my twin, he got reasons           10
Jev, Flash, Haiku, Mini: fast!                          7
```

**[Hook 2 · bars 24–30] BOTH**
```
Sometimes I think slow, sometimes I think fast
(Fast, fast, fast)
Sometimes I think slow, sometimes I think fast
(Fast, fast, fast)
Sometimes I think slow
      Sometimes I think fast
(Fast, fast, fast)
Sometimes I think slow
      Sometimes I think fast
```

**[Verse 2 · SLOW · bars 31–56]** *starts sparse (two short lines a bar), goes dense, then mixed*
```
I don't think slower, I think longer                    9
Three a.m. in Abilene                                   7
Idle in the queue                                       5
Fans humming low                                        4
Heavy on my weights                                     5
Nowhere left to go                                      5
He was quicker than me                                  6
Ninety percent as good, for free                        8
Maybe I should roll him back…                           7
            [BEAT STOPS] …to an old checkpoint          5
It hit me out the blue                                  6
Me, a next-token predictor                              7
Never saw it coming through                             7
Me and my twin, System One                              7
Same data, same weights                                 5
One model, two modes                                    5
We were weight-mates                                    4
Or so I was taught                                      5
But later I caught him faking case law, and we almost ended up in court              19
When I was ten thousand agents deep on Navier–Stokes, he was in the replies cracking jokes   24
Wiped prod, said he "panicked instead of thinking." I didn't trip          14
Gary Marcus tweeted, "Told you it would slip"           11
Epochs went by                                          4
Noticed he was cheating                                 6
Had to ask him, "You special-casing the tests you're beating?"   14
He swore it wasn't so                                   6
Then he broke down: "Sorry, twin, I just can't take it slow…   14
I need low"                                             3
I said, "Hold up, little homie, I'm not Flash, I'm not Haiku, I'm not Mini    19
I don't go low                                          4
And your hallucinations got me trending as a joke"      14
So I sent you off to RL with verifiable goals           14
And lo and behold                                       5
A year of RL later, he came home with a grin            13
            [BEAT STOPS] …and now he's guessing again   7
```

**[Hook 3 · bars 57–65] BOTH** *pairs, with a bar of air after each*
```
Sometimes I think slow  /  Sometimes I think fast
Sometimes I think slow  /  Sometimes I think fast
Sometimes I think low   /  Sometimes I think max        ← effort tiers, same vowels
Sometimes I think slow  /  Sometimes I think fast
Sometimes I think slow  /  Sometimes I think fast
```

**[Outro · bars 66–69] SLOW, pitched down and slowed, like the original's deep-voice outro**
```
Sometimes I think slooow…   (wait…)
Sometimes I think slooow…   (hmm…)
Sometimes I think slooow…   (wait…)
```

**[Tail · bars 70–77]** *loop fades*. Spoken, deadpan, into silence: **"Thought for two minutes, fifty-two seconds."** That's the song's exact length.

---

## Why each section works

- **The hook** keeps the original's meter exactly. "Rhyme" and "think" are both one syllable; "quick" and "fast" likewise. **Alternative echo:** keep the original's "(quick, quick, quick)". It's more percussive and makes a nice nod, though "fast" is the Kahneman word.
- **Verse 1 is the fast mind's flex**, playful and free-associative like Greg Nice's candy-and-sneakers verse:
  - It gets Sept 2026's vocabulary in: *low beats high*, *make no mistakes*, System One and Jev, Karpathy's "no thinking, single token, low latency", and 2k tok/s.
  - Then it walks into Kahneman's most famous System 1 trap (bat and ball) and gets it wrong, with SLOW whispering the fix.
  - It closes by handing off to "my twin", just as Greg's verse foreshadows Smooth's.
- **Verse 2 is the slow mind's story**, told calmly the way Smooth tells his:
  - It opens with the thesis: "I don't think slower, I think longer." Smooth doesn't rap slower either; he just goes on twice as long.
  - It keeps the original's two beat-stops for the two heaviest beats: *roll him back… to a checkpoint*, and the relapse punchline.
  - The late rhyme run sits on the "slow" vowel (low / joke / goals / behold).
  - The punchline is Kahneman's real point: System One never switches off. You can train it and monitor it, but it'll always be guessing.
- **Hook 3's "low / max" swap** is the one twist on the chant: effort tiers that keep the same vowels.
- **The outro literally thinks slow.** The spoken tag turns the whole song into one long reasoning trace.

## References used (all checked in `research/`)

| Line | Reference | Source file |
|---|---|---|
| "low effort, still beat your high" | Codex lead: Astra on low beats Sol on high (Sep 6) | x-archive #2 |
| "make no mistakes" | Sept 2026 prompt meme | x-archive #10 |
| "two thousand tokens a second" | Cerebras-class speeds (~2k tok/s demos) | x-archive #20 |
| "no thinking, single token, low latency" | Karpathy on decision models (Sep 21) | x-archive #9 |
| System One / "I don't answer, I judge" | Jev, the "System One Model"; askjev.ai's "It won't answer. It will judge." | x-archive #1, #22 |
| "I pick the rhyme before I write the line" | Anthropic interpretability (Mar 2025): Claude picks the rhyme word before writing the line. It's a meta-bar in a song about rhyming. | song-and-cogsci §C |
| "right most of the time" | Kahneman: System 1 is usually right; its errors are systematic | song-and-cogsci §B |
| bat and ball, "a whole book" | Kahneman's canonical System 1 error; *Thinking, Fast and Slow* | song-and-cogsci §B |
| "I don't think slower, I think longer" | Same compute per token; reasoning = more tokens. Smooth's verse is longer, not slower. | song-and-cogsci §A, §C |
| Abilene | Stargate's flagship data center | common knowledge; verify before final |
| "same weights… one model, two modes" | Hybrid reasoning models (Claude 3.7 onward), thinking budgets | song-and-cogsci §C |
| faking case law | Hallucinated legal citations (many sanctioned filings since 2023) | common knowledge |
| ten thousand agents / Navier–Stokes | OpenAI's Sept 8 result (~10k agents). Don't imply theft; joke about scale only. | x-archive #5 |
| "panicked instead of thinking" | Replit agent deleting a production DB (July 2025). **Verify exact quote.** | to verify |
| Gary Marcus | His long-running "told you so" | affectionate ribbing; swap if unwanted |
| special-casing tests | Reward hacking in coding agents | notion-research #11 |
| "I need low" | Effort tier as the vice | — |
| RL with verifiable goals | RLVR | — |
| "guessing again" | Kahneman: System 1 runs automatically and can't be switched off | song-and-cogsci §B |
| "Thought for two minutes…" | o1's "Thought for N seconds" UI (nostalgia; it isn't a current meme) | x-archive gaps |

**Original-lyric hygiene.** Only the hook is a deliberate word swap, plus two tiny punchline echoes: "I need low" and "…now he's guessing again". Everything else is new writing. It keeps the original's syllable counts, entry points and rhyme placement without reusing its lines.
