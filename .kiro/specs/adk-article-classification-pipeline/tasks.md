# Implementation Plan: ADK Article Classification Pipeline

## Overview

This plan implements a Google ADK multi-agent architecture replacing the existing single-call Gemini classification pipeline. The implementation proceeds bottom-up: data models and configuration first, then services, then agents, then orchestration, and finally the CLI entrypoint and Excel export. Each task builds on previously completed code, and all components are wired together in the final integration steps.

## Tasks

- [x] 1. Set up project structure, configuration, and Pydantic data models
  - [x] 1.1 Create module structure and configuration constants
    - Create `src/__init__.py`, `src/models/__init__.py`, `src/agents/__init__.py`, `src/services/__init__.py`
    - Create `src/config.py` with constants: `ARTIGOS_DIR`, `MAX_DEPTH=3`, `MAX_PDF_CHARS=80000`, `DEFAULT_DELAY=4.0`, `MAX_RETRIES=3`, `BASE_RETRY_DELAY=2`, `CACHE_TTL_DAYS=7`, `TOPICOS_EMENTA` list (14 topics), `UNIDADES` set, `IFRD_WEIGHTS` dict
    - _Requirements: 1.1, 7.4, 9.1, 9.2_

  - [x] 1.2 Create Pydantic input and output models
    - Create `src/models/inputs.py` with `ArticleMetadataDTO`, `ReaderInput`, `ClassifierInput`, `CriticInput`, `SynthesizerInput`, `ArticleResultSummary`
    - Create `src/models/super_summary.py` with `SuperSummary` model (4 fields with validators)
    - Create `src/models/classification.py` with `ClassificationOutput` model (all Literal types, field_validators for publication_year and syllabus_units)
    - Create `src/models/critic_output.py` with `RubricScore`, `CriticOutput` models (score constraints, word count validators, shared_artifacts mutual exclusion)
    - Create `src/models/synthesis.py` with `ThematicRelationship`, `ThematicCluster`, `IFRDDiscussion`, `SynthesisOutput` models
    - Create `src/models/article_result.py` with `ProcessingStatus` enum and `ArticleResult` dataclass
    - _Requirements: 2.3, 3.2, 3.3, 3.4, 4.2, 4.3, 4.4, 4.5, 6.1, 6.2, 6.3, 6.4_

  - [x]* 1.3 Write property tests for data model validation (Properties 5-10)
    - **Property 5: SuperSummary schema validation** — generate valid/invalid SuperSummary data and verify acceptance/rejection
    - **Property 6: ClassificationOutput schema and constraints** — generate enum values and validate syllabus_units, syllabus_topics, publication_year range
    - **Property 7: Publication year rejects hallucinated values** — generate integers outside [1900, current_year] and verify rejection; None accepted
    - **Property 8: Critic rubric scores and justification constraints** — generate scores 1-5 and strings of varying length, verify bounds enforcement
    - **Property 9: Critic summary structure constraints** — generate resumo_pt with varying word counts, main_findings lists of varying lengths
    - **Property 10: Shared artifacts mutual exclusion** — generate lists with/without "Nenhum" and verify mutual exclusion rule
    - **Validates: Requirements 2.3, 3.2, 3.3, 3.4, 4.2, 4.3, 4.4, 4.5**

