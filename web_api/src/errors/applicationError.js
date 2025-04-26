export class ApplicationError extends Error {
  constructor(options) {
    super();

    if (!options.message) {
      throw new Error("ApplicationError: error message required.");
    }

    if (!options.code) {
      throw new Error("ApplicationError: error code required.");
    }

    this.name = "ApplicationError";
    this.type = options.type;
    this.code = options.code;
    this.message = options.message;
    this.errors = options.errors;
    this.meta = options.meta;
    this.statusCode = options.statusCode;
  }

  formatError() {
    const stackTrace = JSON.stringify(this, ["stack"], 4) || {};
    const newError = JSON.parse(JSON.stringify(this));

    // No need to send to client
    newError.statusCode = undefined;
    delete newError.meta;

    return {
      error: {
        ...newError,
        stack: stackTrace.stack,
      },
    };
  }
}
