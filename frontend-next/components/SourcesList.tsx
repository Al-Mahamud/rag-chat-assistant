import type { Source } from "@/lib/types";

export function SourcesList({ sources }: { sources: Source[] }) {
  if (sources.length === 0) {
    return null;
  }

  return (
    <details className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
      <summary className="cursor-pointer select-none">Sources</summary>
      <ul className="mt-1 list-inside list-disc">
        {sources.map((s, i) => (
          <li key={`${s.doc_name}-${s.page_no}-${i}`}>
            {s.doc_name}, p.{s.page_no} (score={s.score.toFixed(3)})
          </li>
        ))}
      </ul>
    </details>
  );
}
