import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

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

  _summarizeDataset(summarizeDatasetRequest, expressResponse) {
    return this.client.summarizeDataset(
      summarizeDatasetRequest,
      (err, pysparkGeneralResponse) => {
        if (err) {
          console.log(err);
        } else {
          expressResponse.json(pysparkGeneralResponse);
        }
      }
    );
  }

  _loadDataset(newDatasetRequestBody, expressResponse) {
    return this.client.loadsDataset(
      newDatasetRequestBody,
      (err, pysparkGeneralResponse) => {
        if (err) {
          console.log(err);
        } else {
          expressResponse.json(pysparkGeneralResponse);
        }
      }
    );
  }

  _filterDataset(filterDatasetRequestBody, expressResponse) {
    return this.client.filterDataset(
      filterDatasetRequestBody,
      (err, pysparkTransformResponse) => {
        if (err) {
          console.log(err);
        } else {
          expressResponse.json(pysparkTransformResponse);
        }
      }
    );
  }

  _createSession(newSessionRequestBody, expressResponse) {
    return this.client.createSession(
      newSessionRequestBody,
      (err, newSessionResponse) => {
        if (err) {
          console.log(err);
        } else {
          expressResponse.json(newSessionResponse);
        }
      }
    );
  }
}
