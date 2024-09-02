//import { vitePreprocess } from "@sveltejs/kit/vite";
import {vitePreprocess} from "@sveltejs/vite-plugin-svelte"
import adapter from "@sveltejs/adapter-static";

export default {
  kit: {
    adapter: adapter({
      // default options are shown. On some platforms
      // these options are set automatically — see below
      pages: "front",
      assets: "front",
      fallback: null,
      precompress: false,
      strict: true,
    }),
  },

  preprocess: [vitePreprocess({})],
};
