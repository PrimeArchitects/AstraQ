# syntax=docker/dockerfile:1

FROM node:20-slim AS base
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1

# --- Dependencies layer (cached separately from source) ---
FROM base AS deps
COPY package.json package-lock.json ./
RUN npm ci

# --- Development image: live reload ---
FROM deps AS development
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# --- Builder: production build ---
FROM deps AS builder
COPY . .
RUN npm run build

# --- Production image: standalone output, non-root ---
FROM base AS production
RUN addgroup --system --gid 1001 astrasphere && \
    adduser --system --uid 1001 astrasphere
COPY --from=builder --chown=astrasphere:astrasphere /app/public ./public
COPY --from=builder --chown=astrasphere:astrasphere /app/.next/standalone ./
COPY --from=builder --chown=astrasphere:astrasphere /app/.next/static ./.next/static
USER astrasphere
EXPOSE 3000
ENV PORT=3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node -e "fetch('http://localhost:3000').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
CMD ["node", "server.js"]
