# Requirements Document

## Introduction

This feature replaces the existing single-call Gemini classification pipeline with a Google Agent Development Kit (ADK) multi-agent architecture. The system processes academic PDF articles from the `artigos/` folder, extracting structured metadata, qualitative assessments, and thematic relationships through specialized agents (Reader, Classifier, Critic, Synthesizer). The goal is to reduce hallucinations and improve classification accuracy by decomposing the complex analysis task into focused agent responsibilities. The final output is a consolidated Excel spreadsheet (`classificacao_artigos.xlsx`) conforming to the course assignment specification.

## Glossary

- **Pipeline**: The end-to-end automated system that discovers articles, processes them through agents, and exports results to Excel.
- **Reader_Agent**: The ADK agent responsible for extracting raw text from PDF files and producing a structured super-summary.
- **Classifier_Agent**: The ADK agent responsible for extracting structured metadata (theme, year, venue, study type, nature) from the super-summary using Pydantic-validated output.
- **Critic_Agent**: The ADK agent responsible for qualitative rubric evaluation (quality, replicability, student adequacy, learning contribution, discipline alignment).
- **Synthesizer_Agent**: The ADK agent responsible for global cross-article thematic relationship analysis (overlap, continuity, complementation) after all individual articles are processed.
- **ADK_Orchestrator**: The top-level Google ADK orchestration component that coordinates the sequential execution of agents per article and the final synthesis pass.
- **Article_Folder**: A subdirectory within `artigos/` that represents a single article, expected to contain `info.md` and optionally `artigo.pdf`.
- **Super_Summary**: A condensed, structured textual representation of the PDF content produced by the Reader_Agent, serving as input for downstream agents.
- **Citation_Lookup_Service**: A web integration component that fetches real citation counts from CrossRef or Semantic Scholar APIs.
- **Classification_Schema**: The Pydantic model defining all structured fields that constitute a complete article classification (based on existing `ArtigoClassificado` model).
- **IFRD_Index**: A composite indicator derived from rubric scores (quality, replicability, applicability, theoretical contribution, adequacy, learning, alignment).

## Requirements

### Requirement 1: PDF Discovery and Filtering

**User Story:** As a researcher, I want the pipeline to automatically discover article folders and skip those without PDFs, so that only analyzable articles are processed.

#### Acceptance Criteria

1. WHEN the Pipeline is started, THE Pipeline SHALL recursively scan the `artigos/` directory up to 3 levels of nesting depth for folders containing an `info.md` file.
2. IF the `artigos/` directory does not exist or is empty, THEN THE Pipeline SHALL terminate with an error message indicating the directory was not found or contains no article folders.
3. WHEN an Article_Folder does not contain an `artigo.pdf` file, THE Pipeline SHALL exclude that article from processing and from the final Excel output.
4. WHEN an Article_Folder contains both `info.md` and `artigo.pdf`, THE Pipeline SHALL include that article in the set of articles to be processed by agents.
5. WHEN the Pipeline parses an `info.md` file, THE Pipeline SHALL extract the metadata fields title (H1 heading text), student (`Aluno` field), group (`Grupo` field), and link (`Link original` field) before initiating agent processing.
6. IF an `info.md` file is missing one or more of the required metadata fields (title, student, group, link), THEN THE Pipeline SHALL use an empty string as the default value for each missing field and continue processing the article.

### Requirement 2: PDF Text Extraction via Reader Agent

**User Story:** As a researcher, I want a dedicated agent to extract and summarize PDF content, so that downstream agents receive clean, focused input rather than raw truncated text.

#### Acceptance Criteria

1. WHEN an article is queued for processing, THE Reader_Agent SHALL extract full text from the `artigo.pdf` file using pypdf, normalizing whitespace by collapsing consecutive whitespace characters into a single space within each page.
2. WHEN the normalized extracted text exceeds 80,000 characters, THE Reader_Agent SHALL truncate the text to 80,000 characters measured from the beginning of the document.
3. WHEN text extraction succeeds, THE Reader_Agent SHALL send the extracted text to the Gemini API and produce a Super_Summary containing exactly four fields: `core_research_question` (single string), `methodology_description` (single string), `key_findings` (list of at least 1 and at most 10 strings), and `statistical_techniques` (list of 0 or more strings, empty list permitted when no statistical techniques are present in the article).
4. IF the PDF file is not found at the expected path, THEN THE Reader_Agent SHALL log a warning indicating the missing file path and return an empty extraction result, and the article SHALL proceed to classification with metadata-only context.
5. IF the PDF extraction fails due to corrupted, encrypted, or otherwise unreadable files, THEN THE Reader_Agent SHALL return an error status with a message indicating the failure cause (e.g., corruption or encryption), and the article SHALL proceed to classification with metadata-only context.
6. IF the Gemini API call for summarization fails due to network error, quota exhaustion, or invalid response, THEN THE Reader_Agent SHALL raise an error indicating the summarization failure cause, and the article SHALL not proceed to downstream agents until retried or manually resolved.

