import { writable, derived } from 'svelte/store';

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


export const apiData = writable([]);

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



export const beggining_datetime = writable( new Date());
export const map_datetime = writable( new Date());
export const checking_datetime = writable( new Date());
export const dqa_datetime = writable( new Date());
export const validator_datetime = writable( new Date());


export const promise_upload_file = writable(Promise.resolve());
export const promise_check_sintax = writable(Promise.resolve());
export const promise_dqa = writable(Promise.resolve());
export const promise_validator = writable(Promise.resolve());

export const running_analysis = writable(false)
export const previous_analysis = writable(false)

export const step_running = writable(-1)
export const status_fails = writable(false)

export const status_color = derived(status_fails, ($status_fails) => {
  if ($status_fails){
      return "red"
  }
  return "green";
});