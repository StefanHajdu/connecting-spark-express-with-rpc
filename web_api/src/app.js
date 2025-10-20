import express from "express";
import cors from "cors";
import asyncHandler from "express-async-handler";
import { stat } from "node:fs/promises";

import { RpcClient } from "./controllers/rpcClient.js";
import { errorHandler } from "./errors/errorHandler.js";
import { ApplicationError } from "./errors/applicationError.js";

const app = express();
const rpcClient = new RpcClient();

app.use(express.json());
app.use(cors());

const validatePath = asyncHandler(async (req, res) => {
  const { path } = req.body ?? {};

  if (!path) {
    throw new ApplicationError({
      code: "PATH_VALIDATION_ERROR",
      message: "Request body must include a path to validate.",
      statusCode: 400,
    });
  }

  try {
    const stats = await stat(path);
    res.json({
      is_file: stats.isFile(),
      is_dir: stats.isDirectory(),
      size: stats.size,
    });
  } catch (error) {
    throw new ApplicationError({
      code: "PATH_VALIDATION_ERROR",
      message: `Path validation error: ${error.message}`,
      statusCode: error.code === "ENOENT" ? 404 : 400,
    });
  }
});

const createSession = asyncHandler(async (req, res, next) => {
  rpcClient.createSession(req.body, res, next);
});

const getSessionStatus = asyncHandler(async (req, res, next) => {
  rpcClient.getSessionStatus(req.body, res, next);
});

const rebuildSession = asyncHandler(async (req, res, next) => {
  rpcClient.rebuildSession(req.body, res, next);
});

const loadSessions = asyncHandler(async (req, res, next) => {
  rpcClient.loadSessions(req, res, next);
});

const submitLoadDatasetNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitLoadDatasetNode(req.body, res, next);
});

const submitLoadFromSessionNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitLoadFromSessionNode(req.body, res, next);
});

const submitFilterNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitFilterNode(req.body, res, next);
});

const submitAddColumnNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitAddColumnNode(req.body, res, next);
});

const submitJoinNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitJoinNode(req.body, res, next);
});

const submitTableNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitTableNode(req.body, res, next);
});

const submitHistogramNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitHistogramNode(req.body, res, next);
});

const removeNode = asyncHandler(async (req, res, next) => {
  rpcClient.removeNode(req.body, res, next);
});

const toggleNode = asyncHandler(async (req, res, next) => {
  rpcClient.toggleNode(req.body, res, next);
});

const summarizeDataset = asyncHandler(async (req, res, next) => {
  rpcClient.summarizeDataset(req.body, res, next);
});

const previewDataset = asyncHandler(async (req, res, next) => {
  rpcClient.previewDataset(req.body, res, next);
});

const directRouter = express.Router();
directRouter.post("/validatePath", validatePath);

const rpcLoadRouter = express.Router();
rpcLoadRouter.post("/submitLoadDatasetNode", submitLoadDatasetNode);
rpcLoadRouter.post("/submitLoadFromSessionNode", submitLoadFromSessionNode);
rpcLoadRouter.get("/sessions", loadSessions);

const rpcSessionRouter = express.Router();
rpcSessionRouter.post("/create", createSession);
rpcSessionRouter.post("/", createSession);
rpcSessionRouter.post("/status", getSessionStatus);
rpcSessionRouter.post("/rebuild", rebuildSession);

const rpcSessionNodeTransformRouter = express.Router();
rpcSessionNodeTransformRouter.post("/submitLoadDatasetNode", submitLoadDatasetNode);
rpcSessionNodeTransformRouter.post("/submitLoadFromSessionNode", submitLoadFromSessionNode);
rpcSessionNodeTransformRouter.post("/submitFilterNode", submitFilterNode);
rpcSessionNodeTransformRouter.post("/submitAddColumnNode", submitAddColumnNode);
rpcSessionNodeTransformRouter.post("/submitJoinNode", submitJoinNode);
rpcSessionNodeTransformRouter.post("/submitTableNode", submitTableNode);
rpcSessionNodeTransformRouter.post("/submitHistogramNode", submitHistogramNode);
rpcSessionNodeTransformRouter.post("/removeNode", removeNode);
rpcSessionNodeTransformRouter.post("/toggleNode", toggleNode);

const rpcSessionNodeActionRouter = express.Router();
rpcSessionNodeActionRouter.post("/summarize", summarizeDataset);
rpcSessionNodeActionRouter.post("/preview", previewDataset);

app.use("/direct", directRouter);
app.use("/rpc/load", rpcLoadRouter);
app.use("/rpc/session", rpcSessionRouter);
app.use("/rpc/sessionNode/transform", rpcSessionNodeTransformRouter);
app.use("/rpc/sessionNode/action", rpcSessionNodeActionRouter);

app.use(errorHandler);

app.listen(4444);
