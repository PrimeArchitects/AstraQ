import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest';
import { api, ApiError } from '../api';

describe('api client', () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  it('returns parsed JSON on success', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ status: 'ok' }),
    });

    const result = await api.health();
    expect(result).toEqual({ status: 'ok' });
  });

  it('throws ApiError on non-2xx response', async () => {
    (global.fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      text: async () => 'boom',
    });

    await expect(api.health()).rejects.toBeInstanceOf(ApiError);
  });
});
