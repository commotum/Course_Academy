<script lang="ts">
	import type { Quiz } from "../schemas";
	import InlineMarkdown from "./InlineMarkdown.svelte";
	import type { AppContext } from "../markdown";
	import autosize from "svelte-autosize";
	import { tick } from "svelte";
	import type { QuizSavedState } from "../persistence";
	import { initial } from "./initial";

	type SavedState = Extract<QuizSavedState, { type: "free" }>;

	interface Props {
		ctx: AppContext,
		quiz: Extract<Quiz, { type: "free" }>;
		stableId: string;
		savedState?: SavedState;
		onStateChange: (state: SavedState) => void;
		onFinish: () => void;
		onReset: () => void;
	}

	let { ctx, stableId, quiz, savedState, onStateChange, onFinish, onReset }: Props = $props();
	let answer = $state(initial(() => savedState?.answer ?? ""));
	let frozen = $state(initial(() => savedState?.frozen ?? false));
	let textarea: Element;

	function save(nextAnswer: string, nextFrozen: boolean) {
		onStateChange({ type: "free", answer: nextAnswer, frozen: nextFrozen });
	}

	function setAnswer(value: string) {
		answer = value;
		save(value, frozen);
	}

	function onCheck() {
		// We can't grade free text yet; "Check" just freezes the input
		// and reveals the reference answer (if provided).
		if (answer.trim().length === 0) return;
		frozen = true;
		save(answer, true);
		onFinish();
	}

	async function reset() {
		answer = "";
		frozen = false;
		await tick();
		autosize.update(textarea);
		onReset();
	}
</script>

<form class="quiz-form">
	<textarea
		name={stableId}
		disabled={frozen}
		rows={4}
		value={answer}
		placeholder="Type your answer…"
		use:autosize
		bind:this={textarea}
		oninput={(e) => setAnswer(e.currentTarget.value)}
	></textarea>

	{#if frozen && quiz.correct && quiz.correct.trim().length > 0}
		<div class="quiz-text-correct">
			<InlineMarkdown {ctx} markdown={quiz.correct}/>
		</div>
	{/if}

	{#if frozen && quiz.feedback && quiz.feedback.trim().length > 0}
		<div class="quiz-text-feedback">
			<InlineMarkdown {ctx} markdown={quiz.feedback}/>
		</div>
	{/if}
</form>

<div class="quiz-actions">
	{#if !frozen}
		<button class="quiz-check" type="button" onclick={onCheck} disabled={answer.trim().length === 0}>
			Check
		</button>
	{:else}
		<button class="quiz-reset" type="button" onclick={reset} aria-label="Reset quiz" title="Reset quiz">
			↻
		</button>
	{/if}
</div>

<style>
	textarea {
		width: 100%;
		max-width: 100%;
		min-height: 96px;
		resize: vertical;
		font: inherit;
		color: inherit;
	}
</style>
