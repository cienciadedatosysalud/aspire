<script>
	import mainlogo from "$lib/images/main_logo.png";
	import eulogo from "$lib/images/eu_flag.jpg";
	import {
		Center,
		Text,
		Divider,
		Space,
		Timeline,
	} from "@svelteuidev/core";
	import { typewriter } from "@svelteuidev/motion";
	import { onMount } from "svelte";
	import {
		Footer,
		FooterBrand,
		FooterCopyright,
		FooterLink,
		FooterLinkGroup,
	} from "flowbite-svelte";
	let text = "Deploy, Check and Run";
	let visible = false;
	
	onMount(async () => {
		visible = true;
	});

	let active = 0

	setInterval(() => {
		active = (active + 1) % 3
	}, 1500);
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Analysis producer app" />
</svelte:head>

<section>
	<h1>
		<span class="welcome">
			<Center>
				<!--<source srcset={welcome} type="image/webp" />-->
				<img
					src={mainlogo}
					alt="Project logo"
					style="max-width: 60%;
				height: auto;"
				/>
			</Center>
		</span>
		{#if visible}
			<p in:typewriter={{ speed: 2 }}>{text}</p>
		{/if}
	</h1>
</section>

<Center>
	<Divider
		label="Steps to follow"
		labelPosition="center"
		style="min-width: 60%;max-width: 55%;"
	/>
</Center>
<Space h="xs" />

<Center>
	<Timeline color="yellow" active={active} lineWidth={4} bulletSize={20}>
		<Timeline.Item title="Map data">
			<Text color="dimmed" size="sm"
				>Select project and map input data</Text
			>
		</Timeline.Item>

		<Timeline.Item title="Run analysis" lineVariant="dashed">
			<Text color="dimmed" size="sm"
				>Select project and launch analysis</Text
			>
		</Timeline.Item>

		<Timeline.Item title="Retrieve outputs">
			<Text color="dimmed" size="sm"
				>Once analyses have run successfully</Text
			>
		</Timeline.Item>
	</Timeline>
</Center>
<Footer class="absolute bottom-0 left-0 z-20 w-full">
	<div style="width: 325px;">
	<FooterBrand  src={eulogo} style= "float:left"/>
	<FooterCopyright href="/" by="Atlas VPM" year={2023} /></div>
	<FooterLinkGroup
		ulClass="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0"
	>
		<FooterLink href="/about">About</FooterLink>
		<FooterLink href="/about#authors">Author(s)</FooterLink>
		<FooterLink href="/about#funding">Funding</FooterLink>
		<FooterLink href="/about#termsconditions">Terms&Conditions</FooterLink>
		<FooterLink href="https://cienciadedatosysalud.org/en/contact/"
			>Contact</FooterLink
		>
	</FooterLinkGroup>
</Footer>
<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
</style>
