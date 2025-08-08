import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

import { ApplicationError } from "../../errors/applicationError.js";

export class RpcClient {
  #protoPath = "../protos/sparkapi.proto";

  constructor() {
    if (RpcClient._instance) {
      // singleton
      return RpcClient._instance;
    }
    RpcClient._instance = this;

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

  // HANDLE SESSIONS
  createSession(body, httpResponse, next) {
    return this.client.createSession(body, (err, rpcResponse) => {
      if (err) {
        return next(new ApplicationError({ message: err.message, code: 500 }));
      } else {
        httpResponse.json(rpcResponse);
      }
    });
  }

  getSessionStatus(urlParams, httpResponse, next) {
    return this.client.getSessionStatus(
      { session_id: urlParams.session_id },
      (err, rpcResponse) => {
        if (err) {
          return next(
            new ApplicationError({ message: err.message, code: 500 })
          );
        } else {
          httpResponse.json(rpcResponse);
        }
      }
    );
  }

  rebuildSession(urlParams, httpResponse, next) {
    return this.client.rebuildSession(
      { session_id: urlParams.session_id },
      (err, rpcResponse) => {
        if (err) {
          return next(
            new ApplicationError({ message: err.message, code: 500 })
          );
        } else {
          httpResponse.json(rpcResponse);
        }
      }
    );
  }

  // ADD NODES
  submitLoadDatasetNode(body, httpResponse, next) {
    return this.client.submit_LoadDatasetNode(body, (err, rpcResponse) => {
      if (err) {
        return next(new ApplicationError({ message: err.message, code: 500 }));
      } else {
        httpResponse.json(rpcResponse);
      }
    });
  }

  submitLoadFromSessionNode(body, httpResponse, next) {
    return this.client.submit_LoadFromSessionNode(body, (err, rpcResponse) => {
      if (err) {
        return next(new ApplicationError({ message: err.message, code: 500 }));
      } else {
        httpResponse.json(rpcResponse);
      }
    });
  }

  submitFilterNode(body, httpResponse, next) {
    return this.client.submit_FilterNode(body, (err, rpcResponse) => {
      if (err) {
        return next(new ApplicationError({ message: err.message, code: 500 }));
      } else {
        httpResponse.json(rpcResponse);
      }
    });
  }

  submitNewColumnNode(body, httpResponseStream, next) {
    httpResponseStream.writeHead(200, {
      "Content-Type": "application/json",
      "Transfer-Encoding": "chunked",
    });
    const previewStream = this.client.submit_NewColumnNode(body);
    previewStream.on("data", (chunk) => {
      console.log(chunk);
      httpResponseStream.write(JSON.stringify(chunk));
    });
    previewStream.on("end", () => {
      httpResponseStream.end();
      next();
    });
  }

  submitTableNode(body, httpResponse, next) {
    return this.client.submit_TableNode(body, (err, rpcResponse) => {
      if (err) {
        return next(new ApplicationError({ message: err.message, code: 500 }));
      } else {
        httpResponse.json(rpcResponse);
      }
    });
  }

  submitHistogramNode(body, httpResponse, next) {
    return this.client.submit_HistogramNode(body, (err, rpcResponse) => {
      if (err) {
        return next(new ApplicationError({ message: err.message, code: 500 }));
      } else {
        httpResponse.json(rpcResponse);
      }
    });
  }

  submitJoinNode(body, httpResponse, next) {
    return this.client.submit_JoinNode(body, (err, rpcResponse) => {
      if (err) {
        return next(new ApplicationError({ message: err.message, code: 500 }));
      } else {
        httpResponse.json(rpcResponse);
      }
    });
  }

  // REMOVE NODE
  removeNode(body, httpResponseStream, next) {
    httpResponseStream.writeHead(200, {
      "Content-Type": "application/json",
      "Transfer-Encoding": "chunked",
    });
    const previewStream = this.client.removeNode(body);
    previewStream.on("data", (chunk) => {
      console.log(chunk);
      httpResponseStream.write(JSON.stringify(chunk));
    });
    previewStream.on("end", () => {
      httpResponseStream.end();
      next();
    });
  }

  // ACTIONS
  previewDataset(body, httpResponseStream, next) {
    httpResponseStream.writeHead(200, {
      "Content-Type": "application/json",
      "Transfer-Encoding": "chunked",
    });
    const previewStream = this.client.previewDataset(body);
    previewStream.on("data", (chunk) => {
      httpResponseStream.write(chunk.data);
    });
    previewStream.on("end", () => {
      httpResponseStream.end();
      next();
    });
  }

  summarizeDataset(body, httpResponse, next) {
    return this.client.summarizeDataset(body, (err, rpcResponse) => {
      if (err) {
        return next(new ApplicationError({ message: err.message, code: 500 }));
      } else {
        httpResponse.json(rpcResponse);
      }
    });
  }
}
