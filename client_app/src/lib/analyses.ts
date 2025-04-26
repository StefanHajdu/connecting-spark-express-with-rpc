interface Analysis {
	id: string;
	name: string;
	status: string;
	buildTime: string;
	resources: string;
	rest: string;
	selected: boolean;
}

export type AnalysesMock = Record<string, Analysis>;

export const analysesMock: AnalysesMock = {
	'id-analysis-#1': {
		id: 'id-analysis-#1',
		name: 'Analysis #1',
		status: 'build',
		buildTime: '10 min 10 sec',
		resources: '4 cores, 32gb',
		rest: '...',
		selected: false
	},
	'id-analysis-#2': {
		id: 'id-analysis-#2',
		name: 'Analysis #2',
		status: 'build',
		buildTime: '10 min 10 sec',
		resources: '4 cores, 32gb',
		rest: '...',
		selected: false
	},
	'id-analysis-#3': {
		id: 'id-analysis-#3',
		name: 'Analysis #3',
		status: 'build',
		buildTime: '10 min 10 sec',
		resources: '4 cores, 32gb',
		rest: '...',
		selected: false
	}
};
