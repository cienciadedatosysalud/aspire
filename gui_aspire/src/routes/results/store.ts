import { writable, derived } from 'svelte/store';

/** Store for your data. 
This assumes the data you're pulling back will be an array.
If it's going to be an object, default this to an empty object.
**/


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



//let ResponseArray:ProjectInfo[] = []
export const apiData = writable([]);

export const newNotification = writable(false);

/** Data transformation.
For our use case, we only care about the drink names, not the other information.
Here, we'll create a derived store to hold the drink names.
**/
/**export const drinkNames = derived(apiData, ($apiData) => {
  if ($apiData.drinks){
    return $apiData.drinks.map(drink => drink.strDrink);
  }
  return [];
});*/


export const listProjects = derived(apiData, ($apiData) => {

    const response:ProjectInfo[] = $apiData.projects
    if (response){
        return response.map(project => project.project);
        //return ["gola"]
    }
    return [];
  });

  export const listFiles = derived(apiData, ($apiData) => {

    const response:[] = $apiData.files
    if (response){
      return response
        //return ["gola"]
    }
    return [];
  });

export const ProjectsInfo = derived(apiData, ($apiData) => {
    const response:ProjectInfo[] = $apiData.projects
    if (response){
        return Object.assign({}, ...response.map((x) => ({[x.project]: x})));
        
        //response.map(project => project.data.metadata.project + ' - ' +project.data.metadata.use_case);
        //return ["gola"]
    }
    return {};
  });

  