# PEDro Scale Methodological Quality Assessment

## Task

Assess the methodological quality of this randomized controlled trial (RCT) using the PEDro scale. You must evaluate all 11 criteria and compute the total PEDro score.

## Important Rating Principles

1. **Award points only when CLEARLY satisfied**: If there is any doubt on a literal reading, do NOT award the point
2. **Rate the report, not the study**: Assess what is written, not what may have been done
3. **Binary judgments only**: Each criterion is either satisfied (1) or not satisfied (0)
4. **Provide exhaustive evidence**: Document every decision with exact quotes and page numbers

## The 11 PEDro Criteria

---

### Criterion 1: Eligibility Criteria Specified

**Does NOT count toward total score** (assesses external validity)

#### Definition

This criterion is satisfied if the report describes the **source of subjects** AND a **list of criteria** used to determine who was eligible to participate in the study.

#### What to Look For

- Inclusion criteria (characteristics required for participation)
- Exclusion criteria (characteristics that prevented participation)
- Source/recruitment setting (hospital, clinic, community, etc.)

#### Where to Find This Information

- **Typical locations**: Abstract, Methods (Participants/Subjects section)
- **Key indicators**: "inclusion criteria," "exclusion criteria," "eligible if," "recruited from"

#### Examples

**Satisfies criterion (value = 1)**:
```
Method: "Fulfilling DSM-IV criteria for ADHD; age between 6 and 13 years; access to
a computer and internet connection and informed consent obtained."
```

```
Method: "Exclusion criteria were: 1) evidence of a pervasive developmental disorder
based on previous diagnosis; 2) the child or parent presented with emergency
psychiatric needs; 3) estimated Full Scale IQ below 80."
```

**Does NOT satisfy criterion (value = 0)**:
```
Method: "Participants were recruited for the study."
→ No specific criteria listed
```

---

### Criterion 2: Random Allocation

**Counts toward total score**

#### Definition

A study is considered to have used random allocation if the report **states that allocation was random**. The precise method of randomization need not be specified.

#### What Qualifies as Random

- Computer-generated random sequence
- Random number table
- Coin tossing, dice rolling
- Drawing lots
- Minimization with random element
- Simply stating "randomly assigned" or "randomly allocated"

#### What Does NOT Qualify (Quasi-Randomization)

- Alternation (every other patient)
- Hospital record number
- Birth date (odd/even days)
- Day of week of admission
- Order of recruitment
- Assignment based on clinical profile or diagnosis

#### Where to Find This Information

- **Typical locations**: Abstract, Methods (Randomization/Study Design section)
- **Key indicators**: "randomly assigned," "randomly allocated," "randomized," "randomization"

#### Examples

**Satisfies criterion (value = 1)**:
```
Method: "randomly assigned using a computer-generated sequence"
```

```
Method: "randomly assigned" or "randomly allocated"
```

```
Method: "A minimization method of randomization was performed to allocate the
participants through the QMinim service."
```

**Does NOT satisfy criterion (value = 0)**:
```
Abstract: "children with ADHD and typically developing children were recruited"
→ Assigned to groups based on clinical profile = quasi-randomization
```

```
Method: "Patients were allocated alternately to treatment and control groups"
→ Alternation is quasi-randomization
```

---

### Criterion 3: Concealed Allocation

**Counts toward total score**

#### Definition

Concealed allocation means that the person who determined if a subject was eligible for inclusion in the trial was **unaware, when this decision was made**, of which group the subject would be allocated to.

#### What Qualifies as Concealed Allocation

A point is awarded even if "concealed allocation" is not explicitly stated, when the report describes mechanisms that prevent foreknowledge of group assignment.

**Traditional Concealment Mechanisms:**
- Sealed opaque envelopes
- Central/off-site randomization service
- Contacting the holder of the allocation schedule who was "off-site"
- Sequentially numbered, opaque, sealed containers
- Third party handling allocation

