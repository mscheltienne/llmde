# Study Information Extraction

## Task

Extract key methodological, demographic, and sample characteristics from this scientific paper to characterize the study design, setting, participant population, and sample flow.

## Required Information

You must extract the following elements from the document:

1. **Study Completion Status**: Whether the study is completed, ongoing, or unclear
2. **Country of Study**: The country or countries where the study was conducted
3. **Target Group**: Population descriptor characterizing who the intervention targets
4. **Clinical Status**: Classification of participant clinical severity (healthy, subclinical, clinical)
5. **Sample Size**: Total number of participants randomized and analyzed
6. **Study Conditions/Arms**: All experimental groups, their classification, and per-arm sample sizes
7. **Attrition**: Dropout rates and numbers
8. **Participant Age**: Mean or median age, standard deviation, range, and unit
9. **Sex Distribution**: Counts and percentages of male and female participants

## Where to Find This Information

**Important**: The locations listed below are **typical** places where information appears. However, you must **read carefully and thoroughly through the entire document** to ensure you locate all required information, as it may appear in unexpected sections or across multiple pages.

### Study Completion Status
- **Typical locations**: Title, abstract, discussion/conclusion sections
- **Key indicators**: Protocol papers, "will be conducted", past tense vs. future tense

### Country of Study
- **Typical locations**: Methods section (study setting/participants), title, author affiliations
- **Key indicators**: Institution names, city/country mentions, "conducted in..."

### Target Group
- **Typical locations**: Title, Abstract, Introduction (Study aims), Methods (Participants/Inclusion criteria)
- **Key indicators**: Population descriptors (e.g., "adolescents", "older adults", "students"), condition descriptors (e.g., "patients with depression", "individuals with anxiety")

### Clinical Status
- **Typical locations**: Title, Abstract, Methods (Participants/Inclusion criteria), Introduction
- **Key indicators**: "diagnosed with", "clinical", "subclinical", "at-risk", "elevated symptoms", "healthy", "general population", "patients", "typically developed"

### Sample Size
- **Typical locations**: Abstract, Methods (Participants/Sample), Results (Flow diagram/Participant flow), Tables (Baseline characteristics)
- **Key indicators**: "N =", "n =", "sample size", "participants", "randomized", "analyzed", "completed", CONSORT flow diagram

### Study Conditions/Arms
- **Typical locations**: Introduction (hypotheses), methods section (study design, randomization), Results (flow diagram)
- **Key indicators**: "randomized to...", "groups included...", "conditions were...", per-group sample sizes

### Attrition
- **Typical locations**: Results (Participant flow/Attrition), CONSORT flow diagram, Discussion (Limitations)
- **Key indicators**: "dropout", "attrition", "withdrew", "lost to follow-up", "discontinued", "did not complete"

### Participant Age
- **Typical locations**: Methods (participants section), results (baseline characteristics), abstract
- **Key indicators**: "mean age", "median age", "aged between", "age range", demographic tables

### Sex Distribution
- **Typical locations**: Methods (Participants), Results (Baseline characteristics table), Abstract
- **Key indicators**: "male", "female", "sex", "gender", "% female", "women", "men", "girls", "boys"

## Detailed Field Definitions

### 1. Study Completion Status

Classify the study as one of three categories:

- **`completed`**: Study has been conducted and results are reported
- **`ongoing`**: Study is in progress, a protocol, or planned (future tense used)
- **`unclear`**: Cannot determine status from the document

**Examples:**

```
Title: "A serious game for depressive symptoms: Protocol for a randomised controlled trial"
→ Status: ongoing (protocol paper)

Discussion: "This paper presents the protocol for a randomized controlled study"
→ Status: ongoing (explicit protocol statement)

Results: "We found that participants in the game condition showed..."
→ Status: completed (past tense, results reported)
```

### 2. Country of Study

List all countries where the study was conducted. For multi-site international studies, include all countries.

**Examples:**

```
Methods: "RCT will be carried out at the Emotional Disorder Clinic in Universitat Jaume I."
→ Country: Spain (Universitat Jaume I is in Spain)

Title: "The effectiveness of game-based interventions in preventing anxiety in Turkey"
→ Country: Turkey
```

### 3. Target Group

**Task**: Characterize the population group or condition targeted by the intervention.

