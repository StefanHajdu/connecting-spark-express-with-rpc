import type { IAnalysis } from "./dtype";

export type AnalysesMock = Record<string, IAnalysis[]>;

export const analysesMock: any = {
    analyses: [
        {
            id: "id-analysis-#1",
            name: "Analysis #1",
            status: "build",
            buildTime: "10 min 10 sec",
            resources: "4 cores, 32gb",
            rest: "...",
            selected: true,
        },
        {
            id: "id-analysis-#2",
            name: "Analysis #2",
            status: "build",
            buildTime: "10 min 10 sec",
            resources: "4 cores, 32gb",
            rest: "...",
            selected: false,
        },
        {
            id: "id-analysis-#3",
            name: "Analysis #3",
            status: "build",
            buildTime: "10 min 10 sec",
            resources: "4 cores, 32gb",
            rest: "...",
            selected: false,
        },
    ],
};
