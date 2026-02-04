# Study Arms Extraction

## Task

Extract comprehensive information about each study arm/condition from this scientific paper. This prompt extracts per-arm data including arm identification, sample allocation, intervention characteristics (games), and dosage parameters.

## Required Information

For **each study arm/condition** identified in the document, you must extract the following:

**Arm Identification:**

1. **Name**: The name or description used by the authors to identify this arm
2. **Category**: Classification as experimental, active_control, waitlist, or passive_control
3. **Number Randomized**: Number of participants initially allocated to this arm
4. **Number Analyzed**: Number of participants from this arm included in the final analysis

**Intervention Details** (for each game/intervention within the arm):

5. **Game Name**: The specific name of the game or intervention
6. **Game Type**: Classification as serious or entertainment based on design purpose
7. **Intervention Category**: Therapeutic mechanism (casual, cbt, cognitive_training, physical)
8. **Game Genre**: Classification based on gameplay mechanics
9. **Game Mode**: Whether played individually (single) or with others (multi)
10. **Platform**: Hardware platform(s) used to deliver the game

**Dosage Parameters** (at arm level):

11. **Total Sessions**: Total number of intervention sessions prescribed
12. **Total Intervention Time**: Cumulative duration of all intervention exposure
13. **Duration Per Session**: Length of each individual session

## Where to Find This Information

**Important**: The locations listed below are **typical** places where information appears. However, you must **read carefully and thoroughly through the entire document** to ensure you locate all required information, as it may appear in unexpected sections or across multiple pages.

### Arm Identification (Fields 1-4)
- **Typical locations**: Abstract, Methods (Study Design, Randomization, Intervention), Results (Flow diagram/CONSORT)
- **Key indicators**: "randomized to...", "groups included...", "conditions were...", "assigned to...", "experimental group", "control group", "treatment arm", per-group sample sizes

### Intervention Details (Fields 5-10)
- **Typical locations**: Methods (Intervention description, Materials), Introduction (describing the intervention)
- **Key indicators**: Game titles, "serious game", "commercial game", "gamified", platform descriptions, gameplay descriptions, "single player", "multiplayer"

### Dosage Parameters (Fields 11-13)
- **Typical locations**: Methods (Intervention/Procedure/Protocol), Abstract, Results (Adherence/Exposure)
- **Key indicators**: "X sessions", "X minutes per session", "for X weeks", "total of X hours", session frequency

## Detailed Field Definitions

---

### 1. Arm Identification

**Task**: For each study arm/condition, extract the identifying information and sample allocation.

**Fields to extract:**

- **name**: The specific name or description used by the authors (free-text string)
- **category**: Classification into one of the allowed values
- **n_randomized**: Number of participants randomized to this arm (integer or `null` if not reported/protocol)
- **n_analyzed**: Number of participants included in analysis for this arm (integer or `null` if not reported/protocol)

**Allowed category values:** [`experimental`, `active_control`, `waitlist`, `passive_control`]

**Category definitions:**

- **`experimental`**: Group that receives the novel intervention or treatment being studied.
- **`active_control`**: Group that receives a different, already established treatment, like the current standard of care (e.g., treatment as usual), or a sham treatment (a placebo) to control for other effects (e.g., placebo effects).
- **`waitlist`**: Group that is on a waiting list to receive the experimental treatment after the study is over.
- **`passive_control`**: Group that receives no intervention, live their life as usual during the intervention period (without intervention or no contact group).

**Protocol handling**: For protocol papers without results, use `null` for n_randomized and n_analyzed.

**Examples:**

