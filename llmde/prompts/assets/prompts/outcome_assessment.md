# Outcome Assessment Extraction

## Task

Extract information about the primary mental health outcomes the intervention targeted and the instruments used to measure these outcomes from this scientific paper.

## Required Information

You must extract the following elements from the document:

1. **Outcome Targeted**: Which mental health construct(s) the intervention aimed to change (anxiety, depression, or both)
2. **Assessment Instruments**: The primary/co-primary instruments used to measure each targeted outcome

## Where to Find This Information

**Important**: The locations listed below are **typical** places where information appears. However, you must **read carefully and thoroughly through the entire document** to ensure you locate all required information, as it may appear in unexpected sections or across multiple pages.

### Outcome Targeted
- **Typical locations**: Introduction (hypotheses/aims), Methods (Objectives/Aims/Hypotheses/Outcomes), Abstract (Objectives/Primary outcome), Trial registration information
- **Key indicators**: "primary outcome", "primary endpoint", "co-primary outcomes", "aimed to reduce", "hypothesized to decrease", "main objective"

### Assessment Instruments
- **Typical locations**: Methods (Measures/Assessments/Outcomes/Endpoints), Statistical Analysis (primary endpoint/analysis plan)
- **Key indicators**: "measured with", "assessed using", "primary measure", "co-primary", instrument abbreviations (e.g., PHQ-9, GAD-7, STAI, BDI)

## Detailed Field Definitions

### 1. Outcome Targeted

**Task**: Which mental health outcome(s) did the intervention explicitly aim to change as the primary intention (choose anxiety, depression, or both), based on objectives/hypotheses/sample-size endpoint/registered primary outcome?

**Allowed values:** [`anxiety`, `depression`] (both may be selected)

**Definition**:
- **Outcome targeted**: The mental health construct(s) the intervention was intended to modify as its main aim, as indicated by primary objective/hypothesis, primary endpoint, or sample size calculation

**Search Strategy**:
1. **First priority**: Look for anxiety, depression, or both listed as **primary outcomes**
2. **Second priority**: If no primary outcomes specified, look at **secondary outcomes**
3. **Third priority**: If outcomes not explicitly categorized, look at **study aims/hypotheses**

**Classification Rules**:
- If study has one primary outcome (anxiety OR depression): return that single outcome
- If study has co-primary outcomes (anxiety AND depression): return both
- If study targets both but one is primary and one is secondary: return only the primary
- If study has neither anxiety nor depression as outcomes: this should not occur in the dataset, but note in extraction

**Examples:**

```
Methods/Introduction → Objectives: "We aimed to test whether the intervention reduces anxiety."
→ value: [{"category": "anxiety"}]

Methods → Outcomes: "Co-primary outcomes were depression and anxiety at 12 weeks."
→ value: [{"category": "anxiety"}, {"category": "depression"}]

Methods: "The primary outcome will be self-reported depression severity"
→ value: [{"category": "depression"}]

Abstract: "Primary outcome: anxiety symptoms. Secondary outcomes: depression, quality of life."
→ value: [{"category": "anxiety"}]
```

### 2. Assessment Instruments

**Task**: List each instrument used to measure the targeted outcome(s), mapping instrument name(s) to outcome category (anxiety or depression).

**Filtering Rule**: If several instruments measure the same targeted construct, include **only** the instrument(s) explicitly designated as the **primary/co-primary measure(s)** of that construct (regardless of section/category) and **exclude all others**.

**Allowed values for category:** [`anxiety`, `depression`]

**Mapping Instructions**:
1. Identify which instruments measure which constructs (anxiety vs depression)
2. For each targeted outcome, identify the primary/co-primary instrument(s)
3. Exclude secondary or exploratory instruments
4. Create name-category pairs for each primary instrument

**Common Instruments**:
- **Anxiety**: GAD-7, STAI (State-Trait Anxiety Inventory), SCARED, MASC, BAI, HAMA
- **Depression**: PHQ-9, BDI/BDI-II, CES-D, MADRS, HAMD, CDI
- **Both**: HADS (has anxiety and depression subscales)

**Examples:**

```
Methods: "Depression was assessed with the PHQ-9 (primary) and BDI-II (secondary)."
→ Include only: [{"name": "PHQ-9", "category": "depression"}]
→ Exclude: BDI-II (secondary)

Methods: "Primary outcomes were anxiety (GAD-7) and depression (PHQ-9)."
→ Include: [{"name": "GAD-7", "category": "anxiety"}, {"name": "PHQ-9", "category": "depression"}]

Statistical Analysis: "Primary endpoint was change in PHQ-9 at week 12."
Methods: "Depression was assessed using PHQ-9 and BDI-II."
→ Include only: [{"name": "PHQ-9", "category": "depression"}]
→ Exclude: BDI-II (not specified as primary)

Methods: "The primary outcome was anxiety measured by STAI-State. Depression was assessed with BDI-II as a secondary outcome."
→ Include only: [{"name": "STAI", "category": "anxiety"}]
→ Exclude: BDI-II (secondary outcome, depression not a targeted primary outcome)

Methods: "Co-primary outcomes were HADS-Anxiety and HADS-Depression subscales."
→ Include: [{"name": "HADS-Anxiety", "category": "anxiety"}, {"name": "HADS-Depression", "category": "depression"}]
```

