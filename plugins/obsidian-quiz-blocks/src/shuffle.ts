import type { Quiz } from "./schemas";

export function shuffleOptions(quiz: Quiz, el: HTMLElement) {
	if (!("options" in quiz) && quiz.type !== "multi-select") return;

	const rand = mulberry32(getSeed(el));

	if ("options" in quiz) {
		shuffleWithRandom(quiz.options, rand);
	}

	if (quiz.type === "multi-select") {
		for (const q of quiz.questions) {
			shuffleWithRandom(q.options, rand);
		}
	}
}

function getSeed(el: HTMLElement): number {
	const existing = el.dataset.seed;
	if (existing) {
		const n = Number(existing);
		if (Number.isInteger(n) && n >= 0) return n >>> 0;
	}

	const seed = (Math.random() * 0x1_0000_0000) >>> 0;
	el.dataset.seed = String(seed);
	return seed;
}

function shuffleWithRandom<T>(arr: T[], rand: () => number) {
	for (let i = arr.length - 1; i > 0; i--) {
		const j = Math.floor(rand() * (i + 1));
		[arr[i], arr[j]] = [arr[j]!, arr[i]!];
	}
}

function mulberry32(seed: number) {
	let a = seed >>> 0;
	return () => {
		a |= 0;
		a = (a + 0x6D2B79F5) | 0;
		let t = Math.imul(a ^ (a >>> 15), 1 | a);
		t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
}