- [x] 2. Implement article discovery and PDF extraction services
  - [x] 2.1 Implement article discovery module
    - Create `src/discovery.py` with `ArticleMetadata` dataclass, `discover_articles(base_dir, max_depth=3)` function, and `parse_info_md(info_path)` function
    - Recursive scan of `artigos/` up to 3 levels, filter folders with both `info.md` and `artigo.pdf`
    - Parse `info.md`: extract H1 as title, "Aluno"/"Grupo"/"Link original" fields, default empty string for missing fields
    - Raise error if `artigos/` directory does not exist or is empty
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [x]* 2.2 Write property tests for discovery (Properties 1-3)
    - **Property 1: Directory scanning respects depth limit** — generate directory trees with info.md at various depths, verify only depth ≤ 3 returned
    - **Property 2: Article filtering includes only folders with PDF** — generate folder sets with/without artigo.pdf, verify correct inclusion
    - **Property 3: info.md parsing extracts fields with defaults** — generate info.md content with various field combinations, verify extraction with defaults
    - **Validates: Requirements 1.1, 1.3, 1.4, 1.5, 1.6**

  - [x] 2.3 Implement PDF text extraction service
    - Create `src/services/pdf_extractor.py` with `ExtractionResult` dataclass and `extract_pdf_text(pdf_path, max_chars=80000)` function
    - Use pypdf to extract text, normalize whitespace (collapse consecutive whitespace to single space per page), truncate to max_chars
    - Return `ExtractionResult(success=False, error_message=...)` for missing, corrupted, or encrypted PDFs
    - _Requirements: 2.1, 2.2, 2.4, 2.5_

  - [x]* 2.4 Write property tests for PDF text extraction (Property 4)
    - **Property 4: PDF text extraction invariants** — generate strings with various whitespace patterns, verify normalization produces no consecutive whitespace and output ≤ 80,000 chars
    - **Validates: Requirements 2.1, 2.2**

- [x] 3. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Implement citation lookup service with caching
  - [x] 4.1 Implement JSON file cache with TTL
    - Create `src/services/cache.py` with a `FileCache` class: load/save JSON, key-based get/set with timestamp, TTL-based expiration (7 days default)
    - _Requirements: 5.6_

  - [x] 4.2 Implement citation lookup service
    - Create `src/services/citation_lookup.py` with `CitationResult` dataclass and `CitationLookupService` class
    - Implement fallback chain: cache → CrossRef API → Semantic Scholar API → "N/A"
    - Enforce 10-second timeout per request, 2 retries with 2-second delay on failure, 1-second minimum interval between requests to same API
    - Use `requests` library for HTTP calls
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [x]* 4.3 Write property tests for citation service (Properties 11-12)
    - **Property 11: Citation fallback cascade** — mock API responses, verify CrossRef → Semantic Scholar → N/A cascade is always followed correctly
    - **Property 12: Citation cache round-trip with TTL** — generate title/count pairs, verify cache returns same value within 7 days and triggers fresh query after TTL
    - **Validates: Requirements 5.2, 5.3, 5.6**

- [x] 5. Implement IFRD calculation
  - [x] 5.1 Implement IFRD calculator module
    - Create `src/ifrd.py` with `calculate_ifrd(scores)` and `classify_ifrd(ifrd)` functions
    - Formula: IFRD = 0.25×qualidade + 0.20×alinhamento + 0.20×aprendizagem + 0.15×replicabilidade + 0.10×aplicabilidade + 0.10×adequacao, rounded to 2 decimal places
    - Classification: "Bom Artigo" (≥4.0), "Intermediário" (≥3.0, <4.0), "Fraco" (<3.0)
    - _Requirements: 8.5, 8.7_

  - [x]* 5.2 Write property tests for IFRD (Property 13)
    - **Property 13: IFRD calculation correctness** — generate valid rubric scores (1-5 each), verify formula result matches expected calculation and classification thresholds are correct
    - **Validates: Requirements 8.5, 8.7**

- [x] 6. Implement ADK agents
  - [x] 6.1 Implement Reader Agent
    - Create `src/agents/reader_agent.py` with ADK `Agent` definition using `gemini-2.0-flash` model
    - Define focused prompt for summarization: instruct to produce SuperSummary from extracted text
    - Set `output_schema=SuperSummary`
    - _Requirements: 2.3, 2.6_

  - [x] 6.2 Implement Classifier Agent
    - Create `src/agents/classifier_agent.py` with ADK `Agent` definition
    - Include TOPICOS_EMENTA and UNIDADES context in instruction prompt
    - Set `output_schema=ClassificationOutput`
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [x] 6.3 Implement Critic Agent
    - Create `src/agents/critic_agent.py` with ADK `Agent` definition
    - Include rubric criteria with scoring guidelines in instruction prompt
    - Set `output_schema=CriticOutput`
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 6.4 Implement Synthesizer Agent
    - Create `src/agents/synthesizer_agent.py` with ADK `Agent` definition
    - Include instructions for thematic relationships, IFRD discussion, and clustering
    - Set `output_schema=SynthesisOutput`
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

