import { Chat } from "@/components/Chat";
import { UploadPanel } from "@/components/UploadPanel";

export default function Home() {
  return (
    <div className="flex flex-1 justify-center gap-6 p-4">
      <Chat />
      <UploadPanel />
    </div>
  );
}