### Requirement 3: Structured Metadata Classification via Classifier Agent

**User Story:** As a researcher, I want a specialized agent to extract objective metadata from articles, so that categorization fields are accurate and consistent.

#### Acceptance Criteria

1. WHEN the Reader_Agent completes processing, THE Classifier_Agent SHALL receive the Super_Summary and article metadata (title, student, group, link) as input. IF the Reader_Agent returned an error status due to PDF extraction failure, THEN THE Classifier_Agent SHALL proceed using only the article metadata as context.
2. THE Classifier_Agent SHALL produce a Pydantic-validated output containing: theme (free text), publication year (integer), publisher/entity (free text), venue type (one of: "Revista (Journal)", "Conferência (Conference)", "Repositório (arXiv/Preprint)", "Outro"), study type (one of: "Experimento Controlado", "Quase-experimento", "Estudo de Caso", "Survey", "Revisão Sistemática", "Proposta Conceitual", "Outro"), research nature (one of: "Prática (Empírica)", "Teórica", "Híbrida"), data nature (one of: "Quantitativa", "Qualitativa", "Mista"), sample size (descriptive text or "N/A" if not applicable), statistical methods (list of methods or empty list if none identified), and software metrics (list of metrics or empty list if none identified).
3. THE Classifier_Agent SHALL map the article to one or more syllabus units from the set {Unidade 1, Unidade 2, Unidade 3}, selecting at least one unit per article.
4. THE Classifier_Agent SHALL identify specific syllabus topics from the predefined TOPICOS_EMENTA list (14 topics spanning Unidade 1 through Unidade 3) that the article addresses, selecting at least one topic per article.
5. IF the Classifier_Agent produces output that fails Pydantic validation, THEN THE ADK_Orchestrator SHALL retry the classification up to 3 times with exponential backoff starting at a 2-second base delay. IF all 3 retries fail validation, THEN THE ADK_Orchestrator SHALL record a null classification entry for that article and continue processing remaining articles.

### Requirement 4: Qualitative Analysis via Critic Agent

**User Story:** As a researcher, I want a dedicated agent to perform qualitative rubric evaluation, so that subjective assessments are produced with justifications and reduced hallucination risk.

#### Acceptance Criteria

1. WHEN the Classifier_Agent completes processing, THE Critic_Agent SHALL receive the Super_Summary, article metadata, and the Classifier_Agent's structured output as input.
2. THE Critic_Agent SHALL produce rubric scores (integers from 1 to 5) for each of the seven evaluation dimensions: qualidade_academica, replicabilidade, aplicabilidade_pratica, contribuicao_teorica, adequacao_aluno, contribuicao_aprendizagem, and alinhamento_plano.
3. THE Critic_Agent SHALL produce a textual justification (minimum 20 characters, maximum 500 characters) for each rubric score, referencing specific evidence from the Super_Summary.
4. THE Critic_Agent SHALL evaluate reproducibility by classifying data/code availability as one of: "Totalmente Disponível", "Parcialmente Disponível", or "Não Disponível"; identifying replication package links (or an empty list if none exist); and classifying shared artifacts using one or more values from: "Código Fonte", "Dataset", "Scripts R/Python", "Questionários", "Nenhum".
5. THE Critic_Agent SHALL produce a summary in Brazilian Portuguese (maximum 150 words) and identify exactly three main findings (each maximum 50 words) and exactly one principal limitation (maximum 50 words).
6. IF any rubric score falls outside the range 1 to 5, THEN THE ADK_Orchestrator SHALL reject the output and retry the Critic_Agent up to 3 times with exponential backoff.
7. IF the Critic_Agent fails to produce valid output after exhausting 3 retries, THEN THE ADK_Orchestrator SHALL log the failure, record a fallback entry with null rubric scores for that article, and continue processing remaining articles.

