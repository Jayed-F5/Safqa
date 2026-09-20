"use client";

import { useRef, useState } from "react";
import styles from "./UploadForm.module.css";

type UploadResult = {
  id: string;
  filename: string;
  size_bytes: number;
  content_type: string;
  status: string;
};

type UploadState =
  | { phase: "idle" }
  | { phase: "uploading" }
  | { phase: "success"; result: UploadResult }
  | { phase: "error"; message: string };

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} o`;
  return `${(bytes / 1024).toFixed(1)} Ko`;
}

export default function UploadForm() {
  const [state, setState] = useState<UploadState>({ phase: "idle" });
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const file = inputRef.current?.files?.[0];
    if (!file) return;

    setState({ phase: "uploading" });

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        setState({ phase: "error", message: data.detail ?? "Erreur inconnue." });
        return;
      }

      setState({ phase: "success", result: data as UploadResult });
      if (inputRef.current) inputRef.current.value = "";
    } catch {
      setState({
        phase: "error",
        message: "Impossible de contacter le serveur. Le backend est-il démarré ?",
      });
    }
  }

  return (
    <div className={styles.container}>
      <h1>SAFQA — Upload de document</h1>
      <p className={styles.subtitle}>
        Déposez un CPS, RC, Avis d&apos;appel d&apos;offres ou Bordereau des prix
        (PDF ou DOCX). Aucune analyse n&apos;est effectuée à cette étape.
      </p>

      <form onSubmit={handleSubmit} className={styles.form}>
        <input
          ref={inputRef}
          type="file"
          name="file"
          accept=".pdf,.docx"
          required
          className={styles.input}
        />
        <button
          type="submit"
          disabled={state.phase === "uploading"}
          className={styles.button}
        >
          {state.phase === "uploading" ? "Envoi en cours..." : "Uploader"}
        </button>
      </form>

      {state.phase === "success" && (
        <div className={`${styles.status} ${styles.success}`}>
          <strong>Document reçu ✓</strong>
          <ul>
            <li>Nom : {state.result.filename}</li>
            <li>Taille : {formatSize(state.result.size_bytes)}</li>
            <li>Type : {state.result.content_type}</li>
            <li>Id : {state.result.id}</li>
          </ul>
        </div>
      )}

      {state.phase === "error" && (
        <div className={`${styles.status} ${styles.error}`}>
          <strong>Erreur :</strong> {state.message}
        </div>
      )}
    </div>
  );
}
