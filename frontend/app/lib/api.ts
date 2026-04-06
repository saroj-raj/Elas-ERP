const getApiBase = () => {
  const configuredBase = process.env.NEXT_PUBLIC_API_BASE?.trim();
  const isLocalHost = typeof window !== 'undefined' && ['localhost', '127.0.0.1'].includes(window.location.hostname);
  const configuredIsLocalHost = configuredBase ? /localhost|127\.0\.0\.1/i.test(configuredBase) : false;

  if (configuredBase && (!configuredIsLocalHost || isLocalHost)) {
    return configuredBase.replace(/\/$/, '');
  }

  return isLocalHost ? 'http://localhost:8000' : 'https://vizpilot.onrender.com';
};

export const API_BASE = getApiBase();

export async function uploadDemoFile(fd: FormData) {
	const res = await fetch(`${API_BASE}/api/upload`, { method: 'POST', body: fd });
	if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
	return res.json();
}