### Requirement 5: Citation Count Lookup via Web Integration

**User Story:** As a researcher, I want real citation counts fetched from academic APIs, so that the analysis uses verifiable data instead of LLM-estimated values.

#### Acceptance Criteria

1. WHEN an article's title is available from the parsed `info.md` metadata, THE Citation_Lookup_Service SHALL query the CrossRef API using the article title as the search term and retrieve the citation count from the first matching result, with a per-request timeout of 10 seconds.
2. IF the CrossRef API returns zero matching results or returns a match that does not include a citation count field, THEN THE Citation_Lookup_Service SHALL fall back to querying the Semantic Scholar API using the article title as the search term, with a per-request timeout of 10 seconds.
3. IF both APIs return no matching results or no citation count field, THEN THE Citation_Lookup_Service SHALL record the citation count as "N/A" for that article.
4. IF an API request fails due to a network error, HTTP error status (4xx or 5xx), or timeout, THEN THE Citation_Lookup_Service SHALL retry up to 2 additional times with a 2-second delay between attempts before treating that API as failed and proceeding to the next fallback or recording "N/A".
5. THE Citation_Lookup_Service SHALL enforce a minimum interval of 1 second between consecutive requests to the same API.
6. THE Citation_Lookup_Service SHALL persist cached results in a local JSON file keyed by article title, and SHALL reuse cached citation counts for up to 7 days before re-querying the APIs.

### Requirement 6: Cross-Article Thematic Synthesis

**User Story:** As a researcher, I want a synthesis agent to analyze relationships across all articles, so that the final report includes thematic overlap, continuity, and complementation analysis as required by the assignment.

#### Acceptance Criteria

