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
	import { _ } from 'svelte-i18n'
	import {
		Footer,
		FooterBrand,
		FooterCopyright,
		FooterLink,
		FooterLinkGroup,
	} from "flowbite-svelte";
	let text = "Deploy >> Check >> Run";
	let text_app = "Analytic Software Pipeline Interface for Reproducible Execution"
	let text_app_short = "ASPIRE"
	let visible = false;
	let visible2 = false;
	let visible3 = false;
	onMount(async () => {
		visible = true;
		visible2 = true
		setTimeout(() => {
			visible2 = false 
			}, 2500);
		setTimeout(() => {
			visible3 = true}, 3000);
	});

	let active = 0
	let color_ = "yellow"
	setInterval(() => {
		active = (active + 1) % 3
		if(active==2){
			color_ = "green"
		}
		else{
			color_ = "yellow"
		}
	}, 1500);

	import { blur } from 'svelte/transition'; 
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
			<p in:typewriter={{ speed: 2 }}>{$_('home.banner')}</p>
			
		{/if}
		{#if visible2}
			<p style="font-size: 30px;" in:blur={{duration: 500}} out:blur={{duration: 500}}>{text_app}</p>
		{/if}
		{#if visible3}
			<p in:blur={{delay: 0, duration: 1000}}>{text_app_short}</p>
		{/if}
	</h1>
</section>

<Center>
	<Divider
		label="{$_('home.steps_follow')}"
		labelPosition="center"
		style="min-width: 60%;max-width: 55%;"
	/>
</Center>
<Space h="xs" />

<Center>
	<Timeline color={color_} active={active} lineWidth={4} bulletSize={20}>
		<Timeline.Item title="{$_('home.map_data_title')}">
			<Text color="dimmed" size="sm"
				>{$_('home.map_data_text')}</Text
			>
		</Timeline.Item>

		<Timeline.Item title="{$_('home.runanalysis_title')}" lineVariant="dashed">
			<Text color="dimmed" size="sm"
				>{$_('home.runanalysis_text')}</Text
			>
		</Timeline.Item>

		<Timeline.Item title="{$_('home.retrieve_outputs_title')}">
			<Text color="dimmed" size="sm"
				>{$_('home.retrieve_outputs_text')}</Text
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
		<FooterLink href="/about">{$_('footer.about')}</FooterLink>
		<FooterLink href="/about#authors">{$_('footer.authors')}</FooterLink>
		<FooterLink href="/about#funding">{$_('footer.funding')}</FooterLink>
		<FooterLink href="/about#termsconditions">{$_('footer.termconditions')}</FooterLink>
		<FooterLink href="https://cienciadedatosysalud.org/en/contact/"
			>{$_('footer.contact')}</FooterLink
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
