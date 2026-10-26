import express from "express";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json());
app.use(cors());

// Serve static frontend files (Single Page Application)
app.use(express.static(__dirname));

app.post("/api/chat", async (req, res) => {
  try {
    const response = await fetch("http://localhost:11434/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "llama3.2",
        messages: [
          { role: "user", content: req.body.question }
        ],
        stream: false
      })
    });

    const data = await response.json();
    res.json({ answer: data.message.content });
  } catch (error) {
    res.status(500).json({ answer: "Could not connect to Ollama." });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Website API running: http://localhost:${PORT}`));
