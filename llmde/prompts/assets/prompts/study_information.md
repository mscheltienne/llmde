# Study Information Extraction

## Task

Extract key methodological and demographic information from this scientific paper to characterize the study design, setting, and participant characteristics.

## Required Information

You must extract the following elements from the document:

1. **Study Completion Status**: Whether the study is completed, ongoing, or unclear
2. **Country of Study**: The country or countries where the study was conducted
3. **Study Conditions/Arms**: All experimental groups and their classification
4. **Participant Age**: Mean age, standard deviation, range, and unit

## Where to Find This Information

**Important**: The locations listed below are **typical** places where information appears. However, you must **read carefully and thoroughly through the entire document** to ensure you locate all required information, as it may appear in unexpected sections or across multiple pages.

### Study Completion Status
- **Typical locations**: Title, abstract, discussion/conclusion sections
- **Key indicators**: Protocol papers, "will be conducted", past tense vs. future tense

### Country of Study
- **Typical locations**: Methods section (study setting/participants), title, author affiliations
- **Key indicators**: Institution names, city/country mentions, "conducted in..."

### Study Conditions/Arms
- **Typical locations**: Introduction (hypotheses), methods section (study design, randomization)
- **Key indicators**: "randomized to...", "groups included...", "conditions were..."

### Participant Age
- **Typical locations**: Methods (participants section), results (baseline characteristics), abstract
- **Key indicators**: "mean age", "aged between", "age range", demographic tables

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

### 3. Study Conditions/Arms

**Task**: List all study conditions and map each to one of the allowed values.

For each study arm/group/condition, extract:
- **Name**: The specific name or description used by the authors
- **Category**: Classification into one of the allowed values

**Allowed values:** [`experimental`, `active_control`, `waitlist`, `passive_control`]

**Definitions:**

- **`experimental`**: Group that receives the novel intervention or treatment being studied.
- **`active_control`**: Group that receives a different, already established treatment, like the current standard of care (e.g., treatment as usual).
- **`waitlist`**: Group that is on a waiting list to receive the experimental treatment after the study is over.
- **`passive_control`**: Group that receives no intervention at all or a sham treatment (a placebo) that is not expected to have an active effect.

**Examples:**

```
Introduction: "Participants in exercise with VR were expected to report higher level of enjoyment than those who engagement in traditional exercises"
→ 1. name="exercise with VR", category=experimental
→ 2. name="traditional exercises", category=active_control

Methods: "Participants were randomized to one of three cohorts: a BOXVR group, a guided video group, or a nonintervention control group (n = 14)"
→ 1. name="BOXVR group", category=experimental
→ 2. name="guided video group", category=active_control
→ 3. name="nonintervention control group", category=passive_control
```

### 4. Participant Age

Extract all available age information:

- **Mean age**: Average age of participants (if reported)
- **Standard deviation**: SD of age (if reported)
- **Age range**: Minimum and maximum ages (if reported)
- **Unit**: Typically "years"

**Examples:**

```
Methods: "Participants between the ages 10 and 15"
→ age_mean: null, age_sd: null, age_range: [10, 15], unit: "years"

Results: "The mean age was 15.5 years (SD = 2.3)"
→ age_mean: 15.5, age_sd: 2.3, age_range: [null, null], unit: "years"

Methods: "Adult participants (M = 34.2, SD = 8.1, range: 21-58 years)"
→ age_mean: 34.2, age_sd: 8.1, age_range: [21, 58], unit: "years"
```

## Important Instructions

1. **Extract exactly what you see**: Do not infer country from author names alone
2. **Map arms carefully**: Use the definitions provided to categorize each condition
3. **Report all arms**: Include every condition mentioned in the study
4. **Handle missing values**: Use `null` for unreported numerical values
5. **Preserve original naming**: Use the authors' exact names for study arms
6. **Do not convert units**: Report ages in the units provided by authors
7. **Be conservative**: If status or category is ambiguous, choose "unclear" or ask in a note

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
  "arms": [
    {
      "name": "Arm name as stated by authors",
      "category": "experimental" | "active_control" | "waitlist" | "passive_control",
      "pages": [page_number, ...],
      "quotes": ["Exact text from document", ...]
    },
    ...
  ],
  "age": {
    "mean": number or null,
    "sd": number or null,
    "range": [min or null, max or null],
    "unit": "years",
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  }
}
```

**Important**:
- Each field must have matching lengths for `pages` and `quotes` arrays
- Include all supporting evidence, even if the same information appears multiple times

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
  "arms": [
    {
      "name": "SPARX game intervention",
      "category": "experimental",
      "pages": [4, 5],
      "quotes": [
        "Participants randomized to the SPARX game intervention completed seven modules",
        "The SPARX group received weekly gaming sessions"
      ]
    },
    {
      "name": "treatment as usual",
      "category": "active_control",
      "pages": [4],
      "quotes": [
        "The control group received treatment as usual from their primary care provider"
      ]
    }
  ],
  "age": {
    "mean": 14.5,
    "sd": 1.8,
    "range": [12, 17],
    "unit": "years",
    "pages": [1, 5],
    "quotes": [
      "adolescents aged 12-17 years",
      "Participants aged 12-17 years (M = 14.5, SD = 1.8)"
    ]
  }
}
```

## Begin Extraction

Please analyze the provided PDF document and extract the study information according to the specifications above.
