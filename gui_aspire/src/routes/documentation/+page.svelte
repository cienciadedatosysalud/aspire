<script>
	import { onMount } from "svelte";
	import { apiData, listProjects, ProjectsInfo } from "./store";
	import { NativeSelect, Space, Text, Divider, Button } from "@svelteuidev/core";
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

<h1>Documentation</h1>
<p>
	In this page you can see the documentation of all the projects that are loaded
	in the application.
</p>

<NativeSelect
	bind:value={selectedOption}
	data={$listProjects}
	placeholder="Select one project"
	label="Select a project to view its information"
	on:change={() => (ProjectInfoSelected = $ProjectsInfo[selectedOption])}
/>

{#if ProjectInfoSelected}
<Space h="xl" />
<Button color="dark" on:click={downloadDocs}>Download documentation</Button>
<Space h="xl" />
	<Divider label="Metadata" labelPosition="center" size="md" />
	<p>
		<strong>Project: </strong>{ProjectInfoSelected.data.metadata.project}
	</p>
	<p>
		<strong>Use case: </strong>{ProjectInfoSelected.data.metadata.use_case}
	</p>
	<p>
		<strong>Funder: </strong>{ProjectInfoSelected.data.metadata.funder}
	</p>
	<p>
		<strong>Description: </strong>{ProjectInfoSelected.data.metadata
			.description}
	</p>
	<p>
		<strong>Notes: </strong>{ProjectInfoSelected.data.metadata.notes}
	</p>

	<Divider label="Cohort" labelPosition="center" size="md" />
	<p>
		<strong>Name: </strong>{ProjectInfoSelected.data.cohort.name}
	</p>
	<div style="display: flex">
		<Text
			><strong>Beggining study period: </strong>{ProjectInfoSelected.data
				.cohort.beggining_study_period}</Text
		>
		<Space w="lg" />
		<Text
			><strong>End study period: </strong>{ProjectInfoSelected.data.cohort
				.end_study_period}</Text
		>
	</div>
	<p>
		<strong>Inclusion criteria: </strong>{ProjectInfoSelected.data.cohort
			.inclusion_criteria}
	</p>
	<p>
		<strong>Exclusion criteria: </strong>{ProjectInfoSelected.data.cohort
			.exclusion_criteria}
	</p>
{/if}
