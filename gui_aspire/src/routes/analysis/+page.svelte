<script>
	import { onMount } from "svelte";
	import {
		apiData,
		listProjects,
		ProjectsInfo,
		listFiles,
		apiFiles,
		promise,
		status_promise,
		notification_execution,
		dbInfo
	} from "./store";
	import {
		Button,
		Space,
		Divider,
		Notification,
		Center,
	} from "@svelteuidev/core";

	import { newNotification } from "../results/store";

	import { Check, Cross2 } from "radix-icons-svelte";

	import DataTable, { Head, Body, Row, Cell } from "@smui/data-table";

	import {Select} from "flowbite-svelte";

	/**
	 * @type {String}
	 */
	let selectedProject;

	/**
	 * @type {String}
	 */
	let selectedScript;

	/**
	 * @type {import("./store").ProjectInfo}
	 */
	let ProjectInfoSelected;

	/**
	 * @type {any}
	 */
	let ScriptSelected;

	onMount(async () => {
		dbInfo.set([]);
		if (!$status_promise) {
			notification_execution.set(false);
		}
		const response = await fetch("/api/projects");
		const data = await response.json();
		apiData.set(data);
		const response_files = await fetch("/api/analysis");
		const data_files = await response_files.json();
		apiFiles.set(data_files);
	});

	/**
     * @type {any}
     */
	let listFilesProject;

	async function filterScripts() {
		notification_execution.set(false);
		ScriptSelected = undefined;
		ProjectInfoSelected = $ProjectsInfo[selectedProject]["uuid"];
		const response = await fetch(
			`/api/projects/dbinfo/${ProjectInfoSelected}`
		);
		const data = await response.json();
		dbInfo.set(data);
		let key = String(ProjectInfoSelected);
		let listFilesProject_ = $listFiles.filter(function (item) {
			return item.uuid == key;
		});
		const listFilesProject_2 = listFilesProject_[0].files;
		listFilesProject = listFilesProject_2.map((x) => ({value:x, 
        name:x}));
	}

	async function runAnalysis() {
		notification_execution.set(true);
		status_promise.set(true);
		const res = await fetch(
			`/api/analysis/${ProjectInfoSelected}/${ScriptSelected}`
		);
		const res_json = await res.json();
		status_promise.set(false);
		if (res.ok) {
			newNotification.set(true);
			return res_json["output"];
		} else {
			throw new Error(res_json["detail"]);
		}
	}

	function handleClick() {
		const promise_ = runAnalysis();
		promise.set(promise_);
	}


</script>

<svelte:head>
	{#if !$notification_execution}<title>Analysis</title>{/if}
	{#if $notification_execution}<title>Running analysis...</title>{/if}
	<meta name="description" content="Run analysis" />
</svelte:head>

<h1>Run analysis</h1>
<Space h="xl" />
<p>
	Select the project you want to participate in and launch the analyses provided by the project coordinators. Analyses scripts are open source and can be audited by anyone.
</p>
<Space h="xl" />
<Divider label="Projects" labelPosition="center" size="md" />
<Space h="xl" />
<Select
	bind:value={selectedProject}
	items={$listProjects}
	placeholder="Select one project"
	label="Select a project to run its analysis"
	on:change={() => filterScripts()}
/>
<Space h="xl" />
<Divider label="Mapped entities" labelPosition="center" size="md" />
{#if selectedProject}
	<Center>
		<DataTable table$aria-label="db info" style="max-width: 100%;">
			<Head>
				<Row>
					<Cell style="text-align: left;">Entity name</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">N registries</Cell
					>
				</Row>
			</Head>
			<Body>
				{#each $dbInfo as item}
					<Row>
						<Cell numeric>{item.entity}</Cell>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;"
							>{item.n_registries}</Cell
						>
					</Row>
				{/each}
			</Body>
		</DataTable>
	</Center>
{/if}

<Space h="xl" />
<Divider label="Scripts" labelPosition="center" size="md" />
<Space h="xl" />
<Select
	bind:value={selectedScript}
	items={listFilesProject}
	placeholder="Select one script"
	label="Select the main script to run."
	on:change={() => (ScriptSelected = selectedScript)}
/>
<Space h="xl" />
<Space h="xl" />
<Space h="xl" />
<Button
	color="dark"
	radius="lg"
	size="md"
	uppercase
	disabled={ProjectInfoSelected === undefined || ScriptSelected === undefined}
	on:click={handleClick}
>
	Run analysis
</Button>
<Space h="xl" />
<Space h="xl" />
{#if $status_promise || $notification_execution}
	{#await $promise}
		<!-- promise is pending -->
		<Notification title="Executing script" loading withCloseButton={false}>
			Please wait while your data is being analyzed.
		</Notification>
	{:then value}
		<!-- promise was fulfilled -->
		<Notification title='Log "Analysis Execution" preview. For more information go to the outputs tab and download the "analysis_execution.log" file in the logs section.' icon={Check} color="teal">
			<div
				id="bodydesc"
				style="margin-left:auto; margin-right:auto; height: 200px; overflow-y: scroll;"
			>
				<pre
					id="desc"
					style="float:left;color: #666666; width:95%; font-family: Candara,Trebuchet MS,sans-serif; font-size: 12px; font-weight: bold; border-right: thin dotted #666666; line-height: 18px;">
					{value}
				</pre>
			</div>
		</Notification>
	{:catch error}
		<!-- promise was rejected -->
		<Notification title='Log "Analysis Execution" error. For more information go to the outputs tab and download the "analysis_execution.log" file in the logs section.' icon={Cross2} color="red">
			<div
				id="bodydesc"
				style="margin-left:auto; margin-right:auto; height: 200px; overflow-y: scroll;"
			>
				<pre
					id="desc"
					style="float:left;color: #666666; width:auto; font-family: Candara,Trebuchet MS,sans-serif; font-size: 12px; font-weight: bold; border-right: thin dotted #666666; line-height: 18px;">
					{error}
			</pre>
			</div>
		</Notification>
	{/await}
{/if}
