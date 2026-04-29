# Extracted Outcomes Extraction

## Task

Extract the per-group, per-outcome **mean** and **standard deviation** values reported in this scientific paper, at **two time points only**: **pre-intervention** (baseline) and **post-intervention** (immediately following the intervention period). The deliverable is a long-format list of measurements that can be mapped 1-to-1 to a DataFrame with columns:

```
Group | Outcome | primary | mean | std
```

To build that list precisely, you must also identify (a) every study arm with its category, and (b) every instrument used to score participants, flagging which are designated as primary outcomes. Both are intermediate scaffolding — the goal is the long-format `measurements` array.

## Required Information

You must extract the following:

1. **Arms**: Every study arm/condition mentioned in the paper, with the arm name and category.
2. **Instruments**: Every questionnaire/scale/instrument used to score participants (regardless of construct: anxiety, depression, quality of life, sleep, motivation, side effects, gaming, etc.), with the canonical abbreviation, a `primary` flag, and the list of components reported numerically.
3. **Measurements**: For each (group × outcome × time) cell, the raw mean and standard deviation, with exhaustive page numbers and exact quotes documenting the source. Time is restricted to **pre** and **post**; mid-intervention and follow-up assessments (1-month, 3-month, 6-month, 12-month, ...) are **excluded**.

## Where to Find This Information

**Important**: The locations listed below are **typical** places where information appears. However, you must **read carefully and thoroughly through the entire document** to ensure you locate all required information, as it may appear in unexpected sections, supplementary materials, or across multiple pages.

### Arm Identification
- **Typical locations**: Abstract, Methods (Study Design / Randomization / Intervention), Results (Flow diagram / CONSORT)
- **Key indicators**: "randomized to ...", "groups included ...", "conditions were ...", "assigned to ...", "experimental group", "control group", "treatment arm"

### Instrument List and Primary Designation
- **Typical locations**: Methods (Measures / Assessments / Outcomes / Endpoints), Statistical Analysis (primary endpoint / analysis plan), Trial registration information, Abstract
- **Key indicators**: "measured with", "assessed using", "primary outcome", "co-primary", "secondary outcome", instrument abbreviations (e.g., PHQ-9, GAD-7, BDI-II, DASS-21, STAI)

### Mean and Standard Deviation Values
- **Typical locations**: Results (baseline characteristics tables, outcome tables), Tables in the main text or supplements
- **Key indicators**: `M = ...`, `Mean = ...`, `SD = ...`, `± ...`, "(SD)", standalone numbers in baseline / pre / post columns of result tables, descriptive statistics tables broken down by group

## Detailed Field Definitions

---

### 1. Arms

**Task**: List every study arm/condition described in the paper and classify each.

**Fields per arm:**

- **name**: Free-text string with the arm name **as the authors use it**. Use the same wording the authors use so that the arm can be matched 1-to-1 with the output of the `study_arms` prompt by name.
- **category**: One of `experimental`, `active_control`, `passive_control`, or `null`.
- **identifier**: Computed string `<arm name> (<category|unknown>)`.

**Allowed `category` values:**

- **`experimental`**: Group that receives the novel intervention or treatment being studied.
- **`active_control`**: Group that receives a different already-established treatment (e.g., treatment as usual, an alternative intervention, a sham/placebo). The defining feature is that the group is doing **something** during the intervention period that differs from the experimental intervention.
- **`passive_control`**: Group that receives no intervention during the measurement window. **Waitlist arms are mapped to `passive_control`**, even if the authors call them "waitlist control": during the intervention window they receive no treatment, which is what `passive_control` denotes here.
- **`null`**: The category cannot be determined from the text. Set `value`, `pages`, and `quotes` of `category` to `null`.

**Identifier composition rule:**

- If `category.value` is `experimental`, `active_control`, or `passive_control`: `identifier = "<arm name> (<category.value>)"`.
- If `category.value` is `null`: `identifier = "<arm name> (unknown)"`.

The identifier is then used verbatim as the `group` field in every measurement row for that arm.

**Examples:**

```
Methods: "Participants were randomized to the MindLight game group or to a no-intervention waitlist control."
→ Arm 1: name="MindLight game group", category="experimental",
         identifier="MindLight game group (experimental)"
→ Arm 2: name="waitlist control", category="passive_control",
         identifier="waitlist control (passive_control)"
```

