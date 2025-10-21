import express from "express";
import cors from "cors";
import asyncHandler from "express-async-handler";
import { stat } from "node:fs/promises";

import { RpcClient } from "./controllers/rpcClient.js";
import { ApplicationError } from "./errors/applicationError.js";

export const CommonError = {
  UNKNOWN_ERROR: {
    code: "UNKNOWN_ERROR",
    message: "Unknown error",
    statusCode: 500,
  },
};

export function errorHandler(err, req, res, next) {
  console.log(err.stack);

  if (err instanceof ApplicationError) {
    const code = err.statusCode || 500;
    return sendErr(res, code, err);
  } else if (err instanceof Error) {
    const newError = new ApplicationError({
      message: err.details,
    });
    const code = newError.statusCode || 500;
    return sendErr(res, code, newError);
  } else {
    const unknownError = new ApplicationError(CommonError.UNKNOWN_ERROR);
    return sendErr(res, code, unknownError);
  }
}

function sendErr(res, code, err) {
  return res.status(code).json(err.formatError());
}

const app = express();
const rpcClient = new RpcClient();

app.use(express.json());
app.use(cors());


const createSession = asyncHandler(async (req, res, next) => {
  rpcClient.createSession(req.body, res, next);
});

const getSessionStatus = asyncHandler(async (req, res, next) => {
  rpcClient.getSessionStatus(req.body, res, next);
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

const rpcSessionRouter = express.Router();
rpcSessionRouter.post("/", createSession);
rpcSessionRouter.post("/create", createSession);
rpcSessionRouter.post("/status", getSessionStatus);
rpcSessionRouter.get("/sessions", loadSessions);

const rpcSessionNodeRouter = express.Router();
rpcSessionNodeRouter.post("/submitLoadDatasetNode", submitLoadDatasetNode);
rpcSessionNodeRouter.post("/submitLoadFromSessionNode", submitLoadFromSessionNode);
rpcSessionNodeRouter.post("/submitFilterNode", submitFilterNode);
rpcSessionNodeRouter.post("/submitAddColumnNode", submitAddColumnNode);
rpcSessionNodeRouter.post("/submitJoinNode", submitJoinNode);
rpcSessionNodeRouter.post("/submitTableNode", submitTableNode);
rpcSessionNodeRouter.post("/submitHistogramNode", submitHistogramNode);
rpcSessionNodeRouter.post("/removeNode", removeNode);
rpcSessionNodeRouter.post("/toggleNode", toggleNode);
rpcSessionNodeRouter.post("/summarize", summarizeDataset);
rpcSessionNodeRouter.post("/preview", previewDataset);

app.use("/rpc/node", rpcSessionNodeRouter);
app.use("/rpc/session", rpcSessionRouter);

app.use(errorHandler);

app.listen(4444);
