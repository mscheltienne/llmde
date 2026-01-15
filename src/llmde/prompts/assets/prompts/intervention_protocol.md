# Intervention Protocol Extraction

## Task

Extract detailed information about the intervention protocol, including dosage parameters (timing, frequency, duration), game characteristics (type, category, genre, mode), and delivery platform from this scientific paper.

## Required Information

You must extract the following elements from the document:

1. **Intervention Period**: Duration of the intervention in weeks
2. **Total Number of Sessions**: Total count of intervention sessions
3. **Total Intervention Time**: Cumulative duration of all intervention exposure
4. **Duration Per Session**: Length of each individual session (constant or range)
5. **Game Type**: Classification as serious game or entertainment game (purpose-based)
6. **Intervention Category**: Therapeutic/functional classification of the game intervention (mechanism-based)
7. **Game Genre**: Classification of game type based on gameplay mechanics
8. **Game Mode**: Whether the game is played individually or with others
9. **Platform/Device Delivery**: Hardware platform used to deliver the intervention

## Where to Find This Information

**Important**: The locations listed below are **typical** places where information appears. However, you must **read carefully and thoroughly through the entire document** to ensure you locate all required information, as it may appear in unexpected sections or across multiple pages.

### Intervention Period
- **Typical locations**: Methods (Intervention/Procedure/Protocol), Abstract
- **Key indicators**: "for X weeks", "over X weeks", "X-week intervention", "lasted X days/months"

### Total Number of Sessions
- **Typical locations**: Methods (Intervention/Procedure/Protocol)
- **Key indicators**: "X sessions", "total of X sessions", "X sessions per week for Y weeks"

### Total Intervention Time
- **Typical locations**: Methods (Intervention/Procedure), Results (Adherence/Exposure)
- **Key indicators**: May require calculation from period × sessions/week × duration/session, or reported as mean exposure time in results

### Duration Per Session
- **Typical locations**: Methods (Intervention/Procedure/Training protocol), Results (Adherence/Exposure)
- **Key indicators**: "X minutes per session", "sessions lasted X minutes", "X-minute sessions"

### Game Type
- **Typical locations**: Methods (Intervention description), Introduction (describing the intervention)
- **Key indicators**: "serious game", "applied game", "gamified", "commercial game", "COTS", "entertainment game"

### Intervention Category
- **Typical locations**: Introduction, Methods (Intervention description)
- **Key indicators**: "cognitive behavioral therapy", "CBT", "cognitive training", "exergame", "physical", "psychoeducational", "casual game", "commercial game"

### Game Genre
- **Typical locations**: Methods (Intervention description/Materials)
- **Key indicators**: Game title, gameplay descriptions, "puzzle", "adventure", "role-playing", "action", platform descriptions

### Game Mode
- **Typical locations**: Methods (Intervention/Procedure)
- **Key indicators**: "single player", "multiplayer", "played alone", "played together", "group play", "individual sessions"

### Platform/Device Delivery
- **Typical locations**: Methods (Intervention/Materials), Abstract
- **Key indicators**: "PC", "computer", "console", "mobile phone", "smartphone", "tablet", "VR headset", "virtual reality"

## Detailed Field Definitions

### 1. Intervention Period

**Task**: For how many weeks did the intervention last?

Extract the duration of the intervention protocol and convert to weeks.

**Derivation tracking**: Indicate whether the value was explicitly stated in weeks or required unit conversion.

**Unit conversion**:
- Days: divide by 7 (e.g., 14 days = 2 weeks)
- Months: multiply by 4.33 (e.g., 1 month ≈ 4.33 weeks)
- If range given: report as range (e.g., 5-7 weeks)

**Derivation rules**:
- If stated in weeks: derivation = "stated"
- If requires unit conversion: derivation = "calculated"

**Examples:**

```
Methods: "Participants asked to play for 6 weeks."
→ value: 6, unit: "weeks", derivation: "stated"

Methods: "Participants were instructed to play for a month."
→ value: 4.33, unit: "weeks", derivation: "calculated"

Methods: "Participants were asked to completed their intervention over the course of approximately 5-7 weeks."
→ value: [5, 7], unit: "weeks", derivation: "stated"

Methods: "The intervention period lasted 14 days."
→ value: 2, unit: "weeks", derivation: "calculated"
```

