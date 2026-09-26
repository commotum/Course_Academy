<script lang="ts">
	interface Props {
		correct: boolean;
	}

	let { correct }: Props = $props();
</script>

<span
	class="quiz-result-badge"
	class:is-correct={correct}
	class:is-wrong={!correct}
	role="status"
	aria-live="polite"
>
	{correct ? "Correct" : "Incorrect"}
</span>

<style>
	.quiz-result-badge {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		box-sizing: border-box;
		min-height: var(--input-height);
		padding: 0 12px;
		border-radius: var(--button-radius);
		color: white;
		-webkit-text-fill-color: white;
		font-family: inherit;
		font-size: var(--font-ui-small);
		font-weight: 700;
		line-height: var(--line-height-tight);
	}

	.quiz-result-badge.is-correct {
		background-color: var(--quiz-right);
	}

	.quiz-result-badge.is-wrong {
		background-color: var(--quiz-wrong);
	}
</style>