- [x] 7. Implement Pipeline Orchestrator
  - [x] 7.1 Implement orchestrator core logic
    - Create `src/orchestrator.py` with `PipelineOrchestrator` class
    - Instantiate ADK `SequentialAgent` with [reader_agent, classifier_agent, critic_agent]
    - Implement `process_article(metadata)`: PDF extraction → SequentialAgent invocation → citation lookup → ArticleResult construction
    - Implement retry logic with exponential backoff (base 2s, max 3 retries)
    - Implement graceful degradation: PDF extraction failure → proceed with metadata-only; Reader LLM failure → skip Classifier/Critic; Classifier failure → skip Critic
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6_

  - [x] 7.2 Implement synthesis invocation and full pipeline run
    - Implement `run_synthesis(results)`: invoke Synthesizer_Agent once with all ArticleResults
    - Implement `run(articles, progress_callback)`: full pipeline loop with configurable delay, progress reporting, and error handling
    - Handle Synthesizer failure gracefully (preserve all individual results)
    - _Requirements: 7.2, 7.3, 7.5, 7.6_

- [x] 8. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 9. Implement Excel export
  - [x] 9.1 Implement Excel exporter
    - Create `src/excel_exporter.py` with `ExcelExporter` class and `export(results, synthesis, output_path)` static method
    - Main worksheet: one row per article, all ClassificationSchema fields as columns, ProcessingStatus column, IFRD column, citation count column
    - Synthesis worksheet tab "Síntese Temática" with thematic relationship analysis sections
    - Styling: navy blue header with white text, frozen panes, thin borders, auto-adjusted column widths
    - Conditional formatting: green (IFRD ≥ 4.0), yellow (3.0 ≤ IFRD < 4.0), red (IFRD < 3.0)
    - Orange highlight for rows with non-SUCCESS ProcessingStatus
    - Handle incomplete data: include rows with available fields, leave missing fields blank
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8_

  - [x]* 9.2 Write property tests for Excel export (Property 14)
    - **Property 14: Excel export completeness with processing status** — generate lists of ArticleResults with various statuses, verify row count matches article count, all schema columns present, ProcessingStatus column populated
    - **Validates: Requirements 8.2, 8.8**

- [x] 10. Implement CLI entrypoint and environment setup
  - [x] 10.1 Implement CLI entrypoint
    - Create `run_adk_pipeline.py` with argparse for `--dry-run` (flag) and `--delay` (float) arguments
    - Load `.env` via python-dotenv, validate `GEMINI_API_KEY` presence (exit with error if missing/empty)
    - Wire discovery → orchestrator → Excel export
    - Implement tqdm progress bar (article index, total count, truncated title)
    - In dry-run mode: process only first article, log dry-run execution
    - On completion: log output file path and total articles processed
    - Validate `--delay` argument (reject negative/non-numeric values)
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

  - [x] 10.2 Update requirements.txt with all dependencies
    - Ensure `requirements.txt` includes: google-adk, google-genai, pypdf, pydantic, pandas, openpyxl, requests, tqdm, python-dotenv, hypothesis (for testing), each with minimum version constraint
    - _Requirements: 9.2_

- [x] 11. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- The ADK `SequentialAgent` handles only the per-article Reader → Classifier → Critic chain; the `PipelineOrchestrator` controls the full pipeline lifecycle
- All agents use `gemini-2.0-flash` model with Pydantic output schemas for structured validation
- Graceful degradation ensures partial results are preserved even when individual agents fail

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["1.3", "2.1", "2.3", "4.1", "5.1"] },
    { "id": 3, "tasks": ["2.2", "2.4", "4.2", "5.2"] },
    { "id": 4, "tasks": ["4.3", "6.1", "6.2", "6.3", "6.4"] },
    { "id": 5, "tasks": ["7.1"] },
    { "id": 6, "tasks": ["7.2", "9.1"] },
    { "id": 7, "tasks": ["9.2", "10.1", "10.2"] }
  ]
}
```
