import { writable, derived } from 'svelte/store';
import type { DataInfo } from '../documentation/store';

export interface ProjectInfo {
    root_path: string;
    uuid: string;
    data: DataInfo;
  }

  export interface ScriptInfo {
    uuid: string;
    files: string[];
  }

export const apiData = writable([]);
export const apiFiles = writable([]);
export const dbInfo = writable([])



export const promise = writable(Promise.resolve());
export const status_promise = writable(false);
export const notification_execution = writable(false);

export const listProjects = derived(apiData, ($apiData) => {
    const response:ProjectInfo[] = $apiData.projects
    if (response){
        return response.map(x => ({value:x.data.metadata.project + ' - ' +x.data.metadata.use_case, 
        name:x.data.metadata.project + ' - ' +x.data.metadata.use_case}));
    }
    return [];
  });

export const ProjectsInfo = derived(apiData, ($apiData) => {
    const response:ProjectInfo[] = $apiData.projects
    if (response){
        return Object.assign({}, ...response.map((x) => ({[x.data.metadata.project + ' - ' +x.data.metadata.use_case]: x})));
    }
    return {};
  });

  export const listFiles = derived(apiFiles, ($apiFiles) => {
    const response:ScriptInfo[] = $apiFiles.scripts
    if (response){
        return response
    }
    return [];
  });


