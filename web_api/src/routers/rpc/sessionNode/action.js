import express from "express";
import * as rpcController from "../../../controllers/rpc/rpcController.js";

const router = express.Router();

router.post("/summarize", rpcController.summarizeDataset);
router.post("/preview", rpcController.previewDataset);

export default router;
