import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

import { ApplicationError } from "./errors/applicationError.js";

export class SparkClient {
  #protoPath = "../protos/sparkapi.proto";

  constructor() {
    const packageDefinition = protoLoader.loadSync(this.#protoPath, {
      keepCase: true,
      longs: String,
      enums: String,
      defaults: true,
      oneofs: true,
    });
    let sparkApiRpcPkg = grpc.loadPackageDefinition(packageDefinition).sparkapi;
    this.client = new sparkApiRpcPkg.SparkApi(
      "localhost:50051",
      grpc.credentials.createInsecure()
    );
  }

  _previewDataset(previewDatasetRequest, expressResponse, next) {
    return this.client.previewDataset(
      previewDatasetRequest,
      (err, pysparkResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(pysparkResponse);
        }
      }
    );
  }

  _summarizeDataset(summarizeDatasetRequest, expressResponse, next) {
    return this.client.summarizeDataset(
      summarizeDatasetRequest,
      (err, pysparkGeneralResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(pysparkGeneralResponse);
        }
      }
    );
  }

  _submit_LoadDatasetNode(newDatasetRequestBody, expressResponse, next) {
    return this.client.submit_LoadDatasetNode(
      newDatasetRequestBody,
      (err, pysparkGeneralResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(pysparkGeneralResponse);
        }
      }
    );
  }

  _submit_LoadFromSessionNode(
    datasetFromSessionRequestBody,
    expressResponse,
    next
  ) {
    return this.client.submit_LoadFromSessionNode(
      datasetFromSessionRequestBody,
      (err, pysparkGeneralResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(pysparkGeneralResponse);
        }
      }
    );
  }

  _submit_FilterNode(sqlRequestBody, expressResponse, next) {
    return this.client.submit_FilterNode(
      sqlRequestBody,
      (err, pysparkTransformResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(pysparkTransformResponse);
        }
      }
    );
  }

  _submit_NewColumnNode(sqlRequestBody, expressResponse, next) {
    return this.client.submit_NewColumnNode(
      sqlRequestBody,
      (err, pysparkTransformResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(pysparkTransformResponse);
        }
      }
    );
  }

  _submit_TableNode(sqlRequestBody, expressResponse, next) {
    return this.client.submit_TableNode(
      sqlRequestBody,
      (err, pysparkTransformResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(pysparkTransformResponse);
        }
      }
    );
  }

  _submit_HistogramNode(sqlRequestBody, expressResponse, next) {
    return this.client.submit_HistogramNode(
      sqlRequestBody,
      (err, pysparkTransformResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(pysparkTransformResponse);
        }
      }
    );
  }

  _submit_JoinNode(sqlRequestBody, expressResponse, next) {
    return this.client.submit_JoinNode(
      sqlRequestBody,
      (err, pysparkTransformResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(pysparkTransformResponse);
        }
      }
    );
  }

  _removeNode(sqlRequestBody, expressResponse, next) {
    sqlRequestBody.params_json = JSON.stringify(sqlRequestBody.params_json);
    return this.client.removeNode(
      sqlRequestBody,
      (err, pysparkTransformResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(pysparkTransformResponse);
        }
      }
    );
  }

  _createSession(newSessionRequestBody, expressResponse, next) {
    return this.client.createSession(
      newSessionRequestBody,
      (err, newSessionResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(newSessionResponse);
        }
      }
    );
  }

  _getSessionStatus(rebuildStatusParams, expressResponse, next) {
    return this.client.getSessionStatus(
      { session_id: rebuildStatusParams.session_id },
      (err, newSessionResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(newSessionResponse);
        }
      }
    );
  }

  _rebuildSession(rebuildSessionParams, expressResponse, next) {
    return this.client.rebuildSession(
      { session_id: rebuildSessionParams.session_id },
      (err, newSessionResponse) => {
        if (err) {
          return next(
            new ApplicationError({
              message: err.message,
              code: 500,
            })
          );
        } else {
          expressResponse.json(newSessionResponse);
        }
      }
    );
  }
}
