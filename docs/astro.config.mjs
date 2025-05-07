// @ts-check
import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

// https://astro.build/config
export default defineConfig({
  site: "https://nedhmn.github.io",
  base: "/streeteasy-scraper/",
  integrations: [
    starlight({
      title: "StreetEasy Scraper",
      favicon: "/favicon.svg",
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/nedhmn/streeteasy-scraper",
        },
      ],
      sidebar: [
        {
          label: "Getting Started",
          items: [
            { label: "Introduction", slug: "getting-started/introduction" },
            { label: "Installation", slug: "getting-started/installation" },
            { label: "Configuration", slug: "getting-started/configuration" },
            {
              label: "Running the Sync Profile",
              slug: "getting-started/running-the-sync-profile",
            },
          ],
        },
        {
          label: "Guides",
          items: [
            {
              label: "Setting Up The Async Profile",
              slug: "guides/setting-up-the-async-profile",
            },
            {
              label: "Running The Async Profile",
              slug: "guides/running-the-async-profile",
            },
            {
              label: "Providing Addresses for Scraping",
              slug: "guides/providing-addresses-for-scraping",
            },
          ],
        },
      ],
    }),
  ],
});