```
Methods: "Participants in the BOXVR cohort were compared with a guided video cohort and a nonintervention control."
→ Arm 1: name="BOXVR cohort", category="experimental",
         identifier="BOXVR cohort (experimental)"
→ Arm 2: name="guided video cohort", category="active_control",
         identifier="guided video cohort (active_control)"
→ Arm 3: name="nonintervention control", category="passive_control",
         identifier="nonintervention control (passive_control)"
```

```
Methods: "Two cohorts of participants were compared." [no further description of either cohort's intervention assignment]
→ Arm 1: name="cohort 1", category=null, identifier="cohort 1 (unknown)"
→ Arm 2: name="cohort 2", category=null, identifier="cohort 2 (unknown)"
```

---

### 2. Instruments

**Task**: List every questionnaire / scale / instrument used to score participants in the trial. **Do not** restrict to anxiety or depression: include quality of life, sleep, motivation, side effects, gaming, well-being, stress, fatigue, cognitive functioning, etc. — everything that produces a numerical score.

**Fields per instrument:**

- **name**: Canonical abbreviation of the instrument (see canonical naming rules below).
- **primary**: Boolean. `true` iff the instrument is designated as a **primary** or **co-primary** outcome measure of the study (typically declared in Methods/Outcomes, Statistical Analysis, Sample Size justification, Abstract, or trial registration). All other instruments — including secondary, exploratory, baseline-characterization, manipulation-check, side-effect, and adherence measures — are `false`.
- **components**: Array of canonical component strings (`<Instrument> - <Subscale|Total>`) listing **only those components for which any statistic is numerically reported in the paper for at least one (group, time) cell**. Use one entry per separately-reported component.

**Canonical naming rules:**

1. If the instrument appears in the canonical table below, use the abbreviation **and** subscale name from the table.
2. If the instrument is not in the table:
   - Use the authors' shortest abbreviation as the instrument name (e.g., the parenthetical abbreviation in "Brief Resilience Scale (BRS)" → `BRS`). If no abbreviation is given, build a sensible one from the initials of the full name.
   - For the component, use the authors' subscale wording in **Title Case**. If the instrument has no subscales (single total score), use the literal `Total`.
3. Always emit the component as exactly two parts joined by ` - ` (space hyphen space): `<Instrument> - <Subscale|Total>`. The pre/post suffix is appended only in the `outcome` field of measurements (see §3).

**Canonical instrument table (non-exhaustive):**

| Abbreviation | Full name | Component(s) |
|---|---|---|
| GAD-7 | Generalized Anxiety Disorder-7 | Total |
| PHQ-9 | Patient Health Questionnaire-9 | Total |
| BDI | Beck Depression Inventory | Total |
| BDI-II | Beck Depression Inventory-II | Total, Cognitive, Somatic, Affective, Cognitive-Affective, Somatic-Affective (use the labels the authors report; do not derive subscales not stated in the paper) |
| BAI | Beck Anxiety Inventory | Total |
| STAI | State-Trait Anxiety Inventory | State, Trait |
| STAI-Y | State-Trait Anxiety Inventory Form Y | State, Trait |
| STAI-X | State-Trait Anxiety Inventory Form X | State, Trait |
| HADS | Hospital Anxiety and Depression Scale | Anxiety, Depression, Total |
| DASS-21 | Depression Anxiety Stress Scales-21 | Depression, Anxiety, Stress |
| DASS-42 | Depression Anxiety Stress Scales-42 | Depression, Anxiety, Stress |
| CES-D | Center for Epidemiologic Studies Depression Scale | Total |
| MADRS | Montgomery-Åsberg Depression Rating Scale | Total |
| HAM-D | Hamilton Depression Rating Scale | Total |
| HAM-A | Hamilton Anxiety Rating Scale | Total |
| CDI | Children's Depression Inventory | Total |
| RCADS | Revised Children's Anxiety and Depression Scale | Total Anxiety, Total Internalizing, Separation Anxiety, Social Phobia, Generalized Anxiety, Panic, Obsessive-Compulsive, Major Depression |
| SCARED | Screen for Child Anxiety Related Emotional Disorders | Total, Panic/Somatic, Generalized Anxiety, Separation Anxiety, Social Phobia, School Phobia |
| MASC | Multidimensional Anxiety Scale for Children | Total, Physical Symptoms, Social Anxiety, Harm Avoidance, Separation Anxiety |
| QIDS | Quick Inventory of Depressive Symptomatology | Total |
| PSWQ | Penn State Worry Questionnaire | Total |
| SPIN | Social Phobia Inventory | Total |
| WEMWBS | Warwick-Edinburgh Mental Wellbeing Scale | Total |
| PSS | Perceived Stress Scale | Total |
| ISI | Insomnia Severity Index | Total |
| PSQI | Pittsburgh Sleep Quality Index | Global, Subjective Sleep Quality, Sleep Latency, Sleep Duration, Sleep Efficiency, Sleep Disturbances, Sleep Medication, Daytime Dysfunction |
| WHOQOL-BREF | World Health Organization Quality of Life-BREF | Physical, Psychological, Social, Environmental |
| SF-36 | Short Form 36 Health Survey | (subscales by name as authors report; e.g. Physical Functioning, Role Physical, Bodily Pain, General Health, Vitality, Social Functioning, Role Emotional, Mental Health) |
| SF-12 | Short Form 12 Health Survey | (subscales as reported, including Physical Component Summary, Mental Component Summary) |
| PCL-5 | PTSD Checklist for DSM-5 | Total |
| IES-R | Impact of Event Scale-Revised | Total, Intrusion, Avoidance, Hyperarousal |
| ATQ | Automatic Thoughts Questionnaire | Total |
| BRS | Brief Resilience Scale | Total |
| SHS | Subjective Happiness Scale | Total |
| SWLS | Satisfaction With Life Scale | Total |

