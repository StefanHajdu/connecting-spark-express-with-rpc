import fs from "node:fs";
import asyncHandler from "express-async-handler";
import { ApplicationError } from "../../errors/applicationError.js";

export const validatePath = asyncHandler(async (req, res, next) => {
  try {
    const stats = fs.statSync(req.body.path);
    res.json({
      is_file: stats.isFile(),
      is_dir: stats.isDirectory(),
      size: stats.size,
    });
  } catch (err) {
    next(new ApplicationError({ message: err.message, code: 400 }));
  }
});
