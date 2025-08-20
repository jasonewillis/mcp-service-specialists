---
title: "Set Up Feature Flags | Sentry for Python"
source_url: "https://docs.sentry.io/platforms/python/feature-flags/"
scraped_date: "2025-08-19T18:27:45.907233"
description: "With Feature Flags, Sentry tracks feature flag evaluations in your application, keeps an audit log of feature flag changes, and reports any suspicious updates that may have caused an error."
platform: "sentry"
category: "error_monitoring"
stack: "fed_job_advisor"
note: "Documentation focused on Fed Job Advisor production deployment"
---
**Note: This documentation is focused on production deployment for Fed Job Advisor**

# Set Up Feature Flags | Sentry for Python

HomePlatformsPythonFeature Flags Copy pageSet Up Feature FlagsWith Feature Flags, Sentry tracks feature flag evaluations in your application, keeps an audit log of feature flag changes, and reports any suspicious updates that may have caused an error.PrerequisitesYou have the Python SDK installed.Enable Evaluation TrackingIf you use a third-party SDK to evaluate feature flags, you can enable a Sentry SDK integration to track those evaluations. Integrations are provider specific. Documentation for supported SDKs is listed below.LaunchDarklyOpenFeature (multiple providers supported)StatsigUnleashGeneric APIIf you use an unsupported solution, you can use the generic API to manually track feature flag evaluations. These evaluations are held in memory and are sent to Sentry on error and transaction events. At the moment, we only support boolean flag evaluations.PythonCopiedimport sentry_sdk from sentry_sdk.feature_flags import add_feature_flag add_feature_flag('test-flag', False) # Records an evaluation and its result. sentry_sdk.capture_exception(Exception("Something went wrong!")) Go to your Sentry project and confirm that your error event has recorded the feature flag "test-flag" and its value "false".Enable Change TrackingChange tracking requires registering a Sentry webhook with a feature flag provider. For set up instructions, visit the documentation for your provider:FlagsmithLaunchDarklyStatsigUnleashGenericPreviousSet Up User FeedbackNextSet Up Security Policy ReportingWas this helpful?Yes 👍No 👎How can we improve this page?Submit feedbackHelp improve this contentOur documentation is open source and available on GitHub. Your contributions are welcome, whether fixing a typo (drat!) or suggesting an update ("yeah, this would be better").How to contribute | Edit this page | Create a docs issue | Get support Package DetailsLatest version: 2.35.0pypi:sentry-sdkRepository on GitHubAPI documentation