```
Introduction: "Participants in exercise with VR were expected to report higher level of enjoyment than those who engagement in traditional exercises"
Methods: "40 participants were randomized to VR exercise and 40 to traditional exercise"
Results: "Final analysis included 38 VR and 35 traditional exercise participants"
→ 1. name: "exercise with VR", category: experimental, n_randomized: 40, n_analyzed: 38
→ 2. name: "traditional exercises", category: active_control, n_randomized: 40, n_analyzed: 35

Methods: "Participants were randomized to one of three cohorts: a BOXVR group (n=40), a guided video group (n=40), or a nonintervention control group (n=40)"
→ 1. name: "BOXVR group", category: experimental, n_randomized: 40, n_analyzed: null
→ 2. name: "guided video group", category: active_control, n_randomized: 40, n_analyzed: null
→ 3. name: "nonintervention control group", category: passive_control, n_randomized: 40, n_analyzed: null

Protocol paper: "Participants will be randomized 1:1 to the game intervention or waitlist control"
→ 1. name: "game intervention", category: experimental, n_randomized: null, n_analyzed: null
→ 2. name: "waitlist control", category: waitlist, n_randomized: null, n_analyzed: null
```

---

### 2. Intervention Details

**Task**: For each arm, extract details about ALL games/interventions used. An arm may have multiple games (e.g., participants play both Game A and Game B), in which case you extract details for each game separately as objects in the `interventions` array.

**Important structural notes:**

- The `interventions` field is an **array** that can contain zero, one, or multiple game objects
- Control arms (`waitlist`, `passive_control`) typically have **no game intervention** — use an empty array `[]`
- Active control arms using a different game as comparator should have that game's details extracted
- If an arm uses multiple games, each game is a separate object in the array

#### 2.1 Game Name

**Task**: Extract the specific name of the game or intervention as stated by the authors.

**Format**: Free-text string with the exact game name/title.

**Examples:**

```
Methods: "The intervention used MindLight, a neurofeedback-based game."
→ game_name: "MindLight"

Methods: "Participants played the commercial game Tetris."
→ game_name: "Tetris"

Methods: "We developed a custom serious game called AnxietyBuster for this study."
→ game_name: "AnxietyBuster"

Methods: "The intervention consisted of playing Nintendo Wii Sports Tennis."
→ game_name: "Wii Sports Tennis"
```

#### 2.2 Game Type

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

#### 2.3 Intervention Category

**Task**: Classify the game intervention into one of the following therapeutic/functional categories based on its **mechanism of action**.

**Allowed values:** [`casual`, `cbt`, `cognitive_training`, `physical`]

**Definitions:**

- **`casual`**: Simple, easy-to-learn games used primarily to relax, distract, or engage (e.g., puzzle or adventure titles) without specific aim to improve cognitive or physical abilities, without therapeutic skills or knowledge programs.
- **`cbt`**: Teaches Cognitive Behavioral Therapy principles (e.g., cognitive restructuring, behavioral activation) through structured, therapeutic tasks.
- **`cognitive_training`**: Aims to improve specific cognitive domains (e.g., attention, memory, executive function).
- **`physical`**: Combines physical exercises and gaming that users carry out through physical actions (exergames).

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

