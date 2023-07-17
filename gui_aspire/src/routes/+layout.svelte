<script>
  import "../app.postcss";
  import Header from "./Header.svelte";
  import "./styles.css";
  import { SvelteUIProvider } from "@svelteuidev/core";
</script>

<SvelteUIProvider>
  <div class="app">
    <Header />

    <main>
      <slot />
    </main>

    <!--<footer>
			<p>
				visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to learn
				SvelteKit
			</p>
		</footer>-->
  </div>
</SvelteUIProvider>

<style>
  .app {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  main {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    width: 100%;
    max-width: 64rem;
    margin: 0 auto;
    box-sizing: border-box;
  }
  
</style>
