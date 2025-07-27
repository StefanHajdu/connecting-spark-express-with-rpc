import type { AnalysisSnapshot } from "$lib/dtype";
import { nodeFactory, Node } from "../Nodes/NodeClass.svelte";
import { v4 as uuidv4 } from "uuid";
import type { IAnalysis } from "../../lib/dtype";
import { LS_KEY_ANALYSES, toLocalStorage } from "$lib/localStorageHandles";

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
                      colsInNode: [],
                      sumitted: false,
                  }),
              ];
    }

    public setSelected(selected: boolean): void {
        this.selected = selected;
    }

    public getSnapshot(): AnalysisSnapshot {
        return {
            id: $state.snapshot(this.id),
            name: $state.snapshot(this.name),
            status: $state.snapshot(this.status),
            buildTime: $state.snapshot(this.buildTime),
            resources: $state.snapshot(this.resources),
            rest: $state.snapshot(this.rest),
            selected: $state.snapshot(this.selected),
            nodes: this.nodes.map((node) => node.getClassSnapshot()),
        };
    }
}

export function rehydrateAnalysesFromLocalStorage(analysesRaw: IAnalysis[]): AnalysisSession[] {
    return analysesRaw.map((analysisRaw) => {
        return new AnalysisSession({
            ...analysisRaw,
            nodes: analysisRaw.nodes.map((nodeRaw) => {
                return nodeFactory(nodeRaw);
            }),
        });
    });
}

export function saveAnalysesToLocalStorage(analyses: AnalysisSession[]): void {
    toLocalStorage(
        LS_KEY_ANALYSES,
        analyses.map((analysis) => analysis.getSnapshot()),
    );
}
