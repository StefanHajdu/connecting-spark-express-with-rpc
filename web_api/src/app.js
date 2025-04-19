import express from "express";
import cors from "cors";
import { SparkClient } from "./sparkClient.js";
import { errorHandler } from "./errors/errorHandler.js";

const app = express();

app.use(express.json());
app.use(cors());

let sp = new SparkClient();

// CREATE SESSION
app.post("/createSession", (req, res, next) => {
  sp._createSession(req.body, res, next);
});

// ADD NODE
app.post("/submitNode/LoadDatasetNode", (req, res, next) => {
  sp._submit_LoadDatasetNode(req.body, res, next);
});

app.post("/submitNode/LoadFromSessionNode", (req, res, next) => {
  sp._submit_LoadFromSessionNode(req.body, res, next);
});

app.post("/submitNode/FilterNode", (req, res, next) => {
  sp._submit_FilterNode(req.body, res, next);
});

app.post("/submitNode/NewColumnNode", (req, res, next) => {
  sp._submit_NewColumnNode(req.body, res, next);
});

app.post("/submitNode/JoinNode", (req, res, next) => {
  sp._submit_JoinNode(req.body, res, next);
});

app.post("/submitNode/TableNode", (req, res, next) => {
  sp._submit_TableNode(req.body, res, next);
});

app.post("/submitNode/HistogramNode", (req, res, next) => {
  sp._submit_HistogramNode(req.body, res, next);
});

// REMOVE NODE
app.post("/removeNode", (req, res, next) => {
  sp._removeNode(req.body, res, next);
});

// REBUILD SESSION
app.get("/getSessionStatus/:session_id", (req, res, next) => {
  sp._getSessionStatus(req.params, res, next);
});

app.post("/rebuildSession/:session_id", (req, res, next) => {
  sp._rebuildSession(req.params, res, next);
});

// ACTIONS
app.post("/summarize", (req, res, next) => {
  sp._summarizeDataset(req.body, res, next);
});

app.post("/preview", (req, res) => {
  let rowStream = sp._previewDataset(req.body);

  res.writeHead(200, {
    "Content-Type": "text/plain; charset=utf-8",
    "Transfer-Encoding": "chunked",
    "X-Content-Type-Options": "nosniff",
  });

  rowStream.on("data", (row) => {
    res.write(row.row_json + "<stream_chunk_done>");
  });

  rowStream.on("end", () => {
    res.end();
  });
});

app.use(errorHandler);

app.listen(4444);
