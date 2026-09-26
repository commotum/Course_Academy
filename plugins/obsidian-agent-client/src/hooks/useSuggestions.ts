import { useState, useCallback, useMemo, useRef } from "react";
import type { NoteMetadata, IVaultAccess } from "../services/vault-service";
import {
	detectMention,
	replaceMention,
	type MentionContext,
} from "../utils/mention-parser";
import type { SlashCommand } from "../types/session";
import type AgentClientPlugin from "../plugin";
import {
	listCodexSkills,
	type SkillSuggestion,
} from "../services/skill-service";

// ============================================================================
// Types
// ============================================================================

export interface MentionsState {
	/** Note suggestions matching the current mention query */
	suggestions: NoteMetadata[];
	/** Currently selected index in the dropdown */
	selectedIndex: number;
	/** Whether the dropdown is open */
	isOpen: boolean;
	/** Current mention context (query, position, etc.) */
	context: MentionContext | null;

	/** Update mention suggestions based on current input */
	updateSuggestions: (input: string, cursorPosition: number) => Promise<void>;
	/** Select a note from the dropdown. Returns updated input text */
	selectSuggestion: (input: string, suggestion: NoteMetadata) => string;
	/** Navigate the dropdown selection */
	navigate: (direction: "up" | "down") => void;
	/** Close the dropdown */
	close: () => void;

	/** Currently active note for auto-mention */
	activeNote: NoteMetadata | null;
	/** Whether auto-mention is temporarily disabled */
	isAutoMentionDisabled: boolean;
	/** Toggle auto-mention enabled/disabled state */
	toggleAutoMention: (disabled?: boolean) => void;
	/** Update the active note from the vault */
	updateActiveNote: () => Promise<void>;
}

export interface CommandsState {
	/** Filtered slash command suggestions */
	suggestions: SlashCommand[];
	/** Currently selected index in the dropdown */
	selectedIndex: number;
	/** Whether the dropdown is open */
	isOpen: boolean;

	/** Update slash command suggestions based on current input */
	updateSuggestions: (input: string, cursorPosition: number) => void;
	/** Select a slash command from the dropdown. Returns updated input text */
	selectSuggestion: (input: string, command: SlashCommand) => string;
	/** Navigate the dropdown selection */
	navigate: (direction: "up" | "down") => void;
	/** Close the dropdown */
	close: () => void;
}

export interface SkillContext {
	start: number;
	end: number;
	query: string;
}

export interface SkillsState {
	/** Filtered Codex skill suggestions */
	suggestions: SkillSuggestion[];
	/** Currently selected index in the dropdown */
	selectedIndex: number;
	/** Whether the dropdown is open */
	isOpen: boolean;
	/** Current skill invocation context */
	context: SkillContext | null;

	/** Update skill suggestions based on current input */
	updateSuggestions: (input: string, cursorPosition: number) => Promise<void>;
	/** Select a skill from the dropdown. Returns updated input text */
	selectSuggestion: (input: string, skill: SkillSuggestion) => string;
	/** Navigate the dropdown selection */
	navigate: (direction: "up" | "down") => void;
	/** Close the dropdown */
	close: () => void;
}

// Backward-compatible type aliases
export type UseMentionsReturn = MentionsState;
export type UseSlashCommandsReturn = CommandsState;

export interface UseSuggestionsReturn {
	/** Mention dropdown state and operations */
	mentions: MentionsState;
	/** Slash command dropdown state and operations */
	commands: CommandsState;
	/** Codex skill dropdown state and operations */
	skills: SkillsState;
}

// ============================================================================
// Helpers
// ============================================================================

function detectSkillInvocation(
	text: string,
	cursorPosition: number,
): SkillContext | null {
	if (cursorPosition < 0 || cursorPosition > text.length) {
		return null;
	}

	const textUpToCursor = text.slice(0, cursorPosition);
	const dollarIndex = textUpToCursor.lastIndexOf("$");
	if (dollarIndex === -1) {
		return null;
	}

	const beforeDollar = dollarIndex === 0 ? "" : text[dollarIndex - 1];
	if (beforeDollar && !/\s/.test(beforeDollar)) {
		return null;
	}

	const afterDollar = textUpToCursor.slice(dollarIndex + 1);
	if (/\s/.test(afterDollar)) {
		return null;
	}

	return {
		start: dollarIndex,
		end: cursorPosition,
		query: afterDollar,
	};
}