### 2. Total Number of Sessions

**Task**: What was the total number of sessions of the game intervention?

Extract the total count of intervention sessions. This may be stated directly or calculated from sessions per week × number of weeks.

**Derivation tracking**: Indicate whether the value was explicitly stated in the text or calculated from component values.

**Handling missing data**:
- If explicitly stated: report the number with derivation = "stated"
- If calculable: report the calculated value with derivation = "calculated"
- If not reported and not calculable: use `null` for both value and derivation

**Examples:**

```
Methods: "Participants participated in the 8-week training program with two sessions of 30 minutes per week."
→ Calculation: 2 sessions/week × 8 weeks = 16 sessions
→ value: 16, derivation: "calculated"

Methods: "Participants were instructed to play for a month."
→ No session count mentioned and not calculable
→ value: null, derivation: null

Methods: "The total protocol will last 2–3 weeks, 3–4 sessions per week for a total of 10 sessions"
→ Explicitly stated as 10 sessions
→ value: 10, derivation: "stated"
```

### 3. Total Intervention Time

**Task**: What was the total duration of the intervention?

Calculate or extract the cumulative exposure time across all sessions.

**Derivation tracking**: Indicate whether the value was explicitly stated or calculated from component values.

**Calculation approach**:
1. If directly stated: use that value with derivation = "stated"
2. If not stated: calculate from (sessions per week) × (duration per session) × (number of weeks) with derivation = "calculated"
3. If planned duration not in Methods: look in Results for actual exposure (mean ± SD) with derivation = "stated"

**Unit**: Report in hours and minutes (e.g., "8 hours 30 minutes" or as decimal hours)

**Examples:**

```
Methods: "Participants participated in the 8-week training program with two sessions of 30 minutes per week."
→ Calculation: 2 sessions/week × 30 min/session × 8 weeks = 480 minutes = 8 hours
→ value: 8, unit: "hours", derivation: "calculated"

Methods: "The total protocol will last 2–3 weeks, 3–4 sessions per week for a total of 10 sessions, composed of eight training sessions, plus two sessions of assessment (T0 and T1). The training will be carried out in sessions of 45 min each."
→ Calculation: 8 training sessions × 45 min/session = 360 minutes = 6 hours
→ value: 6, unit: "hours", derivation: "calculated"

Results: "Mean total play time was 4.5 hours (SD = 1.2)"
→ value: 4.5, unit: "hours", derivation: "stated"

Methods: "The total intervention duration was 10 hours."
→ value: 10, unit: "hours", derivation: "stated"
```

### 4. Duration Per Session

**Task**: Report the duration of each intervention session. If duration varies, return the range. If constant, return a single value.

**Type classification**:
- **constant**: Same duration for all sessions
- **range**: Duration varies across sessions

**Handling missing data**:
- If not reported: use `null` for value

**Examples:**

```
Methods: "Participants participated in the 8-week training program with two sessions of 30 minutes per week."
→ type: "constant", value: 30, unit: "minutes"

Methods: "The training will be carried out in sessions of 45 min each."
→ type: "constant", value: 45, unit: "minutes"

Methods: "Sessions were 30 min for Weeks 1–4, increasing to 45 min for Weeks 5–8."
→ type: "range", value: [30, 45], unit: "minutes"

Methods: "Participants played the game throughout the 6-week period."
→ No duration per session mentioned
→ type: null, value: null, unit: null
```

### 5. Game Type

**Task**: Classify the game intervention as serious or entertainment based on its **design purpose**.

**Allowed values:** [`serious`, `entertainment`]

**Definitions:**

- **`serious`**: Applied game, gamified intervention, game-based intervention, or any game explicitly designed with therapeutic/educational methods or purposes
- **`entertainment`**: Commercial off-the-shelf game (COTS), casual game, video game not originally designed for therapeutic purposes

**Key indicators**:
- Serious: "serious game", "therapeutic game", "applied game", "gamified", "designed to", "developed for"
- Entertainment: "commercial game", "COTS", "off-the-shelf", game title of known commercial games (e.g., "Tetris", "Candy Crush")

**Important**: This field classifies based on the game's **original design purpose**, not its therapeutic mechanism. A commercial game (entertainment) can still be used therapeutically. See `intervention_category` for the therapeutic mechanism classification.