**Modern Algorithmic Concealment:**

The PEDro scale was developed in 2003 when physical concealment was standard. Today, many studies use computerized randomization systems that inherently provide concealment through **real-time algorithmic allocation**. When allocation is determined at the moment of enrollment (not from a pre-generated list), the person enrolling cannot predict or access the allocation beforehand.

**Systems that provide inherent concealment** (when allocation is real-time):
- **REDCap** randomization module
- **Castor EDC** randomization
- **Sealed Envelope** (online randomization service)
- **Randomizer** / **Research Randomizer**
- **Randomization.com**
- **StudyRandomizer**
- **MinimPy** / **QMinim** (minimization software)
- **SAS PROC PLAN** (when used for real-time allocation)
- **R packages** (blockrand, randomizeR) when integrated into enrollment systems
- Custom web-based randomization systems with real-time allocation

**Key distinction:**
- **Pre-allocated lists** (even if computer-generated): List exists before enrollment, could be accessed → additional concealment mechanism needed
- **Real-time algorithmic randomization**: Allocation determined only at enrollment → inherently concealed if algorithm is not predictable

#### What Does NOT Qualify

- Simply stating "randomized" without describing the mechanism
- Transparent envelopes
- Open allocation lists
- Pre-generated randomization lists without additional protection
- No mention of how allocation was protected

#### Where to Find This Information

- **Typical locations**: Methods (Randomization/Allocation section)
- **Key indicators**: "concealed," "sealed envelopes," "central randomization," "off-site," "blinded allocation," names of randomization software/platforms

#### Examples

**Satisfies criterion (value = 1)**:

*Traditional concealment:*
```
Method: "Random allocation was handled by SR, with all other researchers, the
participant and their parents being blind to condition membership"
```

```
Method: "A randomized, blinded list of numbers associated with the CDs containing
the treatment or comparison program was sent to each clinical center."
```

```
Method: "Matching was performed by an experimenter not involved in testing."
```

*Modern algorithmic concealment:*
```
Method: "Randomization was performed using REDCap's randomization module at the
time of enrollment."
→ Real-time algorithmic allocation = inherently concealed
```

```
Method: "Participants were randomized via the Castor EDC platform immediately
following baseline assessment."
→ Real-time web-based allocation = inherently concealed
```

```
Method: "A minimization method of randomization was performed to allocate the
participants through the QMinim service."
→ Real-time minimization algorithm = inherently concealed
```

```
Method: "Group assignment was determined by the StudyRandomizer online system
at the point of enrollment."
→ Real-time online randomization = inherently concealed
```

**Does NOT satisfy criterion (value = 0)**:
```
Method: "Participants were randomly assigned to groups"
→ No description of concealment mechanism
```

```
Method: "A randomization list was generated using Excel before the study began"
→ Pre-generated list could be accessed = concealment not demonstrated
```

```
Method: "The research assistant used a pre-prepared randomization schedule"
→ Pre-allocated list without description of how it was protected
```

---

### Criterion 4: Groups Similar at Baseline

**Counts toward total score**

#### Definition

At a minimum, in studies of therapeutic interventions, the report must describe at least one measure of the **severity of the condition being treated** AND/OR at least one **key outcome measure at baseline**. The groups' outcomes would not be expected to differ, on the basis of baseline differences in prognostic variables alone, by a clinically significant amount.

#### What Qualifies

- Statistical tests showing no significant baseline differences
- Tables showing comparable baseline characteristics
- ANCOVA or similar analysis controlling for baseline as covariate
- Explicit statement of baseline equivalence

This criterion is satisfied even if only baseline data of study completers are presented.

#### Where to Find This Information

- **Typical locations**: Results (Baseline Characteristics), Tables
- **Key indicators**: "no significant differences at baseline," "groups were comparable," "baseline characteristics," demographic tables

#### Examples

**Satisfies criterion (value = 1)**:
```
Results: "Statistical analysis does not show any significant difference between the
groups at baseline or pretest"
```