function filterSkills(
	skills: SkillSuggestion[],
	query: string,
): SkillSuggestion[] {
	const normalizedQuery = query.toLowerCase();

	return skills
		.filter((skill) => {
			if (!normalizedQuery) return true;
			return (
				skill.name.toLowerCase().includes(normalizedQuery) ||
				skill.description.toLowerCase().includes(normalizedQuery)
			);
		})
		.sort((a, b) => {
			const aScore = scoreSkill(a, normalizedQuery);
			const bScore = scoreSkill(b, normalizedQuery);
			if (aScore !== bScore) return aScore - bScore;
			return a.name.localeCompare(b.name);
		})
		.slice(0, 20);
}

function scoreSkill(skill: SkillSuggestion, query: string): number {
	if (!query) return 0;
	const name = skill.name.toLowerCase();
	if (name === query) return 0;
	if (name.startsWith(query)) return 1;
	if (name.includes(query)) return 2;
	return 3;
}

// ============================================================================
// Hook Implementation
// ============================================================================

/**
 * Hook for managing input suggestions (mentions + slash commands).
 *
 * Handles:
 * - @-mention detection, note searching, and dropdown interaction
 * - /-command filtering and selection
 * - Auto-mention toggle coordination (slash commands disable auto-mention)
 *
 * @param vaultAccess - Vault access for note searching
 * @param plugin - Plugin instance for settings and configuration
 * @param availableCommands - Available slash commands from the agent session
 * @param agentCwd - Agent working directory for repo-scoped skill discovery
 * @param activeAgentId - Current agent ID; skill suggestions are Codex-only
 */
