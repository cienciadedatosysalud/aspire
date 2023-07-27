<script>
	import { onMount } from "svelte";
	import Status from "./status.svelte";
	import {
		apiData,
		listProjects,
		ProjectsInfo,
		beggining_datetime,
		map_datetime,
		checking_datetime,
		dqa_datetime,
		validator_datetime,
		promise_upload_file,
		promise_check_sintax,
		promise_dqa,
		promise_validator,
		running_analysis,
		previous_analysis,
		step_running,
		status_fails,
		status_color,
	} from "./store";
	import { newNotification } from "../results/store";
	import {
		Button,
		Text,
		Timeline,
		Space,
		Notification,
		Divider,
		Center,
	} from "@svelteuidev/core";
	import { goto } from "$app/navigation";

	import { Check, Cross2 } from "radix-icons-svelte";
	import DataTable, { Head, Body, Row, Cell } from "@smui/data-table";
	import {Select} from "flowbite-svelte";
	/**
	 * @type {String}
	 */
	let selectedOption;

	/**
	 * @type {import("./store").ProjectInfo}
	 */
	let ProjectInfoSelected;

	onMount(async () => {
		if (!$running_analysis) {
			previous_analysis.set(false);
			status_fails.set(false)
			step_running.set(-1);
			beggining_datetime.set(new Date());
			map_datetime.set(new Date());
			checking_datetime.set(new Date());
			dqa_datetime.set(new Date());
			validator_datetime.set(new Date());
		}
		const response = await fetch("/api/projects");
		const data = await response.json();
		apiData.set(data);
	});

	async function mapData() {
		
		beggining_datetime.set(new Date());
		const formData = new FormData();
		for (const file of files) {
			formData.append("files", file, file.name);
		}
		const res = await fetch(`/api/uploadfiles/${ProjectInfoSelected}`, {
			method: "POST",
			body: formData,
		});
		const res_json = await res.json();

		map_datetime.set(new Date());
		if (res.status == 200) {
			step_running.set(0);
			return res_json["output"];
		} else {
			status_fails.set(true);
			running_analysis.set(false);
			throw new Error(res_json["detail"]);
		}
	}

	async function doChecking() {
		const res = await fetch(`/api/checking/${ProjectInfoSelected}`);
		const res_json = await res.json();

		checking_datetime.set(new Date());
		dqa_datetime.set(new Date());
		
		if (res.status == 200) {
			step_running.set(1);
			return res_json["output"];
		} else {
			status_fails.set(true);
			running_analysis.set(false);
			throw new Error(res_json["detail"]);
		}
	}

	async function doDQA() {
		const res = await fetch(`/api/dqa/${ProjectInfoSelected}`);

		const res_json = await res.json();
		dqa_datetime.set(new Date());
		if (res.status == 200) {
			step_running.set(2);
			return res_json["output"];
		} else {
			status_fails.set(true);
			running_analysis.set(false);
			throw new Error(res_json["detail"]);
		}
	}

	async function doValidator() {
		const res = await fetch(`/api/validator/${ProjectInfoSelected}`);
		const res_json = await res.json();
		validator_datetime.set(new Date());
		if (res.status == 200) {
			step_running.set(3);
			return res_json["output"];
		} else {
			status_fails.set(true);
			running_analysis.set(false);
			throw new Error(res_json["detail"]);
		}
	}

	/**
	 * @param {{ getTime: () => number; }} dateTimeValue2
	 * @param {{ getTime: () => number; }} dateTimeValue1
	 */
	// ref: https://www.tutorialspoint.com/how-to-calculate-minutes-between-two-dates-in-javascript
	function secondsDiff(dateTimeValue2, dateTimeValue1) {
		var differenceValue =
			(dateTimeValue2.getTime() - dateTimeValue1.getTime()) / 1000;
		return Math.abs(Math.round(differenceValue));
	}

	/**
	 * @type {any}
	 */
	let files;

	async function upload() {
		running_analysis.set(true);
		previous_analysis.set(true);
		status_fails.set(false)
		promise_upload_file.set(mapData());
		await $promise_upload_file;
		newNotification.set(true);
		if ($running_analysis) {
			promise_check_sintax.set(doChecking());
			await $promise_check_sintax;
		}
		if ($running_analysis) {
			promise_dqa.set(doDQA());
			await $promise_dqa;
		}
		if ($running_analysis) {
			promise_validator.set(doValidator());
			await $promise_validator;
		}
		step_running.set(4);
		running_analysis.set(false);
	}

	function goDownloads() {
		goto("/results");
	}

	function uploadFileClick() {
		document.getElementById("file-to-upload")?.click();
	}