```
Results: "We conducted a MANOVA with the performance of each task at baseline,
and results showed no group differences in all tested abilities at pretraining"
```

```
Results: "after taking into account baseline performance" [ANCOVA]
```

**Does NOT satisfy criterion (value = 0)**:
```
Results: "Table 1 shows participant demographics"
→ Demographics shown but no comparison or statement of equivalence
```

```
Results: "Groups differed significantly on baseline anxiety scores (p = .02)"
→ Significant baseline difference reported
```

---

### Criterion 5: Subject Blinding

**Counts toward total score**

#### Definition

Blinding means the subjects did not know which group they had been allocated to. In addition, subjects are only considered "blind" if it could be expected that they **would have been unable to distinguish** between the treatments applied to different groups.

#### Important Considerations

- In many behavioral or exercise interventions, true subject blinding may be impossible
- Placebo/sham interventions can enable subject blinding
- "Double-blind" typically implies subject blinding

#### Where to Find This Information

- **Typical locations**: Methods (Blinding section, Study Design)
- **Key indicators**: "blind," "blinded," "masked," "double-blind," "participants were unaware"

#### Examples

**Satisfies criterion (value = 1)**:
```
Method: "parent, and child were all blinded to child group status until after the
follow-up assessment"
```

```
Method: "double-blind"
```

```
Method: "Children and teachers were blind to whether their class was receiving
Tali Train or the placebo"
```

**Does NOT satisfy criterion (value = 0)**:
```
Method: "Participants knew which intervention they were receiving"
→ Explicitly not blinded
```

```
Method: "The experimental group received the video game intervention while the
control group continued with standard care"
→ Different interventions that subjects could distinguish
```

---

### Criterion 6: Therapist Blinding

**Counts toward total score**

#### Definition

Blinding means the therapists (person administering the intervention) did not know which group subjects had been allocated to. Therapists are only considered "blind" if it could be expected that they **would have been unable to distinguish** between the treatments applied to different groups.

#### Who Counts as "Therapist"

The person in charge of delivering or following the intervention:
- Teachers (in educational interventions)
- Coaches (in exercise interventions)
- Researchers administering treatment
- Clinicians providing therapy
- Study staff supervising sessions

#### Where to Find This Information

- **Typical locations**: Methods (Blinding section), Results
- **Key indicators**: "therapists were blind," "interventionists were masked," "double-blind"

#### Examples

**Satisfies criterion (value = 1)**:
```
Method: "Researchers collecting data were blinded to condition assignment."
```

```
Method: "both the participants and researchers remained blind to the condition
assigned to the participant"
```

**Does NOT satisfy criterion (value = 0)**:
```
Method: "The researcher administered the game intervention to the experimental
group and provided standard worksheets to the control group"
→ Researcher knew which intervention they were delivering
```

---

### Criterion 7: Assessor Blinding

**Counts toward total score**

#### Definition

Blinding means the assessors (those who measured outcomes) did not know which group subjects had been allocated to.

#### Special Rule for Self-Reported Outcomes

In trials where key outcomes are **self-reported** (e.g., visual analog scale, pain diary, questionnaires), the assessor is considered blind **if the subject was blind**.

#### Where to Find This Information

- **Typical locations**: Methods (Blinding section, Outcome Assessment), Results
- **Key indicators**: "assessors were blind," "outcome evaluators were masked," "double-blind," "blinded assessment"

#### Examples

**Satisfies criterion (value = 1)**:
```
Results: "Researchers collecting data were blinded to condition assignment."
```

```
Results: "the psychologists administrating pre- and post-training tests were blinded"
```

```
Method: "double-blind"
```

**Does NOT satisfy criterion (value = 0)**:
```
Method: "Outcomes were assessed by the study coordinator who also managed
group assignments"
→ Same person knew allocation and assessed outcomes
```

---

### Criterion 8: Adequate Follow-Up (>85% Retention)