export function useSuggestions(
	vaultAccess: IVaultAccess,
	plugin: AgentClientPlugin,
	availableCommands: SlashCommand[],
	agentCwd: string,
	activeAgentId: string,
): UseSuggestionsReturn {
	// ============================================================
	// Mention State
	// ============================================================

	const [mentionSuggestions, setMentionSuggestions] = useState<
		NoteMetadata[]
	>([]);
	const [mentionSelectedIndex, setMentionSelectedIndex] = useState(0);
	const [mentionContext, setMentionContext] = useState<MentionContext | null>(
		null,
	);
	const [activeNote, setActiveNote] = useState<NoteMetadata | null>(null);
	const [isAutoMentionDisabled, setIsAutoMentionDisabled] = useState(false);

	const mentionIsOpen =
		mentionSuggestions.length > 0 && mentionContext !== null;

	// ============================================================
	// Command State
	// ============================================================

	const [commandSuggestions, setCommandSuggestions] = useState<
		SlashCommand[]
	>([]);
	const [commandSelectedIndex, setCommandSelectedIndex] = useState(0);

	const commandIsOpen = commandSuggestions.length > 0;

	// ============================================================
	// Skill State
	// ============================================================

	const [skillSuggestions, setSkillSuggestions] = useState<SkillSuggestion[]>(
		[],
	);
	const [skillSelectedIndex, setSkillSelectedIndex] = useState(0);
	const [skillContext, setSkillContext] = useState<SkillContext | null>(null);
	const allSkillsRef = useRef<SkillSuggestion[] | null>(null);
	const allSkillsCwdRef = useRef<string | null>(null);

	const skillIsOpen = skillSuggestions.length > 0 && skillContext !== null;

	// ============================================================
	// Auto-mention toggle (shared between mentions and commands)
	// ============================================================

	const toggleAutoMention = useCallback((disabled?: boolean) => {
		if (disabled === undefined) {
			setIsAutoMentionDisabled((prev) => !prev);
		} else {
			setIsAutoMentionDisabled(disabled);
		}
	}, []);

	// ============================================================
	// Mention Callbacks
	// ============================================================

	const mentionUpdateSuggestions = useCallback(
		async (input: string, cursorPosition: number) => {
			const ctx = detectMention(input, cursorPosition);

			if (!ctx) {
				setMentionSuggestions([]);
				setMentionSelectedIndex(0);
				setMentionContext(null);
				return;
			}

			const results = await vaultAccess.searchNotes(ctx.query);
			setMentionSuggestions(results);
			setMentionSelectedIndex(0);
			setMentionContext(ctx);
		},
		[vaultAccess, plugin],
	);

	const mentionSelectSuggestion = useCallback(
		(input: string, suggestion: NoteMetadata): string => {
			if (!mentionContext) {
				return input;
			}

			const { newText } = replaceMention(
				input,
				mentionContext,
				suggestion.name,
			);

			setMentionSuggestions([]);
			setMentionSelectedIndex(0);
			setMentionContext(null);

			return newText;
		},
		[mentionContext],
	);

	const mentionNavigate = useCallback(
		(direction: "up" | "down") => {
			if (!mentionIsOpen) return;

			const maxIndex = mentionSuggestions.length - 1;
			setMentionSelectedIndex((prev) => {
				if (direction === "down") {
					return Math.min(prev + 1, maxIndex);
				} else {
					return Math.max(prev - 1, 0);
				}
			});
		},
		[mentionIsOpen, mentionSuggestions.length],
	);

	const mentionClose = useCallback(() => {
		setMentionSuggestions([]);
		setMentionSelectedIndex(0);
		setMentionContext(null);
	}, []);

	const updateActiveNote = useCallback(async () => {
		const note = await vaultAccess.getActiveNote();
		setActiveNote(note);
	}, [vaultAccess]);

	// ============================================================
	// Command Callbacks
	// ============================================================

	const commandUpdateSuggestions = useCallback(
		(input: string, cursorPosition: number) => {
			const wasOpen = commandSuggestions.length > 0;

			// Slash commands only trigger at the very beginning of input
			if (!input.startsWith("/")) {
				// Re-enable auto-mention only if dropdown was showing
				if (wasOpen) {
					toggleAutoMention(false);
				}
				setCommandSuggestions([]);
				setCommandSelectedIndex(0);
				return;
			}

			// Extract query after '/'
			const textUpToCursor = input.slice(0, cursorPosition);
			const afterSlash = textUpToCursor.slice(1);

			// If there's a space, the command is complete and user is typing arguments
			if (afterSlash.includes(" ")) {
				setCommandSuggestions([]);
				setCommandSelectedIndex(0);
				// Keep auto-mention disabled (slash command is still active)
				toggleAutoMention(true);
				return;
			}

			const query = afterSlash.toLowerCase();

			// Filter available commands
			const filtered = availableCommands.filter((cmd) =>
				cmd.name.toLowerCase().includes(query),
			);

			setCommandSuggestions(filtered);
			setCommandSelectedIndex(0);
			// Disable auto-mention when slash command is detected
			toggleAutoMention(true);
		},
		[availableCommands, toggleAutoMention, commandSuggestions.length],
	);

	const commandSelectSuggestion = useCallback(
		(_input: string, command: SlashCommand): string => {
			const commandText = `/${command.name} `;

			setCommandSuggestions([]);
			setCommandSelectedIndex(0);

			return commandText;
		},
		[],
	);

	const commandNavigate = useCallback(
		(direction: "up" | "down") => {
			if (commandSuggestions.length === 0) return;

			const maxIndex = commandSuggestions.length - 1;
			setCommandSelectedIndex((current) => {
				if (direction === "down") {
					return Math.min(current + 1, maxIndex);
				} else {
					return Math.max(current - 1, 0);
				}
			});
		},
		[commandSuggestions.length],
	);

	const commandClose = useCallback(() => {
		setCommandSuggestions([]);
		setCommandSelectedIndex(0);
	}, []);

	// ============================================================
	// Skill Callbacks
	// ============================================================

	const skillUpdateSuggestions = useCallback(
		async (input: string, cursorPosition: number) => {
			const ctx = detectSkillInvocation(input, cursorPosition);
			const isCodexAgent = activeAgentId === plugin.settings.codex.id;

			if (!ctx || !isCodexAgent) {
				setSkillSuggestions([]);
				setSkillSelectedIndex(0);
				setSkillContext(null);
				return;
			}

			if (!allSkillsRef.current || allSkillsCwdRef.current !== agentCwd) {
				allSkillsRef.current = listCodexSkills(agentCwd);
				allSkillsCwdRef.current = agentCwd;
			}

			const filtered = filterSkills(allSkillsRef.current, ctx.query);
			setSkillSuggestions(filtered);
			setSkillSelectedIndex(0);
			setSkillContext(ctx);
		},
		[activeAgentId, agentCwd, plugin.settings.codex.id],
	);

	const skillSelectSuggestion = useCallback(
		(input: string, skill: SkillSuggestion): string => {
			if (!skillContext) {
				return input;
			}

			const before = input.slice(0, skillContext.start);
			const after = input.slice(skillContext.end);
			const replacement = `$${skill.name} `;

			setSkillSuggestions([]);
			setSkillSelectedIndex(0);
			setSkillContext(null);

			return before + replacement + after;
		},
		[skillContext],
	);

	const skillNavigate = useCallback(
		(direction: "up" | "down") => {
			if (!skillIsOpen) return;

			const maxIndex = skillSuggestions.length - 1;
			setSkillSelectedIndex((current) => {
				if (direction === "down") {
					return Math.min(current + 1, maxIndex);
				} else {
					return Math.max(current - 1, 0);
				}
			});
		},
		[skillIsOpen, skillSuggestions.length],
	);

	const skillClose = useCallback(() => {
		setSkillSuggestions([]);
		setSkillSelectedIndex(0);
		setSkillContext(null);
	}, []);

	// ============================================================
	// Return
	// ============================================================

	const mentions = useMemo(
		() => ({
			suggestions: mentionSuggestions,
			selectedIndex: mentionSelectedIndex,
			isOpen: mentionIsOpen,
			context: mentionContext,
			updateSuggestions: mentionUpdateSuggestions,
			selectSuggestion: mentionSelectSuggestion,
			navigate: mentionNavigate,
			close: mentionClose,
			activeNote,
			isAutoMentionDisabled,
			toggleAutoMention,
			updateActiveNote,
		}),
		[
			mentionSuggestions,
			mentionSelectedIndex,
			mentionIsOpen,
			mentionContext,
			mentionUpdateSuggestions,
			mentionSelectSuggestion,
			mentionNavigate,
			mentionClose,
			activeNote,
			isAutoMentionDisabled,
			toggleAutoMention,
			updateActiveNote,
		],
	);

	const commands = useMemo(
		() => ({
			suggestions: commandSuggestions,
			selectedIndex: commandSelectedIndex,
			isOpen: commandIsOpen,
			updateSuggestions: commandUpdateSuggestions,
			selectSuggestion: commandSelectSuggestion,
			navigate: commandNavigate,
			close: commandClose,
		}),
		[
			commandSuggestions,
			commandSelectedIndex,
			commandIsOpen,
			commandUpdateSuggestions,
			commandSelectSuggestion,
			commandNavigate,
			commandClose,
		],
	);

	const skills = useMemo(
		() => ({
			suggestions: skillSuggestions,
			selectedIndex: skillSelectedIndex,
			isOpen: skillIsOpen,
			context: skillContext,
			updateSuggestions: skillUpdateSuggestions,
			selectSuggestion: skillSelectSuggestion,
			navigate: skillNavigate,
			close: skillClose,
		}),
		[
			skillSuggestions,
			skillSelectedIndex,
			skillIsOpen,
			skillContext,
			skillUpdateSuggestions,
			skillSelectSuggestion,
			skillNavigate,
			skillClose,
		],
	);

	return useMemo(
		() => ({ mentions, commands, skills }),
		[mentions, commands, skills],
	);
}
