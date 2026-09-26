<script lang="ts">
	import { type AppContext, renderInlineMarkdown } from "../markdown";

	interface Props {
		ctx: AppContext,
		markdown?: string;
		class?: string | string[];
		asPlainText?: boolean;
		tag?: "div" | "span";
	}

	let { ctx, markdown, class: cls = '', asPlainText = false, tag = "div" }: Props = $props();
	let host: HTMLElement;

	async function render() {
		if (!host) return;
		host.replaceChildren();
		await renderInlineMarkdown(ctx, markdown ?? "", host, asPlainText);
	}

	$effect(() => {
		ctx;
		markdown;
		void render();
	});
</script>

<svelte:element this={tag} class={cls} bind:this={host}></svelte:element>
