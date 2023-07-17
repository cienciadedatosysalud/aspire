import { writable, derived } from 'svelte/store';

export interface ProjectInfo {
  project: string;
  uuid: string;
}

export interface FileInfo {
  complete_name: string;
  uuid: string;
  filename: string;
  created_at: string;
}


export const apiData = writable([]);

export const newNotification = writable(false);


export const listProjects = derived(apiData, ($apiData) => {

    const response:ProjectInfo[] = $apiData.projects
    if (response){
      return response.map(x => ({value:x.project, name:x.project}));
    }
    return [];
  });

  export const listFiles = derived(apiData, ($apiData) => {

    const response:[] = $apiData.files
    if (response){
      return response
    }
    return [];
  });

export const ProjectsInfo = derived(apiData, ($apiData) => {
    const response:ProjectInfo[] = $apiData.projects
    if (response){
        return Object.assign({}, ...response.map((x) => ({[x.project]: x})));
    }
    return {};
  });

  