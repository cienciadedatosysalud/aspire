import { Face } from 'radix-icons-svelte';
import { writable, derived } from 'svelte/store';

/** Store for your data. 
This assumes the data you're pulling back will be an array.
If it's going to be an object, default this to an empty object.
**/



export interface ProjectInfo {
    root_path: string;
    uuid: string;
    data: DataInfo;
  }

  export interface ScriptInfo {
    uuid: string;
    files: string[];
  }

//let ResponseArray:ProjectInfo[] = []
export const apiData = writable([]);
export const apiFiles = writable([]);
export const dbInfo = writable([])



export const promise = writable(Promise.resolve());
export const status_promise = writable(false);
export const notification_execution = writable(false);

export const listProjects = derived(apiData, ($apiData) => {
    const response:ProjectInfo[] = $apiData.projects
    if (response){
        return response.map(project => project.data.metadata.project + ' - ' +project.data.metadata.use_case);
        //return ["gola"]
    }
    return [];
  });

export const ProjectsInfo = derived(apiData, ($apiData) => {
    const response:ProjectInfo[] = $apiData.projects
    if (response){
        return Object.assign({}, ...response.map((x) => ({[x.data.metadata.project + ' - ' +x.data.metadata.use_case]: x})));
        
        //response.map(project => project.data.metadata.project + ' - ' +project.data.metadata.use_case);
        //return ["gola"]
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


