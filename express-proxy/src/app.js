import express from "express";
import { SparkClient } from "./sparkClient.js";
import { errorHandler } from "./errors/errorHandler.js";

const app = express();

app.use(express.json());

let sp = new SparkClient();

app.post("/createSession", (req, res, next) => {
  sp._createSession(req.body, res, next);
});

app.post("/load", (req, res, next) => {
  sp._loadDataset(req.body, res, next);
});

app.post("/loadFromSession", (req, res, next) => {
  sp._loadFromSession(req.body, res, next);
});

app.post("/addNode/filter", (req, res, next) => {
  sp._create_FilterNode(req.body, res, next);
});

app.post("/addNode/addColumn", (req, res, next) => {
  sp._create_AddColumnNode(req.body, res, next);
});

app.post("/addNode/tableNode", (req, res, next) => {
  sp._create_TableNode(req.body, res, next);
});

app.post("/addNode/join", (req, res, next) => {
  sp._create_JoinNode(req.body, res, next);
});

app.post("/editNode/join", (req, res, next) => {
  sp._edit_JoinNode(req.body, res, next);
});

app.post("/editNode/filter", (req, res, next) => {
  sp._edit_FilterNode(req.body, res, next);
});

app.post("/editNode/addColumn", (req, res, next) => {
  sp._edit_AddColumnNode(req.body, res, next);
});

app.post("/removeNode", (req, res, next) => {
  sp._removeNode(req.body, res, next);
});

app.get("/getSessionStatus/:session_id", (req, res, next) => {
  sp._getSessionStatus(req.params, res, next);
});

app.post("/rebuildSession/:session_id", (req, res, next) => {
  sp._rebuildSession(req.params, res, next);
});

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