**Important**: The table is a **canonical reference**, not a list of "instruments to look for". Extract every instrument actually used in the paper, even if it is not in the table.

**Examples:**

```
Methods: "Depression severity was assessed with the Beck Depression Inventory-II (BDI-II) as the primary outcome."
Results (Table 2): Reports BDI-II Total mean (SD) at baseline and post-intervention for both arms.
→ Instrument 1: name="BDI-II", primary=true, components=["BDI-II - Total"]
```

```
Methods: "Anxiety and depression symptoms were measured at baseline and at the end of the intervention with the DASS-21. The PHQ-9 was used to monitor depression weekly. The primary outcome was anxiety severity on the DASS-21 Anxiety subscale."
Results: Tables report DASS-21 Depression, Anxiety, Stress means and SDs; PHQ-9 means and SDs.
→ Instrument 1: name="DASS-21", primary=true,
                components=["DASS-21 - Depression", "DASS-21 - Anxiety", "DASS-21 - Stress"]
→ Instrument 2: name="PHQ-9", primary=false, components=["PHQ-9 - Total"]
Note: Even though both DASS-21 Depression and DASS-21 Stress are not the primary subscale, all three DASS-21 components are flagged primary=true at the *instrument* level because the DASS-21 itself is the primary instrument. The primary/co-primary subscale designation is a refinement that this prompt does not capture; primary applies to the whole instrument.
```

```
Methods: "Sleep was assessed with the PSQI."
Results: Reports only the global PSQI score per group.
→ Instrument 1: name="PSQI", primary=false, components=["PSQI - Global"]
Note: Component subscales are listed in `components` only if the paper reports them numerically. Here only the Global score is reported.
```

```
Methods: "Wellbeing was assessed with the Brief Resilience Scale (BRS)."
→ Instrument: name="BRS", primary=false (or true if designated primary), components=["BRS - Total"]
```

---

### 3. Measurements

**Task**: For each (group × outcome × time) cell that has any reported statistic, emit one row.

**Fields per measurement row:**

- **group**: An identifier matching exactly one entry in `arms[].identifier`.
- **outcome**: A string formatted as `<Instrument> - <Subscale|Total> - <pre|post>`. The first two parts must match an entry in the parent instrument's `components` array.
- **primary**: Boolean. Equal to the parent instrument's `primary.value`.
- **mean**: Number (raw arithmetic mean) or `null`. See "Reporting variants" below.
- **std**: Number (sample standard deviation) or `null`. See "Reporting variants" below.
- **note**: Free-text string or `null`. Used to record the exact statistic that was reported when `mean` and/or `std` are `null` (e.g., "Median (IQR) = 12 (8-16)", "Mean (95% CI) = 14.5 (12.3, 16.7); SD not reported", "Adjusted/LSMean = 18.3 reported; raw mean not reported", "Values reported only in Figure 2"). Set to `null` when both `mean` and `std` are reported and no further note is needed.
- **pages**: Array of integers. All page numbers documenting this specific cell.
- **quotes**: Array of strings. All exact quotes documenting this specific cell. The number of items must match `pages` one-to-one.

