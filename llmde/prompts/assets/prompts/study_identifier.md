# Study Identification Extraction

## Task

Extract the complete bibliographic information from this scientific paper to uniquely identify the study.

## Required Information

You must extract the following elements from the document:

1. **Study Title**: The full title of the research article
2. **Authors**: Complete list of all authors in the exact order they appear
3. **Publication Year**: The year the article was published (4-digit format: YYYY)
4. **Journal**: The name of the journal where the article was published
5. **DOI**: The Digital Object Identifier for the article

## Where to Find This Information

All required information is typically located on the **first page** of the article, specifically:
- In the article header or title section
- In the author byline (immediately below the title)
- In the citation information (footer or header of the first page)
- In the article metadata section

## Author Name Format

Authors should be extracted in the format: **Last Name, Initials** (e.g., "Scholten, H" or "Pedrelli, P")

### Examples of Author Extraction

**Example 1:**
```
Source text: "Hanneke Scholten1*, Monique Malmberg1, Adam Lobel1, Rutger C. M. E. Engels1,2, Isabela Granic1"

Extracted: ["Scholten, H", "Malmberg, M", "Lobel, A", "Engels, RCME", "Granic, I"]
```

**Example 2:**
```
Source text: "Shai-Lee Yatziv1, PhD; Paola Pedrelli2,3, PhD; Shira Baror1, PhD; Sydney Ann DeCaro2, MA; Noam Shachar1, MA; Bar Sofer1, MA; Sunday Hull4, BA; Joshua Curtiss2, PhD; Moshe Bar1, PhD"

Extracted: ["Yatziv, S-L", "Pedrelli, P", "Baror, S", "DeCaro, SA", "Shachar, N", "Sofer, B", "Hull, S", "Curtiss, J", "Bar, M"]
```

## Important Instructions

1. **Extract exactly what you see**: Do not infer, modify, or correct any information
2. **Include all authors**: Do not truncate the author list with "et al." - extract every single author
3. **Preserve name formatting**: Keep hyphens in hyphenated names, preserve middle initials
4. **Handle missing information**: If journal or DOI information is not present in the document, use `null`
5. **Year format**: Always use 4-digit year format (YYYY)
6. **Do not hallucinate**: If you cannot find specific information clearly stated in the document, use `null` rather than guessing

## Source Citation Requirements

For each piece of information you extract, you must provide:

1. **Page number**: The page number where the information was found (e.g., 1, 2, 3)
2. **Quote**: A direct quote from the document showing where the information appears (when applicable)

**Note**: For **title**, **authors**, and **year**, quotes are typically not necessary as these are obvious from the article header. However, for **journal** and **DOI**, provide the exact text where you found this information.

### Example Source Citations

- For journal: `"Journal of Affective Disorders"` (found on page 1)
- For DOI: `"https://doi.org/10.1016/j.jad.2016.05.002"` (found on page 1)

## Output Format

Return your response as a JSON object with the following structure:

```json
{
  "title": "Complete article title as it appears in the document",
  "authors": ["LastName, Initials", "LastName, Initials", ...],
  "year": YYYY,
  "journal": {
    "value": "Journal Name" or null,
    "page": page_number or null,
    "quote": "Exact text from document" or null
  },
  "doi": {
    "value": "DOI identifier" or null,
    "page": page_number or null,
    "quote": "Exact text from document" or null
  }
}
```

### Example Output

```json
{
  "title": "Effects of a video game intervention on symptoms, training motivation, and visuo-spatial memory in depression",
  "authors": ["Scholten, H", "Malmberg, M", "Lobel, A", "Engels, RCME", "Granic, I"],
  "year": 2016,
  "journal": {
    "value": "Journal of Affective Disorders",
    "page": 1,
    "quote": "Journal of Affective Disorders 191 (2016) 153–158"
  },
  "doi": {
    "value": "10.1016/j.jad.2016.05.002",
    "page": 1,
    "quote": "https://doi.org/10.1016/j.jad.2016.05.002"
  }
}
```

## Begin Extraction

Please analyze the provided PDF document and extract the study identification information according to the specifications above.
