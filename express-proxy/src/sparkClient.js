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

  _previewDataset(previewDatasetRequestBody) {
    return this.client.previewDataset(previewDatasetRequestBody);
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

  _loadDataset(newDatasetRequestBody, expressResponse, next) {
    return this.client.loadsDataset(
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

  _loadFromSession(datasetFromSessionRequestBody, expressResponse, next) {
    return this.client.loadFromSession(
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

  _runSql(sqlRequestBody, expressResponse, next) {
    sqlRequestBody.params_json = JSON.stringify(sqlRequestBody.params_json);
    return this.client.runSql(
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

  _getRebuildStatus(rebuildStatusParams, expressResponse, next) {
    return this.client.getRebuildStatus(
      { id: rebuildStatusParams.id },
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
      { id: rebuildSessionParams.id },
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
