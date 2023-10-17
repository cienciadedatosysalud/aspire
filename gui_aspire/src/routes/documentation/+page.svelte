<script>
	import { onMount } from "svelte";
	import { apiData, listProjects, ProjectsInfo } from "./store";
	import {Space, Text, Divider, Button } from "@svelteuidev/core";
	import {Select} from "flowbite-svelte";
	import { _ } from 'svelte-i18n'
	import.meta.env.MODE;
	/**
	 * @type {String}
	 */
	let selectedOption;

	/**
	 * @type {import("./store").ProjectInfo}
	 */
	let ProjectInfoSelected;

	onMount(async () => {
		const response = await fetch("/api/projects");
		const data = await response.json();
		apiData.set(data);
	});

	async function downloadDocs(){
		const filename = "documentation.zip"
		let project_id = $ProjectsInfo[selectedOption]["uuid"];
		let res = await fetch(`/api/datamodel/${project_id}`);
		let blob = await res.blob();
		var url = window.URL || window.webkitURL;
		let link = url.createObjectURL(blob);
		let a = document.createElement("a");
		a.setAttribute("download", `${filename}`);
		a.setAttribute("href", link);
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
	}

</script>

<svelte:head>
	<title>Documentation</title>
	<meta name="Documentation" content="Documentation" />
</svelte:head>

<h1>{$_('documentation.title')}</h1>
<Space h="xl" />
<p>
	{$_('documentation.explanation')}
</p>
<Space h="xl" />
<Select
	bind:value={selectedOption}
	items={$listProjects}
	placeholder="{$_('documentation.selector_project')}"
	label="Select a project to view its information"
	on:change={() => (ProjectInfoSelected = $ProjectsInfo[selectedOption])}
/>

{#if ProjectInfoSelected}
<Space h="xl" />
<Button color="dark" on:click={downloadDocs}>{$_('documentation.button_download')}</Button>
<Space h="xl" />
	<Divider label="{$_('documentation.label_metadata')}" labelPosition="center" size="md" />
	<p>
		<strong>{$_('documentation.doc_project')} </strong>{ProjectInfoSelected.data.metadata.project}
	</p>
	<p>
		<strong>{$_('documentation.doc_usecase')} </strong>{ProjectInfoSelected.data.metadata.use_case}
	</p>
	<p>
		<strong>{$_('documentation.doc_funder')} </strong>{ProjectInfoSelected.data.metadata.funder}
	</p>
	<p>
		<strong>{$_('documentation.doc_description')} </strong>{ProjectInfoSelected.data.metadata
			.description}
	</p>
	<p>
		<strong>{$_('documentation.doc_notes')} </strong>{ProjectInfoSelected.data.metadata.notes}
	</p>

	<Divider label="{$_('documentation.label_cohort')}" labelPosition="center" size="md" />
	<p>
		<strong>{$_('documentation.doc_name')} </strong>{ProjectInfoSelected.data.cohort.name}
	</p>
	<Space h="xs" />
	<div style="display: flex">
		<Text
			><strong>{$_('documentation.doc_bstudydate')} </strong>{ProjectInfoSelected.data
				.cohort.beggining_study_period}</Text
		>
		<Space w="lg" />
		<Text
			><strong>{$_('documentation.doc_estudydate')} </strong>{ProjectInfoSelected.data.cohort
				.end_study_period}</Text
		>
	</div>
	<Space h="xs" />
	<p>
		<strong>{$_('documentation.doc_icriteria')} </strong>{ProjectInfoSelected.data.cohort
			.inclusion_criteria}
	</p>
	<p>
		<strong>{$_('documentation.doc_ecriteria')} </strong>{ProjectInfoSelected.data.cohort
			.exclusion_criteria}
	</p>
{/if}