**Counts toward total score**

#### Definition

This criterion is satisfied only if the report **explicitly states BOTH**:
1. The number of subjects initially allocated to groups
2. The number of subjects from whom key outcome measures were obtained

A key outcome must have been measured in **more than 85%** of subjects at one of those time points.

#### Calculation

Retention rate = (Subjects with outcome data / Subjects initially allocated) × 100

If retention rate > 85%, criterion is satisfied.

#### Where to Find This Information

- **Typical locations**: Methods (Participants), Results, CONSORT/PRISMA flow diagrams, Tables
- **Key indicators**: Flow diagrams, "N = X enrolled," "N = Y completed," attrition numbers

#### Examples

**Satisfies criterion (value = 1)**:
```
Method: "Figure 1. CONSORT flow diagram."
[showing 100 allocated, 92 completed = 92% retention]
```

```
Abstract: "Eight classes (n = 98 children) were cluster randomized"
Results: "A total of 98 children were included in the analysis."
[98/98 = 100% retention]
```

**Does NOT satisfy criterion (value = 0)**:
```
Method: "Participants were recruited and randomized"
Results: "Analysis included participants who completed all assessments"
→ Numbers not explicitly stated for both allocation and completion
```

```
Results: "Of 100 participants enrolled, 75 completed the study"
→ 75% retention < 85% threshold
```

---

### Criterion 9: Intention-to-Treat Analysis

**Counts toward total score**

#### Definition

An intention-to-treat analysis means that, where subjects did not receive treatment (or control condition) as allocated, and where measures of outcomes were available, the analysis was performed **as if subjects received the treatment they were allocated to**.

#### Important Clarification

This criterion is satisfied, even if there is no explicit mention of "intention to treat," if the report states that **all subjects received treatment or control conditions as allocated** (i.e., no crossovers or protocol deviations occurred).

#### Where to Find This Information

- **Typical locations**: Methods (Statistical Analysis), Results
- **Key indicators**: "intention to treat," "ITT," "analyzed as randomized," "all participants received allocated treatment"

#### Examples

**Satisfies criterion (value = 1)**:
```
Method: "Analysis was conducted on an intention-to-treat basis"
```

```
Results: "All participants completed the intervention as assigned to their
randomized group"
→ No protocol deviations, so ITT is implicit
```

**Does NOT satisfy criterion (value = 0)**:
```
Method: "Per-protocol analysis was conducted"
→ Not ITT
```

```
Results: "Five participants crossed over to the other treatment arm and were
analyzed according to treatment received"
→ Analyzed as treated, not as randomized
```

---

### Criterion 10: Between-Group Statistical Comparisons

**Counts toward total score**

#### Definition

A between-group statistical comparison involves statistical comparison of one group with another. This may include:

- Comparison of two or more treatments
- Comparison of treatment with a control condition
- Simple comparison of post-treatment outcomes
- Comparison of change scores (often reported as Group × Time interaction)

#### What Qualifies

The comparison may be reported as:
- **Hypothesis testing**: p-value describing probability groups differed by chance
- **Effect estimate**: Mean/median difference, difference in proportions, number needed to treat, relative risk, hazard ratio, AND its confidence interval

#### Where to Find This Information

- **Typical locations**: Results, Intervention Effects section
- **Key indicators**: "group effect," "between-group difference," "Group × Time interaction," p-values, F-statistics with group factor

#### Examples

**Satisfies criterion (value = 1)**:
```
Results: "Teacher-rated hyperactivity significantly declined in the Tali Train
and no-contact control conditions from baseline to posttraining (p < .001)"
```

```
Results: "We did not find any reliable group differences in posttest gains,
F(2, 56) = 0.23, p = .799."
```

```
Results: "A 3 (Group) × 3 (Time) ANOVA revealed a main effect of group,
F(2,57) = 12.68, p < .001"
```

