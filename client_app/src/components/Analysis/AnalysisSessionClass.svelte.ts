import { post, textBufferSparkStreamingApi } from "$lib/clientApi";
import type { SparkTransform } from "$lib/dtype";
import { nodeFactory, Node } from "../Nodes/NodeClass.svelte";
import { v4 as uuidv4 } from "uuid";

export class AnalysisSession {
    id: string = $state("");
    name: string = $state("");
    status: string = $state("");
    buildTime: string = $state("");
    resources: string = $state("");
    rest: string = $state("");
    selected: boolean = $state(false);
    nodes: Node[] = $state([
        nodeFactory({
            title: "Load",
            colsInNode: [],
            sumitted: false,
        }),
    ]);

    constructor(params: any) {
        this.id = params.id ? params.id : "analysis-" + uuidv4();
        this.name = params.name ? params.name : "random-analysis-name-" + uuidv4();
        this.status = params.status ? params.status : "";
        this.buildTime = params.buildTime ? params.buildTime : "";
        this.resources = params.resources ? params.resources : "";
        this.rest = params.rest ? params.rest : "";
        this.selected = params.selected ? params.selected : false;
        this.nodes = params.nodes
            ? params.nodes
            : [
                  nodeFactory({
                      title: "Load",
                      columnsOnNodeInput: [],
                      sumitted: false,
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
            prevNodeId: this.nodes[prevNodeIndex].id,
            columnsOnNodeInput: this.nodes[prevNodeIndex].columnsOnNodeOutput,
        });

        // current node = nodeIndex, inserted node = nodeIndex + 1
        if (this.nodes[nodeIndex + 1]) {
            this.nodes[nodeIndex + 1].prevNodeId = node.id;
        }
        return node;
    }

    public async insertNode(node: Node, nodeIndex: number): Promise<void> {
        // submit empty node, empty node returns 'select * from df'
        let _ = await node.submit({
            session_id: this.id,
            node_id: node.id,
            prev_node_id: node.prevNodeId,
        });
        this.nodes = this.nodes.toSpliced(nodeIndex + 1, 0, node);
    }

    public async removeNode(nodeIndex: number): Promise<void> {
        const params = {
            session_id: this.id,
            node_id: this.nodes[nodeIndex].id,
        };
        const streamingResponse = await post("rpc/sessionNode/transform/removeNode", params);
        const objs = await textBufferSparkStreamingApi(streamingResponse);
        const recordedTransforms: SparkTransform[] = JSON.parse(objs);

        this.nodes.splice(nodeIndex, 1);
        this.updateNodes(recordedTransforms);
    }

    public async toggleNode(nodeIndex: number, toggle: boolean): Promise<void> {
        const params = {
            session_id: this.id,
            node_id: this.nodes[nodeIndex].id,
            toggle: toggle,
        };
        const streamingResponse = await post("rpc/sessionNode/transform/toggleNode", params);
        const objs = await textBufferSparkStreamingApi(streamingResponse);
        const recordedTransforms: SparkTransform[] = JSON.parse(objs);

        this.updateNodes(recordedTransforms);
    }

    public async submitNode(node: Node, params: any): Promise<void> {
        const recordedTransforms = await node.submit(params);
        this.updateNodes(recordedTransforms);
    }

    public updateNodes(transforms: SparkTransform[]): void {
        for (let i = 0; i < transforms.length; i++) {
            let nodeIndex = this.nodes.map((n) => n.id).indexOf(transforms[i].node_id);
            if (nodeIndex > 0) {
                let node = this.nodes[nodeIndex];
                let prevNode = this.nodes[nodeIndex - 1];
                node.columnsOnNodeInput = prevNode.columnsOnNodeOutput;
                node.columnsOnNodeOutput = transforms[i].columns;
                node.invalidState = transforms[i].invalid_state;
            }
        }
    }
}
