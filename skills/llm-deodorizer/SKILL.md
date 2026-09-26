---
name: llm-deodorizer
description: Audit and revise files whose prose sounds generic, synthetic, over-polished, promotional, vaguely sourced, structurally templated, or contaminated by assistant drafting artifacts. Use when the user asks to deodorize, humanize, de-AI, clean up, or remove LLM-like writing from Markdown, plain text, source comments, documentation, or document content while preserving facts, citations, intended meaning, and the conventions of the target genre.
---

# LLM Deodorizer

Revise the writing, not merely its surface tells. Make every retained sentence specific, accountable, appropriately sourced, and natural for its genre. Do not optimize for an AI detector or manufacture human-looking errors.

## Workflow

1. Resolve the exact target file and read it completely. Preserve the file format, metadata, code, frontmatter, links, citation syntax, and unrelated user edits.
2. Identify the genre, intended audience, purpose, and existing voice from the artifact and nearby context. Ask only when a missing choice would materially change the result.
3. Run the bundled scanner on text-like files to locate likely hotspots:

   ```bash
   python3 scripts/scan_prose.py /absolute/path/to/file
   ```

   Treat scanner findings as leads, never proof. Read `references/failure-points.md` before revising for the full semantic audit.
4. Audit the entire artifact, including passages the scanner cannot recognize. Classify each issue by its underlying failure: unsupported claim, absent evidence, vague actor, inflated importance, promotional tone, abstract non-analysis, templated structure, terminology drift, ornamental formatting, drafting artifact, speculation, or citation mismatch.
5. Revise in place unless the user requests a copy, redline, or report only. Use `apply_patch` for local text files. For DOCX, PDF, slides, or spreadsheets, use the applicable artifact skill and follow its render-and-verify workflow.
6. Re-read the revised file as a whole. Run the scanner again, review the diff, and verify that the revision preserved meaning and improved substance rather than merely swapping trigger words.

## Revision Rules

- Recover the intended claim before editing its phrasing. Delete filler when no defensible claim remains.
- Replace labels of importance with the concrete consequence, dependency, change, or measured result.
- Replace vague attribution with a named, scoped source. Never turn one source into consensus.
- Use direct verbs when accurate. Prefer `is`, `has`, `uses`, `wrote`, or `made` over ceremonial alternatives, but do not perform blind substitutions.
- Replace abstract nouns with the people, actions, measurements, events, constraints, or causal relationships they hide.
- Remove trailing clauses that only restate significance. Keep participial clauses that express a real action, method, or result.
- Use exactly the number of points supported by the content. Break formulaic triads, contrasts, and symmetrical conclusions when they exist only for rhetorical completeness.
- Organize around the reader's real questions, not a universal overview/background/features/challenges/future/conclusion template.
- Repeat precise terms when needed. Do not cycle through near-synonyms merely to avoid repetition.
- Match the genre. Do not force every artifact into a polished, explanatory, diplomatically positive voice.
- Keep lists, headings, bolding, tables, rules, and dashes only when they improve navigation or expose a real relationship.
- Remove assistant preambles, invitations, prompt fragments, placeholders, internal citation tokens, tracking parameters, broken links, unused references, and malformed markup.
- Preserve genuine personality, sharp claims, contractions, technical language, and irregular structure when they fit the author, evidence, and genre.

## Evidence and Citations

- Do not invent facts, names, measurements, quotations, motives, or sources to make a weak passage more concrete.
- Do not convert an unsuccessful search into a likely-sounding explanation. State the knowledge boundary or mark a supported hypothesis explicitly.
- When factual verification is authorized and relevant, open every cited source and confirm that it exists, supports the adjacent claim, and warrants the stated certainty. Add a page, section, figure, or table locator when the genre requires one.
- Distinguish the source's conclusion from the writer's inference.
- If a claim cannot be repaired from available evidence, qualify it, flag it clearly, or remove it according to the document's purpose. Do not silently fabricate a repair.

## Guardrails

- Do not ban isolated words, em dashes, good grammar, headings, bullet lists, formal language, or triads. These are weak indicators without context.
- Do not add typos, slang, fragments, anecdotes, inconsistent punctuation, or fake opinions to simulate authorship.
- Do not flatten the author's voice or replace every sentence. Make the smallest revision that fixes the underlying failure.
- Do not change quoted text. Edit the surrounding analysis or replace the quotation only when the user has authorized source-level changes.
- Do not alter facts, numerical values, code behavior, math, legal meaning, or citation targets without evidence.
- Do not claim that a file is human-authored or will evade detection. Report the concrete editorial problems fixed.

## Verification

Before finishing, confirm:

- every substantive retained claim has evidence, reasoning, or an explicit firsthand basis;
- significance is expressed as a consequence rather than asserted as a label;
- actors and attributions are named and scoped;
- uncertainty matches the evidence;
- terminology stays consistent;
- section order follows the subject and audience;
- formatting has a functional purpose;
- no drafting artifacts or placeholders remain;
- citations and links still resolve when verification is in scope;
- the diff contains no unintended factual, structural, or formatting changes.

Report the target path, the main classes of fixes, any claims or citations that could not be verified, and the verification performed.