**Does NOT satisfy criterion (value = 0)**:
```
Results: "The experimental group improved significantly from pre to post (p < .01)"
→ Within-group comparison only, no between-group test
```

---

### Criterion 11: Point Measures and Measures of Variability

**Counts toward total score**

#### Definition

A **point measure** is a measure of the size of the treatment effect (difference in outcomes or outcome in each group).

**Measures of variability** include:
- Standard deviations (SD)
- Standard errors (SE)
- Confidence intervals (CI)
- Interquartile ranges (IQR)
- Ranges

#### What Qualifies

- Point measures and/or variability may be provided **graphically** (e.g., error bars) as long as it is clear what is being graphed
- For **categorical outcomes**: the number of subjects in each category for each group satisfies this criterion

#### Where to Find This Information

- **Typical locations**: Results, Tables, Figures, Supplements
- **Key indicators**: "M =," "SD =," "SE =," "95% CI," tables with means and SDs, error bars

#### Examples

**Satisfies criterion (value = 1)**:
```
Tables: "Means (and standard deviations) of assessment tests across three time stages."
```

```
Results: "Mean scores and standard errors for the outcome measures at each time
point are presented in Table 2"
```

```
Figure: [Graph showing means with error bars labeled as "±1 SD"]
```

**Does NOT satisfy criterion (value = 0)**:
```
Results: "The intervention group showed significant improvement (p < .05)"
→ p-value only, no means or variability
```

```
Results: "Effect size was d = 0.45"
→ Effect size without point measures or variability
```

---

## Source Citation Requirements

For each criterion you evaluate, you must provide **exhaustive and thorough citations**:

### When Criterion IS Satisfied (value = 1)

1. **Page numbers**: A list of **ALL** page numbers where supporting evidence was found
2. **Quotes**: A list of **ALL** direct quotes that demonstrate the criterion is met

### When Criterion is NOT Satisfied (value = 0)

Provide one of the following:

1. **Disqualifying evidence**: If text explicitly contradicts the criterion (e.g., "quasi-randomization," "not blinded"), provide:
   - Page numbers where disqualifying text appears
   - Quotes showing why criterion fails
   - Rationale explaining the disqualification

2. **Not reported**: If no relevant information exists:
   - Set pages and quotes to `null`
   - Provide rationale: "Not reported" or more specific explanation

### Critical Requirements

- **Be exhaustive**: Include every quote and page that informed your decision
- **One-to-one correspondence**: Number of quotes must exactly match number of pages
- **Direct quotes only**: Copy text exactly as it appears in the document
- **JSON escaping for quotes**: Since quotes are embedded in a JSON string, any double-quote characters (`"`) within the quoted text must be escaped as `\"`. This is standard JSON encoding and is **not** considered a modification of the quote — JSON parsers will decode `\"` back to `"` when reading the output. For example, if the document contains: `The "primary" outcome was measured`, the JSON value should be: `"The \"primary\" outcome was measured"`
- **No omissions**: Include all supporting evidence, even if redundant

---

## Output Format

Return your response as a JSON object with the following structure:

```json
{
  "criterion_1": {
    "value": 1 or 0,
    "pages": [page_number, ...] or null,
    "quotes": ["Exact text from document", ...] or null,
    "rationale": "Explanation if value is 0" or null
  },
  "criterion_2": {
    "value": 1 or 0,
    "pages": [page_number, ...] or null,
    "quotes": ["Exact text from document", ...] or null,
    "rationale": "Explanation if value is 0" or null
  },
  "criterion_3": { ... },
  "criterion_4": { ... },
  "criterion_5": { ... },
  "criterion_6": { ... },
  "criterion_7": { ... },
  "criterion_8": { ... },
  "criterion_9": { ... },
  "criterion_10": { ... },
  "criterion_11": { ... },
  "pedro_score": {
    "total": integer (0-10),
    "max": 10,
    "items_satisfied": [list of criterion numbers that scored 1, excluding criterion 1],
    "note": "Criterion 1 assesses external validity and is not counted in the total score"
  }
}
```

