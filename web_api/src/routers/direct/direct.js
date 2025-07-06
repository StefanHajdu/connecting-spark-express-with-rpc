import express from "express";
import * as directController from "../../controllers/direct/directController.js";

const router = express.Router();

router.post("/validatePath", directController.validatePath);

export default router;
