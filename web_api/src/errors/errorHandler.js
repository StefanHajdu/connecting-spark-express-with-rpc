import { ApplicationError } from "./applicationError.js";
import { CommonError } from "./commonError.js";

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
