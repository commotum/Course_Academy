import { z } from "zod";

export const QUIZ_TYPES = ["radio", "checkbox", "free", "select", "multi-select", "noodle", "blank"] as const;

export const nullToUndefined = <T extends z.ZodType>(schema: T) =>
	z.preprocess((v) => (v === null ? undefined : v), schema);

const trimmedString = z.string().trim();
const scalarText = (schema: z.ZodString) => z.preprocess((v) => {
	if (typeof v === "string" || typeof v === "number" || typeof v === "boolean") return String(v);
	return v;
}, schema);
const requiredText = nullToUndefined(scalarText(trimmedString.min(1)));
const optionalText = nullToUndefined(scalarText(trimmedString)).default("");

const idSchema = z.preprocess((v) => {
	if (v === undefined || v === null) return undefined;
	return typeof v === "string" || typeof v === "number" || typeof v === "boolean" ? String(v) : v;
}, trimmedString.min(1));

const optionalIdSchema = idSchema.optional();

export const QuizOptionSchema = z.preprocess((input) => {
	if (input === null || input === undefined) return input;
	if (typeof input === "string" || typeof input === "number" || typeof input === "boolean") {
		const content = String(input);
		return { content, id: content };
	}
	if (typeof input !== "object") return input;

	const obj = input as Record<string, unknown>;
	const content = obj.content ?? obj.text ?? obj.answer ?? obj.option;
	const id = obj.id ?? content ?? undefined;

	// Strip aliases so strict() can catch real unknown keys.
	const rest = { ...obj } as Record<string, unknown>;
	delete rest.text;
	delete rest.answer;
	delete rest.option;

	return { ...rest, id, content };
}, z.object({
	id: optionalIdSchema,
	correct: nullToUndefined(z.boolean()).default(false),
	content: requiredText,
	feedback: optionalText,
}).strict());

function preprocessChoiceQuestion(input: unknown): unknown {
	if (typeof input !== "object" || input === null) return input;

	const obj = input as Record<string, unknown>;
	const content = obj.content ?? obj.text ?? obj.question;
	const correct_option =
		obj.correct_option ?? obj.correctOption ?? obj.correct ?? obj.correctId ?? obj.correct_option_id;

	// Strip aliases so strict() can catch real unknown keys.
	const rest = { ...obj } as Record<string, unknown>;
	delete rest.text;
	delete rest.question;
	delete rest.correctOption;
	delete rest.correct;
	delete rest.correctId;
	delete rest.correct_option_id;

	return { ...rest, content, correct_option };
}

const QuizChoiceQuestionBaseSchema = z.object({
	id: optionalIdSchema,
	content: requiredText,
	correct_option: idSchema,
	feedback: optionalText,
}).strict();

export const QuizChoiceQuestionSchema = z.preprocess(
	preprocessChoiceQuestion,
	QuizChoiceQuestionBaseSchema
);

export const QuizMultiSelectQuestionSchema = z.preprocess(
	preprocessChoiceQuestion,
	QuizChoiceQuestionBaseSchema.extend({
		options: z.array(QuizOptionSchema).min(1),
	}).strict()
);

// Common fields shared by all quizzes.
export const BaseQuizSchema = z.object({
	id: optionalIdSchema,
	content: optionalText,
	// `gated: true` hides quiz content until started, and (when active) hides the rest of the note.
	gated: nullToUndefined(z.boolean()).default(false),
	// `shuffle: true` mixes options on first render and keeps the seed in the element to ensure stability.
	shuffle: nullToUndefined(z.boolean()).default(false),
});

/* quiz types */

const QuizRadioSchema = createOptionQuizSchema("radio");
const QuizCheckboxSchema = createOptionQuizSchema("checkbox");

const QuizSelectSchema = createPairQuizSchema("select");
const QuizMultiSelectSchema = createMultiSelectQuizSchema();
const QuizNoodleSchema = createPairQuizSchema("noodle");

const QuizFreeSchema = BaseQuizSchema.extend({
	type: z.literal("free"),
	// Free-text quizzes can't be auto-graded (yet). This is the reference answer.
	correct: optionalText,
	// Optional extra feedback/explanation shown after checking.
	feedback: optionalText,
}).strict();

