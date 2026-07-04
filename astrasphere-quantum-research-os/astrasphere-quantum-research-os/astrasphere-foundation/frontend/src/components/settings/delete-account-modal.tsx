"use client";

import { signOut } from "next-auth/react";
import { useState, type ReactNode } from "react";

import { Button } from "@/components/ui/button";
import { FormMessage } from "@/components/ui/form-message";
import { Input } from "@/components/ui/input";
import { Modal, ModalClose, ModalContent, ModalTrigger } from "@/components/ui/modal";
import { apiClient } from "@/lib/api-client";

export function DeleteAccountModal({
  trigger,
  hasPassword,
}: {
  trigger: ReactNode;
  hasPassword: boolean;
}) {
  const [open, setOpen] = useState(false);
  const [password, setPassword] = useState("");
  const [confirmText, setConfirmText] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const confirmed = confirmText === "DELETE";

  async function handleDelete() {
    setError(null);
    setIsSubmitting(true);
    try {
      await apiClient.delete("/users/me", {
        password: hasPassword ? password : undefined,
        confirm: true,
      });
      await signOut({ callbackUrl: "/login" });
    } catch {
      setError("Couldn't delete your account. Check your password and try again.");
      setIsSubmitting(false);
    }
  }

  return (
    <Modal open={open} onOpenChange={setOpen}>
      <ModalTrigger asChild>{trigger}</ModalTrigger>
      <ModalContent
        title="Delete your account"
        description="This permanently deletes your profile, papers, and research data. This cannot be undone."
      >
        {error && <FormMessage variant="error">{error}</FormMessage>}

        {hasPassword && (
          <div className="mb-3">
            <label
              htmlFor="deletePassword"
              className="mb-1.5 block text-body-sm text-foreground-muted"
            >
              Confirm your password
            </label>
            <Input
              id="deletePassword"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        )}

        <div>
          <label htmlFor="confirmText" className="mb-1.5 block text-body-sm text-foreground-muted">
            Type <span className="font-mono text-danger">DELETE</span> to confirm
          </label>
          <Input
            id="confirmText"
            value={confirmText}
            onChange={(e) => setConfirmText(e.target.value)}
          />
        </div>

        <div className="mt-6 flex justify-end gap-2">
          <ModalClose asChild>
            <Button variant="outline" size="sm">
              Cancel
            </Button>
          </ModalClose>
          <Button
            variant="destructive"
            size="sm"
            disabled={!confirmed || (hasPassword && !password) || isSubmitting}
            onClick={handleDelete}
          >
            {isSubmitting ? "Deleting..." : "Delete my account"}
          </Button>
        </div>
      </ModalContent>
    </Modal>
  );
}
