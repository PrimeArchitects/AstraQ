import { Upload } from "lucide-react";

import { UploadPaperModal } from "@/components/dashboard/upload-paper-modal";
import { AppShell } from "@/components/layout/app-shell";
import { PageHeader } from "@/components/layout/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { RECENT_PAPERS, SAVED_PAPERS, type Paper } from "@/data/mock";

const STATUS_VARIANT: Record<Paper["status"], "neutral" | "success" | "info" | "warning"> = {
  new: "info",
  reading: "warning",
  reviewed: "success",
  saved: "neutral",
};

// Merge and de-duplicate the two mock sets for a fuller table — a real
// implementation sources this from GET /papers with pagination/sorting.
const ALL_PAPERS = [...RECENT_PAPERS, ...SAVED_PAPERS].filter(
  (paper, index, arr) => arr.findIndex((p) => p.id === paper.id) === index,
);

export default function MyPapersPage() {
  return (
    <AppShell>
      <div className="mx-auto max-w-6xl">
        <PageHeader
          title="My Papers"
          description={`${ALL_PAPERS.length} papers in your library`}
          action={
            <UploadPaperModal
              trigger={
                <Button size="sm" className="gap-1.5">
                  <Upload className="h-3.5 w-3.5" aria-hidden />
                  Upload Paper
                </Button>
              }
            />
          }
        />
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Title</TableHead>
              <TableHead>Authors</TableHead>
              <TableHead>Venue</TableHead>
              <TableHead>Year</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {ALL_PAPERS.map((paper) => (
              <TableRow key={paper.id}>
                <TableCell className="max-w-xs truncate font-medium">{paper.title}</TableCell>
                <TableCell className="text-foreground-muted">{paper.authors.join(", ")}</TableCell>
                <TableCell className="text-foreground-muted">{paper.venue}</TableCell>
                <TableCell className="font-mono text-data text-foreground-muted">
                  {paper.year}
                </TableCell>
                <TableCell>
                  <Badge variant={STATUS_VARIANT[paper.status]}>{paper.status}</Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </AppShell>
  );
}
