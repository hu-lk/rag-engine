"use client";

import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";

interface Source {
  document_id: number;
  content: string;
}

interface Message {
  role: "user" | "ai";
  text: string;
  sources?: Source[];
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setUploadStatus("Uploading and processing...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE}/documents/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      const data = await response.json();
      setUploadStatus(`Success! Document "${data.name}" ingested.`);
    } catch (error) {
      console.error(error);
      setUploadStatus("Error processing document.");
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: userMsg }]);
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/query/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userMsg, top_k: 5 }),
      });

      if (!response.ok) throw new Error("Query failed");

      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: data.answer,
          sources: data.sources,
        },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "Sorry, I encountered an error while processing your request.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="main-container">
      <header className="header">
        <div className="logo">RAG Engine Pro</div>
        {/* <div>
          <span style={{ fontSize: '0.8rem', opacity: 0.6 }}>Backend: {API_BASE}</span>
        </div> */}
      </header>

      <div className="grid">
        <aside className="upload-container">
          <div className="card upload-section">
            <h3>Knowledge Base</h3>
            <p style={{ fontSize: "0.9rem", opacity: 0.7 }}>
              Upload PDFs to train the engine on your specific data.
            </p>

            <input
              type="file"
              accept=".pdf"
              onChange={handleUpload}
              ref={fileInputRef}
              disabled={uploading}
              style={{ display: "none" }}
              id="pdf-upload"
            />

            <label htmlFor="pdf-upload" style={{ width: "100%" }}>
              <button
                className="secondary"
                style={{ width: "100%" }}
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading}
              >
                {uploading ? "Processing..." : "Upload PDF"}
              </button>
            </label>

            {uploadStatus && (
              <div
                style={{
                  fontSize: "0.85rem",
                  color: uploadStatus.includes("Error")
                    ? "var(--error)"
                    : "var(--success)",
                  padding: "0.5rem",
                  borderRadius: "8px",
                  background: "rgba(255,255,255,0.03)",
                }}
              >
                {uploadStatus}
              </div>
            )}
          </div>
        </aside>

        <section className="card chat-section">
          <div className="chat-messages">
            {messages.length === 0 && (
              <div
                style={{ textAlign: "center", opacity: 0.4, marginTop: "20%" }}
              >
                <p>
                  Hello! Upload a document and ask me anything about its
                  content.
                </p>
              </div>
            )}

            {messages.map((m, i) => (
              <div
                key={i}
                className={`message ${m.role === "user" ? "user-message" : "ai-message"}`}
              >
                <div>
                  {m.role === "ai" ? (
                    <ReactMarkdown>{m.text}</ReactMarkdown>
                  ) : (
                    m.text
                  )}
                </div>
                {m.sources && m.sources.length > 0 && (
                  <div className="sources">
                    <strong>Sources:</strong>
                    <div
                      style={{
                        maxHeight: "100px",
                        overflowY: "auto",
                        marginTop: "5px",
                      }}
                    >
                      {m.sources.map((s, si) => (
                        <div
                          key={si}
                          style={{ fontStyle: "italic", marginBottom: "5px" }}
                        >
                          "...{s.content.substring(0, 100)}..."
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="message ai-message">
                <span className="loading-dots">Generating answer</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleQuery} className="chat-input-container">
            <input
              type="text"
              placeholder="Ask a question..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
            />
            <button type="submit" disabled={loading || !input.trim()}>
              Send
            </button>
          </form>
        </section>
      </div>
    </main>
  );
}
