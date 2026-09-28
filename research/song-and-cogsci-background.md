# Background research: the song, dual-process theory, and fast/slow AI

For **"Sometimes I Think Slow"**, an AI-POV homage to Nice & Smooth's "Sometimes I Rhyme Slow" (1991).
Compiled 2026-09-28. Every factual claim links to a source.

**House rules followed here**
- **No song lyrics are reproduced.** Verses are paraphrased at the level of theme, and structure is given as timings and bar counts. The same applies to "Fast Car" and to the songs that sampled it.
- **Book text:** the unauthorized archive.org and pubhtml5 copies of *Thinking, Fast and Slow* were not used or cited. Book content comes from Wikipedia, publisher-sanctioned excerpts, Kahneman's own lectures and interviews, and reputable summaries.
- Direct quotation is kept to one short line. Everything else is paraphrase.
- Items marked **UNVERIFIED** could not be pinned to a reliable source.

---

## 0. The ten facts that matter most

1. **"Fast Car" was replayed, not sampled.** The 12" credits Jamie Propp on acoustic guitar ([Discogs](https://www.discogs.com/release/499142-Nice-Smooth-Sometimes-I-Rhyme-Slow)). Smooth B later said they hired a guitarist to replay the riff as an interpolation ([AllHipHop, 2020](https://allhiphop.com/features/smooth-b-remembers-epic-night-with-tupac-talks-new-single-before/)). Most outlets still call it a sample ([Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow)).
2. **The two verses really are a fast mind and a slow mind.** Greg Nice's verse is a hyper, free-associative boast. Smooth B's is a long causal story about a partner's cocaine addiction and relapse ([Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow); [uDiscover, 2025](https://www.udiscovermusic.com/stories/nice-and-smooth-aint-a-damn-thing-changed-feature/)). Smooth's verse runs about 27 bars against Greg's 16 ([project analysis](../analysis/vocal-lines.json)).
3. **"Slow" means more steps, not slower delivery.** Smooth B raps slightly denser than Greg (about 10.6 against 9.8 syllables per bar) and simply goes on longer ([project analysis](../analysis/vocal-lines.json)). A reasoning model works the same way: same token speed, many more tokens.
4. **Charts.** Hot Rap Singles #1 for the week of June 20, 1992. Hot 100 peak #44, also that week. Hot R&B/Hip-Hop #17 ([Wikipedia list](https://en.wikipedia.org/wiki/List_of_Billboard_number-one_rap_singles_of_the_1980s_and_1990s); [Billboard data mirror](https://billboard.elpee.jp/single/Sometimes%20I%20Rhyme%20Slow/The%20Nice/); [Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow)).
5. **"Fast Car" came back.** Luke Combs' 2023 cover reached #2 on the Hot 100 and #1 on Country Airplay. Chapman became the first Black songwriter to win CMA Song of the Year (Nov 8, 2023), and she sang it with Combs at the Grammys on Feb 4, 2024 ([Rolling Stone](https://www.rollingstone.com/music/music-country/tracy-chapman-luke-combs-fast-car-song-of-the-year-2023-cmas-1234873495/); [Rolling Stone](https://www.rollingstone.com/music/music-country/tracy-chapman-luke-combs-fast-car-2024-grammys-performance-1234957795/)).
6. **Kahneman called System 1 and System 2 *fictitious characters*,** nicknames for two modes of thought rather than brain modules. He also described accessibility as a continuum rather than a dichotomy ([Scientific American excerpt](https://www.scientificamerican.com/article/kahneman-excerpt-thinking-fast-and-slow/); [Nobel lecture](https://www.nobelprize.org/uploads/2018/06/kahnemann-lecture.pdf)). He died March 27, 2024 ([Princeton](https://www.princeton.edu/news/2024/03/28/daniel-kahneman-pioneering-behavioral-psychologist-nobel-laureate-and-giant-field)).
7. **Parts of the book failed to replicate.** Kahneman conceded the priming chapter rested on underpowered studies ([Gelman blog, reproducing his comment](https://statmodeling.stat.columbia.edu/2017/02/18/pizzagate-kahneman-two-great-flavors-etc/)). Ego depletion failed multi-lab replications ([Wikipedia](https://en.wikipedia.org/wiki/Ego_depletion)). The bat-and-ball error and anchoring hold up.
8. **Search sharpens intuition, then gets distilled back into it.** AlphaGo Zero's raw network, with no lookahead, rated 3,055 Elo; the same network guiding tree search rated 5,185. Search is the *policy improvement operator* whose results are trained back into the network ([Silver et al., 2017](https://discovery.ucl.ac.uk/10045895/1/agz_unformatted_nature.pdf)). Anthony, Tian & Barber named this loop *thinking fast and slow* in 2017 ([arXiv](https://arxiv.org/abs/1705.08439)).
9. **Thinking time is a scaling axis.** On AIME 2024, o1 scored 74% with one sample, 83% with a 64-sample consensus and 93% when re-ranking 1,000 samples; GPT-4o scored 12% ([OpenAI](https://openai.com/index/learning-to-reason-with-llms/)). Noam Brown's poker bot got the same gain from 20 seconds of thinking as from a roughly 100,000× bigger model ([VentureBeat](https://venturebeat.com/ai/openai-noam-brown-stuns-ted-ai-conference-20-seconds-of-thinking-worth-100000x-more-data)).
10. **The fast pass plans, and the slow narration can be unfaithful.** Claude picks its rhyme word before writing a line. It explains addition as carrying the one while actually running parallel approximate and exact paths ([Anthropic, 2025](https://www.anthropic.com/research/tracing-thoughts-language-model)). Reasoning traces mention a planted hint only 25–39% of the time ([Anthropic, 2025](https://www.anthropic.com/research/reasoning-models-dont-say-think)).

---

# Part A. "Sometimes I Rhyme Slow"

## A1. Release, label, album

- **Album.** *Ain't a Damn Thing Changed*, the duo's second album, came out September 3, 1991 on Rush Associated Labels (RAL) and Columbia. It was recorded 1990–91 at Unique Recording (NYC) and Power Play (Long Island City) ([Wikipedia](https://en.wikipedia.org/wiki/Ain%27t_a_Damn_Thing_Changed)). It peaked at #141 on the Billboard 200 and #29 on Top R&B/Hip-Hop Albums (same source).
- **How they got there.** The duo reached Def Jam through the RAL umbrella ([The Quietus](https://thequietus.com/opinion-and-essays/anniversary/nice-and-smooth/)). Def Jam/RAL picked up their contract, and EPMD's, when Fresh Records folded ([uDiscover, Jeff "Chairman" Mao, 2025](https://www.udiscovermusic.com/stories/nice-and-smooth-aint-a-damn-thing-changed-feature/)).
- **Track details.** Track 4, 2:52, credited to Gregory Mays, Darryl Barnes and Tracy Chapman ([Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow)). Genius lists a release date of Sep 17, 1991 ([Genius credits](https://genius.com/Nice-and-smooth-sometimes-i-rhyme-slow-lyrics)).
- **Lead single, or third single?** Sources disagree.
  - Wikipedia and Genius call it the lead single ([Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow)).
  - Albumism calls it the album's third single ([Albumism, 2021](https://albumism.com/features/tribute-celebrating-30-years-of-nice-and-smooth-aint-a-damn-thing-changed)). A 2018 chart blog orders the singles as "Hip Hop Junkies", then "How to Flow", then this song ([twostepcub](https://twostepcub.blogspot.com/2018/06/robbed-hit-of-week-61818-nice-smooths.html)). A 2015 review calls "Hip Hop Junkies" the first single ([Time Is Illmatic](https://timeisillmatic.me/2015/04/20/nice-smooth-aint-a-damn-thing-changed-september-3-1991/)).
  - Catalog numbers support the later date. The US "Hip Hop Junkies" 12" is 44 73738 (1991) ([Discogs](https://www.discogs.com/release/7726383-Nice-Smooth-Hip-Hop-Junkies)). The US "Sometimes I Rhyme Slow" 12" is 44 74166 (1992) and carries a "Hip Hop Junkies" remix on its B-side ([Discogs](https://www.discogs.com/release/499142-Nice-Smooth-Sometimes-I-Rhyme-Slow)). An Australian CD single appeared in 1991 ([Discogs master](https://www.discogs.com/master/150256-Nice-Smooth-Sometimes-I-Rhyme-Slow)).
  - The song entered the Hot 100 on May 9, 1992 ([Billboard data mirror](https://billboard.elpee.jp/single/Sometimes%20I%20Rhyme%20Slow/The%20Nice/)).
  - **Best reading:** it is the album's signature song, but in the US it was worked as a spring-1992 single, most likely the third.
- **US 12" contents.** LP Version, Original Mix, Low-Key A Cappella, Stay Faithful Mix, Stay Faithful Instrumental, plus two "Hip Hop Junkies" mixes ([Discogs](https://www.discogs.com/release/499142-Nice-Smooth-Sometimes-I-Rhyme-Slow)).

## A2. Producers and credits

- **Produced by Nice & Smooth,** credited on the 12" as "Gregg Nice & Smooth Bee" for production and remixes ([Discogs](https://www.discogs.com/release/499142-Nice-Smooth-Sometimes-I-Rhyme-Slow); [Wikipedia](https://en.wikipedia.org/wiki/Ain%27t_a_Damn_Thing_Changed)). The only other producer on the album is Louie Vega, on "Paranoia" (same Wikipedia source).
- **Session credits.**
  - Acoustic guitar: Jamie Propp (the three A-side versions).
  - Recorded by D'Anthony Johnson at Unique Recording, NYC.
  - Mixed by Rory Young at Acme, Mamaroneck, NY.
  - Mastered by Tony Dawsey at Masterdisk ([Discogs](https://www.discogs.com/release/499142-Nice-Smooth-Sometimes-I-Rhyme-Slow); [Genius credits](https://genius.com/Nice-and-smooth-sometimes-i-rhyme-slow-lyrics)).
  - Genius lists the acoustic guitar as "Jamie Propp & Tracy Chapman", reflecting the replay-versus-sample ambiguity.
- **Tempo.** About 108 BPM. The project's own beat tracking measures 108.34 BPM, about 2.215 s per bar ([analysis/grid-original.json](../analysis/grid-original.json); cf. [songbpm](https://songbpm.com/@nice-smooth/sometimes-i-rhyme-slow)). "Fast Car" is listed at about 104 BPM and 4:57 ([songbpm](https://songbpm.com/@tracy-chapman/fast-car)). So the song called "slow" is faster and shorter than the one called "Fast Car". The BPM values are algorithmic estimates.

## A3. The "Fast Car" element, and other samples

- **What it uses.** The acoustic guitar intro of Tracy Chapman's "Fast Car" (1988), with drums added ([Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow); [The Quietus](https://thequietus.com/opinion-and-essays/anniversary/nice-and-smooth/)). WhoSampled lists "Fast Car" as the source of the hook/riff ([WhoSampled sample page](https://www.whosampled.com/sample/204/Nice-&-Smooth-Sometimes-I-Rhyme-Slow-Tracy-Chapman-Fast-Car/); element type shown on a [related WhoSampled page](https://www.whosampled.com/sample/1433869/Kokane-Too-Short-Rhyme-Slow-Nice-%26-Smooth-Sometimes-I-Rhyme-Slow/)).
- **Replay, not sample.** Smooth B's account ([AllHipHop, 2020](https://allhiphop.com/features/smooth-b-remembers-epic-night-with-tupac-talks-new-single-before/)):
  - Greg Nice used to drive around blasting Tracy Chapman and pitched flipping "Fast Car".
  - They hired an acoustic guitarist to replay it, so it is an interpolation rather than a sample, and it differs audibly from the original.
  - The 12" guitarist credit backs this up ([Discogs](https://www.discogs.com/release/499142-Nice-Smooth-Sometimes-I-Rhyme-Slow)). Albumism also noted the track appears to be replayed ([Albumism](https://albumism.com/features/tribute-celebrating-30-years-of-nice-and-smooth-aint-a-damn-thing-changed)).
- **Chapman's reaction.** In a 2005 interview with *The Voice* (Russel Myrie), she said she was upset because she had not authorized it, from an era when people sampled first and sought approval later. She described herself as protective of her work, and the article notes she had recently turned down a sampling request from Kanye West ([reproduced on about-tracy-chapman.net](https://www.about-tracy-chapman.net/2005-driving-fast-cars/)).
- **Publishing.** Smooth B says Chapman took most of the publishing. By contrast, Prince and Elton John gave them 50/50 splits on other uses ([VladTV, 2020](https://www.vladtv.com/article/263616/smooth-b-on-tracy-chapman-taking-all-publishing-for-sometimes-i-rhyme)). Chapman is a credited co-writer ([Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow)).
- **Other samples.** None documented. WhoSampled, as surfaced in search, and Genius's credits list only "Fast Car" ([Genius credits](https://genius.com/Nice-and-smooth-sometimes-i-rhyme-slow-lyrics); [WhoSampled](https://www.whosampled.com/Nice-&-Smooth/Sometimes-I-Rhyme-Slow/)). No drum source is credited.
  - *Caveat:* WhoSampled's main song page was behind bot protection and could not be read in full. Its entries were gathered from search results and individual sample pages.
- **A thematic echo.** "Fast Car" is about a working-class woman trying to escape generational poverty ([Wikipedia](https://en.wikipedia.org/wiki/Fast_Car)). Its cyclical story, in which she escapes a drinking father only to end up with a drinking partner, mirrors the addiction-and-relapse loop of Smooth B's verse ([Eagranie Yuh, 2023](https://eagranieyuh.substack.com/p/story-46-fast-car-driving-in-circles)).

## A4. Structure, with timings but no lyrics

**Timing sources:** the project's automated vocal-onset analysis ([analysis/vocal-lines.json](../analysis/vocal-lines.json)), which uses 1 bar ≈ 2.215 s, cross-checked against an independent user-synced timing file ([lyricdown LRC](https://www.lyricdown.com/lrc/nice-smooth-sometiems-i-rhyme-slow-32358963), used for timestamps only). Treat bar counts as ±1.

| Section | Time | ≈ Bars | Who | What happens (paraphrase) | Density |
|---|---|---|---|---|---|
| Intro | 0:00–0:04 | 2 | instrumental | the replayed "Fast Car" guitar figure over drums | — |
| Opening refrain | 0:04–0:15 | 5 | Greg Nice | the title idea chanted several times as a lead-in, entering on a pickup on beat 4 | ~7.4 syll/bar |
| **Verse 1** | 0:15–0:51 | **16** | **Greg Nice** | a buoyant, free-associative boast (sweets, dates, clothes, cars, fine dining) with passing asides about guns and about excess breeding addiction; ends with a roll-call of the crew | **~9.8 syll/bar** |
| Chorus / hook | 0:51–1:04 | 6 | uncredited (see A5) | the title idea chanted, one line spread across about 2 bars | ~6.8 syll/bar |
| **Verse 2** | 1:04–2:04 | **~27** | **Smooth B** | a first-person story, framed as a heartbroken moment on a Harlem corner, of living with a partner who becomes addicted to cocaine while he tours; he reads the signs, confronts her, refuses to fund it, quietly puts her in rehab, and she relapses about 18 months later | **~10.6 syll/bar** |
| Outro refrain | 2:04–2:29 | ~12 | chorus | the title idea repeated; the last few repetitions tighten from about one per two bars to about one per bar | ~6.2 syll/bar |
| Tail | 2:29–2:52 | ~10 | instrumental | the riff plays out | — |

**What the timings show**
- **Two verses, one refrain.** The refrain opens the song, splits the verses and closes the song.
- **Smooth's verse is the long one.** It is about 1.7 times the length of Greg's in bars and about 1.8 times in syllables: 287 against 157 ([project analysis](../analysis/vocal-lines.json)). "Slow" here means a longer chain, not slower syllables.
- **The refrain is the sparsest part.** Refrain lines sit about 2 bars apart, while verse lines run about one per bar. The song's slowest rhyming happens in the part that talks about rhyming slow.
- **The outro speeds up.** Near the end the refrain lines move closer together. Both timing sources show this, but verify by ear.
- **Rhyme scheme.** Greg's first several verse lines keep the refrain's end-rhyme before he moves to new rhyme families every couple of lines. Smooth changes rhyme family as the story advances. This comes from the phonetic rhyme tags in the analysis file.
- **Verse themes, per sources.**
  - Greg's verse: the lyrics touch on drug abuse, guns and violence ([Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow)), but critics hear it as Greg's usual good-humored free association ([The Quietus](https://thequietus.com/opinion-and-essays/anniversary/nice-and-smooth/); [AV Club](https://www.avclub.com/1991-found-hip-hop-in-transition-with-2pac-leading-the-1798233140)).
  - Smooth B's verse is about loving a cocaine addict who relapses after 18 months in rehab ([Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow)). He says it combines three real relationships into one character ([AllHipHop](https://allhiphop.com/features/smooth-b-remembers-epic-night-with-tupac-talks-new-single-before/)).

## A5. Who performs what

- **Greg Nice:** the opening refrain and verse 1. **Smooth B:** verse 2 ([Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow); section headers on [Genius](https://genius.com/Nice-and-smooth-sometimes-i-rhyme-slow-lyrics)).
- **The hook: UNVERIFIED.** Genius labels it only "[Chorus]" with no performer. The video doesn't lip-sync it; those passages show the duo in conversation and the girlfriend character (see A7). The project's separated vocal stems could settle it by ear or with speaker diarization.
- AllMusic calls the vocal hook insanely catchy ([AllMusic album review](https://www.allmusic.com/album/aint-a-damn-thing-changed-mw0000675412)).

## A6. Chart performance

| Chart (Billboard, 1992) | Peak | Detail |
|---|---|---|
| Hot Rap Singles | **1** | 1 week, issue dated June 20, 1992. Preceded by Das EFX's "They Want EFX", followed by Pete Rock & CL Smooth's "T.R.O.Y." ([Wikipedia list](https://en.wikipedia.org/wiki/List_of_Billboard_number-one_rap_singles_of_the_1980s_and_1990s)) |
| Hot 100 | **44** | Debuted #97 on May 9, 1992; peaked June 20 and again July 11; 18 weeks on the chart ([Billboard data mirror](https://billboard.elpee.jp/single/Sometimes%20I%20Rhyme%20Slow/The%20Nice/); [Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow)) |
| Hot R&B/Hip-Hop Songs | **17** | ([Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow)) |
| Year-End Hot Rap Singles 1992 | **13** | ([Wikipedia](https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_Rap_Singles_of_1992)) |

- It is the duo's highest Hot 100 entry; "Old to the New" reached #59 ([Wikipedia discography](https://en.wikipedia.org/wiki/Nice_%26_Smooth)).
- Commentators call it their biggest national hit, just missing the Top 40 ([twostepcub](https://twostepcub.blogspot.com/2018/06/robbed-hit-of-week-61818-nice-smooths.html)).

## A7. Music video

- **Director: UNVERIFIED.** One aggregator credits Eric Meza, with an unexplained "Lynn Rose" ([AltSounds.TV](https://altsounds.tv/video/nice-smooth-sometimes-i-rhyme-slow/)). Meza's IMVDb filmography doesn't list the video ([IMVDb](https://imvdb.com/n/eric-meza)). Treat the credit as unconfirmed.
- **Circulation and airplay.** The clip circulated on the April 1992 *Rock America Urban* video pool ([mv-rock listing](https://www.mv-rock.com/performer/nice_and_smooth/)). It is said to have been in heavy MTV rotation in summer 1992 ([Hip Hop Scriptures](https://www.hiphopscriptures.com/blog/2021/9/17/nice-amp-smooths-aint-a-damn-thing-changed-album-anniversary)). The official VEVO upload has about 3.9M views ([YouTube](https://www.youtube.com/watch?v=dkl_Vq1SWKg)).
- **Look.** The official upload was geo-blocked in the browser used, so this description comes from a broadcast copy of the video ([YouTube](https://www.youtube.com/watch?v=GuM3qbooHsU)). It is moody and noir-ish rather than a party video, and it visualizes Smooth B's story:
  - It opens on a hard-edged silhouette of a capped figure thrown onto a sunlit white wall.
  - The recurring setup is the two MCs in denim jackets and caps, crouched against a bright wall striped with window-lattice shadows, talking and gesturing like a confession.
  - Other shots include amber- or sepia-lit stairwells and hallways, tight performance close-ups against black, and cool blue shots of a woman in a sequined dress dancing in near-darkness (the girlfriend character).
  - Near the end there is a blue-tinted close-up of a hand at a mirror-like surface that evokes drug use.

## A8. Critical reception

- **AllMusic (Stanton Swihart).**
  - Calls the song simply "Fast Car"'s track with the duo's rhymes superimposed.
  - Praises its vocal hook.
  - Contrasts Greg Nice's abrupt, roughneck dramatics with Smooth B's serene, butter-slick delivery as the perfect vocal balance ([AllMusic](https://www.allmusic.com/album/aint-a-damn-thing-changed-mw0000675412)).
  - AllMusic's artist bio calls the track biting, nicely written and bitterly performed ([AllMusic bio](https://www.allmusic.com/artist/mn0000393513)).
- **The Quietus (Angus Batey; first published Dec 27, 2011).**
  - Calls the concept deceptively, even outrageously, simple, and says it could have bridged the Public Enemy and De La Soul audiences.
  - Finds Smooth's verse so out of character that you can't be sure it's real, yet its detail and the sample's melancholy make it feel remembered rather than studied ([The Quietus](https://thequietus.com/opinion-and-essays/anniversary/nice-and-smooth/); summarized on [Wikipedia](https://en.wikipedia.org/wiki/Sometimes_I_Rhyme_Slow)).
- **AV Club (Nathan Rabin, 2012).** Hears unintended comedy in the clash between Greg's high-spirited verse and Smooth's dark narrative, all over a melancholy guitar figure ([AV Club](https://www.avclub.com/1991-found-hip-hop-in-transition-with-2pac-leading-the-1798233140)).
- **uDiscover (Jeff "Chairman" Mao, 2025).** Describes a playful first act with jittery drums matching Greg's hyper verse, then Smooth's sobering second act. Calls it a stunning turn in an otherwise happy-go-lucky hit ([uDiscover](https://www.udiscovermusic.com/stories/nice-and-smooth-aint-a-damn-thing-changed-feature/)).
- **Rankings.** uDiscover's 2026 "Best 90s Hip Hop Songs" puts it at #62 and praises both MCs for switching cadences and flow patterns ([uDiscover](https://www.udiscovermusic.com/stories/best-90s-hip-hop-songs/)).

## A9. Legacy: who sampled or referenced it

**Sampled**, per Genius's community credits ([Genius](https://genius.com/Nice-and-smooth-sometimes-i-rhyme-slow-lyrics)) and WhoSampled search results:
- Xzibit, "Paparazzi"
- Young Black Teenagers, "Tap the Bottle"
- Showbiz & A.G., "He Say, She Say" and "Still Diggin'"
- Nappy Roots feat. Greg Nice, "No Static" (2008, *The Humdinger*, prod. Sol Messiah) ([Wikipedia](https://en.wikipedia.org/wiki/The_Humdinger); [WhoSampled](https://www.whosampled.com/sample/4032/Nappy-Roots-No-Static-Nice-&-Smooth-Sometimes-I-Rhyme-Slow/))
- Big K.R.I.T. feat. Warren G, "No Static"
- Sha Stimuli, "Sometimes" ([WhoSampled](https://www.whosampled.com/sample/75926/Sha-Stimuli-Sometimes-Nice-&-Smooth-Sometimes-I-Rhyme-Slow/))
- Lil B, "Real Based" ([WhoSampled](https://www.whosampled.com/sample/269804/Lil-B-Real-Based-Nice-&-Smooth-Sometimes-I-Rhyme-Slow/))
- Jay Electronica, "Be Easy"
- Fabolous feat. Jeremih, "Thim Slick"
- Gangrene, "Gluttony"
- quickly, quickly, "Graze"
- Elwood, "Sundown"

**Interpolated or referenced:**
- **Madvillain, "All Caps" (2004).** MF DOOM twists the title phrase. WhoSampled tags it as a vocals/lyrics element ([WhoSampled](https://www.whosampled.com/Madvillain/All-Caps/samples/); [AV Club](https://www.avclub.com/1991-found-hip-hop-in-transition-with-2pac-leading-the-1798233140)).
- **P. Diddy feat. Pharrell, "Diddy" (2001, prod. The Neptunes).** Listed as an interpolation by WhoSampled and Genius; the first verse opens by borrowing the title couplet and the Harlem-corner setting ([WhoSampled](https://www.whosampled.com/sample/75925/P.-Diddy-Pharrell-Williams-Diddy-Nice-&-Smooth-Sometimes-I-Rhyme-Slow/); [Genius credits](https://genius.com/Nice-and-smooth-sometimes-i-rhyme-slow-lyrics); release details on [Wikipedia](https://en.wikipedia.org/wiki/Diddy_(song))).
- **Kokane feat. Too $hort, "Rhyme Slow" (1999).** A replayed interpolation of the vocals ([WhoSampled](https://www.whosampled.com/sample/1433869/Kokane-Too-Short-Rhyme-Slow-Nice-%26-Smooth-Sometimes-I-Rhyme-Slow/); [Wikipedia](https://en.wikipedia.org/wiki/They_Call_Me_Mr._Kane)).
- **Per Genius:** Missy Elliott ("Go to the Floor"), G-Unit ("Groupie Love"), Shaquille O'Neal ("Nobody"), Rick Ross ("Get Away"), Shindy ("Tiffany").
- **Cloonee, "I Rhyme Quick" (2026, dance).** Listed on WhoSampled ([WhoSampled](https://www.whosampled.com/sample/1433869/Kokane-Too-Short-Rhyme-Slow-Nice-%26-Smooth-Sometimes-I-Rhyme-Slow/)). *Fast/slow inversions of the title already exist in the wild.*

**Broader legacy:**
- De La Soul's Trugoy borrowed the duo's flow on "Simply" (2001) and named them as favorite MCs.
- De La Soul, The Roots, MF DOOM and DJ Premier have all paid tribute ([AV Club](https://www.avclub.com/1991-found-hip-hop-in-transition-with-2pac-leading-the-1798233140)).
- The duo's verse on Gang Starr's "DWYCK" (1992) is their other signature appearance ([Wikipedia](https://en.wikipedia.org/wiki/Nice_%26_Smooth)).

## A10. The duo: personas and delivery

- **Who they are** ([Wikipedia](https://en.wikipedia.org/wiki/Nice_%26_Smooth)):
  - **Greg Nice** is Gregory O. Mays, born May 30, 1967.
  - **Smooth B** is Darryl O. Barnes, born Aug 3, 1965.
  - They are a Bronx duo with four albums, 1989–1997.
- **How they met** ([AllHipHop](https://allhiphop.com/features/smooth-b-remembers-epic-night-with-tupac-talks-new-single-before/)):
  - Smooth B had been writing raps and singing backup for Bobby Brown on tour.
  - Greg Nice originally preferred beatboxing and making beats.
  - They teamed up after the murder of Greg's earlier partner, June Love.
- **Contrasting styles, as critics describe them:**
  - **Greg Nice:** high-pitched non-sequiturs ([uDiscover](https://www.udiscovermusic.com/stories/nice-and-smooth-aint-a-damn-thing-changed-feature/)); abrupt, roughneck dramatics ([AllMusic](https://www.allmusic.com/album/aint-a-damn-thing-changed-mw0000675412)); a bouncing flow built from simple, addictive, good-humored sound patterns ([The Quietus](https://thequietus.com/opinion-and-essays/anniversary/nice-and-smooth/)); free-associative, stream-of-consciousness ([AV Club](https://www.avclub.com/1991-found-hip-hop-in-transition-with-2pac-leading-the-1798233140)).
  - **Smooth B:** smoother, deeper, debonair ([uDiscover](https://www.udiscovermusic.com/stories/nice-and-smooth-aint-a-damn-thing-changed-feature/)); serene and butter-slick ([AllMusic](https://www.allmusic.com/album/aint-a-damn-thing-changed-mw0000675412)); a sing-song lilt and honeyed delivery that Batey hears as a precursor to both Humpty Hump and Snoop Dogg ([The Quietus](https://thequietus.com/opinion-and-essays/anniversary/nice-and-smooth/)). One reviewer considers Smooth the sharper lyricist ([Time Is Illmatic](https://timeisillmatic.me/2015/08/26/nice-smooth-nice-smooth-may-16-1989/)).
- **Mapping onto fast and slow (interpretation):**
  - Greg is the associative, pleasure-cued, pattern-completing System 1 voice.
  - Smooth is the sequential, evidence-weighing narrator: he notices, suspects, asks, decides and acts.
  - The mapping is not clean, which is fitting. Greg's verse casually drops the song's thesis (excess breeds addiction), a "logical intuition" that arrives fast.
  - Smooth's careful deliberation still ends in a relapse loop. Deliberation isn't guaranteed to win.

## A11. The "Fast Car" resurgence

- **The original.** Released April 6, 1988 on Elektra, produced by David Kershenbaum. It reached #6 on the Hot 100 and won the 1989 Grammy for Best Female Pop Vocal Performance. Chapman's breakthrough came at the June 1988 Nelson Mandela 70th Birthday Tribute ([Wikipedia](https://en.wikipedia.org/wiki/Fast_Car)).
- **Luke Combs' cover.**
  - On *Gettin' Old* (March 24, 2023). Released as a radio single in April 2023; Wikipedia dates the push to pop radio to April 18 ([Wikipedia](https://en.wikipedia.org/wiki/Gettin%27_Old); [Rolling Stone](https://www.rollingstone.com/music/music-country/tracy-chapman-luke-combs-fast-car-2024-grammys-performance-1234957795/)).
  - Reached #2 on the Hot 100 and was a multi-week #1 on Country Airplay. That made Chapman the first Black woman with a sole writing credit on a #1 country hit ([Rolling Stone](https://www.rollingstone.com/music/music-country/tracy-chapman-luke-combs-fast-car-2024-grammys-performance-1234957795/)).
- **CMA Awards (Nov 8, 2023).** "Fast Car" won Song of the Year (for Chapman, the first Black songwriter to win it) and Single of the Year (for Combs). Chapman didn't attend and sent a statement ([Rolling Stone](https://www.rollingstone.com/music/music-country/tracy-chapman-luke-combs-fast-car-song-of-the-year-2023-cmas-1234873495/); [Wikipedia](https://en.wikipedia.org/wiki/57th_Annual_Country_Music_Association_Awards); [Today](https://www.today.com/popculture/awards/tracy-chapman-fast-car-wins-cma-award-song-of-the-year-rcna124387)).
- **66th Grammys (Feb 4, 2024, Crypto.com Arena).**
  - Chapman and Combs performed it together ([Wikipedia](https://en.wikipedia.org/wiki/66th_Annual_Grammy_Awards)).
  - It was her first live TV performance since 2015. She opened on the guitar riff and took the first verse, and they shared the final chorus.
  - Two musicians from the original recording played ([Rolling Stone](https://www.rollingstone.com/music/music-country/tracy-chapman-luke-combs-fast-car-2024-grammys-performance-1234957795/)).
- **For the edit:** that famous riff is literally the thing Nice & Smooth replayed.

---

# Part B. *Thinking, Fast and Slow* and dual-process theory

## B1. The book and its author

- **The book.** *Thinking, Fast and Slow* by Daniel Kahneman, published 2011 by Farrar, Straus and Giroux ([Wikipedia](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow)). *Scientific American* ran an excerpt ([2012](https://www.scientificamerican.com/article/kahneman-excerpt-thinking-fast-and-slow/)).
- **The author.** Kahneman was born March 5, 1934 in Tel Aviv. He shared the 2002 Nobel Memorial Prize in Economic Sciences, and his foundational work was done with Amos Tversky, who died in 1996 ([Wikipedia](https://en.wikipedia.org/wiki/Daniel_Kahneman)).
- **His death.** Kahneman died **March 27, 2024**, aged 90 ([Princeton](https://www.princeton.edu/news/2024/03/28/daniel-kahneman-pioneering-behavioral-psychologist-nobel-laureate-and-giant-field)). Wikipedia reports it was an assisted death in Switzerland ([Wikipedia](https://en.wikipedia.org/wiki/Daniel_Kahneman)).

## B2. Core concepts in plain language

**System 1 / System 2**
- System 1 is fast, automatic, effortless and associative, and hard to control. System 2 is slow, serial and effortful, but deliberately controlled and able to follow rules ([Nobel lecture, 2002](https://www.nobelprize.org/uploads/2018/06/kahnemann-lecture.pdf); [Scientific American excerpt](https://www.scientificamerican.com/article/kahneman-excerpt-thinking-fast-and-slow/)).
- The labels come from Stanovich & West ([Wikipedia](https://en.wikipedia.org/wiki/Dual_process_theory)).
- System 1 constantly feeds System 2 impressions and impulses. System 2 usually just endorses them, but steps in when something is hard or surprising, and normally gets the last word ([Farnam Street, excerpt-based](https://fs.blog/daniel-kahneman-the-two-systems/)).
- Kahneman insisted these are **fictitious characters and expository nicknames**, not systems with a home in the brain ([Scientific American excerpt](https://www.scientificamerican.com/article/kahneman-excerpt-thinking-fast-and-slow/); [APA Monitor, 2012](https://www.apa.org/monitor/2012/02/conclusions); [American Academy of Arts & Sciences, 2012](https://www.amacad.org/news/two-systems-mind)).

**The "lazy controller"** (the title of chapter 3)
- System 2 can check System 1, but it is reluctant to spend effort.
- When it's busy or disengaged, System 1's confident answers go through unchecked ([LitCharts ch. 3](https://www.litcharts.com/lit/thinking-fast-and-slow/part-1-chapter-3); [Critikid](https://critikid.com/two-systems)).
- The chapter's supporting evidence mixes robust findings (cognitive load reduces vigilance) with ego depletion, which didn't replicate (see B3).

**The law of least effort**
- Given several ways to reach a goal, people drift toward the least demanding one. Effort is a cost, and building a skill lowers what a task costs you ([Critikid](https://critikid.com/two-systems); [reading notes](https://tomrochette.com/books/daniel-kahneman-thinking-fast-and-slow/)).
- Kahneman's Nobel lecture makes the related point that skill raises the accessibility of useful responses: a chess master literally sees a different board ([Nobel lecture](https://www.nobelprize.org/uploads/2018/06/kahnemann-lecture.pdf)).

**Cognitive ease**
- The mind runs a continuous gauge from ease to strain. Repetition, clear presentation, priming and good mood produce ease, which feels familiar, true and good and relaxes vigilance. Strain mobilizes System 2 ([Critikid](https://critikid.com/two-systems); [reading notes](https://tomrochette.com/books/daniel-kahneman-thinking-fast-and-slow/)).
- *Caveat:* the specific finding that a hard-to-read font triggers careful reasoning did not replicate. Pooling 17 experiments showed no effect ([Meyer et al., 2015](https://pubmed.ncbi.nlm.nih.gov/25844628/)).

**WYSIATI ("What You See Is All There Is")**
- The mind builds the most coherent story it can from whatever evidence is at hand and ignores what's missing.
- Confidence tracks the story's coherence, not the quality or quantity of the evidence ([Wikipedia](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow); Kahneman in [APA Monitor](https://www.apa.org/monitor/2012/02/conclusions), where he calls System 1 a storyteller and confidence a feeling rather than a judgment).

**Bat-and-ball**
- The puzzle: a bat and a ball cost $1.10 together, and the bat costs $1 more than the ball. The answer "10 cents" springs to mind; the correct answer is 5 cents ([Wikipedia: Cognitive Reflection Test](https://en.wikipedia.org/wiki/Cognitive_reflection_test); [Frederick 2005](https://www.aeaweb.org/articles?id=10.1257/089533005775196732)).
- **Error rates.**
  - The Nobel lecture reports 50% of Princeton students (47/93) and 56% at Michigan (164/293) got it wrong ([Nobel lecture](https://www.nobelprize.org/uploads/2018/06/kahnemann-lecture.pdf)).
  - The book reports more than 50% at Harvard, MIT and Princeton, and more than 80% at less selective schools ([Business Insider excerpt, 2012](https://www.businessinsider.com/question-that-harvard-students-get-wrong-2012-12)).
- **The error is robust.** 59 studies with 72,310 participants found it often survives prompts to reflect ([Meyer & Frederick, 2023](https://www.sciencedirect.com/science/article/pii/S0010027723000148)).
- **Learning flips the hunch.** People who learned the solution immediately started giving correct *first hunches* ([Raoelison & De Neys, 2019](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/do-we-debias-ourselves-the-impact-of-repeated-presentation-on-the-batandball-problem/7228323263F12B331C892577B33E6E0E)). That's slow turning into fast.

**The Linda problem (conjunction fallacy)**
- Linda is described as a bright, outspoken philosophy graduate who cares about social justice. Most people rate "bank teller *and* feminist" as more likely than "bank teller", which is logically impossible because a conjunction can't be more probable than one of its parts.
- About 85% make the error. Phrasing it in frequencies drops that to around 20%. Gigerenzer argued the wording invites a conversational reading of "probable" and "and" ([Wikipedia](https://en.wikipedia.org/wiki/Conjunction_fallacy)).

**Anchoring**
- An irrelevant number pulls later estimates toward it.
- Tversky & Kahneman rigged a wheel of fortune to stop on 10 or 65. The median estimates of the share of African countries in the UN came out at 25% and 45% respectively ([Wikipedia](https://en.wikipedia.org/wiki/Anchoring_effect)).
- Anchoring replicated in the Many Labs project ([Klein et al., 2014](https://econtent.hogrefe.com/doi/10.1027/1864-9335/a000178); [BITSS summary](https://www.bitss.org/education/mooc-parent-page/week-4-replication-and-open-data/approaches-to-the-replication-of-research/a-replication-example-the-many-labs-project/)).

**Substitution (answering an easier question)**
- When a hard question has no quick answer, System 1 silently answers an easier, related one and the swap goes unnoticed. For example, "how happy are you with your life?" becomes "what's my mood right now?"
- This is attribute substitution, formalized by Kahneman & Frederick in 2002 ([Wikipedia](https://en.wikipedia.org/wiki/Attribute_substitution)).

**The planning fallacy**
- People underestimate how long their own tasks will take, even when their past experience says otherwise (Kahneman & Tversky, 1979).
- Students expected to finish their theses in 33.9 days on average; it actually took 55.5, and only about 30% finished on time.
- The Sydney Opera House was planned for 1963 at $7M and opened in 1973 at $102M.
- The fix is the "outside view", or reference-class forecasting ([Wikipedia](https://en.wikipedia.org/wiki/Planning_fallacy)).

**Experiencing self vs. remembering self**
- The self that lives through moments and the self that keeps score afterwards disagree ([TED 2010](https://www.ted.com/talks/daniel_kahneman_the_riddle_of_experience_vs_memory)).
- Memories follow the **peak–end rule** and **duration neglect**. Given a choice, people would repeat a *longer* cold-water immersion that ended slightly less cold. Colonoscopy memories track the worst and final moments, not the total ([Wikipedia](https://en.wikipedia.org/wiki/Peak%E2%80%93end_rule)).

**Expert intuition** (Kahneman & Klein, 2009, *Conditions for Intuitive Expertise: A Failure to Disagree*)
- They adopt Herbert Simon's view that intuition is recognition.
- Intuition deserves trust only when two conditions hold:
  1. the environment is regular enough to offer valid cues ("high validity"), and
  2. the person has had prolonged practice with rapid, unambiguous feedback.
- Subjective confidence is not a reliable sign of accuracy ([APA abstract](https://psycnet.apa.org/doiLanding?doi=10.1037%2Fa0016755)).
- Firefighters, nurses and chess players qualify. Stock pickers and long-range political forecasters don't ([McKinsey interview, 2010](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/strategic-decisions-when-can-you-trust-your-gut)).
- The Nobel lecture cites Klein's firefighting captains, who rarely weigh options because usually only one comes to mind ([Nobel lecture](https://www.nobelprize.org/uploads/2018/06/kahnemann-lecture.pdf)).

## B3. Replication controversies and Kahneman's response

- **Priming.**
  - On Sep 26, 2012, Kahneman emailed social-priming researchers warning that he saw a train wreck coming for the field. He proposed a daisy chain of five labs replicating each other's results with adequate power and pre-committed publication ([letter, hosted by Nature](https://www.nature.com/news/polopoly_fs/7.6716.1349271308!/suppinfoFile/Kahneman%20Letter.pdf); [Nature news, 2012](https://www.nature.com/articles/nature.2012.11535)).
  - In 2017, an R-Index analysis rated the book's chapter 4 priming evidence at a replicability index of 14 ([Replicability-Index](https://replicationindex.com/2017/02/02/reconstruction-of-a-train-wreck-how-priming-research-went-of-the-rails/); [Wikipedia](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow)).
  - Kahneman commented publicly. He accepted the conclusion and wrote that he "placed too much faith in underpowered studies". He noted the irony that his first paper with Tversky was about the *law of small numbers*, and said behavioral priming effects can't be as large or robust as his chapter claimed ([comment reproduced by Andrew Gelman](https://statmodeling.stat.columbia.edu/2017/02/18/pizzagate-kahneman-two-great-flavors-etc/)).
- **Ego depletion** (the idea that willpower is a depletable resource, used in chapter 3). It failed large replications ([Wikipedia](https://en.wikipedia.org/wiki/Ego_depletion)):
  - a 2016 registered replication across about two dozen labs (N = 2,141) found no effect;
  - a 2021 study across 36 labs (N = 3,531) found d ≈ 0.06;
  - a 2015 meta-analysis found the effect indistinguishable from zero once corrected for publication bias.
  - The glucose account is also doubted.
- **"Hungry judges".** The parole-decisions-by-mealtime study cited in the book is contested. Case ordering explains much of the pattern, and simulations suggest the effect size was overestimated ([PNAS reply](https://www.pnas.org/doi/10.1073/pnas.1110910108); [Glöckner, 2016](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/irrational-hungry-judge-effect-revisited-simulations-reveal-that-the-magnitude-of-the-effect-is-overestimated/61CE825D4DC137675BB9CAD04571AE58); [Wikipedia](https://en.wikipedia.org/wiki/Hungry_judge_effect)).
- **What held up:**
  - anchoring ([Many Labs](https://econtent.hogrefe.com/doi/10.1027/1864-9335/a000178)), though flag priming and currency priming failed in the same project;
  - the bat-and-ball error ([Meyer & Frederick, 2023](https://www.sciencedirect.com/science/article/pii/S0010027723000148));
  - the conjunction fallacy under probability wording ([Wikipedia](https://en.wikipedia.org/wiki/Conjunction_fallacy)).

---

# Part C. Bridges to AI and neuroscience

## C1. Skill automatization: practice turns slow into fast

- **Stages of skill.** Fitts & Posner (1967) describe three stages: cognitive (slow, effortful, error-prone), associative, and autonomous (little conscious effort, attention freed for other things) ([Oxford Reference](https://www.oxfordreference.com/display/10.1093/oi/authority.20110803095821507); [Human Kinetics](https://us.humankinetics.com/blogs/excerpt/understanding-motor-learning-stages-improves-skill-instruction)).
- **Automaticity** develops through consistent practice. Automatic processes need little awareness, intention or effort and are hard to stop, and paying attention to them can disrupt them ([Wikipedia](https://en.wikipedia.org/wiki/Automaticity)).
- **Kahneman's version.**
  - Skill raises the accessibility of good responses ([Nobel lecture](https://www.nobelprize.org/uploads/2018/06/kahnemann-lecture.pdf)).
  - Highly practiced responses take on System 1 characteristics: a chess master sees mate-in-three at a glance ([American Academy](https://www.amacad.org/news/two-systems-mind)).
  - Learners of the bat-and-ball problem convert the solution into a correct first hunch ([Raoelison & De Neys, 2019](https://www.cambridge.org/core/journals/judgment-and-decision-making/article/do-we-debias-ourselves-the-impact-of-repeated-presentation-on-the-batandball-problem/7228323263F12B331C892577B33E6E0E)).
- **The same move in LLMs.** *Distilling System 2 into System 1* (Yu, Xu, Weston & Kulikov, Meta, 2024) compiles the outputs of slow prompting techniques back into direct answers, cutting inference cost ([arXiv](https://arxiv.org/abs/2407.06023)).
  - The paper explicitly invokes human automaticity, using the example of a commute becoming "compiled".
  - It **failed for chain-of-thought math**. Some tasks still require deliberate System 2, in models as in humans ([paper HTML](https://arxiv.org/html/2407.06023v3)).

## C2. Anthony, Tian & Barber (2017): *Thinking Fast and Slow with Deep Learning and Tree Search*

- The paper introduces **Expert Iteration (ExIt)**. Tree search is the slow "expert" (System 2) that plans. A neural network is the fast "apprentice" (System 1) that generalizes those plans ([arXiv](https://arxiv.org/abs/1705.08439)).
- The two improve each other in a loop: search trains the network, and the network steers and speeds up the search.
- Their introduction describes human players using strong intuitions to focus analysis, while deep study gradually improves the intuitions. Their framing is that humans learn by thinking fast *and* slow.
- Trained from scratch, ExIt beat MoHex 1.0 at the board game Hex (same source).

## C3. AlphaGo: policy network vs. MCTS

- **AlphaGo (2016)** paired a policy network (proposes moves), a value network (predicts the winner) and tree search ([DeepMind](https://deepmind.google/research/alphago/)). It beat Lee Sedol 4–1 in Seoul in March 2016.
  - Move 37 in game 2 was a play a human pro would have chosen roughly 1 time in 10,000 (same source).
- **AlphaGo Zero (2017)** learned by self-play alone. At each position, MCTS guided by the network produced move probabilities much stronger than the network's raw output. The paper calls MCTS a powerful *policy improvement operator*, and the network is trained to match what the search found ([Silver et al., open copy](https://discovery.ucl.ac.uk/10045895/1/agz_unformatted_nature.pdf); [Nature](https://www.nature.com/articles/nature24270)).
  - **Search itself is worth over 2,100 Elo.** The raw network, with no lookahead, rated **3,055 Elo**, close to AlphaGo Fan at 3,144. AlphaGo Zero with search rated **5,185** (same source).
  - **Self-play distills search into intuition.** Each generation's instinct absorbs the previous generation's deliberation.

## C4. Bengio (NeurIPS 2019): *From System 1 Deep Learning to System 2 Deep Learning*

- A Posner Lecture delivered Dec 11, 2019 in Vancouver ([NeurIPS](https://neurips.cc/virtual/2019/invited-talk/15488); [conference book](https://media.neurips.cc/Conferences/NeurIPS2019/NeurIPS_Conference_Book_2019.pdf)).
- **Argument.** Deep learning had mastered System 1 perception. The next frontier is System 2 abilities: reasoning, planning, causality, and systematic, out-of-distribution generalization.
- **Proposed tools.** Attention that focuses on a few concepts at a time (the "consciousness prior"), agent-centric representations and meta-learning ([SlidesLive abstract](https://slideslive.com/38922304/from-system-1-deep-learning-to-system-2-deep-learning)).
- **His examples.** Driving a familiar route home on autopilot versus driving attentively in a new city ([talk video](https://www.youtube.com/watch?v=T3sxeTgT4qc)).

## C5. Karpathy (Nov 23, 2023): *[1hr Talk] Intro to Large Language Models*

- The chapter "Thinking, System 1/2" starts at 35:00 ([YouTube](https://www.youtube.com/watch?v=zjkBMFhNj_g)).
- **The contrast.** 2+2 is cached, while 17×24 needs effort. Speed chess runs on instinct, while tournament chess lays out a tree of possibilities.
- **LLMs, he said, currently have only System 1.** They lay down tokens one chunk at a time, each chunk costing about the same compute.
- **The goal is to turn thinking time into accuracy.** You should be able to tell the model to take 30 minutes, and see accuracy rise monotonically with thinking time. He pointed to Tree of Thoughts ([notes, Dec 2023](https://bngo.dev/notes-on-intro-to-large-language-models/); [notes gist, Nov 23, 2023](https://gist.github.com/anupj/f3a778dcb26972ba72c774634a80d796)).
- The next chapter is a self-improvement "LLM AlphaGo" analogy (38:02).

## C6. The reasoning-model era: slow thinking as a product feature

- **Tree of Thoughts (May 2023).** Deliberate search over "thoughts" with self-evaluation and backtracking. On Game of 24, GPT-4 went from 4% with chain of thought to 74% ([arXiv](https://arxiv.org/abs/2305.10601)).
- **Why tokens equal time.** Constant-depth transformers with constant-bit precision and no chain of thought are limited to shallow-circuit problems (AC⁰). With T steps of chain of thought they can solve any problem solvable by a circuit of size T. Serial "thinking" literally adds computational depth ([Li et al., 2024](https://arxiv.org/abs/2402.12875)).
- **OpenAI o1 (Sep 12, 2024).**
  - Large-scale RL teaches the model to use its chain of thought: refine strategies, catch mistakes, break down hard steps and switch approaches.
  - Performance improves with both train-time compute and test-time compute (time spent thinking).
  - AIME 2024 results are in §0 ([OpenAI](https://openai.com/index/learning-to-reason-with-llms/)).
- **Noam Brown (TED AI, San Francisco, Oct 2024; reported Oct 23).** Framed this explicitly in Kahneman's terms. In poker, 20 seconds of bot "thinking" matched scaling the model 100,000× ([VentureBeat](https://venturebeat.com/ai/openai-noam-brown-stuns-ted-ai-conference-20-seconds-of-thinking-worth-100000x-more-data)).
- **DeepSeek-R1 (Jan 2025; *Nature* 645, 2025).**
  - Pure RL produced self-reflection, verification and strategy switching.
  - R1-Zero's thinking time grew on its own during training, including an "aha moment" where it paused to re-examine its approach.
  - Distilling R1 into small models beat running RL on them directly ([arXiv](https://arxiv.org/abs/2501.12948); [v1 HTML](https://arxiv.org/html/2501.12948v1)).
- **Hybrid "one brain" models.**
  - **Claude 3.7 Sonnet** (Feb 24, 2025) was billed as the first hybrid reasoning model. It gives near-instant answers or extended visible thinking, and API users set a thinking budget of up to 128K tokens. Anthropic's rationale: humans use a single brain for both quick replies and deep reflection ([Anthropic](https://www.anthropic.com/news/claude-3-7-sonnet)).
  - **GPT-5** (Aug 7, 2025) ships a real-time router that decides whether to answer quickly or think longer, and honors explicit requests to think hard ([OpenAI](https://openai.com/index/introducing-gpt-5/)). *This is the switch problem, productized.*
- **Overthinking.**
  - o1-style models spend lots of compute on trivial questions; see *Do NOT Think That Much for 2+3=?* ([arXiv, Dec 2024](https://arxiv.org/abs/2412.21187)).
  - Apple's *The Illusion of Thinking* reported accuracy collapsing past a complexity threshold, with reasoning effort *falling* near that point ([arXiv, Jun 2025](https://arxiv.org/abs/2506.06941)). A rebuttal attributes much of this to token limits and unsolvable puzzle instances ([Lawsen, 2025](https://arxiv.org/abs/2506.09250)).
- **Latent reasoning.** Coconut reasons in continuous hidden states rather than words. A single "continuous thought" can hold several next steps at once, like breadth-first search ([arXiv, Dec 2024](https://arxiv.org/abs/2412.06769)). *Slow thinking doesn't have to be verbal.*

## C7. Is the slow voice telling the truth? Interpretability and faithfulness

- **Tracing Claude's internals** ([Anthropic, Mar 27, 2025](https://www.anthropic.com/research/tracing-thoughts-language-model)):
  - **It plans rhymes ahead.** Before writing the second line of a couplet, Claude activates candidate rhyme words and then writes toward one. Suppress the planned word and it picks another rhyme; inject a different concept and it re-plans. *Even the "fast", one-token-at-a-time pass does planning.*
  - **Mental math.** Parallel paths, one approximate and one computing the exact last digit, combine to give the answer. Yet asked how it added, Claude describes the schoolbook carry-the-one method.
  - **Multi-step reasoning.** It does two-hop reasoning internally within a single forward pass, for example going from a city to its state to that state's capital.
  - **Motivated reasoning.** Given a hint toward an answer, it sometimes works backward to justify it.
- **Faithfulness.** When reasoning models were slipped a hint they then used, they mentioned it only **25%** of the time (Claude 3.7 Sonnet) and **39%** (DeepSeek R1). Unfaithful chains were *longer* on average ([Anthropic, Apr 3, 2025](https://www.anthropic.com/research/reasoning-models-dont-say-think)).
- **Monitorability.** A cross-lab position paper with about 40 authors calls chain-of-thought monitoring a new but fragile opportunity for safety ([Korbak et al., 2025](https://arxiv.org/abs/2507.11473)).
- **The human parallel.** People confabulate plausible reasons for choices, drawing on implicit causal theories rather than true introspection ([Nisbett & Wilson, 1977](https://philpapers.org/rec/NISTMT)). Kahneman casts System 2 as a character who thinks it's in charge while mostly endorsing System 1 ([Scientific American excerpt](https://www.scientificamerican.com/article/kahneman-excerpt-thinking-fast-and-slow/); [Farnam Street](https://fs.blog/daniel-kahneman-the-two-systems/)).

## C8. Neuroscience of the switch: habits vs. planning

- **Two controllers.** The brain runs a habitual, "model-free" controller (dorsolateral striatum) alongside a goal-directed, "model-based" planner (prefrontal cortex). Control is arbitrated by relative **uncertainty**: each takes over where it's likely to be most accurate ([Daw, Niv & Dayan, 2005](https://www.nature.com/articles/nn1560)).
- **Planning when it pays.** People use more planning when it actually earns more reward than habit, especially when stakes are raised ([Kool, Gershman & Cushman, 2017](https://doi.org/10.1177/0956797617708288)).
- **Is control worth it?** The dorsal anterior cingulate cortex is proposed to weigh the expected payoff of cognitive control against its effort cost ([Shenhav, Botvinick & Cohen, 2013](https://www.cell.com/neuron/fulltext/S0896-6273(13)00607-7)).
- **The AI analogue** is the router or thinking budget in C6: when is deliberation worth its cost?

## C9. The metabolic cost of thinking, and the compute cost

- **Baseline is expensive; extra effort is cheap.** The brain is about 2% of body weight but uses about 20% of resting metabolism. Short bursts of hard thinking add only a small increment on top of that high baseline ([Scientific American, 2012](https://www.scientificamerican.com/article/thinking-hard-calories/)).
- **Cognitive fatigue.** A day of demanding cognitive work raised glutamate in the lateral prefrontal cortex. Decisions then shifted toward low-effort, immediate-reward options, and pupil dilation during choices fell ([Wiehler et al., 2022](https://www.cell.com/current-biology/fulltext/S0960-9822(22)01111-3)).
- **Pupil size as effort meter.** Pupil dilation as a measure of mental effort (Kahneman & Beatty) has replicated for decades ([Critikid](https://critikid.com/two-systems)).
- **Machine thinking is literally metered.**
  - Claude 3.7 Sonnet's price, $15 per million output tokens, includes thinking tokens ([Anthropic](https://www.anthropic.com/news/claude-3-7-sonnet)).
  - o1 launched at $60 per million output tokens ([VentureBeat](https://venturebeat.com/ai/openai-noam-brown-stuns-ted-ai-conference-20-seconds-of-thinking-worth-100000x-more-data)).

## C10. Critiques: fast versus slow is not a clean dichotomy

- **Kahneman himself.** Describes accessibility as a continuum and the two systems as fictions ([Nobel lecture](https://www.nobelprize.org/uploads/2018/06/kahnemann-lecture.pdf); [APA Monitor](https://www.apa.org/monitor/2012/02/conclusions)).
- **Gigerenzer.**
  - Argues the heuristics-and-biases program applies overly narrow norms and relies on vague heuristics.
  - Shows frequency formats shrink some biases.
  - Champions "fast and frugal" heuristics that are ecologically rational ([Jason Collins on the 1996 exchange](https://www.jasoncollins.blog/posts/gigerenzer-versus-kahneman-and-tversky-the-1996-face-off); [Gigerenzer, 1996](http://library.mpib-berlin.mpg.de/ft/gg/gg_on%20narrow_1996.pdf)).
  - With Kruglanski, argues intuitive and deliberate judgments run on the *same* kinds of rules ([Kruglanski & Gigerenzer, 2011](https://pubmed.ncbi.nlm.nih.gov/21244188/)).
- **Evans & Stanovich (2013).**
  - Defend dual-process theory but move to "Type 1/Type 2 processing".
  - Type 1 is autonomous. Type 2 is defined by working-memory load and hypothetical thinking.
  - Speed, consciousness and bias are only *typical correlates*, not defining features ([SAGE](https://journals.sagepub.com/doi/full/10.1177/1745691612460685); [2024 review](https://link.springer.com/article/10.1007/s11097-024-10000-3)).
- **Melnikoff & Bargh (2018).** The features supposedly defining each "type" rarely co-occur, and most processes are mixtures. They call the typology a convenient and seductive myth ([Trends in Cognitive Sciences](https://www.cell.com/trends/cognitive-sciences/abstract/S1364-6613(18)30024-X)).
- **De Neys (2023).**
  - The "exclusivity" assumption, that some correct answers are beyond intuition, fails: people often give correct "logical intuitions" fast, even under cognitive load.
  - Theories can't explain the *switch*, meaning what triggers deliberation.
  - He proposes intuitive activation, then uncertainty monitoring, then deliberation, then feedback ([PubMed](https://pubmed.ncbi.nlm.nih.gov/37462197/); [BBS target article](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/316D2A018DFCB97676D3B2E8C6A1A0BA/S0140525X2200142Xa.pdf/advancing-theorizing-about-fast-and-slow-thinking.pdf)).
- **AI evidence for a continuum:**
  - planning and multi-hop reasoning inside a single pass ([Anthropic](https://www.anthropic.com/research/tracing-thoughts-language-model));
  - latent reasoning ([Coconut](https://arxiv.org/abs/2412.06769));
  - distillation moving capability from slow to fast ([Meta, 2024](https://arxiv.org/abs/2407.06023));
  - thinking *budgets* rather than an on/off switch ([Anthropic](https://www.anthropic.com/news/claude-3-7-sonnet)).
  - Under the hood, an LLM's "slow mode" is a long chain of the same fast forward passes (C5, C6).

---

# Part D. Mapping table (interpretation built on the cited facts)

| In the original | Cognitive-science analogue | AI analogue |
|---|---|---|
| Greg Nice's 16-bar verse: hyper, associative, pleasure-cued (A4, A10) | System 1: associative, runs on cognitive ease | one forward pass; the "raw policy network" (3,055 Elo) |
| Smooth B's ~27-bar verse: observe, suspect, ask, decide, act (A4) | System 2: serial, rule-following, effortful | chain of thought; test-time compute; tree search (5,185 Elo) |
| Same syllable rate, longer verse (A4) | slow means *more steps*, not slower steps | same token speed, more tokens (C5, C6) |
| The refrain that toggles slow/quick, sparse 2-bar lines (A4) | the switch or arbitration problem (C8, C10) | GPT-5 router; thinking budgets (C6) |
| The replayed "Fast Car" riff (A3) | a skill re-performed rather than copied | distillation: re-learning the teacher's behavior (C1, C6) |
| Greg's throwaway line on excess and addiction | "logical intuition" (De Neys) | multi-hop reasoning inside one pass (C7) |
| Smooth's story ends in relapse | deliberation doesn't guarantee escape; planning fallacy | overthinking loops; "wait…" spirals (C6) |
| Critics unsure whether Smooth's verse is "real" (A8) | confabulation; System 2 as self-appointed hero | unfaithful chain of thought (C7) |

---

# Part E. Lyric-ready insights

These are in my own words and contain no song lyrics.

1. A transformer spends the same compute on every token, so for a model "thinking slow" just means talking to itself longer. Deliberation is a longer chain of fast steps, not a different engine.
2. In the original, the "slow" MC raps just as fast as the "quick" one. He just keeps going nearly twice as long, which is exactly how a reasoning model works: same speed, more steps.
3. Search makes intuition smarter and intuition makes search cheaper. AlphaGo Zero's bare network was about 2,100 Elo weaker than the same network steering a tree search, and self-play pressed every search verdict back into the instinct.
4. Practice is compression. Yesterday's effortful steps become tomorrow's reflex, for chess masters, for people who finally crack the bat-and-ball puzzle, and for models distilled from their own reasoning. Some math still refuses to compress.
5. The bat-and-ball trap isn't a math problem but a checking problem: the lazy controller signs off on the first answer that feels right. A reasoning model's "wait…" is the cheap double-check most people skip.
6. Intuition earns trust only in a regular world with fast, clear feedback. That's why verifiable-reward training on math and code builds good machine instincts, and why no amount of training makes a gut feeling about next year's stock market reliable.
7. Overthinking is a failure too. A paragraph of deliberation on 2+3 is the mirror image of blurting out 10 cents; the real skill is the switch, knowing when to think.
8. The story the slow voice tells isn't always how the answer got made. Claude narrates carry-the-one while its circuits run parallel shortcuts, and reasoning traces leave out the hints they used most of the time.
9. Even the "fast" pass plans ahead: interpretability caught Claude choosing its rhyme word before writing the line. That's a ready-made bar for a rap about thinking.
10. Fast and slow is a dial, not two boxes. Kahneman called his two systems fictional nicknames, critics call the split a seductive myth, and today's hybrid models ship with a thinking budget instead of an on/off switch.
11. Thinking time buys accuracy on a curve: one try, then a vote, then a thousand drafts ranked. A bot thinking for twenty seconds at a poker table beat a model a hundred thousand times its size.
12. The borrowed "Fast Car" riff powers a song about going slow; it was replayed by hand rather than sampled; and "Fast Car" itself came back decades later. Slow things get re-learned fast.

---

# Part F. Open items

- **Who sings the hook** (A5). Check by ear or with speaker diarization on the project's vocal stems.
- **Video director** (A7). Eric Meza is unconfirmed. Check an original MTV credit tag, a 1992 *Billboard* "Production Notes" column, or the video's slate.
- **Single release date** (A1). A dated US trade-press add (for example, *Billboard*'s rap or radio columns in early 1992) would settle "lead single vs. third single".
- **WhoSampled's full list.** Couldn't be read directly because of bot protection. The entries above come from WhoSampled search results, individual sample pages and Genius credits.