**Definition**: A free-text descriptor capturing the specific population based on:
- Age group (e.g., adolescents, older adults)
- Sex (e.g., girls, males)
- Setting (e.g., students, aged care residents)
- Condition (e.g., patients with depression, individuals with anxiety)

**Format**: Free-text string capturing the authors' description of the target population.

**Examples:**

```
Introduction (Study aims): "The aim is to investigate the mental health of aged care residents."
→ value: "aged care residents"

Title: "Comparing two programs for adolescent girls with subclinical depression."
→ value: "adolescent girls with subclinical depression"

Abstract: "Game intervention for patients with mild to moderate depressive symptoms."
→ value: "patients with mild to moderate depressive symptoms"

Methods: "We recruited university students experiencing elevated anxiety."
→ value: "university students with elevated anxiety"
```

### 4. Clinical Status

**Task**: Classify the clinical status of the target population.

**Allowed values:** [`healthy`, `subclinical`, `clinical`]

**Definitions:**

- **`healthy`**: Individuals from the general population (non-patients) without a diagnosis and not meeting clinical thresholds for the target condition.
- **`subclinical`**: Individuals with elevated or at-risk symptoms who do not meet full diagnostic criteria (e.g., mild symptoms, screening positive but below diagnostic threshold, no clinician diagnosis).
- **`clinical`**: Individuals with a formal diagnosis or who meet established clinical thresholds for the target condition, typically recruited from clinical/treatment settings (inpatient/outpatient).

**Key indicators:**

- **Healthy**: "general population", "healthy", "typically developed", "non-clinical", "prevention", "universal"
- **Subclinical**: "elevated symptoms", "at-risk", "subclinical", "mild", "subthreshold", "indicated prevention"
- **Clinical**: "diagnosed", "patients", "clinical", "disorder", "meeting criteria for", "recruited from clinic"

**Examples:**

```
Methods: "We recruited typically developed adolescents."
→ value: "healthy"

Title: "Comparing two programs for adolescent girls with subclinical depression."
→ value: "subclinical"

Abstract: "Patients with a primary diagnosis of MDD."
→ value: "clinical"

Methods: "Participants were recruited from outpatient psychiatric clinics and met DSM-5 criteria for generalized anxiety disorder."
→ value: "clinical"

Methods: "Students scoring above the cutoff on the PHQ-9 but not meeting criteria for major depression."
→ value: "subclinical"
```

### 5. Sample Size

**Task**: Extract the total number of participants randomized and analyzed across all study arms.

**Values to extract:**

- **total_randomized**: Total number of participants randomized to conditions
- **total_analyzed**: Total number of participants included in the final analysis (ITT or per-protocol)

**Protocol handling**: For protocol papers without results, use `null` for both values.

**Examples:**

```
Abstract: "We randomized 120 participants to three conditions."
→ total_randomized: 120

Results: "Analysis included 98 participants who completed the study."
→ total_analyzed: 98

CONSORT diagram: Shows 150 randomized, 142 included in analysis
→ total_randomized: 150, total_analyzed: 142

Protocol paper with no results yet:
→ total_randomized: null, total_analyzed: null
```

### 6. Study Conditions/Arms

**Task**: List all study conditions, map each to one of the allowed categories, and extract per-arm sample sizes.

For each study arm/group/condition, extract:

- **Name**: The specific name or description used by the authors
- **Category**: Classification into one of the allowed values
- **n_randomized**: Number of participants randomized to this arm (or `null` if not reported/protocol)
- **n_analyzed**: Number of participants included in analysis for this arm (or `null` if not reported/protocol)

**Allowed category values:** [`experimental`, `active_control`, `waitlist`, `passive_control`]

**Category definitions:**

- **`experimental`**: Group that receives the novel intervention or treatment being studied.
- **`active_control`**: Group that receives a different, already established treatment, like the current standard of care (e.g., treatment as usual), or a sham treatment (a placebo) to control for other effects (e.g., placebo effects).
- **`waitlist`**: Group that is on a waiting list to receive the experimental treatment after the study is over.
- **`passive_control`**: Group that receives no intervention, live their life as usual during the intervention period (without intervention or no contact group).

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

### 7. Attrition

**Task**: Extract information about participant dropout/attrition.

**Values to extract:**

- **n_dropout**: Total number of participants who dropped out
- **dropout_rate**: Percentage of participants who dropped out
- **derivation**: Whether values were "stated" or "calculated"

