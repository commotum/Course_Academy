<script lang="ts">
	import type { Quiz, QuizChoiceQuestion, QuizMultiSelectQuestion, QuizOption } from "../schemas";
	import InlineMarkdown from "./InlineMarkdown.svelte";
	import { type AppContext } from "../markdown";
	import type { QuizSavedState } from "../persistence";
	import { initial } from "./initial";
	import QuizResultBadge from "./QuizResultBadge.svelte";

	type ChoiceQuiz = Extract<Quiz, { type: "select" | "multi-select" }>;
	type ChoiceQuestion = QuizChoiceQuestion | QuizMultiSelectQuestion;
	type SavedState = Extract<QuizSavedState, { type: "select" | "multi-select" }>;

	interface Props {
		ctx: AppContext,
		quiz: ChoiceQuiz;
		savedState?: SavedState;
		onStateChange: (state: SavedState) => void;
		onFinish: () => void;
		onReset: () => void;
	}

	let { ctx, quiz, savedState, onStateChange, onFinish, onReset }: Props = $props();
	let answers = $state<string[]>(initial(() => normalizeAnswers(savedState?.answers ?? [], quiz.questions.length)));
	let frozen = $state(initial(() => savedState?.frozen ?? false));
	let openIndex = $state<number | null>(null);

	function optionId(opt: QuizOption): string {
		return opt.id ?? opt.content;
	}

	function questionOptions(q: ChoiceQuestion): QuizOption[] {
		return quiz.type === "multi-select" ? (q as QuizMultiSelectQuestion).options : quiz.options;
	}

	function normalizeAnswers(values: string[], length: number): string[] {
		return Array.from({ length }, (_, i) => values[i] ?? "");
	}

	function save(nextAnswers: string[], nextFrozen: boolean) {
		if (quiz.type === "multi-select") {
			onStateChange({ type: "multi-select", answers: nextAnswers, frozen: nextFrozen });
		} else {
			onStateChange({ type: "select", answers: nextAnswers, frozen: nextFrozen });
		}
	}

	function setAnswer(i: number, value: string) {
		const next = [...answers];
		next[i] = value;
		answers = next;
		save(next, frozen);
		openIndex = null;
	}

	let questionCount = $derived(quiz.questions.length);
	let questionsLeft = $derived(Math.max(0, questionCount - answers.filter(Boolean).length));

	$effect(() => {
		if (answers.length !== questionCount) {
			answers = normalizeAnswers(answers, questionCount);
		}
	});

	function onCheck() {
		openIndex = null;
		frozen = true;
		save(answers, true);
		onFinish();
	}

	function reset() {
		answers = Array(questionCount).fill("");
		frozen = false;
		openIndex = null;
		onReset();
	}

	function toggleDropdown(i: number) {
		openIndex = openIndex === i ? null : i;
	}

	function closeOnOutsideClick(node: HTMLElement, params: { index: number }) {
		let index = params.index;
		const onPointerDown = (event: PointerEvent) => {
			if (openIndex !== index) return;
			if (event.target instanceof Node && node.contains(event.target)) return;
			openIndex = null;
		};

		document.addEventListener("pointerdown", onPointerDown, true);

		return {
			update(next: { index: number }) {
				index = next.index;
			},
			destroy() {
				document.removeEventListener("pointerdown", onPointerDown, true);
			},
		};
	}

	function selectedOption(q: ChoiceQuestion, id: string) {
		if (!id) return undefined;
		return questionOptions(q).find((o) => optionId(o) === id);
	}

	function isCorrect(q: ChoiceQuestion, selectedId: string) {
		return selectedId !== "" && q.correct_option === selectedId;
	}

	let isAnswerCorrect = $derived(quiz.questions.every((q, i) => isCorrect(q, answers[i] ?? "")));
</script>

<div class="quiz-choice">
	{#each quiz.questions as q, i (q.id ?? i)}
		{@const selectedId = answers[i] ?? ""}
		{@const options = questionOptions(q)}
		{@const selectedOpt = selectedOption(q, selectedId)}
		{@const correctOpt = selectedOption(q, q.correct_option)}
		{@const correct = selectedId ? isCorrect(q, selectedId) : false}

		<div class="quiz-choice-question">
			<div class="quiz-choice-question-text">
				<InlineMarkdown {ctx} markdown={q.content}/>
			</div>

			{#if !frozen}
				<div
					class="quiz-choice-select"
					class:is-placeholder={selectedId === ""}
					use:closeOnOutsideClick={{ index: i }}
				>
					<button
						class="quiz-choice-select-control"
						type="button"
						aria-haspopup="listbox"
						aria-expanded={openIndex === i}
						aria-label="Select an answer"
						onclick={() => toggleDropdown(i)}
					>
						<span class="quiz-choice-select-value">
							{#if selectedOpt}
								<InlineMarkdown {ctx} markdown={selectedOpt.content} tag="span"/>
							{:else}
								<span>Select an answer</span>
							{/if}
						</span>
						<span class="quiz-choice-select-arrow" aria-hidden="true"></span>
					</button>

					{#if openIndex === i}
						<div class="quiz-choice-select-menu" role="listbox" aria-label="Answer choices">
							{#each options as opt (optionId(opt))}
								{@const id = optionId(opt)}
								<button
									class="quiz-choice-select-option"
									class:is-selected={id === selectedId}
									type="button"
									role="option"
									aria-selected={id === selectedId}
									onclick={() => setAnswer(i, id)}
								>
									<InlineMarkdown {ctx} markdown={opt.content} tag="span"/>
								</button>
							{/each}
						</div>
					{/if}
				</div>
			{:else}
				<div class="quiz-choice-result">
					<div
						class="quiz-choice-select"
						class:is-correct={correct}
						class:is-wrong={!correct}
					>
						<button
							class="quiz-choice-select-control"
							type="button"
							aria-label="Selected answer"
							disabled
						>
							<span class="quiz-choice-select-value">
								{#if selectedOpt}
									<InlineMarkdown {ctx} markdown={selectedOpt.content} tag="span"/>
								{/if}
							</span>
							<span class="quiz-choice-select-arrow" aria-hidden="true"></span>
						</button>
					</div>

					{#if !correct && correctOpt}
						<div class="quiz-choice-feedback is-wrong">
							<span>Correct answer: </span>
							<InlineMarkdown {ctx} markdown={correctOpt.content}/>
						</div>
					{/if}

					{#if q.feedback}
						<div class="quiz-choice-feedback" class:is-correct={correct} class:is-wrong={!correct}>
							<InlineMarkdown {ctx} markdown={q.feedback}/>
						</div>
					{/if}
				</div>
			{/if}
		</div>
	{/each}
</div>

<div class="quiz-actions">
	{#if !frozen}
		<button class="quiz-check" type="button" onclick={onCheck} disabled={questionsLeft > 0}>
			{#if questionsLeft === 0}
				Check
			{:else}
				Check ({questionsLeft} questions left)
			{/if}
		</button>
	{:else}
		<button class="quiz-reset" type="button" onclick={reset} aria-label="Reset quiz" title="Reset quiz">
			↻
		</button>
		<QuizResultBadge correct={isAnswerCorrect}/>
	{/if}
</div>

<style>
	@import "QuizChoice.css";
</style>