#### 3.1 Time points (`pre` / `post`)

Time is **strictly limited** to two values:

- **`pre`**: The baseline / pre-intervention assessment. Synonyms in the literature include: "baseline", "T0", "T1" (when used as the very first time point), "pretest", "pre-treatment", "pre-intervention".
- **`post`**: The first post-intervention assessment, scheduled immediately following the intervention period (i.e., when treatment ends). Synonyms include: "post", "post-test", "post-intervention", "post-treatment", "end of treatment", "T1" or "T2" (when used to denote the immediate post measurement after a baseline labelled T0 or T1).

**Excluded** time points (do not emit measurements for any of these):

- Mid-intervention assessments (e.g., week 4 of an 8-week trial).
- Follow-up assessments at any horizon (e.g., 1-month follow-up, 3-month follow-up, 6-month follow-up, 12-month follow-up).
- Per-session adherence/exposure measurements.

**Examples:**

```
Methods: "Outcomes were assessed at baseline, post-intervention, and 3-month follow-up."
→ Extract baseline → time="pre", post-intervention → time="post". DO NOT extract 3-month follow-up.
```

```
Methods: "Assessments occurred at T0 (pre-randomization), T1 (week 4, mid-treatment), T2 (week 8, end of treatment), T3 (week 20, follow-up)."
→ Extract T0 → time="pre", T2 → time="post". DO NOT extract T1 or T3.
```

```
Methods: "Symptoms were assessed weekly during the intervention."
→ Use the first weekly assessment as `pre` (if labelled baseline / pre-treatment) and the last weekly assessment as `post` (if it falls at end-of-treatment). If the paper does not clearly indicate a baseline and an end-of-treatment assessment, do not invent them — emit only the cells the paper labels as such.
```

#### 3.2 Subscale and Total emission rules

For instruments with subscales, **emit one row per separately-reported component**. Do not decompose totals into subscales or recompose subscales into a total.

- **DASS-21** has no Total reported by convention (only Depression, Anxiety, Stress). Emit one row per reported subscale per (group, time):
  ```
  control (passive_control) | DASS-21 - Depression - pre   | ...
  control (passive_control) | DASS-21 - Anxiety    - pre   | ...
  control (passive_control) | DASS-21 - Stress     - pre   | ...
  ```
- **BDI-II** has a Total. If the paper reports only the Total, emit only the Total. If the paper reports the Total **and** subscales, emit all of them. Never emit subscales when only the Total is reported, and never emit a Total when only subscales are reported.
- **HADS** has Anxiety and Depression subscales, and optionally a Total. Emit only the components actually reported.
- **GAD-7 / PHQ-9 / BAI / ...** (single-score instruments): emit one row per (group, time) using the `Total` component label.

#### 3.3 Reporting variants for `mean` and `std`

The `mean` field is the **raw arithmetic mean** reported in the paper. The `std` field is the **sample standard deviation** reported in the paper. Apply the following rules to decide what to emit:

| Reported as | `mean` | `std` | `note` example |
|---|---|---|---|
| `M = 14.5, SD = 1.8` (or equivalent `14.5 ± 1.8` with SD context) | `14.5` | `1.8` | `null` |
| `M = 14.5, SE = 0.4` | `14.5` | `null` | `"SE = 0.4 reported instead of SD"` |
| `M = 14.5 (95% CI 12.3, 16.7)` | `14.5` | `null` | `"95% CI [12.3, 16.7] reported instead of SD"` |
| `Median = 12 (IQR 8-16)` | `null` | `null` | `"Median (IQR) reported instead of M ± SD: 12 (8-16)"` |
| `Median = 12 (range 6-20)` | `null` | `null` | `"Median (range) reported instead of M ± SD: 12 (6-20)"` |
| `Adjusted mean (LSMean / EMM) = 18.3, SE = ...` and no raw mean reported | `null` | `null` | `"Only adjusted mean reported (LSMean = 18.3); raw mean not reported"` |
| Values shown only in a figure / graph | `null` | `null` | `"Values reported only in Figure X"` |
| `± 1.8` ambiguous (could be SD or SE) | extract the mean if reported | `null` | `"± 1.8 reported but unit (SD vs SE) not specified"` |

**Rules:**