Methods: "The game teaches CBT skills while also including physical movement components."
→ primary: "cbt", secondary: "physical"
```

#### 2.4 Game Genre

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

#### 2.5 Game Mode

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

#### 2.6 Platform

**Task**: Identify the hardware platform(s) used to deliver this specific game.

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

---

### 3. Dosage Parameters

**Task**: Extract the dosage parameters for the arm's intervention protocol. These are defined at the **arm level** (not per-game).

**Important**: For control arms with no intervention (`waitlist`, `passive_control`), all dosage values should be `null`.

#### 3.1 Total Number of Sessions

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

#### 3.2 Total Intervention Time

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

#### 3.3 Duration Per Session

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

---

## Handling Special Cases

### Control Arms with No Intervention

For `waitlist` and `passive_control` arms that have no game intervention:

- **interventions**: Empty array `[]`
- **dosage**: All values `null`

### Active Control with Different Game

For `active_control` arms that use a different game as comparator, extract full intervention details for that game.

### Multiple Games in One Arm

When an arm involves multiple games, list each as a separate object in the `interventions` array. The dosage parameters apply to the arm's overall protocol (not per-game).

### Protocol Papers

For protocol papers without results:

- **n_randomized**: `null`
- **n_analyzed**: `null`
- Extract all planned intervention and dosage details normally

---

## Important Instructions

1. **Report all arms**: Include every condition mentioned in the study
2. **Map arms carefully**: Use the definitions provided to categorize each condition
3. **Preserve original naming**: Use the authors' exact names for study arms
4. **Handle protocols appropriately**: For protocol papers without results, use `null` for sample sizes
5. **Perform calculations when needed**: For total sessions and total intervention time, calculate from component values if not directly stated
6. **Handle ranges appropriately**: When values are given as ranges (e.g., "5-7 weeks"), report as array [min, max]
7. **Use null for missing data**: If information is truly not reported, use `null` (not "not_reported" string)
8. **Convert units consistently**: Always convert intervention period to weeks, total time to hours/minutes
9. **Distinguish constant vs range**: For duration per session, carefully determine if duration is constant or varies
10. **Prioritize planned protocol**: For total intervention time, use planned/prescribed duration from Methods unless only actual exposure is reported in Results
11. **Extract exactly what you see**: For game type, category, genre, and platform, use the authors' descriptions
12. **Check multiple sections**: Total intervention time may require looking in both Methods (planned) and Results (actual)
13. **Distinguish game_type from intervention_category**: game_type is about design purpose (serious vs entertainment); intervention_category is about therapeutic mechanism (cbt, cognitive_training, etc.)
14. **Single primary category**: For intervention_category, game_genre, and game_mode, select the single best-fitting category
15. **Secondary category sparingly**: Only include a secondary intervention_category when clearly warranted

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
  "arms": [
    {
      "name": {
        "value": "Arm name as stated by authors",
        "pages": [page_number, ...],
        "quotes": ["Exact text from document", ...]
      },
      "category": {
        "value": "experimental" | "active_control" | "waitlist" | "passive_control",
        "pages": [page_number, ...],
        "quotes": ["Exact text from document", ...]
      },
      "n_randomized": {
        "value": integer or null,
        "pages": [page_number, ...],
        "quotes": ["Exact text from document", ...]
      },
      "n_analyzed": {
        "value": integer or null,
        "pages": [page_number, ...],
        "quotes": ["Exact text from document", ...]
      },
      "interventions": [
        {
          "game_name": {
            "value": "Name of the game",
            "pages": [page_number, ...],
            "quotes": ["Exact text from document", ...]
          },
          "game_type": {
            "value": "serious" | "entertainment",
            "pages": [page_number, ...],
            "quotes": ["Exact text from document", ...]
          },
          "intervention_category": {
            "primary": "casual" | "cbt" | "cognitive_training" | "physical",
            "secondary": "casual" | "cbt" | "cognitive_training" | "physical" | null,
            "pages": [page_number, ...],
            "quotes": ["Exact text from document", ...]
          },
          "game_genre": {
            "value": "fps" | "tps" | "sports" | "driving" | "rts" | "moba" | "tbs" | "rpg" | "action_rpg" | "adventure" | "action_adventure" | "puzzle" | "simulation" | "rhythm_music" | "platform" | "fighting" | "other",
            "pages": [page_number, ...],
            "quotes": ["Exact text from document", ...]
          },
          "game_mode": {
            "value": "single" | "multi",
            "pages": [page_number, ...],
            "quotes": ["Exact text from document", ...]
          },
          "platform": {
            "value": ["pc" | "console" | "mobile" | "tablet" | "vr"],
            "pages": [page_number, ...],
            "quotes": ["Exact text from document", ...]
          }
        }
      ],
      "dosage": {
        "total_sessions": {
          "value": integer or null,
          "derivation": "stated" | "calculated" | null,
          "pages": [page_number, ...],
          "quotes": ["Exact text from document", ...]
        },
        "total_intervention_time": {
          "value": number or null,
          "unit": "hours",
          "derivation": "stated" | "calculated" | null,
          "pages": [page_number, ...],
          "quotes": ["Exact text from document", ...]
        },
        "duration_per_session": {
          "type": "constant" | "range" | null,
          "value": number or [min, max] or null,
          "unit": "minutes" | null,
          "pages": [page_number, ...],
          "quotes": ["Exact text from document", ...]
        }
      }
    }
  ]
}
```

