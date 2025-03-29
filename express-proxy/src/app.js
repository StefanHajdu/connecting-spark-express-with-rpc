import express from "express";
import { SparkClient } from "./sparkClient.js";
import { errorHandler } from "./errors/errorHandler.js";

const app = express();

app.use(express.json());

let sp = new SparkClient();

// CREATE SESSION
app.post("/createSession", (req, res, next) => {
  sp._createSession(req.body, res, next);
});

// ADD NODE
app.post("/addNode/LoadDatasetNode", (req, res, next) => {
  sp._create_loadDatasetNode(req.body, res, next);
});

app.post("/addNode/LoadFromSessionNode", (req, res, next) => {
  sp._create_loadFromSessionNode(req.body, res, next);
});

app.post("/addNode/FilterNode", (req, res, next) => {
  sp._create_FilterNode(req.body, res, next);
});

app.post("/addNode/NewColumnNode", (req, res, next) => {
  sp._create_NewColumnNode(req.body, res, next);
});

app.post("/addNode/JoinNode", (req, res, next) => {
  sp._create_JoinNode(req.body, res, next);
});

app.post("/addNode/TableNode", (req, res, next) => {
  sp._create_TableNode(req.body, res, next);
});

// EDIT NODE
app.post("/editNode/FilterNode", (req, res, next) => {
  sp._edit_FilterNode(req.body, res, next);
});

app.post("/editNode/NewColumnNode", (req, res, next) => {
  sp._edit_NewColumnNode(req.body, res, next);
});

app.post("/editNode/JoinNode", (req, res, next) => {
  sp._edit_JoinNode(req.body, res, next);
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
    res.write(JSON.stringify(row.row_json));
  });

  rowStream.on("end", () => {
    res.end();
  });
});

app.use(errorHandler);

app.listen(4444);
