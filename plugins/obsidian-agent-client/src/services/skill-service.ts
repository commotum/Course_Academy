/**
 * Skill Service
 *
 * Discovers Codex agent skills for $-invocation suggestions.
 *
 * Skill authoring locations follow the Codex skill docs:
 * - repo-scoped .agents/skills from cwd up to repository root
 * - user-scoped ~/.agents/skills
 * - admin-scoped /etc/codex/skills
 *
 * Codex installations also expose bundled and plugin skills under CODEX_HOME
 * (default ~/.codex), so those locations are scanned as well.
 */

import {
	existsSync,
	readFileSync,
	readdirSync,
	realpathSync,
	statSync,
} from "fs";
import { dirname, join, resolve } from "path";
import { homedir } from "os";

// ============================================================================
// Types
// ============================================================================

export type SkillScope = "repo" | "user" | "admin" | "system" | "plugin";

export interface SkillSuggestion {
	/** Invocation name inserted into the prompt, without the leading $ */
	name: string;
	/** Short trigger description from SKILL.md frontmatter */
	description: string;
	/** Absolute path to the SKILL.md file */
	path: string;
	/** Discovery scope for display/debugging */
	scope: SkillScope;
}

interface SkillRoot {
	path: string;
	scope: SkillScope | "codex";
	maxDepth: number;
}

interface CachedSkills {
	cwd: string;
	timestamp: number;
	skills: SkillSuggestion[];
}

// ============================================================================
// Constants
// ============================================================================

const SKILL_FILE_NAME = "SKILL.md";
const SKILL_CACHE_TTL_MS = 10_000;
const MAX_SKILLS_PER_SCAN = 500;

let cachedSkills: CachedSkills | null = null;

// ============================================================================
// Public API
// ============================================================================

/**
 * List Codex skills visible from a working directory.
 */
export function listCodexSkills(cwd: string): SkillSuggestion[] {
	const normalizedCwd = resolve(cwd || process.cwd());
	const now = Date.now();

	if (
		cachedSkills &&
		cachedSkills.cwd === normalizedCwd &&
		now - cachedSkills.timestamp < SKILL_CACHE_TTL_MS
	) {
		return cachedSkills.skills;
	}

	const roots = getSkillRoots(normalizedCwd);
	const skillFiles = new Map<string, SkillRoot>();

	for (const root of roots) {
		for (const skillFile of findSkillFiles(root.path, root.maxDepth)) {
			const key = safeRealpath(skillFile) ?? skillFile;
			if (!skillFiles.has(key)) {
				skillFiles.set(key, root);
			}
			if (skillFiles.size >= MAX_SKILLS_PER_SCAN) break;
		}
		if (skillFiles.size >= MAX_SKILLS_PER_SCAN) break;
	}

	const skills = Array.from(skillFiles.entries())
		.map(([skillFile, root]) => parseSkillFile(skillFile, root.scope))
		.filter((skill): skill is SkillSuggestion => skill !== null)
		.sort(compareSkills);

	cachedSkills = { cwd: normalizedCwd, timestamp: now, skills };
	return skills;
}

// ============================================================================
// Discovery
// ============================================================================

function getSkillRoots(cwd: string): SkillRoot[] {
	const home = homedir();
	const codexHome = process.env.CODEX_HOME || join(home, ".codex");

	return dedupeRoots([
		...getRepoSkillRoots(cwd),
		{ path: join(home, ".agents", "skills"), scope: "user", maxDepth: 3 },
		{ path: join(codexHome, "skills"), scope: "codex", maxDepth: 5 },
		{
			path: join(codexHome, "plugins", "cache"),
			scope: "plugin",
			maxDepth: 8,
		},
		{ path: "/etc/codex/skills", scope: "admin", maxDepth: 3 },
	]);
}

function getRepoSkillRoots(cwd: string): SkillRoot[] {
	const roots: SkillRoot[] = [];
	let current = safeStat(cwd)?.isDirectory() ? cwd : dirname(cwd);

	while (true) {
		roots.push({
			path: join(current, ".agents", "skills"),
			scope: "repo",
			maxDepth: 3,
		});

		if (existsSync(join(current, ".git"))) {
			break;
		}

		const parent = dirname(current);
		if (parent === current) {
			break;
		}
		current = parent;
	}

	return roots;
}

