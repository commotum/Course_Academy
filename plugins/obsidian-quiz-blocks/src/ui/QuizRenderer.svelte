<script lang="ts">
	import "./__variables.css";
	import type { AppContext } from "../markdown";
	import type { Quiz } from "../schemas";

	import InlineMarkdown from "./InlineMarkdown.svelte";
	import QuizGate from "./QuizGate.svelte";
	import QuizChoice from "./QuizChoice.svelte";
	import QuizRadio from "./QuizRadio.svelte";
	import QuizCheckbox from "./QuizCheckbox.svelte";
	import QuizNoodle from "./QuizNoodle.svelte";
	import QuizText from "./QuizText.svelte";
	import QuizPrompt from "./QuizPrompt.svelte";
	import type { QuizSavedState } from "../persistence";

	interface Props {
		ctx: AppContext;
		stableId: string;
		quiz: Quiz;
		savedState?: QuizSavedState;
		onStateChange: (state: QuizSavedState) => void;
		onStateReset: () => void;
	}

	let { ctx, stableId, quiz, savedState, onStateChange, onStateReset }: Props = $props();

	let gate: { disable: () => void; };

	let typeState = $derived(savedState?.type === quiz.type ? savedState : undefined);
	let quizWasStarted = $derived(typeState !== undefined);
	let quizWasCompleted = $derived(isCompleted(typeState));

	function isCompleted(state: QuizSavedState | undefined): boolean {
		if (!state) return false;

		switch (state.type) {
			case "blank":
				return state.checked;
			case "radio":
			case "checkbox":
			case "select":
			case "multi-select":
			case "noodle":
			case "free":
				return state.frozen;
		}
	}

	function onFinish() {
		gate?.disable();
	}

	function onReset() {
		onStateReset();
	}
</script>

<QuizGate
	bind:this={gate}
	{ctx}
	{stableId}
	{quiz}
	initialRevealed={quizWasStarted}
	initialCompleted={quizWasCompleted}
>
	{#snippet children()}
		{#if quiz.type !== "blank"}
			<div class="quiz-title">
				<InlineMarkdown {ctx} markdown={quiz.content}/>
			</div>
		{/if}

		{#if quiz.type === "blank"}
			<QuizPrompt
				{ctx}
				{quiz}
				savedState={typeState?.type === "blank" ? typeState : undefined}
				{onStateChange}
				{onFinish}
				{onReset}
			/>
		{:else if quiz.type === "select" || quiz.type === "multi-select"}
			<QuizChoice
				{ctx}
				{quiz}
				savedState={typeState?.type === "select" || typeState?.type === "multi-select" ? typeState : undefined}
				{onStateChange}
				{onFinish}
				{onReset}
			/>
		{:else if quiz.type === "noodle"}
			<QuizNoodle
				{ctx}
				{quiz}
				savedState={typeState?.type === "noodle" ? typeState : undefined}
				{onStateChange}
				{onFinish}
				{onReset}
			/>
		{:else if quiz.type === "free"}
			<QuizText
				{ctx}
				{stableId}
				{quiz}
				savedState={typeState?.type === "free" ? typeState : undefined}
				{onStateChange}
				{onFinish}
				{onReset}
			/>
		{:else if quiz.type === "radio"}
			<QuizRadio
				{ctx}
				{stableId}
				{quiz}
				savedState={typeState?.type === "radio" ? typeState : undefined}
				{onStateChange}
				{onFinish}
				{onReset}
			/>
		{:else if quiz.type === "checkbox"}
			<QuizCheckbox
				{ctx}
				{stableId}
				{quiz}
				savedState={typeState?.type === "checkbox" ? typeState : undefined}
				{onStateChange}
				{onFinish}
				{onReset}
			/>
		{/if}
	{/snippet}
</QuizGate>

<style>
	:global(.quiz-block) {
		border: 1px solid var(--quiz-block-border-color);
		border-radius: 10px;
		padding: 12px;
		margin: 2px; /* offset from in-editor outline */
	}

	:global(.quiz-block .quiz-form) {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.quiz-title {
		&:not(:empty) {
			padding: 0 4px 24px;
		}

		:global(p) {
			margin-top: 0;

			&:last-of-type {
				margin-bottom: 0;
			}
		}

	}

    :global(.quiz-block .quiz-actions) {
		display: flex;
		align-items: stretch;
		gap: 8px;
		padding-top: 30px;
	}
</style>