1. WHEN all individual articles have been processed by the Reader, Classifier, and Critic agents, THE Synthesizer_Agent SHALL receive the complete set of classification results (including theme, rubric scores, syllabus units, and Super_Summary for each article) as input.
2. THE Synthesizer_Agent SHALL produce a thematic relationship analysis that identifies article pairs or groups for each relationship type: overlapping themes (two or more articles addressing the same core topic), continuity (articles that build upon each other's findings), and complementation (articles covering different aspects of the same broader topic), referencing each article by its folder name.
3. THE Synthesizer_Agent SHALL produce an IFRD feasibility discussion that addresses: the proposed formula or weighting rationale across the seven rubric dimensions, at least one identified limitation of the composite indicator, and a conclusion on whether the indicator is viable for the analyzed corpus.
4. THE Synthesizer_Agent SHALL group articles into thematic clusters, assigning each processed article to at least one cluster and providing a descriptive label (maximum 60 characters) for each cluster.
5. IF no articles are found for a given relationship type (overlap, continuity, or complementation), THEN THE Synthesizer_Agent SHALL explicitly state that no such relationship was identified in the corpus rather than omitting the section.
6. THE Synthesizer_Agent SHALL produce all output as structured text sections (one section per relationship type, one for clusters, one for IFRD discussion) suitable for inclusion in an Excel worksheet.

### Requirement 7: ADK Multi-Agent Orchestration

**User Story:** As a researcher, I want the agents to be orchestrated through Google ADK's framework, so that the system benefits from ADK's built-in agent coordination, tool management, and structured output capabilities.

#### Acceptance Criteria

1. THE ADK_Orchestrator SHALL execute agents in sequential order per article: Reader_Agent, then Classifier_Agent, then Critic_Agent.
2. WHEN all individual article processing is complete, THE ADK_Orchestrator SHALL execute the Synthesizer_Agent exactly once, passing the complete set of classification results as input.
3. WHEN an agent fails after exhausting 3 retry attempts, THE ADK_Orchestrator SHALL log the failure details (agent name, article title, error description), record a fallback entry using the predefined error template for that article, and continue processing remaining articles.
4. THE ADK_Orchestrator SHALL enforce a configurable delay between consecutive Gemini API calls, defaulting to 4 seconds, with a minimum of 1 second and a maximum of 60 seconds.
5. WHEN each article completes processing through all three agents (or fails), THE ADK_Orchestrator SHALL report progress including the current article index (1-based), total article count, and article title via a callback mechanism.
6. IF the Synthesizer_Agent fails after exhausting 3 retry attempts, THEN THE ADK_Orchestrator SHALL log the synthesis failure and complete the pipeline run without thematic relationship data, preserving all individual article results.

### Requirement 8: Excel Export with Consolidated Results

**User Story:** As a researcher, I want the final output as a styled Excel spreadsheet with all classification data, so that it can be directly used in the course presentation.

#### Acceptance Criteria

1. WHEN all articles are processed and synthesis is complete, THE Pipeline SHALL export results to `classificacao_artigos.xlsx` in the project root directory using pandas and openpyxl.
2. THE Pipeline SHALL include all fields from the Classification_Schema in the Excel output, organized with one row per article in the main worksheet.
3. THE Pipeline SHALL include the Synthesizer_Agent's thematic relationship analysis in a separate worksheet tab named "Síntese Temática".
4. THE Pipeline SHALL include citation counts obtained from the Citation_Lookup_Service in the exported data, displaying "N/A" for articles where citation lookup failed.
5. THE Pipeline SHALL calculate and include the IFRD composite index for each article using the weighted formula: IFRD = 0.25×Qualidade + 0.20×Alinhamento + 0.20×Aprendizagem + 0.15×Replicabilidade + 0.10×Aplicabilidade + 0.10×Adequação, rounded to 2 decimal places.
6. THE Pipeline SHALL apply visual styling consisting of: navy blue header row with white text, frozen panes below the header row, thin borders on all cells, and auto-adjusted column widths to fit content.
7. THE Pipeline SHALL apply conditional row formatting based on IFRD score: green background for IFRD >= 4.0 ("Bom Artigo"), yellow background for IFRD >= 3.0 and < 4.0 ("Intermediário"), and red background for IFRD < 3.0 ("Fraco").
8. IF an article has incomplete classification data due to agent failures, THEN THE Pipeline SHALL include that article's row in the Excel output with available fields populated and missing fields left blank.

### Requirement 9: Environment and Dependency Management

**User Story:** As a developer, I want the pipeline to run in a local Python virtual environment with clearly specified dependencies, so that setup is reproducible and isolated.

#### Acceptance Criteria

1. THE Pipeline SHALL execute within a Python virtual environment (`.venv`) using Python 3.10 or later.
2. THE Pipeline SHALL declare all dependencies in a `requirements.txt` file including: google-adk, google-genai, pypdf, pydantic, pandas, openpyxl, requests, tqdm, and python-dotenv, each with a minimum version constraint.
3. THE Pipeline SHALL read the Gemini API key from the `GEMINI_API_KEY` environment variable, loading it from a `.env` file located in the project root directory via python-dotenv.
4. IF the `GEMINI_API_KEY` environment variable is not set or is empty, THEN THE Pipeline SHALL exit with a non-zero exit code and print an error message to stderr indicating that the `GEMINI_API_KEY` variable is missing or empty.
5. IF the `.env` file does not exist in the project root directory, THEN THE Pipeline SHALL continue execution and rely on the `GEMINI_API_KEY` being set directly in the system environment.

### Requirement 10: CLI Interface and Execution Modes

**User Story:** As a developer, I want a command-line interface with dry-run and progress reporting, so that I can test the pipeline incrementally and monitor long-running executions.

#### Acceptance Criteria

1. THE Pipeline SHALL provide a CLI entrypoint (`run_adk_pipeline.py`) that accepts `--dry-run` (flag) and `--delay` (float, in seconds) command-line arguments via argparse.
2. WHEN the `--dry-run` flag is provided, THE Pipeline SHALL process only the first discovered article, produce the Excel output file with that single article's results, and log that it executed in dry-run mode.
3. WHEN the `--delay` argument is provided with a value greater than or equal to 0, THE Pipeline SHALL use the specified value (in seconds) as the inter-request delay instead of the default of 4.0 seconds.
4. WHILE articles are being processed, THE Pipeline SHALL display a tqdm progress bar showing the current article index, total article count, and article title (truncated to 30 characters if longer).
5. WHEN processing completes successfully, THE Pipeline SHALL log the absolute output file path and the total number of articles processed.
6. IF the `--delay` argument is provided with a negative value or a non-numeric value, THEN THE Pipeline SHALL exit with an error message indicating the invalid delay parameter.
