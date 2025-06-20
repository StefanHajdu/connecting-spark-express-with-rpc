import express from "express";
import * as rpcController from "../../controllers/rpc/rpcController.js";

const router = express.Router();

router.post("/create", rpcController.createSession);
router.post("/status", rpcController.getSessionStatus);
router.post("/rebuild", rpcController.rebuildSession);

export default router;
