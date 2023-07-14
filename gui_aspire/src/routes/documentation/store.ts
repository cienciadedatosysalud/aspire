import { writable, derived } from 'svelte/store';

/** Store for your data. 
This assumes the data you're pulling back will be an array.
If it's going to be an object, default this to an empty object.
**/

interface CohortInfo {
    name: string;
    inclusion_criteria: string;
    exclusion_criteria:string;
    beggining_study_period: string;
    end_study_period: string;
    description: string;
    cohort_definition_inclusion: string;
    cohort_definition_exclusion: string;
}
interface AuthorInfo {
    name: string;
    affiliation: string;
    id:string;
}

interface MetadataInfo {
    authors: AuthorInfo[];
    description: string;
    document: string;
    funder: string;
    keywords: string[]
    license: string;
    notes: string;
    project: string;
    spatial_coverage: string;
    url_project: string;
    use_case: string;
    uuid: string;
    version_sem: string;
    work_package: string;
}

 interface DataInfo {
    cohort: CohortInfo;
    metadata: MetadataInfo;
  }

export interface ProjectInfo {
    root_path: string;
    uuid: string;
    data: DataInfo;
  }


//let ResponseArray:ProjectInfo[] = []
export const apiData = writable([]);

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