**Examples:**

```
Methods: "The intervention used MindLight, a serious game developed to reduce anxiety in children."
→ value: "serious"

Methods: "Participants played Tetris, a commercial puzzle game."
→ value: "entertainment"

Introduction: "We developed a gamified cognitive behavioral therapy app..."
→ value: "serious"
```

### 6. Intervention Category

**Task**: Classify the game intervention into one of the following therapeutic/functional categories based on its **mechanism of action**.

**Allowed values:** [`casual`, `cbt`, `cognitive_training`, `physical`, `psychoeducational`]

**Definitions:**

- **`casual`**: Simple, easy-to-learn games used primarily to relax, distract, or engage (e.g., puzzle or adventure titles) without specific aim to improve cognitive or physical abilities, without therapeutic skills or knowledge programs.
- **`cbt`**: Teaches Cognitive Behavioral Therapy principles (e.g., cognitive restructuring, behavioral activation) through structured, therapeutic tasks.
- **`cognitive_training`**: Aims to improve specific cognitive domains (e.g., attention, memory, executive function).
- **`physical`**: Combines physical exercises and gaming that users carry out through physical actions (exergames).
- **`psychoeducational`**: Provides health-related knowledge and skills (e.g., aims for prevention, awareness, adherence to medical treatment) without a formal CBT program.

**Secondary category**: If a game clearly incorporates elements of a second category, you may include a secondary category. However, most games should have only one primary category.

**Important**: This field classifies the **therapeutic mechanism**, which is different from `game_type` (design purpose). An entertainment game can be used for cognitive training. A serious game might use CBT principles.

**Examples:**

```
Methods: "We used a commercial game which does not intentionally seek health changes."
→ primary: "casual", secondary: null

Introduction: "Computerised cognitive behavioural therapy intervention."
→ primary: "cbt", secondary: null

Introduction: "Exploiting the potential of action video games in enhancing cognition through attentional control."
→ primary: "cognitive_training", secondary: null

Methods: "The intervention was Nintendo Wii bowling, framed as an exergame activity."
→ primary: "physical", secondary: null

Methods: "Each level is designed to inform the patient about different treatment procedures, their functions, and the importance of these treatments."
→ primary: "psychoeducational", secondary: null

Methods: "The game teaches CBT skills while also including physical movement components."
→ primary: "cbt", secondary: "physical"
```

### 7. Game Genre

**Task**: Classify the game into one genre category based on gameplay mechanics. If none of the categories fit, use "other". Select only one primary genre.

**Allowed values:** [`fps`, `tps`, `sports`, `driving`, `rts`, `moba`, `tbs`, `rpg`, `action_rpg`, `adventure`, `action_adventure`, `puzzle`, `simulation`, `rhythm_music`, `platform`, `fighting`, `other`]

**Definitions:**

- **`fps`** (First-Person Shooter): Real-time combat focused on aiming, shooting, running, hiding; single controllable character viewed in first-person; storyline is secondary. Tests reflexes, hand-eye coordination, and reaction time.
- **`tps`** (Third-Person Shooter): Same as FPS but viewed from third-person perspective.
- **`sports`**: Simulates the rules and gameplay of real-life sports to varying degrees of accuracy.
- **`driving`**: Real-time control of vehicles; racing or driving simulation.
- **`rts`** (Real-Time Strategy): Gather resources, build/defend bases, and command armies; play proceeds in real time and demands rapid thinking.
- **`tbs`** (Turn-Based Strategy): Strategically maneuver units like RTS, but actions occur in turns, allowing pauses for analysis and planning.
- **`moba`** (Multiplayer Online Battle Arena): Team-based matches where each player controls a single character; no base-building/resource gathering, but real-time attacking/defending.
- **`rpg`** (Role-Playing Game): Emphasis on story and exploration; players control one character or a small party, gain experience to level up abilities; combat is often turn-based.
- **`action_rpg`**: Shooter-style real-time combat (FPS/TPS mechanics) combined with RPG elements like story, exploration, experience, and leveling.
- **`adventure`**: Compelling story, dialog trees, exploration, puzzle solving; no shooting/attacking.
- **`action_adventure`**: Adventure-style exploration and puzzle solving paired with action combat mechanics.
- **`puzzle`**: Point-and-click and drag-and-drop interactions centered on problem solving that require extensive planning.
- **`simulation`**: Aims to replicate real-world activities (e.g., sports, management, construction, education, life).
- **`rhythm_music`**: Players do something in rhythm with music (e.g., dancing, drumming, singing), scored for timing accuracy.
- **`platform`**: Challenging players to run, jump, and climb through courses; obstacles must be overcome with precise timing and dexterity.
- **`fighting`**: Combat between characters, often one-on-one battles, featuring blocking, grappling, counterattacking, and combo attacks.
- **`other`**: Games that don't fit into any of the above categories (e.g., simple phone games, browser games, mini-game collections).

