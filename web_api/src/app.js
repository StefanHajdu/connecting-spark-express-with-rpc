import express from "express";
import cors from "cors";
import { errorHandler } from "./errors/errorHandler.js";

import directRouter from "./routers/direct/direct.js";
import rpcSessionRouter from "./routers/rpc/session.js";
import rpcSessionNodeTransformRouter from "./routers/rpc/sessionNode/transform.js";
import rpcSessionNodeActionRouter from "./routers/rpc/sessionNode/action.js";

const app = express();

app.use(express.json());
app.use(cors());
app.use("/direct", directRouter);
app.use("/rpc/session", rpcSessionRouter);
app.use("/rpc/sessionNode/transform", rpcSessionNodeTransformRouter);
app.use("/rpc/sessionNode/action", rpcSessionNodeActionRouter);
app.use(errorHandler);

app.listen(4444);
