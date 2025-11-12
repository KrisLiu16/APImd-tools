import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const staticDir = path.join(__dirname, 'public');

app.use(express.static(staticDir));

app.get('*', (_req, res) => {
  res.sendFile(path.join(staticDir, 'index.html'));
});

const port = process.env.PORT || 5173;
app.listen(port, () => {
  console.log(`API Markdown helper running at http://localhost:${port}`);
});
