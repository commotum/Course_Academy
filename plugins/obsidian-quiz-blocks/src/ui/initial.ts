export function initial<T>(read: () => T): T {
	return read();
}
