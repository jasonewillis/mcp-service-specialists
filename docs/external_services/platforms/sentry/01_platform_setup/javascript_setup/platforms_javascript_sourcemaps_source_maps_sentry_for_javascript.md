---
title: "Source Maps | Sentry for JavaScript"
source_url: "https://docs.sentry.io/platforms/javascript/sourcemaps/"
scraped_date: "2025-08-19T18:28:15.320326"
description: "Upload your source maps to Sentry to enable readable stack traces in your errors."
platform: "sentry"
category: "error_monitoring"
stack: "fed_job_advisor"
note: "Documentation focused on Fed Job Advisor production deployment"
---
**Note: This documentation is focused on production deployment for Fed Job Advisor**

# Source Maps | Sentry for JavaScript

HomePlatformsJavaScriptSource Maps Copy pageSource MapsUpload your source maps to Sentry to enable readable stack traces in your errors.To enable readable stack traces in your Sentry errors, you need to upload your source maps to Sentry. Learn how to unminify your JavaScript code by watching this video or reading the step-by-step instructions below.Uploading Source MapsThe easiest way to configure uploading source maps is by using the Sentry Wizard:BashCopiednpx @sentry/wizard@latest -i sourcemaps The wizard will guide you through the following steps:Logging into Sentry and selecting a projectInstalling the necessary Sentry packagesConfiguring your build tool to generate and upload source mapsConfiguring your CI to upload source mapsThis guide assumes you are using a Browser JavaScript SDK. For instructions on how to set up source maps for React Native, follow the source maps guide for React Native.If you want to configure source maps to upload manually, follow the guide for your bundler or build tool below.Sentry Bundler SupportwebpackRollupViteesbuildGuides for Source MapsTypeScript (tsc)If you're using one of webpack, Vite, Rollup, or Esbuild, use the corresponding Sentry plugin instead (see section "Sentry Bundler Support").UglifyJSSystemJSGitHub ActionsOther ToolsIf you're not using one of these tools, we assume you already know how to generate source maps with your toolchain and we recommend you upload them using Sentry CLI.Though we strongly recommend uploading source maps as part of your build process, for browser applications it's also possible to host your source maps publicly.Additional ResourcesUsing sentry-cli to Upload Source Maps4 Reasons Why Your Source Maps Are BrokenPreviousAPIsNextUploading Source MapsWas this helpful?Yes 👍No 👎How can we improve this page?Submit feedbackHelp improve this contentOur documentation is open source and available on GitHub. Your contributions are welcome, whether fixing a typo (drat!) or suggesting an update ("yeah, this would be better").How to contribute | Edit this page | Create a docs issue | Get support Package DetailsLatest version: 10.5.0npm:@sentry/browserRepository on GitHub