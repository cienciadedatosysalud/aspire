<script>
	import { page } from "$app/stores";
	import atlaslogo from "$lib/images/atlas_logo.png";
	import github from "$lib/images/github.svg";
	import { Bell } from "radix-icons-svelte";
	import { newNotification } from "./results/store";
	import { scale } from "svelte/transition";
	import { quintOut } from "svelte/easing";
	
</script>

<header>
	<div class="corner">
		<a href="https://cienciadedatosysalud.org/" target="_blank">
			<img style="width: 100%; margin-left: 15px;" src={atlaslogo} alt="LogoAtlasVPM" />
		</a>
	</div>

	<nav>
		<svg viewBox="0 0 2 3" aria-hidden="true">
			<path d="M0,0 L1,2 C1.5,3 1.5,3 2,3 L2,0 Z" />
		</svg>
		<ul>
			<li aria-current={$page.url.pathname === "/" ? "page" : undefined}>
				<a href="/">Home</a>
			</li>
			<li
				aria-current={$page.url.pathname === "/mapdata"
					? "page"
					: undefined}
			>
				<a href="/mapdata">Map data</a>
			</li>
			
			<li
				aria-current={$page.url.pathname === "/analysis"
					? "page"
					: undefined}
			>
				<a href="/analysis">Run analysis</a>
			</li>
			
			<li
				aria-current={$page.url.pathname === "/results"
					? "page"
					: undefined}
			>
				<a href="/results"
					>Outputs
					{#if $newNotification}
						<div
							transition:scale={{
								duration: 500,
								delay: 500,
								opacity: 1,
								start: 0.5,
								easing: quintOut,
							}}
						>
							<Bell />
						</div>
					{/if}
				</a>
			</li>
			<hr class="dashed" style="height:30%;"/>
			<li
				aria-current={$page.url.pathname === "/documentation"
					? "page"
					: undefined}
			>
				<a href="/documentation">Documentation</a>
			</li>
			<hr class="dashed" style="height:30%;"/>
			<li
				aria-current={$page.url.pathname === "/about"
					? "page"
					: undefined}
			>
				<a href="/about">About</a>
			</li>
		</ul>
		<svg viewBox="0 0 2 3" aria-hidden="true">
			<path d="M0,0 L0,3 C0.5,3 0.5,3 1,2 L2,0 Z" />
		</svg>
	</nav>

	<div class="corner">
		<a href="https://github.com/cienciadedatosysalud" target="_blank">
			<img src={github} alt="GitHub" />
		</a>
	</div>
</header>

<style>
	header {
		display: flex;
		justify-content: space-between;
	}

	.corner {
		width: 3em;
		height: 3em;
	}

	.corner a {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.corner img {
		width: 2em;
		height: 2em;
		object-fit: contain;
	}

	nav {
		display: flex;
		justify-content: center;
		--background: rgba(255, 255, 255, 0.7);
	}

	svg {
		width: 2em;
		height: 3em;
		display: block;
	}

	path {
		fill: var(--background);
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background: var(--background);
		background-size: contain;
	}

	li {
		position: relative;
		height: 100%;
	}

	li[aria-current="page"]::before {
		--size: 6px;
		content: "";
		width: 0;
		height: 0;
		position: absolute;
		top: 0;
		left: calc(50% - var(--size));
		border: var(--size) solid transparent;
		border-top: var(--size) solid var(--color-theme-1);
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.5rem;
		color: var(--color-text);
		font-weight: 700;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	a:hover {
		color: var(--color-theme-1);
	}
	
</style>
