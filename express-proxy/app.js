import express from "express";
import { SparkClient } from "./SparkClient.js";

const app = express();

app.use(express.json());

let sp = new SparkClient();

// curl -X POST http://localhost:4444/preview -H 'Content-Type: application/json' -d '{"id": "0000", "limit": 12}' -N -w '\nTotal: %{time_total}s\n'
app.post("/preview", (req, res) => {
  let rowStream = sp._previewDataset(req.body);

  res.writeHead(200, {
    "Content-Type": "text/plain; charset=utf-8",
    "Transfer-Encoding": "chunked",
    "X-Content-Type-Options": "nosniff",
  });

  rowStream.on("data", (row) => {
    res.write(JSON.stringify(row.row_json));
  });

  rowStream.on("end", () => {
    res.end();
  });
});

// curl -X POST http://localhost:4444/load -H 'Content-Type: application/json' -d '{"id": "0000", "df_path": "/home/stephenx/Documents/Datasets/domains_sub2.csv", "df_type": "csv"}' -w '\nTotal: %{time_total}s\n'
app.post("/load", (req, res) => {
  sp._loadDataset(req.body, res);
});

// curl -X POST http://localhost:4444/createSession -H 'Content-Type: application/json' -d '{"id": "0000"}' -w '\nTotal: %{time_total}s\n'
app.post("/createSession", (req, res) => {
  sp._createSession(req.body, res);
});

app.listen(4444);