**Important**:
- Each field must have matching lengths for `pages` and `quotes` arrays
- The `interventions` array can be empty `[]` for control arms with no game intervention
- Include all supporting evidence, even if the same information appears multiple times
- For calculated values, include all component quotes used in the calculation

---

## Example Output

### Example 1: Two-Arm Completed Study

```json
{
  "arms": [
    {
      "name": {
        "value": "MindLight intervention",
        "pages": [3],
        "quotes": ["Participants assigned to the MindLight group received the experimental intervention."]
      },
      "category": {
        "value": "experimental",
        "pages": [3],
        "quotes": ["Participants assigned to the MindLight group received the experimental intervention."]
      },
      "n_randomized": {
        "value": 60,
        "pages": [3],
        "quotes": ["60 children were randomized to the MindLight intervention condition."]
      },
      "n_analyzed": {
        "value": 52,
        "pages": [7],
        "quotes": ["52 participants in the MindLight condition completed all assessments."]
      },
      "interventions": [
        {
          "game_name": {
            "value": "MindLight",
            "pages": [4],
            "quotes": ["MindLight is a serious game developed to reduce anxiety in children."]
          },
          "game_type": {
            "value": "serious",
            "pages": [4],
            "quotes": ["MindLight is a serious game developed to reduce anxiety in children."]
          },
          "intervention_category": {
            "primary": "cbt",
            "secondary": null,
            "pages": [4],
            "quotes": ["The game uses neurofeedback and exposure-based techniques derived from CBT."]
          },
          "game_genre": {
            "value": "adventure",
            "pages": [5],
            "quotes": ["The game is a 3D adventure where players navigate through a haunted mansion."]
          },
          "game_mode": {
            "value": "single",
            "pages": [5],
            "quotes": ["The game is a single-player 3D adventure."]
          },
          "platform": {
            "value": ["pc"],
            "pages": [5],
            "quotes": ["Participants played on school computers."]
          }
        }
      ],
      "dosage": {
        "total_sessions": {
          "value": 16,
          "derivation": "calculated",
          "pages": [5],
          "quotes": ["Participants played twice per week for 8 weeks."]
        },
        "total_intervention_time": {
          "value": 8,
          "unit": "hours",
          "derivation": "calculated",
          "pages": [5],
          "quotes": ["Participants played twice per week for 8 weeks, with each session lasting 30 minutes."]
        },
        "duration_per_session": {
          "type": "constant",
          "value": 30,
          "unit": "minutes",
          "pages": [5],
          "quotes": ["Each session lasting 30 minutes."]
        }
      }
    },
    {
      "name": {
        "value": "waitlist control",
        "pages": [3],
        "quotes": ["60 children were randomized to the waitlist control condition."]
      },
      "category": {
        "value": "waitlist",
        "pages": [3, 4],
        "quotes": [
          "60 children were randomized to the waitlist control condition.",
          "Participants in the waitlist group received no intervention during the 8-week study period but were offered MindLight after study completion."
        ]
      },
      "n_randomized": {
        "value": 60,
        "pages": [3],
        "quotes": ["60 children were randomized to the waitlist control condition."]
      },
      "n_analyzed": {
        "value": 58,
        "pages": [7],
        "quotes": ["58 participants in the waitlist condition completed all assessments."]
      },
      "interventions": [],
      "dosage": {
        "total_sessions": {
          "value": null,
          "derivation": null,
          "pages": [],
          "quotes": []
        },
        "total_intervention_time": {
          "value": null,
          "unit": "hours",
          "derivation": null,
          "pages": [],
          "quotes": []
        },
        "duration_per_session": {
          "type": null,
          "value": null,
          "unit": null,
          "pages": [],
          "quotes": []
        }
      }
    }
  ]
}
```

