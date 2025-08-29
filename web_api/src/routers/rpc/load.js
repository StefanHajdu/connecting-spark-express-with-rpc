import express from "express";
import * as rpcController from "../../controllers/rpc/rpcController.js";

const router = express.Router();

router.get("/sessions", rpcController.loadSessions);

export default router;
