<script>
	import { onDestroy, onMount } from "svelte";
	import {
		Button,
		Divider,
		Space,
		Center,
		Modal,
	} from "@svelteuidev/core";
	import {
		apiData,
		listProjects,
		ProjectsInfo,
		listFiles,
		newNotification,
	} from "./store";
	import { File } from "radix-icons-svelte";
	import DataTable, { Head, Body, Row, Cell } from "@smui/data-table";
	import {Select} from "flowbite-svelte";
	/**
	 * @type {String}
	 */
	let selectedOption;

	onMount(async () => {
		newNotification.set(false);
		const response = await fetch("/api/results");
		const data = await response.json();
		apiData.set(data);
	});
	

	/**
	 * @type {any}
	 */
	let listFilesTabHtml = [];

	/**
	 * @type {any}
	 */
	let listFilesTabCsv = [];

	/**
	 * @type {any}
	 */
	let listFilesTabjson = [];

	/**
	 * @type {any}
	 */
	let listFilesTabZip = [];

	/**
	 * @type {any}
	 */
	let listFilesTabOthers = [];

	/**
	 * @type {any}
	 */
	let listFilesTabLogs = [];

	/**
	 * @param {any} filename
	 */
	async function downloadFile(filename) {
		let project_id = $ProjectsInfo[selectedOption]["uuid"];
		let res = await fetch(
			`/api/download/${project_id}/${filename}`,
			{
				method: "GET",
			}
		);
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

	/**
	 * @param {string} project_uuid
	 */
	function projectChange(project_uuid) {
		listFilesTabHtml = $listFiles.filter(function (item) {
			return (
				item.uuid == project_uuid &&
				item.filename.split(".")[1].toLowerCase() == "html"
			);
		});

		listFilesTabCsv = $listFiles.filter(function (item) {
			return (
				item.uuid == project_uuid &&
				item.filename.split(".")[1].toLowerCase() == "csv"
			);
		});

		listFilesTabjson = $listFiles.filter(function (item) {
			return (
				item.uuid == project_uuid &&
				item.filename.split(".")[1].toLowerCase() == "json"
			);
		});

		listFilesTabZip = $listFiles.filter(function (item) {
			return (
				item.uuid == project_uuid &&
				item.filename.split(".")[1].toLowerCase() == "zip"
			);
		});

		listFilesTabLogs = $listFiles.filter(function (item) {
			return (
				item.uuid == project_uuid &&
				item.filename.split(".")[1].toLowerCase() == "log"
			);
		});

		listFilesTabOthers = $listFiles.filter(function (item) {
			return (
				item.uuid == project_uuid &&
				!["zip", "html", "csv", "json", "log"].includes(
					item.filename.split(".")[1].toLowerCase()
				)
			);
		});
	}

	async function deleteAllFiles() {
		let project_id = $ProjectsInfo[selectedOption]["uuid"];
		await fetch(
			`/api/delete/${project_id}`,
			{
				method: "DELETE",
			}
		);

		const response = await fetch("/api/results");
		const data = await response.json();
		apiData.set(data);
		selectedOption = "";
		deletedModalOpened = false;
	}

	let deletedModalOpened = false;
</script>

<svelte:head>
	<title>Outputs</title>
	<meta name="Outputs" content="Outputs" />
</svelte:head>

<h1>Outputs</h1>
<Space h="xl" />
<p>
	Retrieve your outputs once the analyses have run successfully. Outputs from
	the analysis may include interactive reports (in HTML format), the DQA
	report of the data analysed (in HTML format) and aggregated data files to
	share for the federated analysis for each use case.
</p>
<p>(If you cannot select a project, it means that no output files have been found for any of the loaded projects.)</p>
<Space h="xl" />
<Divider label="List of projects" labelPosition="center" size="md" />
<Space h="xl" />
<Select
	bind:value={selectedOption}
	items={$listProjects}
	placeholder="Select one project"
	label="Select a project to view its result files"
	on:change={() => projectChange($ProjectsInfo[selectedOption]["uuid"])}
/>
<Space h="xl" />
<Divider label="Output files" labelPosition="center" size="md" />
{#if selectedOption}
	{#if listFilesTabHtml.length > 0}
	<Divider label="HTML files" labelPosition="center" variant="dashed" />
	<Center>
		<DataTable table$aria-label="db info" style="max-width: 100%;">
			<Head>
				<Row>
					<Cell style="text-align: left;">Filename</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Date</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Action</Cell>
				</Row>
			</Head>
			<Body>
				{#each listFilesTabHtml as item}
					<Row>
						<Cell>{item.filename}</Cell>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;"
							>{item.created_at}</Cell
						>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;">
							<Button
								variant="outline"
								on:click={() => downloadFile(item.filename)}
								><File /> <Space w="xs" /> Download</Button
							></Cell
						>
					</Row>
				{/each}
			</Body>
		</DataTable>
	</Center>
	{/if}
	{#if listFilesTabCsv.length > 0}
	<Divider label="CSV files" labelPosition="center" variant="dashed" />
	<Center>
		<DataTable table$aria-label="db info" style="max-width: 100%;">
			<Head>
				<Row>
					<Cell style="text-align: left;">Filename</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Date</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Action</Cell>
				</Row>
			</Head>
			<Body>
				{#each listFilesTabCsv as item}
					<Row>
						<Cell>{item.filename}</Cell>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;"
							>{item.created_at}</Cell
						>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;">
							<Button
								variant="outline"
								on:click={() => downloadFile(item.filename)}
								><File /> <Space w="xs" /> Download</Button
							></Cell
						>
					</Row>
				{/each}
			</Body>
		</DataTable>
	</Center>
	{/if}
	{#if listFilesTabjson.length > 0}
	<Divider label="JSON files" labelPosition="center" variant="dashed" />
	<Center>
		<DataTable table$aria-label="db info" style="max-width: 100%;">
			<Head>
				<Row>
					<Cell style="text-align: left;">Filename</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Date</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Action</Cell>
				</Row>
			</Head>
			<Body>
				{#each listFilesTabjson as item}
					<Row>
						<Cell>{item.filename}</Cell>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;"
							>{item.created_at}</Cell
						>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;">
							<Button
								variant="outline"
								on:click={() => downloadFile(item.filename)}
								><File /> <Space w="xs" /> Download</Button
							></Cell
						>
					</Row>
				{/each}
			</Body>
		</DataTable>
	</Center>
	{/if}
	{#if listFilesTabZip.length > 0}
	<Divider label="ZIP files" labelPosition="center" variant="dashed" />
	<Center>
		<DataTable table$aria-label="db info" style="max-width: 100%;">
			<Head>
				<Row>
					<Cell style="text-align: left;">Filename</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Date</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Action</Cell>
				</Row>
			</Head>
			<Body>
				{#each listFilesTabZip as item}
					<Row>
						<Cell>{item.filename}</Cell>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;"
							>{item.created_at}</Cell
						>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;">
							<Button
								variant="outline"
								on:click={() => downloadFile(item.filename)}
								><File /> <Space w="xs" /> Download</Button
							></Cell
						>
					</Row>
				{/each}
			</Body>
		</DataTable>
	</Center>
	{/if}
	{#if listFilesTabLogs.length > 0}
	<Divider label="Log files" labelPosition="center" variant="dashed" />
	<Center>
		<DataTable table$aria-label="db info" style="max-width: 100%;">
			<Head>
				<Row>
					<Cell style="text-align: left;">Filename</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Date</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Action</Cell>
				</Row>
			</Head>
			<Body>
				{#each listFilesTabLogs as item}
					<Row>
						<Cell>{item.filename}</Cell>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;"
							>{item.created_at}</Cell
						>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;">
							<Button
								variant="outline"
								on:click={() => downloadFile(item.filename)}
								><File /> <Space w="xs" /> Download</Button
							></Cell
						>
					</Row>
				{/each}
			</Body>
		</DataTable>
	</Center>
	{/if}
	{#if listFilesTabOthers.length > 0}
	<Divider label="OTHERS files" labelPosition="center" variant="dashed" />
	<Center>
		<DataTable table$aria-label="db info" style="max-width: 100%;">
			<Head>
				<Row>
					<Cell style="text-align: left;">Filename</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Date</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Action</Cell>
				</Row>
			</Head>
			<Body>
				{#each listFilesTabOthers as item}
					<Row>
						<Cell>{item.filename}</Cell>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;"
							>{item.created_at}</Cell
						>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;">
							<Button
								variant="outline"
								on:click={() => downloadFile(item.filename)}
								><File /> <Space w="xs" /> Download</Button
							></Cell
						>
					</Row>
				{/each}
			</Body>
		</DataTable>
	</Center>
	{/if}
	<Divider labelPosition="center" size="md" />
	<Space h="xl" />
	<Button color="red" on:click={() => (deletedModalOpened = true)}
		>Delete all files</Button
	>
	<Modal
		opened={deletedModalOpened}
		on:close={() => (deletedModalOpened = false)}
		centered
		withCloseButton={false}
	>
		<p>Are you sure you want to delete all files in the outputs folder?</p>
		<p><strong>This operation is not reversible.</strong></p>
		<Center
			><Button color="red" on:click={deleteAllFiles}>
				Remove</Button
			></Center
		>
	</Modal>
{/if}
