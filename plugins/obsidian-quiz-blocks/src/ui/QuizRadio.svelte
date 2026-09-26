<script lang="ts">
	import type { Quiz, QuizOption } from "../schemas";
	import InlineMarkdown from "./InlineMarkdown.svelte";
	import type { AppContext } from "../markdown";
	import Icon from "./Icon.svelte";
	import type { QuizSavedState } from "../persistence";
	import { initial } from "./initial";
	import QuizResultBadge from "./QuizResultBadge.svelte";

	type SavedState = Extract<QuizSavedState, { type: "radio" }>;

	interface Props {
		ctx: AppContext,
		quiz: Extract<Quiz, { type: "radio" }>;
		stableId: string;
		savedState?: SavedState;
		onStateChange: (state: SavedState) => void;
		onFinish: () => void;
		onReset: () => void;
	}

	let { ctx, stableId, quiz, savedState, onStateChange, onFinish, onReset }: Props = $props();
	let selectedId = $state<string | null>(initial(() => savedState?.selectedId ?? null));
	let frozen = $state(initial(() => savedState?.frozen ?? false));

	function optionId(opt: QuizOption): string {
		return opt.id ?? opt.content;
	}

	function save(nextSelectedId: string | null, nextFrozen: boolean) {
		onStateChange({ type: "radio", selectedId: nextSelectedId, frozen: nextFrozen });
	}

	let isAnswerCorrect = $derived(
		selectedId !== null && quiz.options.some((opt) => optionId(opt) === selectedId && opt.correct)
	);

	function toggle(id: string) {
		if (frozen) return;
		selectedId = id;
		save(id, frozen);
	}

	function onCheck() {
		if (!selectedId) return;
		frozen = true;
		save(selectedId, true);
		onFinish();
	}

	function reset() {
		selectedId = null;
		frozen = false;
		onReset();
	}
</script>

<form class="quiz-form">
	{#each quiz.options as opt (optionId(opt))}
		{@const id = optionId(opt)}
		{@const selected = id === selectedId}
		{@const checked = frozen && opt.correct || selected}
		{@const missed = frozen && opt.correct && !selected}
		{@const mistaken = frozen && !opt.correct && selected}

		<div class="quiz-option" class:selected={selected} class:frozen={frozen}>
			<label class="option-label">
				<div
					class={["option-indicator", "radio"]}
					class:frozen={frozen}
					class:correct={opt.correct}
					class:selected={selected}
				>
					<span class="visually-hidden">
						<input
							type="radio"
							name={stableId}
							value={id}
							disabled={frozen}
							checked={selected}
							aria-checked={checked ? "true" : "false"}
							onchange={() => toggle(id)}
						/>
					</span>
					<Icon icon={mistaken ? "close" : (missed ? "minus" : (frozen && selected ? "tick" : "none"))}/>
				</div>

				<div class="quiz-option-text">
					<InlineMarkdown {ctx} markdown={opt.content}/>
				</div>
			</label>

			{#if opt.feedback && frozen && (opt.correct || selected)}
				<div class="option-feedback" class:is-correct={opt.correct} class:is-wrong={!opt.correct}>
					<InlineMarkdown {ctx} markdown={opt.feedback}/>
				</div>
			{/if}
		</div>
	{/each}
</form>

<div class="quiz-actions">
	{#if !frozen}
		<button class="quiz-check" type="button" onclick={onCheck} disabled={selectedId === null}>
			Check
		</button>
	{:else}
		<button class="quiz-reset" type="button" onclick={reset} aria-label="Reset quiz" title="Reset quiz">
			↻
		</button>
		<QuizResultBadge correct={isAnswerCorrect}/>
	{/if}
</div>

<style>
	@import "./QuizOption.css";
</style>
