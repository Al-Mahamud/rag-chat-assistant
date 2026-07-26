"use client";

import { useState, type FormEvent } from "react";
import { useRouter } from "next/navigation";
import { SourcesList } from "./SourcesList";
import type { Message } from "@/lib/types";

export function Chat() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const query = input.trim();
    if (!query || isLoading) {
      return;
    }

    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (response.status === 401) {
        router.push("/login");
        return;
      }

      if (response.status === 429) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: "You're sending messages too fast — please wait a moment and try again." },
        ]);
        return;
      }

      if (!response.ok) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: "The assistant hit an error — please try again." },
        ]);
        return;
      }

      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer, sources: data.sources },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Could not reach the server. Please check your connection and try again." },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex w-full max-w-2xl flex-1 flex-col gap-4 p-4">
      <div className="flex flex-1 flex-col gap-3 overflow-y-auto">
        {messages.map((message, i) => (
          <div
            key={i}
            className={
              message.role === "user"
                ? "self-end rounded-lg bg-zinc-900 px-4 py-2 text-white dark:bg-zinc-100 dark:text-zinc-900"
                : "self-start rounded-lg bg-zinc-100 px-4 py-2 dark:bg-zinc-800"
            }
          >
            <p>{message.content}</p>
            {message.sources && <SourcesList sources={message.sources} />}
          </div>
        ))}
        {isLoading && <p className="self-start text-zinc-500">Thinking...</p>}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about the company documents..."
          disabled={isLoading}
          className="flex-1 rounded border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="rounded bg-zinc-900 px-4 py-2 text-white disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
        >
          Send
        </button>
      </form>
    </div>
  );
}