const QuizBlankSchema = BaseQuizSchema.extend({
	type: z.literal("blank"),
	// `require_exact: false` turns blanks into answer reveal fields instead of exact-match grading.
	require_exact: nullToUndefined(z.boolean()).default(true),
	// Optional extra feedback/explanation shown after checking.
	feedback: optionalText,
}).strict();

export const QuizSchema = z.preprocess((input) => {
	if (typeof input !== "object" || input === null) return input;

	const obj = input as Record<string, unknown>;
	const content = obj.content ?? obj.text ?? obj.question;
	const rest = { ...obj } as Record<string, unknown>;
	delete rest.text;
	delete rest.question;

	return { ...rest, content };
}, z.discriminatedUnion("type", [
	QuizRadioSchema,
	QuizCheckboxSchema,
	QuizFreeSchema,
	QuizSelectSchema,
	QuizMultiSelectSchema,
	QuizNoodleSchema,
	QuizBlankSchema,
]));

function enforceUniqueIds(
	kind: "options" | "questions",
	items: Array<{ id?: string }>,
	ctx: z.RefinementCtx,
	message: (id: string) => string,
	pathPrefix: PropertyKey[] = [kind],
): Set<string> {
	const ids = new Set<string>();
	items.forEach((item, i) => {
		if (!item.id) return;
		if (ids.has(item.id)) {
			ctx.addIssue({
				code: "custom",
				message: message(item.id),
				path: [...pathPrefix, i, "id"],
			});
		} else {
			ids.add(item.id);
		}
	});
	return ids;
}

function optionIdDuplicateMessage(id: string): string {
	return `Duplicate option id: ${id}. Add explicit ids or make content unique.`;
}

function questionIdDuplicateMessage(id: string): string {
	return `Duplicate question id: ${id}.`;
}

function createOptionQuizSchema<T extends "radio" | "checkbox">(type: T) {
	return BaseQuizSchema.extend({
		type: z.literal(type),
		options: z.array(QuizOptionSchema).min(1),
	})
		.strict()
		.superRefine((quiz, ctx) => {
			enforceUniqueIds("options", quiz.options, ctx, optionIdDuplicateMessage);
		});
}

function createPairQuizSchema<T extends "select" | "noodle">(type: T) {
	return BaseQuizSchema.extend({
		type: z.literal(type),
		options: z.array(QuizOptionSchema).min(1),
		questions: z.array(QuizChoiceQuestionSchema).min(1),
	})
		.strict()
		.superRefine((quiz, ctx) => {
			const ids = enforceUniqueIds("options", quiz.options, ctx, optionIdDuplicateMessage);
			enforceUniqueIds("questions", quiz.questions, ctx, questionIdDuplicateMessage);

			quiz.questions.forEach((q, i) => {
				if (!ids.has(q.correct_option)) {
					ctx.addIssue({
						code: "custom",
						message: `questions[${i}].correct_option references unknown option id: ${q.correct_option}`,
						path: ["questions", i, "correct_option"],
					});
				}
			});
		});
}

function createMultiSelectQuizSchema() {
	return BaseQuizSchema.extend({
		type: z.literal("multi-select"),
		questions: z.array(QuizMultiSelectQuestionSchema).min(1),
	})
		.strict()
		.superRefine((quiz, ctx) => {
			enforceUniqueIds("questions", quiz.questions, ctx, questionIdDuplicateMessage);

			quiz.questions.forEach((q, i) => {
				const ids = enforceUniqueIds(
					"options",
					q.options,
					ctx,
					optionIdDuplicateMessage,
					["questions", i, "options"],
				);

				if (!ids.has(q.correct_option)) {
					ctx.addIssue({
						code: "custom",
						message: `questions[${i}].correct_option references unknown option id: ${q.correct_option}`,
						path: ["questions", i, "correct_option"],
					});
				}
			});
		});
}

export type QuizOption = z.infer<typeof QuizOptionSchema>;
export type QuizChoiceQuestion = z.infer<typeof QuizChoiceQuestionSchema>;
export type QuizMultiSelectQuestion = z.infer<typeof QuizMultiSelectQuestionSchema>;
export type Quiz = z.infer<typeof QuizSchema>;
