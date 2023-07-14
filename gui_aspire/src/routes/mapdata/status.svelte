<script>
	import { Check, Cross2 } from "radix-icons-svelte";
    import {
		status_fails
	} from "./store";
</script>

{#if !$status_fails}
    <Check  />
{:else}
    <Cross2 />
{/if}   