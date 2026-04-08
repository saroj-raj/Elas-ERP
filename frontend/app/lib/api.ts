const LEGACY_API_BASE = 'https://vizpilot-api.onrender.com';
const PRODUCTION_API_BASE = 'https://vizpilot.onrender.com';

const normalizeApiBase = (value?: string) => {
  const trimmedValue = value?.trim().replace(/\/$/, '');

  if (!trimmedValue) {
    return undefined;
  }

  return trimmedValue === LEGACY_API_BASE ? PRODUCTION_API_BASE : trimmedValue;
};

const getApiBase = () => {
  const configuredBase = normalizeApiBase(process.env.NEXT_PUBLIC_API_BASE);
  const isLocalHost = typeof window !== 'undefined' && ['localhost', '127.0.0.1'].includes(window.location.hostname);
  const configuredIsLocalHost = configuredBase ? /localhost|127\.0\.0\.1/i.test(configuredBase) : false;

  if (configuredBase && (!configuredIsLocalHost || isLocalHost)) {
    return configuredBase;
  }

  return isLocalHost ? 'http://localhost:8000' : PRODUCTION_API_BASE;
};

export const API_BASE = getApiBase();

export async function uploadDemoFile(fd: FormData) {
	const res = await fetch(`${API_BASE}/api/upload`, { method: 'POST', body: fd });
	if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
	return res.json();
}
