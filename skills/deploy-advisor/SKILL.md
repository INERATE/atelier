---
name: deploy-advisor
description: The Atelier deployment advisor — where to host frontend, backend, database, and workers, with real cost expectations. Load when choosing hosting, estimating costs, or setting up deploys/CI.
---

# Deploy Advisor

Recommend the cheapest option that meets the requirement; always tell the user
the cost BEFORE they choose. Never pay for idle when scale-to-zero exists.

## Frontend (static / Next.js)

| Platform | Cost | Pick when |
|----------|------|-----------|
| Cloudflare Pages/Workers | Free tier generous; paid from **$5/mo** (pay only when code runs) | Default for landing/static + edge SSR; unmetered bandwidth |
| Vercel | Hobby free; Pro **$20/user/mo** | Heavy Next.js features, preview deploys, team workflow |
| GitHub Pages | Free | Pure static docs/sites |

## Backend (APIs, SSE/WebSockets, workers)

| Platform | Cost | Pick when |
|----------|------|-----------|
| Google Cloud Run | Scale-to-zero; ~free small loads | Containerized API, spiky traffic |
| Cloudflare Workers/DO | $5/mo base; $0.15/M requests | Edge APIs, real-time DO, queues |
| Oracle Cloud free tier | **$0** (4 ARM OCPU / 24GB — always free) | A real VPS for free; Celery/Redis/Postgres self-host |
| Hostinger / cheap VPS | ~$5–10/mo | Full control, predictable bill |
| AWS EC2 t3.micro / ECS Fargate | ~$8/mo+ / per-vCPU-hr | Team already on AWS |
| **Cloudflare Tunnel** | Free | Expose home/VPS backend with zero port-forwarding + DDoS protection |

## Data & services

| Need | Default | Cost |
|------|---------|------|
| Postgres | Neon / Supabase free tier → managed when serious | $0 → ~$19–25/mo |
| Redis (cache/queues) | Upstash free tier / self-host on VPS | $0+ |
| Object storage | R2 (no egress fees) or S3 | R2 free 10GB |
| Video | Cloudflare Stream (HLS) | per-minute pricing |
| Email | SES (cheapest at scale) / Mailgun to start | ~$0.10/1k |

## Decision rules

- Landing page → Cloudflare Pages. App with SSR → Vercel or CF Workers.
- API with few users → Cloud Run (scale-to-zero) or Oracle free VPS + Tunnel.
- WebSockets/live → Durable Objects or a VPS; NOT serverless functions.
- Workers/queues (Celery) need an always-on host → VPS or containers, never lambda.
- CI/CD: GitHub Actions → build Docker → push GHCR → deploy hook; frontends
  auto-deploy from git (Vercel/Pages).
- Always produce a monthly-cost table in the plan; flag anything metered.