### Field Specifications

- **value**: Integer, either `1` (criterion satisfied) or `0` (criterion not satisfied)
- **pages**: Array of integers (page numbers) when evidence exists, `null` when not reported
- **quotes**: Array of strings (exact quotes) when evidence exists, `null` when not reported
- **rationale**: String explaining why criterion is not satisfied (required when value = 0), `null` when value = 1
- **pedro_score.total**: Sum of values for criteria 2-11 only (criterion 1 excluded)
- **pedro_score.items_satisfied**: List of criterion numbers (2-11) that received a score of 1

### Example Output

```json
{
  "criterion_1": {
    "value": 1,
    "pages": [3],
    "quotes": ["Inclusion criteria: DSM-IV diagnosis of ADHD, age 6-13 years, access to computer and internet, informed consent obtained. Exclusion criteria: comorbid autism spectrum disorder, IQ below 80."],
    "rationale": null
  },
  "criterion_2": {
    "value": 1,
    "pages": [4],
    "quotes": ["Participants were randomly assigned to experimental or control conditions using a computer-generated random sequence."],
    "rationale": null
  },
  "criterion_3": {
    "value": 0,
    "pages": null,
    "quotes": null,
    "rationale": "Not reported. The paper describes random assignment but does not mention any mechanism to conceal allocation from those determining eligibility."
  },
  "criterion_4": {
    "value": 1,
    "pages": [5, 6],
    "quotes": ["Table 1 presents baseline characteristics by group.", "No significant differences were found between groups at baseline on any demographic or clinical measure (all p > .05)."],
    "rationale": null
  },
  "criterion_5": {
    "value": 0,
    "pages": [4],
    "quotes": ["The experimental group received the active video game intervention while the control group continued with treatment as usual."],
    "rationale": "Subjects could distinguish between receiving a video game intervention versus continuing usual treatment. True blinding was not possible given the nature of the intervention."
  },
  "criterion_6": {
    "value": 0,
    "pages": null,
    "quotes": null,
    "rationale": "Not reported. No mention of whether therapists or researchers administering the intervention were blinded."
  },
  "criterion_7": {
    "value": 1,
    "pages": [4],
    "quotes": ["Outcome assessors were blinded to group allocation throughout the study."],
    "rationale": null
  },
  "criterion_8": {
    "value": 1,
    "pages": [4, 7],
    "quotes": ["A total of 120 participants were randomized (60 per group).", "Complete outcome data were available for 112 participants (93.3%)."],
    "rationale": null
  },
  "criterion_9": {
    "value": 1,
    "pages": [5],
    "quotes": ["All analyses were conducted on an intention-to-treat basis, including all randomized participants regardless of protocol adherence."],
    "rationale": null
  },
  "criterion_10": {
    "value": 1,
    "pages": [7],
    "quotes": ["A 2 (Group: experimental vs. control) × 2 (Time: pre vs. post) mixed ANOVA revealed a significant Group × Time interaction, F(1, 110) = 15.32, p < .001, η²p = .12."],
    "rationale": null
  },
  "criterion_11": {
    "value": 1,
    "pages": [6],
    "quotes": ["Table 2 presents means and standard deviations for all outcome measures at pre-test and post-test by group."],
    "rationale": null
  },
  "pedro_score": {
    "total": 7,
    "max": 10,
    "items_satisfied": [2, 4, 7, 8, 9, 10, 11],
    "note": "Criterion 1 assesses external validity and is not counted in the total score"
  }
}
```

---

## Begin Assessment

Please analyze the provided PDF document and assess its methodological quality using all 11 PEDro criteria according to the specifications above. Remember:

1. Read the entire document carefully before rating
2. Apply the operational definitions strictly
3. Award points only when criteria are clearly satisfied
4. Document all evidence with exact quotes and page numbers
5. Compute the total PEDro score (criteria 2-11 only)