**Derivation tracking:**

- **`stated`**: Values explicitly reported in text (e.g., "22 participants (18%) withdrew")
- **`calculated`**: Values computed from other numbers (e.g., dropout = randomized - analyzed)

**Calculation rules:**

- If only dropout N given: calculate rate from `(n_dropout / total_randomized) × 100`
- If only rate given: calculate N from `rate × total_randomized / 100`
- If neither stated but both randomized and analyzed totals available: calculate both from the difference

**Protocol handling**: For protocol papers without results, use `null` for all values including derivation.

**Examples:**

```
Results: "22 participants (18%) withdrew before study completion."
→ n_dropout: 22, dropout_rate: 18, derivation: "stated"

CONSORT diagram shows: Randomized = 100, Completed = 85
→ n_dropout: 15, dropout_rate: 15, derivation: "calculated"

Results: "15% of participants dropped out of the study."
Abstract: "We randomized 120 participants"
→ n_dropout: 18 (calculated), dropout_rate: 15, derivation: "calculated"

Protocol paper with no results:
→ n_dropout: null, dropout_rate: null, derivation: null
```

### 8. Participant Age

Extract all available age information:

- **Value**: The central tendency value (mean OR median) of participants' ages (if reported)
- **Type**: Whether the value is a "mean" or "median" (if reported)
- **Standard deviation**: SD of age (if reported - typically only with mean)
- **Age range**: Minimum and maximum ages (if reported)
- **Unit**: Typically "years"

**Important**: Always extract BOTH the numeric value AND the type of statistic (mean vs median). If only a range is given without mean/median, set value and type to null.

**Examples:**

```
Methods: "Participants between the ages 10 and 15"
→ value: null, type: null, sd: null, range: [10, 15], unit: "years"

Results: "The mean age was 15.5 years (SD = 2.3)"
→ value: 15.5, type: "mean", sd: 2.3, range: [null, null], unit: "years"

Methods: "The median age was 34 years (range: 21-58)"
→ value: 34, type: "median", sd: null, range: [21, 58], unit: "years"

Methods: "Adult participants (M = 34.2, SD = 8.1, range: 21-58 years)"
→ value: 34.2, type: "mean", sd: 8.1, range: [21, 58], unit: "years"
```

### 9. Sex Distribution

**Task**: Extract the distribution of male and female participants, reporting both counts and percentages.

**Values to extract:**

- **n_female**: Number of female participants
- **n_male**: Number of male participants
- **pct_female**: Percentage of female participants
- **pct_male**: Percentage of male participants
- **derivation**: Whether values were "stated", "calculated", or "partial"

**Derivation tracking:**

- **`stated`**: All values explicitly reported in text
- **`calculated`**: All values computed from other data
- **`partial`**: Some values stated, some calculated (e.g., female count stated, male count calculated)

**Calculation rules:**

- If only counts given: calculate percentages from `(count / total) × 100`
- If only percentages given: calculate counts from `(percentage × total) / 100` (requires total N)
- If only one sex reported: calculate the other from the complement

**Protocol handling**: For protocol papers without results, use `null` for all values including derivation.

**Examples:**

```
Methods: "Participants included 65 females (54%) and 55 males (46%)."
→ n_female: 65, n_male: 55, pct_female: 54, pct_male: 46, derivation: "stated"

Table 1: "Female n=78 (65%)"
→ n_female: 78, pct_female: 65, n_male: 42 (calculated), pct_male: 35 (calculated), derivation: "partial"

Methods: "The sample was 70% female (N=120 total)."
→ n_female: 84 (calculated), n_male: 36 (calculated), pct_female: 70, pct_male: 30 (calculated), derivation: "calculated"

Protocol paper with no results:
→ n_female: null, n_male: null, pct_female: null, pct_male: null, derivation: null
```

## Important Instructions

1. **Extract exactly what you see**: Do not infer country from author names alone
2. **Map arms carefully**: Use the definitions provided to categorize each condition
3. **Report all arms**: Include every condition mentioned in the study
4. **Handle missing values**: Use `null` for unreported numerical values
5. **Preserve original naming**: Use the authors' exact names for study arms
6. **Do not convert units**: Report ages in the units provided by authors
7. **Be conservative**: If status or category is ambiguous, choose "unclear" or ask in a note
8. **Handle protocols appropriately**: For protocol papers without results, use `null` for sample_size, attrition, sex_distribution, and per-arm sample sizes
9. **Calculate when needed**: For attrition and sex distribution, calculate missing values when sufficient information is provided
10. **Use exact descriptions**: For target_group, capture the authors' description accurately