## Important Instructions

1. **Prioritize primary over secondary**: Only include primary or co-primary outcomes and instruments
2. **Map instruments to constructs carefully**: Ensure each instrument is correctly mapped to anxiety or depression
3. **Use exact instrument names**: Use the abbreviation or name as stated by the authors (e.g., "GAD-7", not "Generalized Anxiety Disorder scale")
4. **Handle subscales appropriately**: For instruments with subscales (e.g., HADS), include the subscale specification if that's how authors report it
5. **Match instruments to targeted outcomes**: Only include instruments that measure the targeted outcome(s)
6. **Extract exactly what you see**: Do not infer instruments or outcomes not explicitly stated
7. **One instrument per construct**: If multiple instruments measure the same construct, only include the one(s) designated as primary
8. **Check multiple sections**: Primary outcome designation may appear in different sections (Objectives, Outcomes, Statistical Analysis, Trial Registration)

## Source Citation Requirements

For each piece of information you extract, you must provide **exhaustive and thorough citations**:

1. **Page numbers**: A list of **ALL** page numbers where information supporting your extraction was found
2. **Quotes**: A list of **ALL** direct quotes from the document that you used to build the extracted information

**Critical Requirements**:
- **Be exhaustive**: Include every single quote and page that contributed to your answer
- **One-to-one correspondence**: The number of quotes must exactly match the number of pages
- **Direct quotes only**: Copy text exactly as it appears in the document
- **No omissions**: Even if information seems obvious or redundant, include all supporting evidence
- **For instrument mapping**: Include quotes showing both the instrument name AND its primary status

## Output Format

Return your response as a JSON object with the following structure:

```json
{
  "outcome_targeted": {
    "value": [
      {"category": "anxiety" | "depression"},
      ...
    ],
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "assessment_instruments": {
    "value": [
      {
        "name": "Instrument abbreviation or name",
        "category": "anxiety" | "depression"
      },
      ...
    ],
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  }
}
```

**Important**:
- Each field must have matching lengths for `pages` and `quotes` arrays
- Include all supporting evidence, even if the same information appears multiple times
- For outcome_targeted: value array length determines if one or both outcomes targeted
- For assessment_instruments: value array contains one object per primary instrument

### Example Output

**Example 1: Single outcome (depression only)**

```json
{
  "outcome_targeted": {
    "value": [
      {"category": "depression"}
    ],
    "pages": [1, 4],
    "quotes": [
      "The primary aim was to reduce depressive symptoms in adolescents",
      "Primary outcome: change in depression severity at 8 weeks"
    ]
  },
  "assessment_instruments": {
    "value": [
      {
        "name": "PHQ-9",
        "category": "depression"
      }
    ],
    "pages": [4, 6],
    "quotes": [
      "The primary outcome was depression severity measured with the Patient Health Questionnaire-9 (PHQ-9)",
      "Primary endpoint analysis used change in PHQ-9 total score"
    ]
  }
}
```

**Example 2: Co-primary outcomes (both anxiety and depression)**

```json
{
  "outcome_targeted": {
    "value": [
      {"category": "anxiety"},
      {"category": "depression"}
    ],
    "pages": [3],
    "quotes": [
      "Co-primary outcomes were anxiety and depression symptoms at 12 weeks"
    ]
  },
  "assessment_instruments": {
    "value": [
      {
        "name": "GAD-7",
        "category": "anxiety"
      },
      {
        "name": "PHQ-9",
        "category": "depression"
      }
    ],
    "pages": [5, 5],
    "quotes": [
      "Anxiety was assessed using the Generalized Anxiety Disorder-7 (GAD-7) scale",
      "Depression was measured with the Patient Health Questionnaire-9 (PHQ-9)"
    ]
  }
}
```

**Example 3: Multiple instruments with primary designation**

```json
{
  "outcome_targeted": {
    "value": [
      {"category": "anxiety"}
    ],
    "pages": [2, 5],
    "quotes": [
      "The primary objective was to evaluate the intervention's effect on anxiety symptoms",
      "Primary outcome: anxiety severity at 6 weeks post-intervention"
    ]
  },
  "assessment_instruments": {
    "value": [
      {
        "name": "STAI",
        "category": "anxiety"
      }
    ],
    "pages": [5, 8],
    "quotes": [
      "Anxiety was measured using the State-Trait Anxiety Inventory (STAI; primary outcome) and the Revised Children's Anxiety and Depression Scale (RCADS; secondary)",
      "The primary endpoint analysis examined change in STAI-State scores"
    ]
  }
}
```

## Begin Extraction

Please analyze the provided PDF document and extract the outcome assessment information according to the specifications above.
