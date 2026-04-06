const DEFAULT_BACKEND_BASE = process.env.NEXT_PUBLIC_API_BASE || (typeof window !== 'undefined' && window.location.hostname === 'localhost'
  ? 'http://localhost:8000'
  : 'https://vizpilot.onrender.com');

export const API_BASE = DEFAULT_BACKEND_BASE;

export async function uploadDemoFile(fd: FormData) {
	const res = await fetch(`${API_BASE}/api/upload`, { method: 'POST', body: fd });
	if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
	return res.json();
}
