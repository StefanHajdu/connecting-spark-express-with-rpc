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

  forwardStream(stream, httpResponse, next) {
    httpResponse.writeHead(200, {
      "Content-Type": "application/json",
      "Transfer-Encoding": "chunked",
    });

    let cnt = 0;
    stream.on("data", (chunk) => {
      if (cnt === 0) {
        httpResponse.write("[");
        httpResponse.write(JSON.stringify(chunk));
      } else {
        httpResponse.write(",");
        httpResponse.write(JSON.stringify(chunk));
      }
      cnt += 1;
    });

    stream.on("end", () => {
      httpResponse.write("]");
      httpResponse.end();
      next();
    });

    stream.on("error", (err) => {
      console.log(`ERROR: ${err}`);
    });
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

  loadSessions(req, httpResponse, next) {
    const stream = this.client.loadSessions();
    this.forwardStream(stream, httpResponse, next);
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
    const stream = this.client.submit_LoadDatasetNode(body);
    this.forwardStream(stream, httpResponse, next);
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

  submitAddColumnNode(body, httpResponse, next) {
    const stream = this.client.submit_AddColumnNode(body);
    this.forwardStream(stream, httpResponse, next);
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
  removeNode(body, httpResponse, next) {
    const stream = this.client.removeNode(body);
    this.forwardStream(stream, httpResponse, next);
  }

  toggleNode(body, httpResponse, next) {
    const stream = this.client.toggleNode(body);
    this.forwardStream(stream, httpResponse, next);
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