function dedupeRoots(roots: SkillRoot[]): SkillRoot[] {
	const seen = new Set<string>();
	const result: SkillRoot[] = [];

	for (const root of roots) {
		const key = safeRealpath(root.path) ?? resolve(root.path);
		if (seen.has(key)) continue;
		seen.add(key);
		result.push(root);
	}

	return result;
}

function findSkillFiles(root: string, maxDepth: number): string[] {
	const result: string[] = [];
	const visited = new Set<string>();

	function visit(dir: string, depth: number) {
		if (depth < 0 || result.length >= MAX_SKILLS_PER_SCAN) return;

		const stat = safeStat(dir);
		if (!stat?.isDirectory()) return;

		const realPath = safeRealpath(dir) ?? resolve(dir);
		if (visited.has(realPath)) return;
		visited.add(realPath);

		const skillFile = join(dir, SKILL_FILE_NAME);
		if (safeStat(skillFile)?.isFile()) {
			result.push(skillFile);
			return;
		}

		let entries;
		try {
			entries = readdirSync(dir, { withFileTypes: true });
		} catch {
			return;
		}

		for (const entry of entries) {
			if (entry.name === "node_modules" || entry.name === ".git") {
				continue;
			}
			const childPath = join(dir, entry.name);
			const childStat = entry.isDirectory()
				? safeStat(childPath)
				: entry.isSymbolicLink()
					? safeStat(childPath)
					: null;
			if (childStat?.isDirectory()) {
				visit(childPath, depth - 1);
			}
		}
	}

	visit(root, maxDepth);
	return result;
}

// ============================================================================
// Parsing
// ============================================================================

function parseSkillFile(
	skillFile: string,
	rootScope: SkillRoot["scope"],
): SkillSuggestion | null {
	let content: string;
	try {
		content = readFileSync(skillFile, "utf8");
	} catch {
		return null;
	}

	const frontmatter = parseFrontmatter(content);
	const rawName = frontmatter.get("name");
	if (!rawName) return null;

	const scope = getEffectiveScope(skillFile, rootScope);
	const name =
		scope === "plugin"
			? prefixPluginSkillName(skillFile, rawName)
			: rawName;

	return {
		name,
		description: frontmatter.get("description") ?? "",
		path: skillFile,
		scope,
	};
}

function parseFrontmatter(content: string): Map<string, string> {
	const result = new Map<string, string>();
	if (!content.startsWith("---")) return result;

	const endMatch = content.slice(3).match(/\r?\n---\r?\n/);
	if (!endMatch || endMatch.index === undefined) return result;

	const frontmatter = content.slice(3, 3 + endMatch.index);
	for (const line of frontmatter.split(/\r?\n/)) {
		const match = /^([A-Za-z0-9_-]+):\s*(.*)$/.exec(line);
		if (!match) continue;
		result.set(match[1], stripQuotes(match[2].trim()));
	}

	return result;
}

function stripQuotes(value: string): string {
	if (
		(value.startsWith('"') && value.endsWith('"')) ||
		(value.startsWith("'") && value.endsWith("'"))
	) {
		return value.slice(1, -1);
	}
	return value;
}

function getEffectiveScope(
	skillFile: string,
	rootScope: SkillRoot["scope"],
): SkillScope {
	if (rootScope !== "codex") {
		return rootScope;
	}
	const parts = splitPath(skillFile);
	return parts.includes(".system") ? "system" : "user";
}

function prefixPluginSkillName(skillFile: string, name: string): string {
	if (name.includes(":")) return name;

	const parts = splitPath(skillFile);
	const skillsIndex = parts.lastIndexOf("skills");
	const pluginName = skillsIndex >= 2 ? parts[skillsIndex - 2] : null;
	return pluginName ? `${pluginName}:${name}` : name;
}

// ============================================================================
// Utilities
// ============================================================================

function compareSkills(a: SkillSuggestion, b: SkillSuggestion): number {
	const scopeOrder: Record<SkillScope, number> = {
		repo: 0,
		user: 1,
		system: 2,
		plugin: 3,
		admin: 4,
	};
	const scopeDelta = scopeOrder[a.scope] - scopeOrder[b.scope];
	if (scopeDelta !== 0) return scopeDelta;
	return a.name.localeCompare(b.name);
}

function safeStat(path: string): ReturnType<typeof statSync> | null {
	try {
		return statSync(path);
	} catch {
		return null;
	}
}

function safeRealpath(path: string): string | null {
	try {
		return realpathSync(path);
	} catch {
		return null;
	}
}

function splitPath(path: string): string[] {
	return path.replace(/\\/g, "/").split("/").filter(Boolean);
}