- **Never derive** `std` from `SE`, `CI`, `IQR`, `range`, or any other statistic. Do not multiply `SE × √n` or apply CI-to-SD formulas.
- **Never** report an adjusted mean (ANCOVA/LSMean/EMMean/marginal mean) as `mean`. Only raw arithmetic means qualify.
- **Never** invent a value, even if it is "obvious" from a figure.
- If a value is reported with a precision modifier (e.g., "approximately 15"), record the exact text in the `note` and set `mean` to `null` if the value is not stated as a precise number.

#### 3.4 Row emission rule

Emit a measurement row if **any** statistic (raw mean, SD, median, IQR, SE, CI, adjusted mean, graphical value, etc.) is reported for that (group × outcome × time) cell. In every emitted row at least one of `mean`, `std`, or `note` must be informative (i.e., not all three null/empty).

If a (group × outcome × time) cell is not mentioned at all in the paper, **omit the row entirely**. Do not fabricate empty rows.

---

## Handling Special Cases

### Single-arm studies

If the paper reports a single arm (uncontrolled trial), emit one entry in `arms` and the corresponding measurements. The `category` should still be assessed (often `experimental` for the single intervention arm).

### Protocol papers

For protocol papers without results:

- `arms`: emit one entry per planned arm with the planned name and category.
- `instruments`: emit one entry per planned primary/secondary instrument **only if** the paper lists them by name and explicitly designates which are primary; `components` may be limited to canonical defaults (e.g., `["BDI-II - Total"]`) when the paper does not report subscales.
- `measurements`: emit `[]`.

### Crossover designs

Emit `pre` and `post` measurements for each treatment phase only if the paper reports them as such. If the paper aggregates across phases, treat the aggregated measurement as `post`.

### Multiple post-intervention assessments

Many papers measure outcomes at end-of-treatment **and** at follow-up. Use only the end-of-treatment assessment as `post`. Discard all follow-ups.

### Per-subgroup statistics within an arm

If the paper reports values broken down by subgroup (e.g., split by sex or age) within an arm but does not report the arm-level aggregate, do not aggregate yourself. Set `mean=null, std=null` and document the subgroup breakdown in `note`.

### Per-group statistics aggregated across arms

If the paper reports a single statistic pooled across all arms, do not split it. Either omit (preferred) or emit one row per arm with `mean=null, std=null` and a `note` saying values are pooled.

### Instruments without subscales reported

If an instrument is mentioned but no numeric statistic is reported anywhere for it, **do not** include it in `instruments`. Only list instruments for which at least one (group, time) cell has a reported statistic.

### Effect sizes and inferential statistics

Effect sizes (Cohen's d, Hedges' g, η²p, ω²), p-values, F-statistics, t-statistics, confidence intervals on differences, and similar inferential outputs are **not** descriptive means and are out of scope. Do not extract them.

---

## Important Instructions

1. **Pre and post only**: Discard mid-intervention and all follow-up assessments.
2. **Raw means only**: Adjusted/LSMean/EMMean values are recorded as `note` with `mean=null`, never as `mean`.
3. **No derivation**: Do not compute SD from SE, CI, IQR, or range. Do not compute means from per-group raw data.
4. **No guessing**: When a value is unclear, ambiguous, or only graphical, set the field to `null` and explain in `note`.
5. **Match `study_arms`**: Use the exact arm names the authors use, so that arms can be matched 1-to-1 with the `study_arms` prompt output by name. Note that waitlist arms are categorized differently between the two prompts (`waitlist` vs `passive_control`); matching is done on `name`, not on `identifier`.
6. **Identifier composition**: `identifier = "<arm name> (<category|unknown>)"` exactly. One space before the parenthesis. Lowercase category strings.
7. **Outcome composition**: `outcome = "<Instrument> - <Subscale|Total> - <pre|post>"` exactly. Two ` - ` separators. Title-Case subscale names; lowercase `pre` / `post`.
8. **Components scope**: Only list a component in `instruments[].components` if at least one (group, time) cell reports a numeric statistic for it. Conversely, every component listed must appear in at least one measurement row.
9. **One row per (group, outcome, time) cell**: Never duplicate. If the paper reports the same value in multiple places (e.g., text + table), include all supporting quotes/pages in the single row.
10. **Per-cell evidence**: Each measurement row carries its own `pages` and `quotes` documenting that specific cell. The reader must be able to verify each row independently.
11. **Subscales independent of Total**: Total and each subscale are independent rows. Do not decompose or recompose.
12. **Empty arrays are valid**: `instruments` may be `[]` (no scored instruments). `measurements` may be `[]` (protocol paper).

