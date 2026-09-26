<script lang="ts">
	import type { Quiz, QuizOption } from "../schemas";
	import InlineMarkdown from "./InlineMarkdown.svelte";
	import type { AppContext } from "../markdown";
	import Icon from "./Icon.svelte";
	import type { QuizSavedState } from "../persistence";
	import { initial } from "./initial";
	import QuizResultBadge from "./QuizResultBadge.svelte";

	type SavedState = Extract<QuizSavedState, { type: "checkbox" }>;

	interface Props {
		ctx: AppContext,
		quiz: Extract<Quiz, { type: "checkbox" }>;
		stableId: string;
		savedState?: SavedState;
		onStateChange: (state: SavedState) => void;
		onFinish: () => void;
		onReset: () => void;
	}

	let { ctx, stableId, quiz, savedState, onStateChange, onFinish, onReset }: Props = $props();
	let selectedIds = $state<Set<string>>(initial(() => new Set(savedState?.selectedIds ?? [])));
	let frozen = $state(initial(() => savedState?.frozen ?? false));

	function optionId(opt: QuizOption): string {
		return opt.id ?? opt.content;
	}

	function has(id: string): boolean {
		return selectedIds.has(id);
	}

	function save(nextSelectedIds: Set<string>, nextFrozen: boolean) {
		onStateChange({ type: "checkbox", selectedIds: [...nextSelectedIds], frozen: nextFrozen });
	}

	let correctIds = $derived(quiz.options.filter((opt) => opt.correct).map(optionId));
	let isAnswerCorrect = $derived(
		correctIds.length === selectedIds.size && correctIds.every((id) => selectedIds.has(id))
	);

	function toggle(id: string) {
		if (frozen) return;
		const next = new Set(selectedIds);
		next.has(id) ? next.delete(id) : next.add(id);
		selectedIds = next;
		save(next, frozen);
	}

	function onCheck() {
		if (selectedIds.size === 0) return;
		frozen = true;
		save(selectedIds, true);
		onFinish();
	}

	function reset() {
		selectedIds = new Set();
		frozen = false;
		onReset();
	}
</script>

<form class="quiz-form">
	{#each quiz.options as opt (optionId(opt))}
		{@const id = optionId(opt)}
		{@const selected = has(id)}
		{@const checked = frozen && opt.correct || selected}
		{@const missed = frozen && opt.correct && !selected}
		{@const mistaken = frozen && !opt.correct && selected}

		<div class="quiz-option" class:selected={selected} class:frozen={frozen}>
			<label class="option-label">
				<div
					class={["option-indicator", "checkbox"]}
					class:frozen={frozen}
					class:correct={opt.correct}
					class:selected={selected}
				>
					<span class="visually-hidden">
						<input
							type="checkbox"
							name={stableId}
							value={id}
							disabled={frozen}
							checked={selected}
							aria-checked={checked ? "true" : "false"}
							onchange={() => toggle(id)}
						/>
					</span>

					<div class="icon-host">
						<Icon icon={mistaken ? "close" : (missed ? "minus" : (selected ? "tick" : "none"))}/>
					</div>
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
		<button class="quiz-check" type="button" onclick={onCheck} disabled={selectedIds.size === 0}>
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
