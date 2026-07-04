/** Central place for the FastAPI base URL — server-side code must use
 * the internal Docker-network hostname, browser code the public one. */
export function getBackendUrl(): string {
  return (
    process.env.BACKEND_INTERNAL_URL ??
    process.env.NEXT_PUBLIC_API_BASE_URL ??
    "http://localhost:8000/api/v1"
  );
}
