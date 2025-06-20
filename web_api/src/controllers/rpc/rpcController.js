import asyncHandler from "express-async-handler";
import { RpcClient } from "./rpcClient.js";

const rpcClient = new RpcClient();

// SESSION
export const createSession = asyncHandler(async (req, res, next) => {
  rpcClient.createSession(req.body, res, next);
});

export const getSessionStatus = asyncHandler(async (req, res, next) => {
  rpcClient.getSessionStatus(req.params, res, next);
});

export const rebuildSession = asyncHandler(async (req, res, next) => {
  rpcClient.rebuildSession(req.params, res, next);
});

// ADD NODE
export const submitLoadDatasetNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitLoadDatasetNode(req.body, res, next);
});

export const submitLoadFromSessionNode = asyncHandler(
  async (req, res, next) => {
    rpcClient.submitLoadFromSessionNode(req.body, res, next);
  }
);

export const submitFilterNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitFilterNode(req.body, res, next);
});

export const submitNewColumnNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitNewColumnNode(req.body, res, next);
});

export const submitJoinNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitJoinNode(req.body, res, next);
});

export const submitTableNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitTableNode(req.body, res, next);
});

export const submitHistogramNode = asyncHandler(async (req, res, next) => {
  rpcClient.submitHistogramNode(req.body, res, next);
});

// REMOVE NODE
export const removeNode = asyncHandler(async (req, res, next) => {
  rpcClient.removeNode(req.body, res, next);
});

// ACTIONS
export const summarizeDataset = asyncHandler(async (req, res, next) => {
  rpcClient.summarizeDataset(req.body, res, next);
});

export const previewDataset = asyncHandler(async (req, res, next) => {
  rpcClient.previewDataset(req.body, res, next);
});
