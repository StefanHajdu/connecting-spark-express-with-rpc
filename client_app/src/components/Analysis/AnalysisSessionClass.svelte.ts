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

    public async submitNode(node: Node, params: any): Promise<void> {
        const recordedTransforms = await node.submit(params);
        console.log(`[SUBMIT] ${node.id} -> ${recordedTransforms.length}`);

        for (let i = 0; i < recordedTransforms.length; i++) {
            let nodeIndex = this.nodes.map((n) => n.id).indexOf(recordedTransforms[i].node_id);
            if (nodeIndex > 0) {
                let node = this.nodes[nodeIndex];
                let prevNode = this.nodes[nodeIndex - 1];
                node.columnsOnNodeInput = prevNode.columnsOnNodeOutput;
                node.columnsOnNodeOutput = recordedTransforms[i].columns;
                node.invalidState = recordedTransforms[i].invalid_state;
            }
        }
    }
}