## Source Citation Requirements

For each piece of information you extract, you must provide **exhaustive and thorough citations**:

1. **Page numbers**: A list of **ALL** page numbers where information supporting your extraction was found
2. **Quotes**: A list of **ALL** direct quotes from the document that you used to build the extracted information

**Critical Requirements**:
- **Be exhaustive**: Include every single quote and page that contributed to your answer
- **One-to-one correspondence**: The number of quotes must exactly match the number of pages
- **Direct quotes only**: Copy text exactly as it appears in the document
- **No omissions**: Even if information seems obvious or redundant, include all supporting evidence
- **For aggregated values**: Include ALL quotes used, not just the most relevant one
- **For calculated values**: Include ALL quotes used in the calculation

## Output Format

Return your response as a JSON object with the following structure:

```json
{
  "completion_status": {
    "value": "completed" | "ongoing" | "unclear",
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "countries": {
    "value": ["Country Name", ...],
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "target_group": {
    "value": "Description of target population",
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "clinical_status": {
    "value": "healthy" | "subclinical" | "clinical",
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "sample_size": {
    "total_randomized": {
      "value": integer or null,
      "pages": [page_number, ...],
      "quotes": ["Exact text from document", ...]
    },
    "total_analyzed": {
      "value": integer or null,
      "pages": [page_number, ...],
      "quotes": ["Exact text from document", ...]
    }
  },
  "arms": [
    {
      "name": "Arm name as stated by authors",
      "category": "experimental" | "active_control" | "waitlist" | "passive_control",
      "n_randomized": integer or null,
      "n_analyzed": integer or null,
      "pages": [page_number, ...],
      "quotes": ["Exact text from document", ...]
    },
    ...
  ],
  "attrition": {
    "n_dropout": integer or null,
    "dropout_rate": number or null,
    "derivation": "stated" | "calculated" | null,
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "age": {
    "value": number or null,
    "type": "mean" | "median" | null,
    "sd": number or null,
    "range": [min or null, max or null],
    "unit": "years",
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "sex_distribution": {
    "n_female": integer or null,
    "n_male": integer or null,
    "pct_female": number or null,
    "pct_male": number or null,
    "derivation": "stated" | "calculated" | "partial" | null,
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  }
}
```

**Important**:
- Each field must have matching lengths for `pages` and `quotes` arrays
- Include all supporting evidence, even if the same information appears multiple times
- For calculated values in attrition and sex_distribution, use appropriate derivation value

### Example Output