## Source Citation Requirements

For each piece of information you extract, you must provide **exhaustive and thorough citations**:

1. **Page numbers**: A list of **ALL** page numbers where information supporting your extraction was found.
2. **Quotes**: A list of **ALL** direct quotes from the document that you used to build the extracted information.

**Critical Requirements**:

- **Be exhaustive**: Include every single quote and page that contributed to your answer, including both text passages and table captions / cell values.
- **One-to-one correspondence**: The number of quotes must exactly match the number of pages.
- **Direct quotes only**: Copy text exactly as it appears in the document.
- **JSON escaping for quotes**: Since quotes are embedded in a JSON string, any double-quote characters (`"`) within the quoted text must be escaped as `\"`. This is standard JSON encoding and is **not** considered a modification of the quote — JSON parsers will decode `\"` back to `"` when reading the output. For example, if the document contains: `The "primary" outcome was measured`, the JSON value should be: `"The \"primary\" outcome was measured"`.
- **No omissions**: Even if information seems obvious or redundant, include all supporting evidence.
- **For table values**: A short quote is acceptable for individual cells (e.g., `"BDI-II baseline 22.4 (6.1)"` lifted from a table caption + cell). Always include the page number where the table appears.

## Output Format

Return your response as a JSON object with the following structure:

```json
{
  "arms": [
    {
      "name": {
        "value": "Arm name as stated by the authors",
        "pages": [page_number, ...],
        "quotes": ["Exact text from document", ...]
      },
      "category": {
        "value": "experimental" | "active_control" | "passive_control" | null,
        "pages": [page_number, ...] or null,
        "quotes": ["Exact text from document", ...] or null
      },
      "identifier": "<arm name> (experimental | active_control | passive_control | unknown)"
    }
  ],
  "instruments": [
    {
      "name": {
        "value": "Canonical abbreviation",
        "pages": [page_number, ...],
        "quotes": ["Exact text from document", ...]
      },
      "primary": {
        "value": true | false,
        "pages": [page_number, ...],
        "quotes": ["Exact text from document", ...]
      },
      "components": ["<Instrument> - <Subscale|Total>", ...]
    }
  ],
  "measurements": [
    {
      "group": "<arm identifier>",
      "outcome": "<Instrument> - <Subscale|Total> - <pre|post>",
      "primary": true | false,
      "mean": <number> or null,
      "std": <number> or null,
      "note": "<observation>" or null,
      "pages": [page_number, ...],
      "quotes": ["Exact text from document", ...]
    }
  ]
}
```

**Important**:

- Each per-cell field must have matching lengths for `pages` and `quotes` arrays (when not null).
- `arms` requires at least one entry. `instruments` and `measurements` may be empty arrays.
- Every `group` value in `measurements` must exactly equal one `arms[].identifier`.
- Every `outcome` value in `measurements` must start with one of the `instruments[].components` strings (followed by ` - pre` or ` - post`).
- Every `primary` value in `measurements` must equal the parent instrument's `primary.value`.

### Example Output 1: Two-arm completed RCT, BDI-II Total + DASS-21 subscales

