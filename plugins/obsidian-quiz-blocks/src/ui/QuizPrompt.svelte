<script lang="ts">
	import type { Quiz } from "../schemas";
	import InlineMarkdown from "./InlineMarkdown.svelte";
	import type { AppContext } from "../markdown";
	import type { QuizSavedState } from "../persistence";
	import { initial } from "./initial";
	import QuizResultBadge from "./QuizResultBadge.svelte";

	type SavedState = Extract<QuizSavedState, { type: "blank" }>;

	interface Props {
		ctx: AppContext,
		quiz: Extract<Quiz, { type: "blank" }>;
		savedState?: SavedState;
		onStateChange: (state: SavedState) => void;
		onFinish: () => void;
		onReset: () => void;
	}

	let { ctx, quiz, savedState, onStateChange, onFinish, onReset }: Props = $props();
	let checked = $state(initial(() => savedState?.checked ?? false));
	let answers = $state<string[]>(initial(() => savedState?.answers ?? []));
	let requireExact = $derived(quiz.require_exact);

	type PromptPart =
		| { type: "text"; content: string }
		| { type: "blank"; answer: string; index: number };

	type BlankMarker = {
		answer: string;
		index: number;
		start: number;
		end: number;
	};

	type TextRange = {
		start: number;
		end: number;
	};

	type DisplayMathRange = TextRange & {
		body: string;
		bodyStart: number;
		bodyEnd: number;
	};

	type MathBlank = {
		answer: string;
		index: number;
	};

	type MathBlankRow = {
		before: string;
		blank?: MathBlank;
		after: string;
	};

	type PromptRenderPart =
		| { type: "markdown"; content: string }
		| { type: "math-blank-block"; rows: MathBlankRow[] };

	let parts = $derived(parsePrompt(quiz.content ?? ""));
	let renderParts = $derived(parseRenderParts(quiz.content ?? ""));
	let hasMathBlankBlocks = $derived(renderParts.some((part) => part.type === "math-blank-block"));
	let blankCount = $derived(parts.filter((part) => part.type === "blank").length);
	let blanksLeft = $derived(Math.max(0, blankCount - answers.filter((answer) => answer.trim().length > 0).length));

	$effect(() => {
		if (answers.length !== blankCount) {
			answers = normalizeAnswers(answers, blankCount);
		}
	});

	function normalizeAnswers(values: string[], length: number): string[] {
		return Array.from({ length }, (_, i) => values[i] ?? "");
	}

	function parsePrompt(markdown: string): PromptPart[] {
		const next: PromptPart[] = [];
		let lastIndex = 0;

		for (const marker of findBlankMarkers(markdown)) {
			if (marker.start > lastIndex) {
				next.push({ type: "text", content: markdown.slice(lastIndex, marker.start) });
			}

			next.push({ type: "blank", answer: marker.answer, index: marker.index });
			lastIndex = marker.end;
		}

		if (lastIndex < markdown.length) {
			next.push({ type: "text", content: markdown.slice(lastIndex) });
		}

		return next;
	}

	function parseRenderParts(markdown: string): PromptRenderPart[] {
		const markers = findBlankMarkers(markdown);
		const displayMathRanges = findDisplayMathRanges(markdown);
		const next: PromptRenderPart[] = [];
		let lastIndex = 0;

		for (const range of displayMathRanges) {
			const rangeMarkers = markers.filter((marker) => marker.start >= range.bodyStart && marker.end <= range.bodyEnd);
			if (rangeMarkers.length === 0) continue;

			if (range.start > lastIndex) {
				next.push({ type: "markdown", content: markdown.slice(lastIndex, range.start) });
			}

			const rows = parseMathBlankRows(range.body, rangeMarkers);
			if (rows.some((row) => row.blank)) {
				next.push({ type: "math-blank-block", rows });
			} else {
				next.push({ type: "markdown", content: markdown.slice(range.start, range.end) });
			}

			lastIndex = range.end;
		}

		if (lastIndex < markdown.length) {
			next.push({ type: "markdown", content: markdown.slice(lastIndex) });
		}

		return next.length > 0 ? next : [{ type: "markdown", content: markdown }];
	}

	function parseMathBlankRows(body: string, markers: BlankMarker[]): MathBlankRow[] {
		const rows = splitMathRows(stripMathEnvironment(body));
		let nextMarkerIndex = 0;

		return rows.flatMap((rawRow) => {
			const row = rawRow.trim();
			if (row.length === 0) return [];

			const match = /==([\s\S]+?)==/.exec(row);
			if (!match) return [{ before: normalizeMathFragment(row), after: "" }];

			const marker = markers[nextMarkerIndex];
			nextMarkerIndex += 1;

			const raw = match[0] ?? "";
			const answer = marker?.answer ?? (match[1] ?? "").trim();
			const index = marker?.index ?? nextMarkerIndex - 1;

			return [{
				before: normalizeMathFragment(row.slice(0, match.index)),
				blank: { answer, index },
				after: normalizeMathFragment(row.slice(match.index + raw.length)),
			}];
		});
	}

	function stripMathEnvironment(body: string): string {
		return body
			.trim()
			.replace(/^\\begin\{(?:aligned|gathered|split)\}\s*/, "")
			.replace(/\s*\\end\{(?:aligned|gathered|split)\}$/, "")
			.trim();
	}

	function splitMathRows(body: string): string[] {
		const rows: string[] = [];
		let current = "";
		let i = 0;

		while (i < body.length) {
			if (body[i] === "\\" && body[i + 1] === "\\") {
				rows.push(current);
				current = "";
				i += 2;
			} else {
				current += body[i];
				i += 1;
			}
		}

		rows.push(current);
		return rows;
	}

	function normalizeMathFragment(fragment: string): string {
		return fragment.replace(/&/g, "").trim();
	}

	function inlineMath(fragment: string): string {
		return fragment.trim().length > 0 ? `$${fragment}$` : "";
	}

	function findBlankMarkers(markdown: string): BlankMarker[] {
		const markers: BlankMarker[] = [];
		const pattern = /==([\s\S]+?)==/g;
		let match: RegExpExecArray | null;

		while ((match = pattern.exec(markdown))) {
			const raw = match[0] ?? "";
			const start = match.index;
			const end = start + raw.length;

			markers.push({
				answer: (match[1] ?? "").trim(),
				index: markers.length,
				start,
				end,
			});
		}

		return markers;
	}

	function findDisplayMathRanges(markdown: string): DisplayMathRange[] {
		const ranges: DisplayMathRange[] = [];
		let i = 0;

		while (i < markdown.length) {
			if (isEscaped(markdown, i)) {
				i += 1;
				continue;
			}

			if (markdown.startsWith("$$", i)) {
				const end = findClosingDelimiter(markdown, "$$", i + 2);
				if (end !== -1) {
					ranges.push({
						start: i,
						end: end + 2,
						bodyStart: i + 2,
						bodyEnd: end,
						body: markdown.slice(i + 2, end),
					});
					i = end + 2;
					continue;
				}
			}

			if (markdown.startsWith("\\[", i)) {
				const end = findClosingDelimiter(markdown, "\\]", i + 2);
				if (end !== -1) {
					ranges.push({
						start: i,
						end: end + 2,
						bodyStart: i + 2,
						bodyEnd: end,
						body: markdown.slice(i + 2, end),
					});
					i = end + 2;
					continue;
				}
			}

			i += 1;
		}

		return ranges;
	}

	function findClosingDelimiter(markdown: string, delimiter: string, start: number): number {
		let i = start;

		while (i < markdown.length) {
			const found = markdown.indexOf(delimiter, i);
			if (found === -1) return -1;
			if (!isEscaped(markdown, found)) return found;
			i = found + delimiter.length;
		}

		return -1;
	}

	function isEscaped(markdown: string, index: number): boolean {
		let slashCount = 0;
		let i = index - 1;

		while (i >= 0 && markdown[i] === "\\") {
			slashCount += 1;
			i -= 1;
		}

		return slashCount % 2 === 1;
	}

	function setAnswer(i: number, value: string) {
		const next = [...answers];
		next[i] = value;
		answers = next;
		onStateChange({ type: "blank", answers: next, checked });
	}

	function isCorrect(expected: string, actual: string) {
		return actual.trim().toLocaleLowerCase() === expected.trim().toLocaleLowerCase();
	}

	function onCheck() {
		if (checked) return;
		checked = true;
		onStateChange({ type: "blank", answers, checked: true });
		onFinish();
	}

	let isAnswerCorrect = $derived(
		requireExact && parts.every((part) => part.type === "text" || isCorrect(part.answer, answers[part.index] ?? ""))
	);

	function reset() {
		checked = false;
		answers = Array(blankCount).fill("");
		onReset();
	}
