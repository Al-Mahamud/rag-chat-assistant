"use client";

import { useRef, useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";

export function UploadPanel() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const file = fileInputRef.current?.files?.[0];
    if (!file) {
      return;
    }

    setIsUploading(true);
    setMessage(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/upload", { method: "POST", body: formData });

      if (response.status === 401) {
        router.push("/login");
        return;
      }

      if (response.status === 429) {
        setMessage({ type: "error", text: "Too many requests — please wait a moment and try again." });
        return;
      }

      const data = await response.json();

      if (!response.ok) {
        setMessage({ type: "error", text: data.detail ?? "Upload failed — please try again." });
        return;
      }

      setMessage({
        type: "success",
        text: `Indexed ${data.filename}: ${data.pages_indexed} page(s), ${data.chunks_indexed} chunk(s).`,
      });
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch {
      setMessage({ type: "error", text: "Could not reach the server. Please try again." });
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <div className="flex w-full max-w-xs flex-col gap-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
      <h2 className="font-semibold">Documents</h2>

      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          disabled={isUploading}
          className="text-sm"
        />
        <button
          type="submit"
          disabled={isUploading}
          className="rounded bg-zinc-900 px-3 py-1.5 text-sm text-white disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
        >
          {isUploading ? "Indexing..." : "Index this PDF"}
        </button>
      </form>

      {message && (
        <p
          className={
            message.type === "success"
              ? "text-sm text-green-700 dark:text-green-400"
              : "text-sm text-red-600 dark:text-red-400"
          }
        >
          {message.text}
        </p>
      )}

      <p className="text-xs text-zinc-500 dark:text-zinc-500">
        Uploaded files are indexed for this session only — the backend runs on a free tier with no
        persistent storage, so uploads are cleared on redeploy or after ~15 minutes of inactivity.
      </p>
    </div>
  );
}
