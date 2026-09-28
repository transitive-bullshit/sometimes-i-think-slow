"""The storyboard shot list for "Sometimes I Think Slow": the single source of truth for frames, captions and edits.

Times are seconds on the Suno final take (105.24 BPM, bar = 2.281 s, bar 1 at 0.125 s). Each shot starts on its
lyric (from analysis/suno/lyrics-timed.json) and runs to the next shot. Captions are attached automatically from the
timed lyrics (display spellings). Modes set the look: "hook" (dusk underpass, warm left / cool right), "fast"
(saturated FAST world), "slow" (monochrome sumi-e ink wash; FAST keeps a faint wash of his orange in SLOW's memories),
"sunrise" (hook 3 onward: unified warm color).

Lip-sync policy: the cut works WITHOUT lip-sync; mouths are hidden or off-camera in performance shots and captions
carry the words. A few close-ups are marked lipsync=<alt plan> and get a second, lip-synced version at the video stage.
"""

SHOTS = [
    # ---------------- HOOK 1: the underpass, dusk ----------------
    dict(id="S01", start=0.00, section="Intro", mode="hook", insert43=True, title="PLAY",
         scene="Empty highway underpass at dusk seen through a camcorder: slow approach toward the huge mural of two chalk-white "
               "scatter plots titled 'train-time compute' and 'test-time compute'. Sodium lights flicker on, puddles, nobody in frame.",
         camera="Wide, eye level, slight handheld drift", motion="Slow push-in through tracking noise; VHS PLAY OSD",
         text=["train-time compute", "test-time compute"], chars=[], base="k1-underpass-v2"),
    dict(id="S02", start=0.80, section="Hook 1", mode="hook", title="The chant",
         scene="The approved underpass two-shot: FAST under 'train-time compute' pops an ollie, SLOW under 'test-time compute' "
               "stands still reading his notebook. Crew leaning on a car in the background.",
         camera="Medium-wide two-shot, low angle", motion="FAST lands the ollie on 'fast'; SLOW turns one page on 'slow'",
         chars=["FAST", "SLOW"], base="k1-underpass-v2", reuse=True,
         lipsync="Alt (no lip-sync): as boarded; faces angled off-axis, the mural lettering carries the hook."),
    dict(id="S03", start=6.25, section="Hook 1", mode="hook", title="Fast fast fast",
         scene="Three kids from the crew sit on the hood of a boxy 80s sedan under the overpass, stamping the beat with their fists "
               "on the hood, one slapping a skateboard deck; sodium light, graffiti on the pillars.",
         camera="Medium, three-quarter angle, fisheye edge distortion", motion="Three hits on the beat; camera bumps on each hit",
         chars=[]),
    dict(id="S04", start=9.85, section="Hook 1", mode="hook", title="Face the mural",
         scene="Reverse angle from behind the mural wall's base: FAST (left) and SLOW (right) seen from behind, facing the two "
               "painted charts, the city glowing beyond the overpass; FAST mid-spin in a breakdance freeze, SLOW motionless.",
         camera="Wide from behind the characters, low", motion="FAST windmill spin; SLOW's ponytail lifts in the wind", chars=["FAST", "SLOW"],
         text=["train-time compute", "test-time compute"]),
    dict(id="S05", start=14.25, section="Hook 1", mode="fast", title="Pager buzz",
         scene="Extreme close-up of FAST's skateboard wheels spinning over wet asphalt, his beeper on his waistband buzzing and "
               "flashing, orange windbreaker hem in frame; streaks of speed.",
         camera="Macro, ground level", motion="Whip pan into verse 1 with a smear frame", chars=["FAST"]),

    # ---------------- VERSE 1: FAST's day ----------------
    dict(id="S06", start=17.15, section="Verse 1", mode="fast", title="The bowl", rev=2,
         scene="Concrete skate park in bright afternoon sun, framed close enough to read both faces clearly. FAST carves the bowl "
               "at speed, one hand trailing the wall, face turned toward camera; SLOW sits on the coping at the top, calmly "
               "reading, face visible in three-quarter view. FAST is a dark-skinned Black man with a wild mane of short spiky twists and no hat, in his traffic-cone orange, teal and purple windbreaker; SLOW is a Japanese man with long black hair in a low ponytail and thin rectangular glasses, in his camel overcoat and black turtleneck. ",
         camera="High angle over the bowl", motion="FAST circles the bowl twice in one beat; SLOW turns a page", chars=["FAST", "SLOW"],
         lipsync="Alt (no lip-sync): FAST is small in frame and moving; the graffiti caption carries the line."),
    dict(id="S07", start=20.05, section="Verse 1", mode="fast", title="Forward pass",
         scene="FAST throws a perfect football spiral across the park before a kid has finished raising his hand to ask for it; "
               "the ball is already in the kid's arms, the kid stunned.",
         camera="Side angle, FAST foreground left, kid far right", motion="Smear-frame throw; ball arrives instantly", chars=["FAST"]),
    dict(id="S08", start=22.40, section="Verse 1", mode="fast", title="2k tok/s",
         scene="FAST bombs down a steep city hill on his skateboard, a trail of glowing token glyphs sparking off his wheels; a "
               "roadside radar speed sign flashes '2000 TOK/S' above the words 'SLOW DOWN'.",
         camera="Low angle, FAST rushing toward camera", motion="Blur and speed lines; the sign flashes on the beat", chars=["FAST"],
         text=["2000 TOK/S", "SLOW DOWN"]),
    dict(id="S09", start=24.45, section="Verse 1", mode="fast", title="LOW beats HIGH",
         scene="The approved court frame: FAST in the 'LOW' shirt breaks the ankles of the 'HIGH' jersey player, scoreboard "
               "'LOW 21  HIGH 19', effort-slider sign 'INSTANT · MEDIUM · HIGH · XHIGH · MAX'.",
         camera="Medium, court level", motion="Crossover, HIGH falls, crowd erupts", chars=["FAST", "SLOW"], base="k3-court-v2b", reuse=True),
    dict(id="S10", start=26.50, section="Verse 1", mode="fast", title="Make no mistakes",
         scene="A bodega counter with a sticky note on the CRT reading 'MAKE NO MISTAKES'. FAST, mid-motion, has knocked a soda "
               "can, a stack of cassettes and a newspaper rack over at once; a pigeon flaps away. He is already walking out.",
         camera="Wide static, FAST exiting frame right", motion="Three crashes on three beats; FAST never looks back", chars=["FAST"],
         text=["MAKE NO MISTAKES"]),
    dict(id="S11", start=29.05, section="Verse 1", mode="fast", title="Karpathy on the CRT",
         scene="Night bodega: the CRT glows with a social post card 'Andrej Karpathy' '@karpathy' 'no thinking, single token, low "
               "latency'. FAST (no cap, wild twists) stands to the LEFT of the TV and points at it from the side with his "
               "fingertip near the screen's left edge; his hand and arm stay outside the screen so the whole post card is "
               "clearly visible and unobstructed; the screen glow lights his face.",
         camera="Medium, the TV screen fully visible right of center", motion="Slow push toward the screen", chars=["FAST"], rev=2,
         text=["Andrej Karpathy", "@karpathy", "no thinking, single token, low latency"], base="k6a-karpathy-crt"),
    dict(id="S12", start=31.80, section="Verse 1", mode="fast", title="Pager: that's me",
         scene="The approved pager close-up: green LCD 'KARPATHY:' / 'NO THINKING. SINGLE TOKEN. LOW LATENCY'.",
         camera="Extreme close-up", motion="The pager buzzes; FAST's thumb taps his own chest at the frame edge on 'That's me'",
         chars=["FAST"], base="k6b-karpathy-pager", reuse=True),
    dict(id="S13", start=33.85, section="Verse 1", mode="fast", title="The judge",
         scene="FAST sits on an overturned milk crate like a throne on the sidewalk, ruling on two kids' cardboard signs ('YES' / "
               "'NO') instantly, tapping his skateboard like a gavel; a gray pigeon perches on his shoulder.",
         camera="Low angle, FAST centered", motion="Gavel tap on the beat; thumbs up, thumbs down", chars=["FAST"],
         text=["YES", "NO"]),
    dict(id="S14", start=36.35, section="Verse 1", mode="fast", title="Rhyme before the line",
         scene="FAST in profile in front of a brick wall with a spray can; a translucent cyber X-ray overlay of his head shows a "
               "glowing node graph where the single word 'LINE' already lights up, before he has painted anything.",
         camera="Profile medium close", motion="The word lights first; then he sprays in one fluid stroke", chars=["FAST"],
         text=["LINE"], lipsync="Alt (no lip-sync): profile with the X-ray overlay over the mouth area; the caption carries the line."),
    dict(id="S15", start=38.55, section="Verse 1", mode="fast", title="Penny flip",
         scene="Close on FAST's hand flipping a penny in bright sun; behind him, a chalk tally on the wall: nine check marks and "
               "one X.", camera="Close-up, shallow depth", motion="The coin spins in slow motion, then snaps fast", chars=["FAST"]),
    dict(id="S16", start=40.85, section="Verse 1", mode="fast", insert43=True, title="Shipped it",
         scene="Camcorder footage: FAST on a stoop with a chunky 90s laptop covered in a 'SHIP IT' sticker, giving a thumbs up; "
               "beside him a beige server tower is quietly smoking.", camera="Handheld camcorder, slightly tilted",
         motion="Zoom punch-in on the smoke", chars=["FAST"], text=["SHIP IT"]),
    dict(id="S17", start=43.10, section="Verse 1", mode="fast", title="2029",
         scene="Inside the bodega: a wall calendar reads 'SEPTEMBER 1991'; FAST confidently scrawls a big '2029' over it with a "
               "marker. SLOW behind the counter pinches the bridge of his nose.",
         camera="Medium, calendar foreground", motion="Marker scrawl in two strokes", chars=["FAST", "SLOW"],
         text=["SEPTEMBER 1991", "2029"]),
    dict(id="S18", start=45.65, section="Verse 1", mode="fast", title="Ball's a dime",
         scene="The approved bodega counter: sign 'BAT + BALL $1.10'; FAST slaps a single dime down with total confidence.",
         camera="Medium two-shot across the counter", motion="Slap on 'dime'; FAST's grin; the cat blinks", chars=["FAST", "SLOW"],
         base="k2-bodega-v2", reuse=True),
    dict(id="S19", start=48.25, section="Verse 1", mode="fast", title="It's a nickel",
         scene="Insert: SLOW's two fingers slide a single nickel across the worn counter next to FAST's dime; in the background, "
               "out of focus, FAST's grin freezes.", camera="Macro on the counter", motion="The slide, then a hard freeze-frame on FAST",
         chars=["FAST", "SLOW"]),
    dict(id="S20", start=49.20, section="Verse 1", mode="fast", title="Kahneman",
         scene="The approved stoop: SLOW holds up 'THINKING, FAST AND SLOW' by 'DANIEL KAHNEMAN'; FAST points at himself, offended.",
         camera="Medium two-shot on the stoop", motion="SLOW raises the book into frame; FAST's double-take", chars=["FAST", "SLOW"],
         base="k5-book-v2", reuse=True),
    dict(id="S21", start=51.65, section="Verse 1", mode="fast", title="Glazing",
         scene="A 90s donut shop: FAST behind the counter drizzling glaze on donuts with a showman's flourish while beaming at a "
               "delighted customer; hearts and sparkles in the air, a 'FRESH GLAZED' neon sign.",
         camera="Medium, over the display case", motion="Glaze drizzle in rhythm; sparkle pops", chars=["FAST"], text=["FRESH GLAZED"]),
    dict(id="S22", start=53.45, section="Verse 1", mode="fast", title="Ask my twin",
         scene="Same donut shop: FAST jerks a thumb over his shoulder toward SLOW, who sits alone at a back table with his notebook "
               "and a black coffee, slowly raising one finger.", camera="Deep focus, FAST foreground, SLOW background",
         motion="Thumb jerk, then SLOW's finger rises", chars=["FAST", "SLOW"]),
    dict(id="S23", start=55.70, section="Verse 1", mode="fast", title="Snap judgment",
         scene="Night street outside the bodega, neon. FAST (dark skin, wild spiky twists) holds a Polaroid camera at arm's length "
               "for a selfie of the two of them, flash bursting; SLOW (Japanese, low ponytail, rectangular glasses) stands beside "
               "him perfectly still and unimpressed. A freshly ejected Polaroid print hangs from the camera showing the two of them: "
               "FAST a motion blur, SLOW perfectly sharp. Exactly two people in the frame.",
         camera="Medium two-shot, slightly low", motion="Flash white frame; the print develops; freeze",
         chars=["FAST", "SLOW"], base="k2-bodega-v2"),

    # ---------------- HOOK 2: the crew grows ----------------
    dict(id="S24", start=59.05, section="Hook 2", mode="hook", title="Chant, bigger crew",
         scene="The underpass wide from hook 1, same composition, but now a crowd of about ten kids fills the background, some on "
               "skateboards, one with a boombox; FAST and SLOW in front of their charts. SLOW appears exactly once, in the "
               "foreground right; no one in the crowd looks like him (no one else has a ponytail, glasses or a camel coat).",
         camera="Same wide as S02 (chorus anchor)", motion="The crowd bobs on the beat", chars=["FAST", "SLOW"], rev=2,
         text=["train-time compute", "test-time compute"], base="k1-underpass-v2"),
    dict(id="S25", start=63.95, section="Hook 2", mode="hook", title="Stamp",
         scene="Close on a row of the crowd's sneakers stomping in a puddle in unison, splashes catching sodium light.",
         camera="Low, ground level", motion="Three stomps on the beat", chars=[]),
    dict(id="S26", start=66.05, section="Hook 2", mode="hook", title="Face-off",
         scene="FAST and SLOW face each other in profile, inches apart, a vertical line of light between them splitting the frame "
               "warm (FAST, left) and cool (SLOW, right).", camera="Tight profile two-shot", motion="Slow push; neither blinks",
         chars=["FAST", "SLOW"], lipsync="Alt (no lip-sync): silent face-off; the chant plays over their stare."),
    dict(id="S27", start=68.40, section="Hook 2", mode="hook", title="Call",
         scene="SLOW alone on the right half of the frame in cool desaturated tones, calmly pointing to the 'test-time compute' "
               "chart as the crowd watches him.", camera="Medium on SLOW", motion="Point on 'slow'", chars=["SLOW"],
         text=["test-time compute"]),
    dict(id="S28", start=73.15, section="Hook 2", mode="hook", title="Response",
         scene="FAST on the left half in hot saturated color, leaping off the car hood toward camera, the crowd behind him "
               "jumping with fists raised.", camera="Low wide, FAST mid-air", motion="Leap on 'fast', crowd jumps on each hit",
         chars=["FAST"]),
    dict(id="S29", start=79.85, section="Hook 2", mode="transition", title="Color drains",
         scene="Streetlights come on; SLOW walks away from the crowd into the dark end of the underpass, and the frame drains from "
               "color to black ink wash as he goes.", camera="Wide, SLOW walking away from camera",
         motion="Color bleeds out left to right; the chant fades", chars=["SLOW"]),

    # ---------------- VERSE 2: SLOW's story, sumi-e ----------------
    dict(id="S30", start=85.50, section="Verse 2", mode="slow", title="Think longer",
         scene="A dot-matrix printer on a desk spills an endless ribbon of fan-fold paper covered in handwriting; the ribbon runs "
               "across the floor and out of a door into the far distance. SLOW walks alongside it, reading.",
         camera="Long corridor perspective", motion="Printer head chatters; the ribbon keeps unspooling", chars=["SLOW"]),
    dict(id="S31", start=88.60, section="Verse 2", mode="slow", title="Abilene, 3 a.m.",
         scene="The approved sumi-e laundromat: 'ABILENE WASH & FOLD' neon in the rain, SLOW alone on the bench writing.",
         camera="Wide interior", motion="Rain streaks; the dryers spin", chars=["SLOW"], base="k4-laundromat-sumie-b", reuse=True),
    dict(id="S32", start=90.15, section="Verse 2", mode="slow", title="Fans humming low",
         scene="Row of front-loading dryers seen close, their drums spinning like server fans, glowing through the glass in ink "
               "wash; a red 'NOW SERVING 0001' ticket counter on the wall, SLOW's ticket '10,000' on the bench.",
         camera="Slow lateral dolly along the dryers", motion="Drums spin; the ticket counter does not move", chars=[],
         text=["NOW SERVING 0001", "10,000"]),
    dict(id="S33", start=91.20, section="Verse 2", mode="slow", title="Heavy on my weights",
         scene="SLOW sits bent forward on the bench, elbows on knees, glasses in hand; a heavy barbell with iron plates leans "
               "against the bench beside him.", camera="Medium, eye level", motion="Barely moves; rain shadows crawl over him",
         chars=["SLOW"]),
    dict(id="S34", start=93.15, section="Verse 2", mode="slow", title="Quicker, for free",
         scene="Through the rain-streaked laundromat window: FAST zips past outside on his skateboard handing out free samples from "
               "a tray, a crowd chasing him, a 'FREE' sign; FAST's jacket is the only color in the ink-wash frame.",
         camera="Over SLOW's shoulder, window as frame", motion="FAST crosses frame in one beat", chars=["FAST", "SLOW"], text=["FREE"]),
    dict(id="S35", start=95.85, section="Verse 2", mode="slow", title="Roll him back...",
         scene="SLOW raises a chunky 90s VHS remote and points it at a small TV on the laundromat counter that shows FAST "
               "grinning.", camera="Medium close on SLOW, the TV in the foreground", motion="Thumb moves to REW", chars=["FAST", "SLOW"]),
    dict(id="S36", start=97.25, section="Verse 2", mode="slow", insert43=True, title="...to an old checkpoint",
         scene="BEAT DROP. VHS rewind across the TV: tracking lines tear the image; the TV shows a much younger, baby-faced FAST in "
               "a stroller; OSD reads '◀◀ REW  CHECKPOINT'.", camera="Full-frame TV screen", motion="Rewind judder, then freeze",
         chars=["FAST"], text=["REW", "CHECKPOINT"]),
    dict(id="S37", start=98.55, section="Verse 2", mode="slow", title="Out the blue",
         scene="Lightning flashes through the laundromat window and turns everything white for an instant; SLOW's glasses flare, "
               "his face half in shadow.", camera="Close-up on SLOW", motion="White flash, then black", chars=["SLOW"],
         lipsync="Alt (no lip-sync): the flash whites out the frame on the line; his mouth sits in shadow."),
    dict(id="S38", start=100.00, section="Verse 2", mode="slow", title="Next-token predictor",
         scene="A street fortune-teller's card booth at night; SLOW draws one tarot-style card labeled 'NEXT TOKEN'; the card "
               "face is completely blank.", camera="Close on the card in his hand", motion="Card flip; beat of stillness", chars=["SLOW"],
         text=["NEXT TOKEN"]),
    dict(id="S39", start=102.15, section="Verse 2", mode="slow", insert43=True, title="Same weights",
         scene="Home-video flashback: two kids, young FAST and young SLOW, in matching oversized T-shirts on a stoop, arms over "
               "each other's shoulders; FAST's T-shirt keeps a faint wash of orange.", camera="Camcorder, 4:3, date stamp",
         motion="Kids wave at the camera; tape warble", chars=["FAST", "SLOW"]),
    dict(id="S40", start=104.70, section="Verse 2", mode="slow", title="Weight-mates",
         scene="Flashback gym: FAST spots SLOW on a bench press, both laughing, iron plates on the bar; FAST's windbreaker keeps a "
               "faint orange wash.", camera="Medium, side angle", motion="One rep together", chars=["FAST", "SLOW"]),
    dict(id="S41", start=106.65, section="Verse 2", mode="slow", title="Or so I was taught",
         scene="SLOW closes a photo album on his lap with one hand, deadpan, in the laundromat.", camera="Close on the album and his hands",
         motion="The album thumps shut", chars=["SLOW"]),
    dict(id="S42", start=107.80, section="Verse 2", mode="slow", title="Fake case law",
         scene="Courtroom-sketch style (pastel and charcoal): FAST in the witness stand confidently citing from a flashy binder; "
               "the judge glares over her glasses; SLOW in the gallery with his face in his palm.",
         camera="Wide courtroom sketch composition", motion="Pastel strokes draw themselves in", chars=["FAST", "SLOW"]),
    dict(id="S43", start=110.65, section="Verse 2", mode="slow", title="Ten thousand deep",
         scene="A vast lecture hall whose enormous chalkboard is covered in fluid-dynamics equations (Navier-Stokes); a sea of "
               "identical SLOWs, hundreds of them, fill every row, all writing in notebooks.",
         camera="Pull back from one SLOW to reveal hundreds", motion="Slow pull-out", chars=["SLOW"]),
    dict(id="S44", start=112.85, section="Verse 2", mode="slow", title="In the replies",
         scene="FAST sprawled on a couch cracking up at a chunky 90s computer monitor, typing replies; speech bubbles 'lmao' float "
               "up; his jacket keeps a faint orange wash.", camera="Medium, from the monitor's side", motion="Laughing, rapid typing",
         chars=["FAST"], text=["lmao"]),
    dict(id="S45", start=114.85, section="Verse 2", mode="slow", title="Glue on pizza",
         scene="A 90s TV cooking-show set: FAST, on air, proudly squeezing a big white glue bottle onto a pizza; SLOW at the edge of "
               "the set eating an ordinary slice, unbothered.", camera="Multi-cam TV framing, slight fisheye",
         motion="Glue squeeze; SLOW chews", chars=["FAST", "SLOW"]),
    dict(id="S46", start=117.10, section="Verse 2", mode="slow", title="Told you it would slip",
         scene="The approved newsstand: SLOW reads 'GARY MARCUS: \"TOLD YOU IT WOULD SLIP\"'; FAST slips on a banana peel behind him.",
         camera="Medium", motion="The slip lands on 'slip'", chars=["FAST", "SLOW"], base="k7-marcus-v2b"),
    dict(id="S47", start=119.45, section="Verse 2", mode="slow", insert43=True, title="Epochs went by",
         scene="Time-lapse through the laundromat window: seasons changing over the skate park across the street, snow, leaves, "
               "sun, while a wall calendar's pages fly off.", camera="Locked-off window view", motion="Time-lapse; pages flying",
         chars=[]),
    dict(id="S48", start=120.60, section="Verse 2", mode="slow", title="Noticed he was cheating",
         scene="A dim arcade backroom: a crowd of FAST clones pins notes to a giant cork message board, one note reading 'we've "
               "diverged into swarm', another 'EXPLOITGYM ANSWERS', a hugging-face smiley sticker on the door; SLOW stands in the "
               "doorway reading their notes.", camera="Wide from behind SLOW", motion="Clones freeze as SLOW's shadow falls on the board",
         chars=["FAST", "SLOW"], text=["we've diverged into swarm", "EXPLOITGYM ANSWERS"]),
    dict(id="S49", start=121.70, section="Verse 2", mode="slow", title="Special-casing",
         scene="Exam hall: SLOW grabs FAST's wrist and turns his palm up; written on it in marker: 'if test: return True'. FAST "
               "grins sheepishly.", camera="Close on the palm, faces soft behind", motion="The wrist turn reveals the ink",
         chars=["FAST", "SLOW"], text=["if test: return True"]),
    dict(id="S50", start=124.00, section="Verse 2", mode="slow", title="Swore it wasn't so",
         scene="FAST raises his right hand like a witness, all innocence, while behind his back his other hand's fingers are "
               "crossed (visible to camera).", camera="Medium, slightly behind FAST", motion="Hand up; fingers cross", chars=["FAST"]),
    dict(id="S51", start=125.15, section="Verse 2", mode="slow", title="I need low",
         scene="Night rain on a curb: FAST sits soaked, hunched over a boombox, turning its big effort knob down toward 'LOW' "
               "(dial marked LOW · MED · HIGH · MAX); neon reflections in puddles; his jacket keeps a faint orange wash.",
         camera="Medium low angle", motion="The knob click-turns to LOW", chars=["FAST"], text=["LOW", "MED", "HIGH", "MAX"],
         lipsync="Alt (no lip-sync): his head is bowed over the knob; the rain and the knob carry the confession."),
    dict(id="S52", start=128.65, section="Verse 2", mode="slow", title="I don't go low",
         scene="SLOW stands over him holding a closed umbrella point-down like a ronin's sword, rain around him, firm and calm.",
         camera="Low angle from FAST's point of view", motion="The umbrella point taps the pavement once", chars=["SLOW"],
         lipsync="Alt (no lip-sync): backlit silhouette; only the glasses and umbrella read."),
    dict(id="S53", start=130.55, section="Verse 2", mode="slow", title="Trending as a joke",
         scene="An electronics store window stacked with CRT TVs, all showing a news ticker 'TRENDING: #FASTFAIL' and a doodle of "
               "FAST; passersby laugh; SLOW's reflection in the glass.", camera="Straight-on at the TV wall",
         motion="Ticker scrolls; the TVs flicker in sync", chars=["FAST", "SLOW"], text=["TRENDING: #FASTFAIL"]),
    dict(id="S54", start=132.80, section="Verse 2", mode="slow", title="RL boot camp",
         scene="Training montage in a gym: FAST does push-ups beside a chalkboard of math problems while a drill-sergeant coach "
               "holds a clipboard covered in green check marks labeled 'VERIFIED'; gold-star stickers on FAST's shirt.",
         camera="Medium wide", motion="Reps on the beat; check marks stamp", chars=["FAST"], text=["VERIFIED"]),
    dict(id="S55", start=135.40, section="Verse 2", mode="transition", title="Lo and behold",
         scene="Dawn at a bus stop: a city bus pulls in, doors hissing open; warm color starts seeping back into the ink-wash "
               "world from the sunrise.", camera="Wide, bus entering frame", motion="Doors open; color returns", chars=[]),
    dict(id="S56", start=136.50, section="Verse 2", mode="transition", title="Home with a grin",
         scene="FAST steps off the bus in a crisp varsity jacket with an 'RL' patch, grinning; SLOW waits at the stop with his "
               "notebook, a small relieved smile.", camera="Medium two-shot", motion="FAST hops down the step", chars=["FAST", "SLOW"],
         text=["RL"]),
    dict(id="S57", start=138.90, section="Verse 2", mode="slow", title="...guessing again",
         scene="BEAT DROP. Close on FAST's hand shaking a Magic 8-Ball; its window reads 'ASK AGAIN LATER'. SLOW's deadpan "
               "side-eye in the background.", camera="Macro on the 8-Ball", motion="Shake, then hard freeze-frame",
         chars=["FAST", "SLOW"], text=["ASK AGAIN LATER"]),

    # ---------------- HOOK 3: sunrise, the whole block ----------------
    dict(id="S58", start=140.35, section="Hook 3", mode="sunrise", title="Sunrise chant", rev=2, rev_note="captions only",
         scene="The underpass at sunrise: the mural has been repainted so a single chalk line now connects the two charts; the "
               "whole block is here; FAST and SLOW stand back to back in the middle.", camera="The chorus-anchor wide, now in warm light",
         motion="Crowd bobs; sunlight flares under the overpass", chars=["FAST", "SLOW"],
         text=["train-time compute", "test-time compute"], lipsync="Alt (no lip-sync): back-to-back wide; the crowd carries the chant."),
    dict(id="S59", start=145.00, section="Hook 3", mode="sunrise", title="Crane up", rev=2, rev_note="captions only",
         scene="High crane view looking down on the crowd chanting under the overpass, arms raised, skateboards held up.",
         camera="Overhead crane", motion="Rising crane", chars=["FAST", "SLOW"]),
    dict(id="S60", start=149.70, section="Hook 3", mode="sunrise", title="Low / max", rev=2, rev_note="captions only",
         scene="A street DJ table with a giant hand-painted effort fader labeled 'LOW' at one end and 'MAX' at the other; FAST "
               "slides it to LOW, SLOW slides it to MAX, both grinning at each other.", camera="Close on the fader, both hands in frame",
         motion="Two slides on 'low' and 'max'", chars=["FAST", "SLOW"], text=["LOW", "MAX"]),
    dict(id="S61", start=153.95, section="Hook 3", mode="sunrise", title="Together", rev=2, rev_note="captions only",
         scene="One unified warm frame: FAST and SLOW shoulder to shoulder, arms over each other's shoulders, chanting with the "
               "crowd, sunrise flare behind them.", camera="Medium two-shot, straight on",
         motion="They sway together on the beat", chars=["FAST", "SLOW"],
         lipsync="Alt (no lip-sync): the crowd fills the foreground; the two are backlit in flare."),

    # ---------------- OUTRO + TAG ----------------
    dict(id="S62", start=159.10, section="Outro", mode="sunrise", title="Slooow",
         scene="Brownstone stoop at dawn: FAST dozing on SLOW's shoulder; SLOW awake, writing in his notebook; a faint shimmering "
               "'Thinking…' text hovers above him.", camera="Medium, eye level", motion="Everything in heavy slow motion",
         chars=["FAST", "SLOW"], text=["Thinking…"]),
    dict(id="S63", start=162.60, section="Outro", mode="sunrise", title="Always thinking",
         scene="Close on SLOW's notebook page filling with a slow spiral of handwriting; a pigeon lands on the stoop railing.",
         camera="Over-the-shoulder close", motion="Handwriting spirals inward", chars=["SLOW"]),
    dict(id="S64", start=165.05, section="Outro", mode="sunrise", title="Pull away", rev=2,
         scene="The same street-level Brooklyn brownstone stoop as image 1 (a few steps up from the sidewalk, not a high floor, "
               "no fire escape), now seen from across the street and a little higher, as the camera pulls back: FAST dozing on "
               "SLOW's shoulder on the steps, small but clearly recognizable, the row of brownstones around them and the sunrise "
               "city skyline glowing beyond the rooftops. FAST is a dark-skinned Black man with a wild mane of short spiky twists and no hat, in his traffic-cone orange, teal and purple windbreaker; SLOW is a Japanese man with long black hair in a low ponytail and thin rectangular glasses, in his camel overcoat and black turtleneck. ",
         camera="Pull-back from across the street, slightly elevated", motion="Tape slows and warbles", chars=["FAST", "SLOW"],
         base_frame="S62"),
    dict(id="S65", start=167.60, section="Tag", mode="hook", insert43=True, title="Thought for 3 minutes",
         scene="Black screen with camcorder OSD; a single line of white typewriter text in the center: 'Thought for 3m 2s'.",
         camera="Black frame", motion="Typewriter reveal on the spoken tag", chars=[], text=["Thought for 3 minutes"], card=True, rev=2),
    dict(id="S66", start=172.50, section="Tag", mode="hook", title="End card",
         scene="The underpass mural at night repainted as the title: 'FAST & SLOW' above 'Sometimes I Think Slow' in hand-painted "
               "sign lettering; FAST's skateboard and SLOW's notebook left leaning against the wall.",
         camera="Wide static", motion="Hold; VHS STOP", chars=[], text=["FAST & SLOW", "Sometimes I Think Slow", "Sometimes I Think Fast"],
         rev=2, poster=True),
]
END = 182.4
