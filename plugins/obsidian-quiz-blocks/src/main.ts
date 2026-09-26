import { Plugin } from "obsidian";
import {
	blankSnippet,
	checkboxSnippet,
	freeSnippet,
	multiSelectSnippet,
	noodleSnippet,
	radioSnippet,
	selectSnippet,
} from "./snippets";
import { renderQuiz } from "./renderer";
import { yamlSyntaxHighlighter } from "./syntax-highlighter/extension";
import {
	createEmptyQuizBlocksData,
	normalizeQuizBlocksData,
	type QuizBlocksData,
	type QuizSavedState,
	type QuizStateStore,
} from "./persistence";

export default class QuizBlocksPlugin extends Plugin implements QuizStateStore {
	private data: QuizBlocksData = createEmptyQuizBlocksData();
	private saveTimer: number | null = null;

	async onload() {
		this.data = normalizeQuizBlocksData(await this.loadData());

		this.registerEditorExtension(yamlSyntaxHighlighter);

		this.registerMarkdownCodeBlockProcessor("quiz", (source, el, ctx) => {
			renderQuiz({
				app: this.app,
				component: this,
				source,
				el,
				ctx,
			});
		});

		const snippets = [
			{ id: "quiz-block-insert-radio", name: "Insert radio", snippet: radioSnippet },
			{ id: "quiz-block-insert-checkbox", name: "Insert checkbox", snippet: checkboxSnippet },
			{ id: "quiz-block-insert-free", name: "Insert free", snippet: freeSnippet },
			{ id: "quiz-block-insert-blank", name: "Insert blank", snippet: blankSnippet },
			{ id: "quiz-block-insert-select", name: "Insert select", snippet: selectSnippet },
			{ id: "quiz-block-insert-multi-select", name: "Insert multi-select", snippet: multiSelectSnippet },
			{ id: "quiz-block-insert-noodle", name: "Insert noodle", snippet: noodleSnippet },
		];

		for (let { id, name, snippet } of snippets) {
			this.addCommand({
				id,
				name,
				editorCallback: editor => editor.replaceRange(snippet, editor.getCursor()),
			});
		}
	}

	onunload() {
		if (this.saveTimer !== null) {
			window.clearTimeout(this.saveTimer);
			this.saveTimer = null;
			void this.saveData(this.data);
		}
	}

	getQuizState(key: string): QuizSavedState | undefined {
		return this.data.quizStates[key];
	}

	setQuizState(key: string, state: QuizSavedState): void {
		this.data.quizStates[key] = state;
		this.queueSave();
	}

	clearQuizState(key: string): void {
		if (!(key in this.data.quizStates)) return;
		delete this.data.quizStates[key];
		this.queueSave();
	}

	private queueSave(): void {
		if (this.saveTimer !== null) window.clearTimeout(this.saveTimer);

		this.saveTimer = window.setTimeout(() => {
			this.saveTimer = null;
			void this.saveData(this.data);
		}, 250);
	}
}

declare module "obsidian" {
	interface Vault {
		getConfig(key: string): unknown;
	}
}