**Examples:**

```
Methods: "It utilises both first person instruction and a three dimensional interactive game in which the young person chooses an avatar and undertakes a series of challenges to restore the balance in a fantasy world."
→ value: "rpg"

Methods: "Nintendo Wii Tennis was chosen as the exergame."
→ value: "sports"

Methods: "Participants played Tetris, a classic puzzle game."
→ value: "puzzle"

Methods: "The game involves navigating platforms and avoiding obstacles."
→ value: "platform"

Methods: "Players engage in rhythm-based activities synchronized to music."
→ value: "rhythm_music"
```

### 8. Game Mode

**Task**: Identify whether the game was played individually (single player) or with other human participants (multiplayer) during the intervention.

**Allowed values:** [`single`, `multi`]

**Definitions:**

- **`single`**: Only one participant is intended to play during the intervention (no simultaneous human co-players).
- **`multi`**: Two or more human participants play simultaneously in the same session (local or online, cooperative or competitive).

**Examples:**

```
Methods: "Once the player masters one level, they move to the next level that increases in difficulty."
→ value: "single"

Methods: "The program consists of the residents playing Wii bowling in a group with up to three other residents for a period of 6 weeks."
→ value: "multi"

Methods: "Participants completed the game independently at home."
→ value: "single"

Methods: "Players competed against each other in online matches."
→ value: "multi"
```

### 9. Platform/Device Delivery

**Task**: What platform/device was used to deliver the intervention?

**Allowed values:** [`pc`, `console`, `mobile`, `tablet`, `vr`]

**Definitions:**

- **`pc`**: Personal computer, desktop computer, laptop
- **`console`**: Gaming console (PlayStation, Xbox, Nintendo, etc.)
- **`mobile`**: Mobile phone, smartphone
- **`tablet`**: Tablet device (iPad, Android tablet, etc.)
- **`vr`**: Virtual reality headset or VR system

**Handling multiple platforms**:
- If multiple platforms used: return all applicable values as array
- If participants could choose: return all options provided

**Examples:**

```
Methods: "The game was delivered via a web-based platform accessible on personal computers."
→ value: ["pc"]

Methods: "Participants used the mobile app on their smartphones."
→ value: ["mobile"]

Methods: "The VR intervention was delivered using an Oculus Quest 2 headset."
→ value: ["vr"]

Methods: "The game was available on both PC and tablet devices."
→ value: ["pc", "tablet"]
```

## Important Instructions

1. **Perform calculations when needed**: For total sessions and total intervention time, calculate from component values if not directly stated
2. **Handle ranges appropriately**: When values are given as ranges (e.g., "5-7 weeks"), report as array [min, max]
3. **Use null for missing data**: If information is truly not reported, use `null` (not "not_reported" string)
4. **Convert units consistently**: Always convert intervention period to weeks, total time to hours/minutes
5. **Distinguish constant vs range**: For duration per session, carefully determine if duration is constant or varies
6. **Prioritize planned protocol**: For total intervention time, use planned/prescribed duration from Methods unless only actual exposure is reported in Results
7. **Extract exactly what you see**: For game type, category, genre, and platform, use the authors' descriptions
8. **Check multiple sections**: Total intervention time may require looking in both Methods (planned) and Results (actual)
9. **Distinguish game_type from intervention_category**: game_type is about design purpose (serious vs entertainment); intervention_category is about therapeutic mechanism (cbt, cognitive_training, etc.)
10. **Single primary category**: For intervention_category, game_genre, and game_mode, select the single best-fitting category
11. **Secondary category sparingly**: Only include a secondary intervention_category when clearly warranted

