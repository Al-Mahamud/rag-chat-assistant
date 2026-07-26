export type Source = {
  doc_name: string;
  page_no: number;
  score: number;
};

export type ChatResponse = {
  answer: string;
  sources: Source[];
};

export type UploadResponse = {
  filename: string;
  pages_indexed: number;
  chunks_indexed: number;
};

export type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};
