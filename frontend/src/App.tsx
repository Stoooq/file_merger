import { useState, type ChangeEvent } from "react";
import "./App.css";
import { Button } from "./components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card";
import { Input } from "./components/ui/input";

function App() {
  const [isMerging, setIsMerging] = useState(false);
  const [files, setFiles] = useState<File[] | null>(null);
  const [downloadData, setDownloadData] = useState<{
    url: string;
    name: string;
  } | null>(null);

  const readFileContent = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = () => {
        const result = reader.result as string;
        if (file.name.endsWith(".xlsx")) {
          const base64Content = result.split(",")[1];
          resolve(base64Content);
        } else {
          resolve(result);
        }
      };

      reader.onerror = reject;

      if (file.name.endsWith(".xlsx")) {
        reader.readAsDataURL(file);
      } else {
        reader.readAsText(file);
      }
    });
  };

  const mergeDocuments = async () => {
    if (!files) return;

    setIsMerging(true);
    try {
      const filesData = await Promise.all(
        files.map(async (file) => ({
          name: file.name,
          content: await readFileContent(file),
        }))
      );

      const response = await fetch("http://127.0.0.1:8000/merge", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ files: filesData }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data)
        const { name, content } = data.merged_file;

        const blob = new Blob([content], { type: "text/csv;charset=utf-8;" });

        const url = window.URL.createObjectURL(blob);

        setDownloadData({
          url: url,
          name: name || "merged_data.csv",
        });

        setFiles(null);
      } else {
        console.error("Failed to merge documents");
      }
    } catch (error) {
      console.error("Error merging documents:", error);
    } finally {
      setIsMerging(false);
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
      setDownloadData(null);
    }
  };

  return (
    <div className="w-full flex flex-col p-12 gap-12">
      <Card className="w-full">
        <CardHeader>
          <CardTitle>File Merger</CardTitle>
          <CardDescription>Choose files to merge them</CardDescription>
        </CardHeader>
        <CardContent className="w-full">
          <Input
            type="file"
            onChange={handleFileChange}
            multiple
            accept=".csv, .xlsx, .txt, .log"
          />
        </CardContent>
        <CardFooter className="gap-6">
          <Button
            variant="my"
            onClick={mergeDocuments}
            disabled={!files || files.length === 0 || isMerging}
          >
            {isMerging ? "Merging..." : "Merge Documents"}
          </Button>

          {downloadData && (
            <a
              href={downloadData.url}
              download={downloadData.name}
              className="w-full"
            >
              <Button
                variant="shadow"
                className="w-full"
              >
                Download {downloadData.name}
              </Button>
            </a>
          )}
        </CardFooter>
      </Card>
    </div>
  );
}

export default App;