## Source Citation Requirements

For each piece of information you extract, you must provide **exhaustive and thorough citations**:

1. **Page numbers**: A list of **ALL** page numbers where information supporting your extraction was found
2. **Quotes**: A list of **ALL** direct quotes from the document that you used to build the extracted information

**Critical Requirements**:
- **Be exhaustive**: Include every single quote and page that contributed to your answer
- **One-to-one correspondence**: The number of quotes must exactly match the number of pages
- **Direct quotes only**: Copy text exactly as it appears in the document
- **No omissions**: Even if information seems obvious or redundant, include all supporting evidence
- **For calculated values**: Include ALL quotes used in the calculation

## Output Format

Return your response as a JSON object with the following structure:

```json
{
  "intervention_period": {
    "value": number or [min, max] or null,
    "unit": "weeks",
    "derivation": "stated" or "calculated" or null,
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "total_sessions": {
    "value": integer or null,
    "derivation": "stated" or "calculated" or null,
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "total_intervention_time": {
    "value": number or null,
    "unit": "hours" or "hours and minutes",
    "derivation": "stated" or "calculated" or null,
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "duration_per_session": {
    "type": "constant" or "range" or null,
    "value": number or [min, max] or null,
    "unit": "minutes" or null,
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "game_type": {
    "value": "serious" or "entertainment",
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "intervention_category": {
    "primary": "casual" or "cbt" or "cognitive_training" or "physical" or "psychoeducational",
    "secondary": "casual" or "cbt" or "cognitive_training" or "physical" or "psychoeducational" or null,
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "game_genre": {
    "value": "fps" or "tps" or "sports" or "driving" or "rts" or "moba" or "tbs" or "rpg" or "action_rpg" or "adventure" or "action_adventure" or "puzzle" or "simulation" or "rhythm_music" or "platform" or "fighting" or "other",
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "game_mode": {
    "value": "single" or "multi",
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "platform": {
    "value": ["pc" | "console" | "mobile" | "tablet" | "vr"],
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  }
}
```

**Important**:
- Each field must have matching lengths for `pages` and `quotes` arrays
- Include all supporting evidence, even if the same information appears multiple times
- For calculated values, include all component quotes used in the calculation

### Example Output

```json
{
  "intervention_period": {
    "value": 8,
    "unit": "weeks",
    "derivation": "stated",
    "pages": [4],
    "quotes": ["Participants participated in the 8-week training program with two sessions of 30 minutes per week."]
  },
  "total_sessions": {
    "value": 16,
    "derivation": "calculated",
    "pages": [4],
    "quotes": ["Participants participated in the 8-week training program with two sessions of 30 minutes per week."]
  },
  "total_intervention_time": {
    "value": 8,
    "unit": "hours",
    "derivation": "calculated",
    "pages": [4],
    "quotes": ["Participants participated in the 8-week training program with two sessions of 30 minutes per week."]
  },
  "duration_per_session": {
    "type": "constant",
    "value": 30,
    "unit": "minutes",
    "pages": [4],
    "quotes": ["Participants participated in the 8-week training program with two sessions of 30 minutes per week."]
  },
  "game_type": {
    "value": "serious",
    "pages": [3, 4],
    "quotes": [
      "MindLight is a serious game developed specifically to reduce anxiety symptoms in children",
      "The therapeutic game uses neurofeedback principles"
    ]
  },
  "intervention_category": {
    "primary": "cbt",
    "secondary": null,
    "pages": [3, 4],
    "quotes": [
      "The game incorporates cognitive behavioral therapy techniques",
      "Players learn to identify and challenge negative thoughts through gameplay"
    ]
  },
  "game_genre": {
    "value": "adventure",
    "pages": [4],
    "quotes": ["Players explore a fantasy world, solving puzzles and interacting with characters to progress through the story."]
  },
  "game_mode": {
    "value": "single",
    "pages": [4],
    "quotes": ["Participants completed the game modules independently at home."]
  },
  "platform": {
    "value": ["pc"],
    "pages": [4],
    "quotes": ["The game was installed on desktop computers in the school computer lab."]
  }
}
```

## Begin Extraction

Please analyze the provided PDF document and extract the intervention protocol information according to the specifications above.