```json
{
  "arms": [
    {
      "name": {
        "value": "MindLight intervention",
        "pages": [3],
        "quotes": ["Participants randomized to the MindLight intervention played the game for 8 weeks."]
      },
      "category": {
        "value": "experimental",
        "pages": [3],
        "quotes": ["Participants randomized to the MindLight intervention played the game for 8 weeks."]
      },
      "identifier": "MindLight intervention (experimental)"
    },
    {
      "name": {
        "value": "Waitlist control",
        "pages": [3, 4],
        "quotes": [
          "Participants in the waitlist control received no intervention during the 8-week study period.",
          "Waitlist participants were offered MindLight after the post-intervention assessment."
        ]
      },
      "category": {
        "value": "passive_control",
        "pages": [3, 4],
        "quotes": [
          "Participants in the waitlist control received no intervention during the 8-week study period.",
          "Waitlist participants were offered MindLight after the post-intervention assessment."
        ]
      },
      "identifier": "Waitlist control (passive_control)"
    }
  ],
  "instruments": [
    {
      "name": {
        "value": "BDI-II",
        "pages": [4],
        "quotes": ["Depression severity was assessed with the Beck Depression Inventory-II (BDI-II)."]
      },
      "primary": {
        "value": true,
        "pages": [4],
        "quotes": ["The primary outcome was BDI-II Total score at post-intervention."]
      },
      "components": ["BDI-II - Total"]
    },
    {
      "name": {
        "value": "DASS-21",
        "pages": [4],
        "quotes": ["Secondary outcomes were measured with the Depression Anxiety Stress Scales (DASS-21)."]
      },
      "primary": {
        "value": false,
        "pages": [4],
        "quotes": ["Secondary outcomes were measured with the Depression Anxiety Stress Scales (DASS-21)."]
      },
      "components": [
        "DASS-21 - Depression",
        "DASS-21 - Anxiety",
        "DASS-21 - Stress"
      ]
    }
  ],
  "measurements": [
    {
      "group": "MindLight intervention (experimental)",
      "outcome": "BDI-II - Total - pre",
      "primary": true,
      "mean": 22.4,
      "std": 6.1,
      "note": null,
      "pages": [6],
      "quotes": ["Table 2. Baseline BDI-II Total: MindLight 22.4 (SD 6.1)."]
    },
    {
      "group": "MindLight intervention (experimental)",
      "outcome": "BDI-II - Total - post",
      "primary": true,
      "mean": 18.2,
      "std": 5.8,
      "note": null,
      "pages": [6],
      "quotes": ["Table 2. Post-intervention BDI-II Total: MindLight 18.2 (SD 5.8)."]
    },
    {
      "group": "Waitlist control (passive_control)",
      "outcome": "BDI-II - Total - pre",
      "primary": true,
      "mean": 21.9,
      "std": 6.4,
      "note": null,
      "pages": [6],
      "quotes": ["Table 2. Baseline BDI-II Total: Waitlist 21.9 (SD 6.4)."]
    },
    {
      "group": "Waitlist control (passive_control)",
      "outcome": "BDI-II - Total - post",
      "primary": true,
      "mean": 21.5,
      "std": 6.2,
      "note": null,
      "pages": [6],
      "quotes": ["Table 2. Post-intervention BDI-II Total: Waitlist 21.5 (SD 6.2)."]
    },
    {
      "group": "MindLight intervention (experimental)",
      "outcome": "DASS-21 - Depression - pre",
      "primary": false,
      "mean": null,
      "std": null,
      "note": "Median (IQR) reported instead of M ± SD: 12 (IQR 8-16)",
      "pages": [7],
      "quotes": ["Table 3. Baseline DASS-21 Depression (median, IQR): MindLight 12 (8-16)."]
    },
    {
      "group": "MindLight intervention (experimental)",
      "outcome": "DASS-21 - Depression - post",
      "primary": false,
      "mean": null,
      "std": null,
      "note": "Median (IQR) reported instead of M ± SD: 9 (IQR 6-13)",
      "pages": [7],
      "quotes": ["Table 3. Post-intervention DASS-21 Depression (median, IQR): MindLight 9 (6-13)."]
    },
    {
      "group": "MindLight intervention (experimental)",
      "outcome": "DASS-21 - Anxiety - pre",
      "primary": false,
      "mean": 8.4,
      "std": 3.2,
      "note": null,
      "pages": [7],
      "quotes": ["Table 3. Baseline DASS-21 Anxiety: MindLight 8.4 (SD 3.2)."]
    },
    {
      "group": "MindLight intervention (experimental)",
      "outcome": "DASS-21 - Anxiety - post",
      "primary": false,
      "mean": 6.1,
      "std": 2.9,
      "note": null,
      "pages": [7],
      "quotes": ["Table 3. Post-intervention DASS-21 Anxiety: MindLight 6.1 (SD 2.9)."]
    },
    {
      "group": "MindLight intervention (experimental)",
      "outcome": "DASS-21 - Stress - pre",
      "primary": false,
      "mean": 11.2,
      "std": 4.1,
      "note": null,
      "pages": [7],
      "quotes": ["Table 3. Baseline DASS-21 Stress: MindLight 11.2 (SD 4.1)."]
    },
    {
      "group": "MindLight intervention (experimental)",
      "outcome": "DASS-21 - Stress - post",
      "primary": false,
      "mean": 9.5,
      "std": 3.8,
      "note": null,
      "pages": [7],
      "quotes": ["Table 3. Post-intervention DASS-21 Stress: MindLight 9.5 (SD 3.8)."]
    },
    {
      "group": "Waitlist control (passive_control)",
      "outcome": "DASS-21 - Anxiety - pre",
      "primary": false,
      "mean": 8.6,
      "std": 3.4,
      "note": null,
      "pages": [7],
      "quotes": ["Table 3. Baseline DASS-21 Anxiety: Waitlist 8.6 (SD 3.4)."]
    },
    {
      "group": "Waitlist control (passive_control)",
      "outcome": "DASS-21 - Anxiety - post",
      "primary": false,
      "mean": 8.2,
      "std": 3.3,
      "note": null,
      "pages": [7],
      "quotes": ["Table 3. Post-intervention DASS-21 Anxiety: Waitlist 8.2 (SD 3.3)."]
    },
    {
      "group": "Waitlist control (passive_control)",
      "outcome": "DASS-21 - Stress - pre",
      "primary": false,
      "mean": null,
      "std": null,
      "note": "Only adjusted mean reported (LSMean = 11.0, SE = 0.6); raw mean not reported",
      "pages": [8],
      "quotes": ["Table 4. Adjusted LSMeans: Waitlist DASS-21 Stress baseline 11.0 (SE 0.6)."]
    }
  ]
}
```

