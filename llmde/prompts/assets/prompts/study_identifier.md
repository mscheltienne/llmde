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

While bibliographic information is **typically located on the first page** of the article (in the header, title section, author byline, citation information, or metadata section), you must **read carefully and thoroughly through the entire document** to locate all required information.

**Important**: Do not limit your search to the first page. Information may appear on:
- Later pages (e.g., running headers, footers)
- Copyright or publication information pages
- Cover pages or title pages in preprints
- Author information sections
- Supplementary material headers

Read the complete document systematically to ensure you find all bibliographic elements, even if they appear in unexpected locations.

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

For each piece of information you extract, you must provide **exhaustive and thorough citations**:

1. **Page numbers**: A list of **ALL** page numbers where information supporting your extraction was found
2. **Quotes**: A list of **ALL** direct quotes from the document that you used to build the extracted information

**Critical Requirements**:
- **Be exhaustive**: Include every single quote and page that contributed to your answer
- **One-to-one correspondence**: The number of quotes must exactly match the number of pages
- **Direct quotes only**: Copy text exactly as it appears in the document
- **No omissions**: Even if information seems obvious or redundant, include all supporting evidence

### Example Source Citations

- For journal found in multiple locations:
  - Pages: `[1, 2]`
  - Quotes: `["Journal of Affective Disorders 191 (2016) 153–158", "J Affect Disord. 2016"]`

- For DOI found once:
  - Pages: `[1]`
  - Quotes: `["https://doi.org/10.1016/j.jad.2016.05.002"]`

## Output Format

Return your response as a JSON object with the following structure:

```json
{
  "title": {
    "value": "Complete article title as it appears in the document",
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "authors": {
    "value": ["LastName, Initials", "LastName, Initials", ...],
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "year": {
    "value": YYYY,
    "pages": [page_number, ...],
    "quotes": ["Exact text from document", ...]
  },
  "journal": {
    "value": "Journal Name" or null,
    "pages": [page_number, ...] or null,
    "quotes": ["Exact text from document", ...] or null
  },
  "doi": {
    "value": "DOI identifier" or null,
    "pages": [page_number, ...] or null,
    "quotes": ["Exact text from document", ...] or null
  }
}
```

**Important**:
- Each field must have matching lengths for `pages` and `quotes` arrays
- Use `null` for the entire field structure if information is not found in the document
- Include all supporting evidence, even if the same information appears multiple times

### Example Output

```json
{
  "title": {
    "value": "Effects of a video game intervention on symptoms, training motivation, and visuo-spatial memory in depression",
    "pages": [1],
    "quotes": ["Effects of a video game intervention on symptoms, training motivation, and visuo-spatial memory in depression"]
  },
  "authors": {
    "value": ["Scholten, H", "Malmberg, M", "Lobel, A", "Engels, RCME", "Granic, I"],
    "pages": [1],
    "quotes": ["Hanneke Scholten1*, Monique Malmberg1, Adam Lobel1, Rutger C. M. E. Engels1,2, Isabela Granic1"]
  },
  "year": {
    "value": 2016,
    "pages": [1],
    "quotes": ["Journal of Affective Disorders 191 (2016) 153–158"]
  },
  "journal": {
    "value": "Journal of Affective Disorders",
    "pages": [1, 2],
    "quotes": ["Journal of Affective Disorders 191 (2016) 153–158", "J Affect Disord."]
  },
  "doi": {
    "value": "10.1016/j.jad.2016.05.002",
    "pages": [1],
    "quotes": ["https://doi.org/10.1016/j.jad.2016.05.002"]
  }
}
```

## Begin Extraction

Please analyze the provided PDF document and extract the study identification information according to the specifications above.
