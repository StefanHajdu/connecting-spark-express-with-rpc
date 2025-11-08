import { post, textBufferSparkStreamingApi, parseJsonStream } from "$lib/clientApi";
import type { SparkTransform } from "$lib/dtype";
import { nodeFactory, Node } from "../Nodes/NodeClass.svelte";
import { v4 as uuidv4 } from "uuid";
import { footerPreview } from "../PreviewStore.svelte";

export class AnalysisSession {
  session_id: string = $state("");
  name: string = $state("");
  status: string = $state("");
  buildTime: string = $state("");
  resources: string = $state("");
  rest: string = $state("");
  selected: boolean = $state(false);
  nodes: Node[] = $state([]);

  constructor(params: any) {
    this.session_id = params.session_id ? params.session_id : "analysis-" + uuidv4();
    this.name = params.name ? params.name : "random-analysis-name-" + uuidv4();
    this.status = params.status ? params.status : "";
    this.buildTime = params.buildTime ? params.buildTime : "";
    this.resources = params.resources ? params.resources : "";
    this.rest = params.rest ? params.rest : "";
    this.selected = params.selected ? params.selected : false;
    this.nodes =
      params.nodes && params.nodes.length > 0
        ? params.nodes
        : [
            nodeFactory({
              title: "LoadNode",
              columnsOnNodeInput: [],
            }),
          ];
  }

  public setSelected(selected: boolean): void {
    this.selected = selected;
  }

  public getIndexOfActivePrevNode(nodeIndex: number): number {
    let index = 0;
    for (let i = nodeIndex; i >= 0; i--) {
      if (this.nodes[i].active) {
        return i;
      }
    }
    return index;
  }

  public createNode(title: string, nodeIndex: number): Node {
    let prevNodeIndex = this.getIndexOfActivePrevNode(nodeIndex);
    let node = nodeFactory({
      title: title,
      prevNodeId: this.nodes[prevNodeIndex].node_id,
      columnsOnNodeInput: this.nodes[prevNodeIndex].columnsOnNodeOutput,
    });
    return node;
  }

  public async insertNode(node: Node, nodeIndex: number): Promise<void> {
    const previousNodeId = this.nodes[nodeIndex]?.node_id;
    const nextNode = this.nodes[nodeIndex + 1];
    const nextNodePrevNodeId = nextNode ? nextNode.prevNodeId : undefined;

    this.nodes = this.nodes.toSpliced(nodeIndex + 1, 0, node);
    if (nextNode) {
      nextNode.prevNodeId = node.node_id;
    }

    try {
      const recordedTransforms = await node.submit({
        session_id: this.session_id,
        node_id: node.node_id,
        prev_node_id: node.prevNodeId,
      });
      this.updateNodes(recordedTransforms);
    } catch (error) {
      this.nodes = this.nodes.filter((existingNode) => existingNode.node_id !== node.node_id);
      if (nextNode) {
        nextNode.prevNodeId = nextNodePrevNodeId ?? previousNodeId ?? nextNode.prevNodeId;
      }
      throw error;
    }
  }

  public async removeNode(nodeIndex: number): Promise<void> {
    const params = {
      session_id: this.session_id,
      node_id: this.nodes[nodeIndex].node_id,
    };
    const streamingResponse = await post("rpc/node/removeNode", params);
    const objs = await textBufferSparkStreamingApi(streamingResponse);
    const recordedTransforms: SparkTransform[] = parseJsonStream<SparkTransform>(objs);

    this.nodes.splice(nodeIndex, 1);
    this.updateNodes(recordedTransforms);
  }

  public async toggleNode(nodeIndex: number, toggle: boolean): Promise<void> {
    const params = {
      session_id: this.session_id,
      node_id: this.nodes[nodeIndex].node_id,
      toggle: toggle,
    };
    const streamingResponse = await post("rpc/node/toggleNode", params);
    const objs = await textBufferSparkStreamingApi(streamingResponse);
    const recordedTransforms: SparkTransform[] = parseJsonStream<SparkTransform>(objs);

    this.updateNodes(recordedTransforms);
  }

  public async submitNode(node: Node, params: any): Promise<void> {
    try {
      const recordedTransforms = await node.submit(params);
      this.updateNodes(recordedTransforms);
      footerPreview.run(this.session_id, node.node_id);
    } catch (error) {
      throw error;
    }
  }

  public updateNodes(transforms: SparkTransform[]): void {
    for (let i = 0; i < transforms.length; i++) {
      let nodeIndex = this.nodes.map((n) => n.node_id).indexOf(transforms[i].node_id);
      if (nodeIndex === -1) {
        continue;
      }

      let node = this.nodes[nodeIndex];
      if (nodeIndex > 0) {
        let prevNode = this.nodes[nodeIndex - 1];
        node.columnsOnNodeInput = prevNode.columnsOnNodeOutput;
      }
      node.columnsOnNodeOutput = transforms[i].columns;
      node.prevNodeId = transforms[i].prev_node_id;
      node.invalidState = transforms[i].invalid_state;
      if (typeof transforms[i].active === "boolean") {
        node.active = transforms[i].active;
      }
    }
  }
}

class GlobalAnalysesState {
  analyses: AnalysisSession[] = $state([]);

  constructor() {
    this.analyses = [];
  }

  public constructNodes(nodeTransforms: SparkTransform[]): Node[] {
    let nodes: Node[] = [];
    for (let i = 0; i < nodeTransforms.length; i++) {
      let node = nodeFactory({
        node_id: nodeTransforms[i].node_id,
        title: nodeTransforms[i].title,
        prevNodeId: nodeTransforms[i].prev_node_id,
        columnsOnNodeOutput: nodeTransforms[i].columns,
        active: nodeTransforms[i].active,
        invalidState: nodeTransforms[i].invalid_state,
      });
      node.setUserInput(JSON.parse(nodeTransforms[i].user_input));
      nodes.push(node);
      if (i > 0) {
        nodes[i].columnsOnNodeInput = nodes[i - 1].columnsOnNodeOutput;
      }
    }

    return nodes;
  }

  public async setAnalysisFromAPI(): Promise<void> {
    const streamingResponse = await fetch("http://localhost:4444/rpc/session/sessions");
    const objs = await textBufferSparkStreamingApi(streamingResponse);
    try {
      let analysesSnapshot = parseJsonStream<any>(objs);
      this.analyses = analysesSnapshot.map((analysisSnapshot: any) => {
        return new AnalysisSession({
          ...analysisSnapshot,
          nodes: this.constructNodes(analysisSnapshot.nodes),
        });
      });
    } catch (error) {
      console.log(error);
      this.analyses = [];
    }
  }
}

export const globalAnalysesState = $state(new GlobalAnalysesState());