</script>

<svelte:head>
	{#if !$running_analysis}<title>Map data</title>{/if}
	{#if $running_analysis}<title>Mapping data...</title>{/if}
	<meta name="Map your data" content="Map data" />
</svelte:head>

<h1>Map your data</h1>
<Space h="xl" />
<p>
	Select the project you want to participate in and introduce your data for
	analysis. Data should be extracted from your health information systems
	following the requirements and specifications of the data model of the use
	case in which you want to participate.
</p>
<Space h="xl" />
<Select
	bind:value={selectedOption}
	items={$listProjects}
	placeholder="Select one project"
	label="Select a project"
	on:change={() => (ProjectInfoSelected = $ProjectsInfo[selectedOption]["uuid"])}
/>
<Space h="xl" />
<Button color="dark" radius="lg" size="md" on:click={uploadFileClick}
	>Select your files</Button
>
<input
	id="file-to-upload"
	type="file"
	accept=".csv"
	multiple
	bind:files
	style="visibility:hidden;"
/>
{#if files && files["length"] > 0}
	<Divider
		label="Selected csv files"
		labelPosition="center"
		variant="dashed"
	/>
	<Center>
		<DataTable table$aria-label="db info" style="max-width: 100%;">
			<Head>
				<Row>
					<Cell style="text-align: left;">Filename</Cell>
					<Space w="xl" />
					<Space w="xl" />
					<Cell style="text-align: center;">Size</Cell>
				</Row>
			</Head>
			<Body>
				{#each files as file}
					<Row>
						<Cell>{file.name}</Cell>
						<Space w="xl" />
						<Space w="xl" />
						<Cell style="text-align: center;"
							>{file.size + " bytes"}</Cell
						>
					</Row>
				{/each}
			</Body>
		</DataTable>
	</Center>
{/if}

<Space h="xl" />
<Button
	color="dark"
	radius="lg"
	size="md"
	uppercase
	disabled={ProjectInfoSelected === undefined ||
		files === undefined ||
		$running_analysis}
	on:click={upload}
>
	Map and check your data
</Button>

<Space h="xl" />
<Space h="xl" />

<Timeline
	active={$step_running}
	color={$status_color}
	radius="lg"
	lineWidth={4}
	bulletSize={20}
>
	<Timeline.Item title="Mapping data" bullet={Status}>
		<Text size="xs"
			>{#if $step_running >= 0}
				{secondsDiff($map_datetime, $beggining_datetime)}
			{:else}
				0
			{/if}seconds</Text
		>
	</Timeline.Item>
	<Timeline.Item title="Checking data syntax" bullet={Status}>
		<Text size="xs"
			>{#if $step_running >= 1}{secondsDiff(
					$checking_datetime,
					$map_datetime
				)}{:else}
				0
			{/if} seconds</Text
		>
	</Timeline.Item>

	<Timeline.Item title="Launching data quality assesment" bullet={Status}>
		<Text size="xs"
			>{#if $step_running >= 2}{secondsDiff(
					$dqa_datetime,
					$checking_datetime
				)}{:else}
				0
			{/if} seconds</Text
		>
	</Timeline.Item>

	<Timeline.Item
		title="Checking data compliance with validation rules"
		lineVariant="dashed"
		bullet={Status}
	>
		<Text size="xs"
			>{#if $step_running >= 3}{secondsDiff(
					$validator_datetime,
					$dqa_datetime
				)}{:else}
				0
			{/if} seconds</Text
		>
	</Timeline.Item>

	<Timeline.Item title="All set! Go for the analyses" />
	<Space h="xl" />
	<Space h="xl" />
	<Button color="dark" disabled={$step_running < 3} on:click={goDownloads}
		>Download log</Button
	>
	<Space h="xl" />
	<Space h="xl" />
	{#if ($running_analysis || $previous_analysis) && $step_running >= -1}
		{#await $promise_upload_file}
			<!-- promise is pending -->
			<Notification
				title="Uploading data"
				loading
				withCloseButton={false}
			>
				Please wait while your files is being uploaded.
			</Notification>
			<Space h="xl" />
		{:then value}
			<!-- promise was fulfilled -->
			<Notification
				title='Log "Mapping data" preview. For more information go to the outputs tab and download the "mapping_input_files.log" file in the logs section.'
				icon={Check}
				color="teal"
				withCloseButton={false}
			>
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
			<Space h="xl" />
		{:catch error}
			<!-- promise was rejected -->
			<Notification icon={Cross2} color="red" withCloseButton={false}>
				<pre
					id="desc"
					style="float:left;color: #666666; width:95%; font-family: Candara,Trebuchet MS,sans-serif; font-size: 12px; font-weight: bold; border-right: thin dotted #666666; line-height: 18px;">
						{error}
					</pre>
			</Notification>
			<Space h="xl" />
		{/await}
	{/if}
	{#if ($running_analysis || $previous_analysis) && $step_running >= 0}
		{#await $promise_check_sintax}
			<!-- promise is pending -->
			<Notification
				title="Checking data syntax"
				loading
				withCloseButton={false}
			>
				Please wait while your data is being checked.
			</Notification>
			<Space h="xl" />
		{:then value}
			<!-- promise was fulfilled -->
			<Notification
				title='Log "Checking data syntax" preview. For more information go to the outputs tab and download the "checking_data_syntax.log" file in the logs section.'
				icon={Check}
				color="teal"
				withCloseButton={false}
			>
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
			<Space h="xl" />
		{:catch error}
			<!-- promise was rejected -->
			<Notification icon={Cross2} color="red" withCloseButton={false}>
				<div
					id="bodydesc"
					style="margin-left:auto; margin-right:auto; height: 200px; overflow-y: scroll;"
				>
					<pre
						id="desc"
						style="float:left;color: #666666; width:95%; font-family: Candara,Trebuchet MS,sans-serif; font-size: 12px; font-weight: bold; border-right: thin dotted #666666; line-height: 18px;">
						{error}
					</pre>
				</div>
			</Notification>
			<Space h="xl" />
		{/await}
	{/if}
	{#if ($running_analysis || $previous_analysis) && $step_running >= 1}
		{#await $promise_dqa}
			<!-- promise is pending -->
			<Notification
				title="Data Quality Assesment"
				loading
				withCloseButton={false}
			>
				Please wait while the data quality assessment is running.
			</Notification>
			<Space h="xl" />
		{:then value}
			<!-- promise was fulfilled -->
			<Notification
				title='Log "Data Quality Assesment" preview. For more information go to the outputs tab and download the "data_quality_assesment.log" file in the logs section.'
				icon={Check}
				color="teal"
				withCloseButton={false}
			>
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
			<Space h="xl" />
		{:catch error}
			<!-- promise was rejected -->
			<Notification icon={Cross2} color="red" withCloseButton={false}>
				<div
					id="bodydesc"
					style="margin-left:auto; margin-right:auto; height: 200px; overflow-y: scroll;"
				>
					<pre
						id="desc"
						style="float:left;color: #666666; width:95%; font-family: Candara,Trebuchet MS,sans-serif; font-size: 12px; font-weight: bold; border-right: thin dotted #666666; line-height: 18px;">
						{error}
					</pre>
				</div>
			</Notification>
			<Space h="xl" />
		{/await}
	{/if}
	{#if ($running_analysis || $previous_analysis) && $step_running >= 2}
		{#await $promise_validator}
			<!-- promise is pending -->
			<Notification
				title="Checking data compliance with validation rules"
				loading
				withCloseButton={false}
			>
				Please wait while data compliance with validation rules is running
			</Notification>
			<Space h="xl" />
		{:then value}
			<!-- promise was fulfilled -->
			<Notification
				title='Log "Checking data compliance with validation rules" preview. For more information go to the outputs tab and download the "checking_data_compliance.log" file in the logs section.'
				icon={Check}
				color="teal"
				withCloseButton={false}
			>
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
			<Space h="xl" />
		{:catch error}
			<!-- promise was rejected -->
			<Notification icon={Cross2} color="red" withCloseButton={false}>
				<div
					id="bodydesc"
					style="margin-left:auto; margin-right:auto; height: 200px; overflow-y: scroll;"
				>
					<pre
						id="desc"
						style="float:left;color: #666666; width:95%; font-family: Candara,Trebuchet MS,sans-serif; font-size: 12px; font-weight: bold; border-right: thin dotted #666666; line-height: 18px;">
						{error}
					</pre>
				</div>
			</Notification>
			<Space h="xl" />
		{/await}
	{/if}
</Timeline>
