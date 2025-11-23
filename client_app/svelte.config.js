import adapter from "@sveltejs/adapter-static";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

const buildDir = "../service/static/client/build";

const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      pages: buildDir,
      assets: buildDir,
      fallback: "index.html",
      precompress: false,
      strict: true,
    }),
  },
};

export default config;
