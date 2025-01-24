import { SparkClient } from "./SparkClient.js";

import grpc from "@grpc/grpc-js";
import protoLoader from "@grpc/proto-loader";

const protoPath = "../protos/sparkapi.proto";

function getMethods(obj) {
  var result = [];
  for (var id in obj) {
    try {
      if (typeof obj[id] == "function") {
        result.push(id + ": " + obj[id].toString());
      }
    } catch (err) {
      result.push(id + ": inaccessible");
    }
  }
  return result;
}

const packageDefinition = protoLoader.loadSync(protoPath, {});

let sparkApiRpcPkg = grpc.loadPackageDefinition(packageDefinition).sparkapi;

let client = new sparkApiRpcPkg.SparkApi(
  "localhost:50051",
  grpc.credentials.createInsecure()
);

console.log(getMethods(client).join("\n"));

let res_ = client.loadsDataset(
  { id: "id", dfPath: "path", dfType: "json" },
  (err, response) => {
    console.log(response);
    console.log(err);
  }
);