</script>

<div class="quiz-prompt-content" class:is-inline={!hasMathBlankBlocks}>
	{#if hasMathBlankBlocks}
		{#each renderParts as renderPart}
			{#if renderPart.type === "markdown"}
				<InlineMarkdown {ctx} markdown={renderPart.content}/>
			{:else}
				<div class="quiz-prompt-math-block">
					{#each renderPart.rows as row}
						<span class="quiz-prompt-math-before">
							{#if row.before}
								<InlineMarkdown {ctx} markdown={inlineMath(row.before)} tag="span"/>
							{/if}
						</span>
						<span class="quiz-prompt-math-blank-slot">
							{#if row.blank}
								{@const blank = row.blank}
								{@const value = answers[blank.index] ?? ""}
								{@const correct = checked && isCorrect(blank.answer, value)}
								<input
									class="quiz-prompt-blank quiz-prompt-math-input"
									class:is-correct={checked && requireExact && correct}
									class:is-wrong={checked && requireExact && !correct}
									type="text"
									value={value}
									disabled={checked}
									aria-label={`Blank ${blank.index + 1}`}
									oninput={(e) => setAnswer(blank.index, e.currentTarget.value)}
								/>
								{#if checked && !requireExact}
									<InlineMarkdown
										{ctx}
										markdown={inlineMath(blank.answer)}
										class="quiz-prompt-answer is-reveal"
										tag="span"
									/>
								{:else if checked && requireExact && !correct}
									<InlineMarkdown
										{ctx}
										markdown={inlineMath(blank.answer)}
										class="quiz-prompt-answer is-wrong"
										tag="span"
									/>
								{/if}
							{/if}
						</span>
						<span class="quiz-prompt-math-after">
							{#if row.after}
								<InlineMarkdown {ctx} markdown={inlineMath(row.after)} tag="span"/>
							{/if}
						</span>
					{/each}
				</div>
			{/if}
		{/each}
	{:else}
		{#each parts as part}
			{#if part.type === "text"}
				<InlineMarkdown {ctx} markdown={part.content}/>
			{:else}
				{@const value = answers[part.index] ?? ""}
				{@const correct = checked && isCorrect(part.answer, value)}
				<input
					class="quiz-prompt-blank"
					class:is-correct={checked && requireExact && correct}
					class:is-wrong={checked && requireExact && !correct}
					type="text"
					value={value}
					disabled={checked}
					aria-label={`Blank ${part.index + 1}`}
					oninput={(e) => setAnswer(part.index, e.currentTarget.value)}
				/>
				{#if checked && !requireExact}
					<InlineMarkdown {ctx} markdown={part.answer} class="quiz-prompt-answer is-reveal"/>
				{:else if checked && !correct}
					<InlineMarkdown {ctx} markdown={part.answer} class="quiz-prompt-answer is-wrong"/>
				{/if}
			{/if}
		{/each}
	{/if}
</div>

{#if checked && quiz.feedback && quiz.feedback.trim().length > 0}
	<div class="feedback">
		<InlineMarkdown {ctx} markdown={quiz.feedback}/>
	</div>
{/if}

<div class="quiz-actions">
	{#if !checked}
		<button class="quiz-check" type="button" onclick={onCheck} disabled={blanksLeft > 0}>
			{#if !requireExact}
				{#if blanksLeft === 0}
					Reveal
				{:else}
					Reveal ({blanksLeft} blanks left)
				{/if}
			{:else if blanksLeft === 0}
				Check
			{:else}
				Check ({blanksLeft} blanks left)
			{/if}
		</button>
	{:else}
		<button class="quiz-reset" type="button" onclick={reset} aria-label="Reset quiz" title="Reset quiz">
			↻
		</button>
		{#if requireExact}
			<QuizResultBadge correct={isAnswerCorrect}/>
		{/if}
	{/if}
</div>

<style>
	.quiz-prompt-content {
		padding: 0 4px;
		line-height: var(--line-height-normal);

		&.is-inline {
			:global(div) {
				display: inline;
			}

			:global(p) {
				display: inline;
				margin: 0;
			}
		}
	}

	.quiz-prompt-math-block {
		display: grid;
		grid-template-columns: max-content minmax(8ch, auto) max-content;
		justify-content: center;
		align-items: center;
		column-gap: 6px;
		row-gap: 6px;
		margin: 0.75em 0;
	}

	.quiz-prompt-math-before,
	.quiz-prompt-math-blank-slot,
	.quiz-prompt-math-after {
		display: inline-flex;
		align-items: center;
		min-height: var(--input-height);
	}

	.quiz-prompt-math-before {
		justify-content: flex-end;
		text-align: right;
	}

	.quiz-prompt-math-blank-slot {
		justify-content: center;
		gap: 4px;
	}

	.quiz-prompt-blank {
		width: 12ch;
		min-width: 8ch;
		max-width: 100%;
		margin: 0 4px;
		padding: 2px 6px;
		border: 1px solid var(--background-modifier-border);
		border-radius: 4px;
		background: var(--background-primary);
		color: var(--text-normal);
		vertical-align: baseline;

		&.is-correct {
			border-color: var(--quiz-right);
			background-color: var(--quiz-right);
			color: white;
			-webkit-text-fill-color: white;
		}

		&.is-wrong {
			border-color: var(--quiz-wrong);
			background-color: var(--quiz-wrong);
			color: white;
			-webkit-text-fill-color: white;
		}

		&:disabled {
			opacity: 1;
		}
	}

	.quiz-prompt-blank.quiz-prompt-math-input {
		width: 8ch;
		min-width: 8ch;
		margin: 0;
		text-align: center;
	}

	:global(.quiz-prompt-answer) {
		display: inline;
		margin-left: 4px;
		font-size: var(--font-smaller);

		&:global(.is-wrong) {
			color: var(--quiz-wrong);
		}

		&:global(.is-reveal) {
			color: var(--quiz-right);
		}

		:global(div),
		:global(p) {
			display: inline;
			margin: 0;
		}
	}

	.feedback {
		margin-top: 6px;
		margin-left: 4px;
		font-size: var(--font-smaller);
		line-height: 1.35;

		& :global(p) {
			margin: 0;
		}
	}
</style>
