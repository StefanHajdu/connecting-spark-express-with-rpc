import type { Analysis } from "./dtype";
import { nodeFactory } from "../components/Nodes/NodeClass.svelte";

export type AnalysesMock = Record<string, Analysis[]>;

export const analysesMock: AnalysesMock = {
    analyses: [
        {
            id: "id-analysis-#1",
            name: "Analysis #1",
            status: "build",
            buildTime: "10 min 10 sec",
            resources: "4 cores, 32gb",
            rest: "...",
            selected: false,
            nodes: [nodeFactory("Load", [])],
        },
        {
            id: "id-analysis-#2",
            name: "Analysis #2",
            status: "build",
            buildTime: "10 min 10 sec",
            resources: "4 cores, 32gb",
            rest: "...",
            selected: false,
            nodes: [nodeFactory("Load", [])],
        },
        {
            id: "id-analysis-#3",
            name: "Analysis #3",
            status: "build",
            buildTime: "10 min 10 sec",
            resources: "4 cores, 32gb",
            rest: "...",
            selected: false,
            nodes: [nodeFactory("Load", [])],
        },
    ],
};
