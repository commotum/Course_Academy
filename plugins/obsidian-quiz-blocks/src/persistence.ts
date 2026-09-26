export type QuizPair = {
	left: string;
	right: string;
};

export type QuizSavedState =
	| { type: "radio"; selectedId: string | null; frozen: boolean }
	| { type: "checkbox"; selectedIds: string[]; frozen: boolean }
	| { type: "select"; answers: string[]; frozen: boolean }
	| { type: "multi-select"; answers: string[]; frozen: boolean }
	| { type: "noodle"; pairs: QuizPair[]; frozen: boolean }
	| { type: "free"; answer: string; frozen: boolean }
	| { type: "blank"; answers: string[]; checked: boolean };

export type QuizBlocksData = {
	version: 1;
	quizStates: Record<string, QuizSavedState>;
};

export interface QuizStateStore {
	getQuizState(key: string): QuizSavedState | undefined;
	setQuizState(key: string, state: QuizSavedState): void;
	clearQuizState(key: string): void;
}

export function createEmptyQuizBlocksData(): QuizBlocksData {
	return {
		version: 1,
		quizStates: {},
	};
}

export function normalizeQuizBlocksData(value: unknown): QuizBlocksData {
	const data = createEmptyQuizBlocksData();
	if (!isRecord(value) || !isRecord(value.quizStates)) return data;

	for (const [key, state] of Object.entries(value.quizStates)) {
		const normalized = normalizeQuizSavedState(state);
		if (normalized) data.quizStates[key] = normalized;
	}

	return data;
}

function normalizeQuizSavedState(value: unknown): QuizSavedState | null {
	if (!isRecord(value) || typeof value.type !== "string") return null;

	const frozen = value.frozen === true;

	switch (value.type) {
		case "radio":
			return {
				type: "radio",
				selectedId: typeof value.selectedId === "string" ? value.selectedId : null,
				frozen,
			};
		case "checkbox":
			return {
				type: "checkbox",
				selectedIds: uniqueStrings(value.selectedIds),
				frozen,
			};
		case "select":
		case "multi-select":
			return {
				type: value.type,
				answers: strings(value.answers),
				frozen,
			};
		case "noodle":
			return {
				type: "noodle",
				pairs: pairs(value.pairs),
				frozen,
			};
		case "free":
			return {
				type: "free",
				answer: typeof value.answer === "string" ? value.answer : "",
				frozen,
			};
		case "blank":
			return {
				type: "blank",
				answers: strings(value.answers),
				checked: value.checked === true,
			};
		default:
			return null;
	}
}

function isRecord(value: unknown): value is Record<string, unknown> {
	return typeof value === "object" && value !== null && !Array.isArray(value);
}

function strings(value: unknown): string[] {
	return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
}

function uniqueStrings(value: unknown): string[] {
	return Array.from(new Set(strings(value)));
}

function pairs(value: unknown): QuizPair[] {
	if (!Array.isArray(value)) return [];

	return value.flatMap((item): QuizPair[] => {
		if (!isRecord(item) || typeof item.left !== "string" || typeof item.right !== "string") return [];
		return [{ left: item.left, right: item.right }];
	});
}
