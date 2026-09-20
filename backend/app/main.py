"""Point d'entrée de l'API SAFQA."""

import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.extraction import extract_text

# Stockage local temporaire (Étape 1). Sera remplacé par Supabase Storage
# à une étape ultérieure — voir cahier des charges.
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

app = FastAPI(
    title="SAFQA API",
    description=(
        "API de détection d'anomalies dans les dossiers d'appels d'offres "
        "publics marocains (marchés de travaux communaux)."
    ),
    version="0.0.0",
)

# Le frontend Next.js tourne sur localhost:3000 en développement.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Vérifie que l'API est en ligne."""
    return {"status": "ok", "service": "safqa-api"}


@app.post("/upload")
async def upload_document(file: UploadFile) -> dict[str, str | int]:
    """Reçoit un document (CPS, RC, Avis, Bordereau...) et confirme sa réception.

    Étape 1 de la roadmap : aucune extraction ni analyse ici, uniquement
    la validation du type de fichier et la confirmation de réception.
    """
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Type de fichier non supporté : '{extension}'. "
            f"Formats acceptés : {', '.join(sorted(ALLOWED_EXTENSIONS))}.",
        )

    document_id = str(uuid.uuid4())
    destination = UPLOAD_DIR / f"{document_id}{extension}"

    contents = await file.read()
    destination.write_bytes(contents)

    return {
        "id": document_id,
        "filename": file.filename or "",
        "size_bytes": len(contents),
        "content_type": file.content_type or "",
        "status": "reçu",
    }


def _find_stored_document(document_id: str) -> Path:
    matches = list(UPLOAD_DIR.glob(f"{document_id}.*"))
    if not matches:
        raise HTTPException(status_code=404, detail="Document introuvable.")
    return matches[0]


@app.get("/documents/{document_id}/text")
def get_document_text(document_id: str) -> dict[str, str | int]:
    """Extrait et retourne le texte brut d'un document déjà uploadé.

    Étape 2 de la roadmap : uniquement l'extraction brute, aucune
    interprétation ni comparaison entre documents à ce stade.
    """
    path = _find_stored_document(document_id)

    try:
        text = extract_text(path)
    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=f"Échec de l'extraction du texte : {error}",
        ) from error

    return {
        "id": document_id,
        "text": text,
        "char_count": len(text),
    }
