# Intervention Protocol Extraction

## Task

Extract detailed information about the intervention protocol, including dosage parameters (timing, frequency, duration) and delivery characteristics (game type, platform) from this scientific paper.

## Required Information

You must extract the following elements from the document:

1. **Intervention Period**: Duration of the intervention in weeks
2. **Total Number of Sessions**: Total count of intervention sessions
3. **Total Intervention Time**: Cumulative duration of all intervention exposure
4. **Duration Per Session**: Length of each individual session (constant or range)
5. **Game Type**: Classification as serious game or entertainment game
6. **Platform/Device Delivery**: Hardware platform used to deliver the intervention

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

**Task**: Classify the game intervention as serious or entertainment.

**Allowed values:** [`serious`, `entertainment`]

**Definitions:**

- **`serious`**: Applied game, gamified intervention, game-based intervention, or any game explicitly designed with therapeutic/educational methods or purposes
- **`entertainment`**: Commercial off-the-shelf game (COTS), casual game, video game not originally designed for therapeutic purposes

**Key indicators**:
- Serious: "serious game", "therapeutic game", "applied game", "gamified", "designed to", "developed for"
- Entertainment: "commercial game", "COTS", "off-the-shelf", game title of known commercial games (e.g., "Tetris", "Candy Crush")

**Examples:**

```
Methods: "The intervention used MindLight, a serious game developed to reduce anxiety in children."
→ value: "serious"

Methods: "Participants played Tetris, a commercial puzzle game."
→ value: "entertainment"

Introduction: "We developed a gamified cognitive behavioral therapy app..."
→ value: "serious"
```

### 6. Platform/Device Delivery

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
7. **Extract exactly what you see**: For game type and platform, use the authors' descriptions
8. **Check multiple sections**: Total intervention time may require looking in both Methods (planned) and Results (actual)

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
  "platform": {
    "value": ["pc"],
    "pages": [4],
    "quotes": ["The game was installed on desktop computers in the school computer lab."]
  }
}
```

## Begin Extraction

Please analyze the provided PDF document and extract the intervention protocol information according to the specifications above.