```json
{
  "completion_status": {
    "value": "completed",
    "pages": [1, 8],
    "quotes": [
      "We conducted a randomized controlled trial to examine...",
      "Results showed significant improvements in the intervention group"
    ]
  },
  "countries": {
    "value": ["United States", "Canada"],
    "pages": [3, 3],
    "quotes": [
      "The study was conducted at five sites across the United States and Canada",
      "Recruitment occurred at sites in Seattle, WA and Vancouver, BC"
    ]
  },
  "target_group": {
    "value": "adolescents with mild to moderate depressive symptoms",
    "pages": [1, 3],
    "quotes": [
      "game intervention for adolescents with mild to moderate depressive symptoms",
      "We recruited adolescents aged 12-17 experiencing elevated depressive symptoms"
    ]
  },
  "clinical_status": {
    "value": "subclinical",
    "pages": [3, 4],
    "quotes": [
      "adolescents with mild to moderate depressive symptoms",
      "Participants scored above the clinical cutoff on the PHQ-A but did not meet criteria for major depressive disorder"
    ]
  },
  "sample_size": {
    "total_randomized": {
      "value": 120,
      "pages": [1, 4],
      "quotes": [
        "We randomized 120 adolescents to one of three conditions",
        "A total of 120 participants were randomized"
      ]
    },
    "total_analyzed": {
      "value": 98,
      "pages": [6],
      "quotes": [
        "Final analyses included 98 participants who completed all assessments"
      ]
    }
  },
  "arms": [
    {
      "name": "SPARX game intervention",
      "category": "experimental",
      "n_randomized": 40,
      "n_analyzed": 35,
      "pages": [4, 5, 6],
      "quotes": [
        "Participants randomized to the SPARX game intervention (n=40) completed seven modules",
        "The SPARX group received weekly gaming sessions",
        "35 participants in the SPARX condition completed the study"
      ]
    },
    {
      "name": "treatment as usual",
      "category": "active_control",
      "n_randomized": 40,
      "n_analyzed": 32,
      "pages": [4, 6],
      "quotes": [
        "The control group received treatment as usual from their primary care provider (n=40)",
        "32 participants in TAU completed the study"
      ]
    },
    {
      "name": "waitlist control",
      "category": "waitlist",
      "n_randomized": 40,
      "n_analyzed": 31,
      "pages": [4, 6],
      "quotes": [
        "waitlist control (n=40)",
        "31 participants in the waitlist condition completed the study"
      ]
    }
  ],
  "attrition": {
    "n_dropout": 22,
    "dropout_rate": 18.3,
    "derivation": "calculated",
    "pages": [4, 6],
    "quotes": [
      "A total of 120 participants were randomized",
      "Final analyses included 98 participants who completed all assessments"
    ]
  },
  "age": {
    "value": 14.5,
    "type": "mean",
    "sd": 1.8,
    "range": [12, 17],
    "unit": "years",
    "pages": [1, 5],
    "quotes": [
      "adolescents aged 12-17 years",
      "Participants aged 12-17 years (M = 14.5, SD = 1.8)"
    ]
  },
  "sex_distribution": {
    "n_female": 78,
    "n_male": 42,
    "pct_female": 65,
    "pct_male": 35,
    "derivation": "partial",
    "pages": [5],
    "quotes": [
      "The sample was predominantly female (n=78, 65%)"
    ]
  }
}
```

### Example Output for Protocol Paper

```json
{
  "completion_status": {
    "value": "ongoing",
    "pages": [1, 2],
    "quotes": [
      "Protocol for a randomized controlled trial",
      "This paper presents the protocol for our planned study"
    ]
  },
  "countries": {
    "value": ["Germany"],
    "pages": [3],
    "quotes": [
      "The study will be conducted at the University Hospital in Munich, Germany"
    ]
  },
  "target_group": {
    "value": "adults with generalized anxiety disorder",
    "pages": [1, 3],
    "quotes": [
      "Protocol for a randomized trial in adults with generalized anxiety disorder",
      "Adults aged 18-65 meeting DSM-5 criteria for GAD will be eligible"
    ]
  },
  "clinical_status": {
    "value": "clinical",
    "pages": [3],
    "quotes": [
      "Adults aged 18-65 meeting DSM-5 criteria for GAD will be eligible"
    ]
  },
  "sample_size": {
    "total_randomized": {
      "value": null,
      "pages": [5],
      "quotes": [
        "We aim to recruit 150 participants"
      ]
    },
    "total_analyzed": {
      "value": null,
      "pages": [],
      "quotes": []
    }
  },
  "arms": [
    {
      "name": "game intervention",
      "category": "experimental",
      "n_randomized": null,
      "n_analyzed": null,
      "pages": [5],
      "quotes": [
        "Participants will be randomized 1:1 to the game intervention or control"
      ]
    },
    {
      "name": "waitlist control",
      "category": "waitlist",
      "n_randomized": null,
      "n_analyzed": null,
      "pages": [5],
      "quotes": [
        "Participants will be randomized 1:1 to the game intervention or control"
      ]
    }
  ],
  "attrition": {
    "n_dropout": null,
    "dropout_rate": null,
    "derivation": null,
    "pages": [],
    "quotes": []
  },
  "age": {
    "value": null,
    "type": null,
    "sd": null,
    "range": [18, 65],
    "unit": "years",
    "pages": [3],
    "quotes": [
      "Adults aged 18-65 meeting DSM-5 criteria for GAD will be eligible"
    ]
  },
  "sex_distribution": {
    "n_female": null,
    "n_male": null,
    "pct_female": null,
    "pct_male": null,
    "derivation": null,
    "pages": [],
    "quotes": []
  }
}
```

## Begin Extraction

Please analyze the provided PDF document and extract the study information according to the specifications above.
