# poc-cloud-deploy

## Elevator pitch (3 lines)
Minimal FastAPI service deployed on Cloud Run, demonstrating containerization, buildpacks usage, environment variables, and managed scaling.  
Proves that cloud-native deployment skills extend beyond RAG and into general-purpose API hosting.  
Designed to show recruiters you can deploy any microservice quickly, cleanly, and reproducibly.

## What this proves (3 bullets)
- Ability to package a FastAPI service with either Docker or Cloud Buildpacks.  
- Correct service configuration: env vars, scaling settings, IAM, and health checks.  
- Independent Cloud Run deployment with working `/health` and `/query` endpoints.

## Quick start
1. Install Python dependencies: `pip install -r requirements.txt`  
2. Run locally: `uvicorn app.main:app --reload`  
3. Deploy with Buildpacks: `gcloud run deploy poc-cloud-deploy --source . --region=<region>`  
4. Add environment variables in the Cloud Run console or via CLI.

## Live demo
- Service URL: _(add after deployment)_  
- Demo GIF: docs/demo.gif

## Repo layout
- `app/` — FastAPI router, endpoints, app factory  
- `src/` — supporting utils  
- `tests/` — placeholder for endpoint tests  
- `docs/` — architecture, implementation notes, run instructions

## Tech stack
FastAPI, Python, Cloud Run, Cloud Buildpacks, Docker (optional)

## License
MIT
