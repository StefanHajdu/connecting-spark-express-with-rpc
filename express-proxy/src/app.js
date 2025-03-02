import express from "express";
import { SparkClient } from "./sparkClient.js";
import { errorHandler } from "./errors/errorHandler.js";

const app = express();

app.use(express.json());

let sp = new SparkClient();

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

app.post("/load", (req, res, next) => {
  sp._loadDataset(req.body, res, next);
});

app.post("/loadFromSession", (req, res, next) => {
  sp._loadFromSession(req.body, res, next);
});

app.post("/addSql", (req, res, next) => {
  sp._addSql(req.body, res, next);
});

app.post("/editSql", (req, res, next) => {
  sp._editSql(req.body, res, next);
});

app.post("/removeSql", (req, res, next) => {
  sp._removeSql(req.body, res, next);
});

app.post("/summarize", (req, res, next) => {
  sp._summarizeDataset(req.body, res, next);
});

app.post("/createSession", (req, res, next) => {
  sp._createSession(req.body, res, next);
});

app.get("/rebuildStatus/:id", (req, res, next) => {
  sp._getRebuildStatus(req.params, res, next);
});

app.post("/rebuildSession/:session_id", (req, res, next) => {
  sp._rebuildSession(req.params, res, next);
});

app.use(errorHandler);

app.listen(4444);