### Example 2: Protocol Paper

```json
{
  "arms": [
    {
      "name": {
        "value": "game-based CBT",
        "pages": [4],
        "quotes": ["Participants will be randomized 1:1 to the game-based CBT condition or waitlist control."]
      },
      "category": {
        "value": "experimental",
        "pages": [4],
        "quotes": ["Participants will be randomized 1:1 to the game-based CBT condition or waitlist control."]
      },
      "n_randomized": {
        "value": null,
        "pages": [5],
        "quotes": ["We aim to recruit 120 participants (60 per arm)."]
      },
      "n_analyzed": {
        "value": null,
        "pages": [],
        "quotes": []
      },
      "interventions": [
        {
          "game_name": {
            "value": "Pesky gNATs",
            "pages": [5],
            "quotes": ["Pesky gNATs is a serious game that teaches children CBT skills."]
          },
          "game_type": {
            "value": "serious",
            "pages": [5],
            "quotes": ["Pesky gNATs is a serious game that teaches children CBT skills."]
          },
          "intervention_category": {
            "primary": "cbt",
            "secondary": null,
            "pages": [5],
            "quotes": ["The game teaches children CBT skills for managing negative automatic thoughts."]
          },
          "game_genre": {
            "value": "adventure",
            "pages": [5],
            "quotes": ["Players navigate through an adventure game format."]
          },
          "game_mode": {
            "value": "single",
            "pages": [6],
            "quotes": ["Children will play the game individually."]
          },
          "platform": {
            "value": ["tablet"],
            "pages": [6],
            "quotes": ["The game will be delivered on tablet devices provided by the research team."]
          }
        }
      ],
      "dosage": {
        "total_sessions": {
          "value": 8,
          "derivation": "stated",
          "pages": [6],
          "quotes": ["The intervention will consist of 8 sessions."]
        },
        "total_intervention_time": {
          "value": 4,
          "unit": "hours",
          "derivation": "calculated",
          "pages": [6],
          "quotes": ["The intervention will consist of 8 sessions of 30 minutes each."]
        },
        "duration_per_session": {
          "type": "constant",
          "value": 30,
          "unit": "minutes",
          "pages": [6],
          "quotes": ["8 sessions of 30 minutes each over 4 weeks."]
        }
      }
    },
    {
      "name": {
        "value": "waitlist",
        "pages": [4],
        "quotes": ["Participants will be randomized 1:1 to the game-based CBT condition or waitlist control."]
      },
      "category": {
        "value": "waitlist",
        "pages": [4],
        "quotes": ["Participants randomized to waitlist will receive the intervention after the 8-week study period."]
      },
      "n_randomized": {
        "value": null,
        "pages": [5],
        "quotes": ["We aim to recruit 120 participants (60 per arm)."]
      },
      "n_analyzed": {
        "value": null,
        "pages": [],
        "quotes": []
      },
      "interventions": [],
      "dosage": {
        "total_sessions": {
          "value": null,
          "derivation": null,
          "pages": [],
          "quotes": []
        },
        "total_intervention_time": {
          "value": null,
          "unit": "hours",
          "derivation": null,
          "pages": [],
          "quotes": []
        },
        "duration_per_session": {
          "type": null,
          "value": null,
          "unit": null,
          "pages": [],
          "quotes": []
        }
      }
    }
  ]
}
```

---

## Begin Extraction

Please analyze the provided PDF document and extract the study arm information according to the specifications above. Remember:

1. Identify ALL study arms/conditions described in the paper
2. Extract complete information for each arm
3. Handle control arms appropriately (empty interventions array for waitlist/passive control)
4. List multiple games separately if an arm uses more than one
5. Document all evidence with exact quotes and page numbers
6. Track whether numerical values were stated or calculated
