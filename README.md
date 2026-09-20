# SAFQA

Application de détection d'anomalies dans les dossiers d'appels d'offres publics marocains (marchés de travaux communaux), avant leur publication.

Voir le cahier des charges complet pour le contexte métier, la roadmap et les règles à encoder.

## Structure du projet

- `frontend/` — Next.js (React) + TypeScript, déployé sur Vercel.
- `backend/` — FastAPI (Python), déployé sur Railway/Render.

## Étape actuelle : 0 — Squelette du projet

Aucune fonctionnalité métier pour l'instant. Objectif : valider que les deux projets démarrent.

### Lancer le frontend

```bash
cd frontend
npm run dev
```

Ouvrir http://localhost:3000

### Lancer le backend

```bash
cd backend
python -m venv venv
# Windows : venv\Scripts\activate | macOS/Linux : source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Vérifier http://localhost:8000/health → `{"status": "ok", "service": "safqa-api"}`

Copier `backend/.env.example` en `backend/.env` pour les futures clés (Gemini, Supabase, Redis) — pas encore nécessaire à cette étape.
