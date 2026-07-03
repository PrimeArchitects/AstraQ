"use client";

import { Upload } from "lucide-react";
import { useState, type ReactNode } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Modal, ModalClose, ModalContent, ModalTrigger } from "@/components/ui/modal";

/**
 * Upload flow UI only — no file is actually persisted or sent anywhere.
 * `handleSubmit` is the seam where a real upload mutation attaches once
 * the backend has an endpoint for it.
 */
export function UploadPaperModal({ trigger }: { trigger: ReactNode }) {
  const [open, setOpen] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);

  function handleSubmit() {
    // Placeholder only — wire to a real upload mutation once the
    // backend exposes a papers-ingest endpoint.
    setOpen(false);
    setFileName(null);
  }

  return (
    <Modal open={open} onOpenChange={setOpen}>
      <ModalTrigger asChild>{trigger}</ModalTrigger>
      <ModalContent
        title="Upload Research Paper"
        description="Add a PDF to your library. AI-assisted summarization attaches once that feature ships."
      >
        <label
          htmlFor="paper-file"
          className="flex cursor-pointer flex-col items-center justify-center gap-2 border border-dashed border-line px-4 py-8 text-center transition-colors hover:border-signal/50"
        >
          <Upload className="h-5 w-5 text-foreground-faint" aria-hidden />
          <span className="text-body-sm text-foreground-muted">
            {fileName ?? "Drop a PDF here, or click to browse"}
          </span>
          <input
            id="paper-file"
            type="file"
            accept="application/pdf"
            className="sr-only"
            onChange={(e) => setFileName(e.target.files?.[0]?.name ?? null)}
          />
        </label>

        <div className="mt-4">
          <label htmlFor="paper-tags" className="mb-1.5 block text-body-sm text-foreground-muted">
            Tags (optional)
          </label>
          <Input id="paper-tags" placeholder="error correction, benchmarking" />
        </div>

        <div className="mt-6 flex justify-end gap-2">
          <ModalClose asChild>
            <Button variant="outline" size="sm">
              Cancel
            </Button>
          </ModalClose>
          <Button size="sm" onClick={handleSubmit} disabled={!fileName}>
            Upload
          </Button>
        </div>
      </ModalContent>
    </Modal>
  );
}