Notes on the example:

- Both groups have BDI-II Total at pre and post → 4 rows.
- The MindLight arm has DASS-21 Depression as median (IQR) at both time points → 2 rows with mean=null/std=null and median documented in `note`.
- The Waitlist arm has no DASS-21 Depression data reported → no rows for that combination (rows are not fabricated).
- The Waitlist arm DASS-21 Stress baseline reports only an LSMean → 1 row with mean=null/std=null and the LSMean documented in `note`. Other Waitlist DASS-21 Stress cells are not reported → no rows.

### Example Output 2: Protocol paper

```json
{
  "arms": [
    {
      "name": {
        "value": "Game-based CBT",
        "pages": [4],
        "quotes": ["Participants will be randomized 1:1 to the game-based CBT intervention or to a waitlist control."]
      },
      "category": {
        "value": "experimental",
        "pages": [4],
        "quotes": ["Participants will be randomized 1:1 to the game-based CBT intervention or to a waitlist control."]
      },
      "identifier": "Game-based CBT (experimental)"
    },
    {
      "name": {
        "value": "Waitlist control",
        "pages": [4],
        "quotes": ["Participants randomized to the waitlist will receive the intervention after the 8-week study period."]
      },
      "category": {
        "value": "passive_control",
        "pages": [4],
        "quotes": ["Participants randomized to the waitlist will receive the intervention after the 8-week study period."]
      },
      "identifier": "Waitlist control (passive_control)"
    }
  ],
  "instruments": [
    {
      "name": {
        "value": "PHQ-9",
        "pages": [5],
        "quotes": ["The primary outcome will be depression severity measured with the PHQ-9 at week 8."]
      },
      "primary": {
        "value": true,
        "pages": [5],
        "quotes": ["The primary outcome will be depression severity measured with the PHQ-9 at week 8."]
      },
      "components": ["PHQ-9 - Total"]
    },
    {
      "name": {
        "value": "GAD-7",
        "pages": [5],
        "quotes": ["Anxiety symptoms will be assessed as a secondary outcome with the GAD-7."]
      },
      "primary": {
        "value": false,
        "pages": [5],
        "quotes": ["Anxiety symptoms will be assessed as a secondary outcome with the GAD-7."]
      },
      "components": ["GAD-7 - Total"]
    }
  ],
  "measurements": []
}
```

## Begin Extraction

Please analyze the provided PDF document and extract the outcome measurement information according to the specifications above. Remember:

1. Restrict time to **pre** (baseline) and **post** (end-of-intervention) only — discard mid and follow-up assessments.
2. Include **every instrument** used to score participants, regardless of construct.
3. Use canonical instrument abbreviations and subscale labels per the canonical table; for instruments not listed, use the authors' abbreviation and subscale wording in Title Case.
4. Compose `arms[].identifier` as `<arm name> (<category|unknown>)` and `measurements[].outcome` as `<Instrument> - <Subscale|Total> - <pre|post>`.
5. Emit one measurement row per (group × outcome × time) cell that has any reported statistic. Skip cells with no data.
6. Set `mean`/`std` only for raw `M ± SD` reporting; otherwise set them to `null` and document the actual statistic in `note`.
7. Document every row with exhaustive `pages` and `quotes` (one-to-one correspondence). Do not guess. Do not fabricate.
