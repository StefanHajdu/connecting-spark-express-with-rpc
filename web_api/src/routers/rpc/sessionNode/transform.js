import express from "express";
import * as rpcController from "../../../controllers/rpc/rpcController.js";

const router = express.Router();

router.post("/submitLoadDatasetNode", rpcController.submitLoadDatasetNode);
router.post(
  "/submitLoadFromSessionNode",
  rpcController.submitLoadFromSessionNode
);
router.post("/submitFilterNode", rpcController.submitFilterNode);
router.post("/submitAddColumnNode", rpcController.submitAddColumnNode);
router.post("/submitJoinNode", rpcController.submitJoinNode);
router.post("/submitTableNode", rpcController.submitTableNode);
router.post("/submitHistogramNode", rpcController.submitHistogramNode);
router.post("/removeNode", rpcController.removeNode);
router.post("/toggleNode", rpcController.toggleNode);

export default router;
