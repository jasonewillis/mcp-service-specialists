---
title: "API Reference"
source_url: "https://docs.sentry.io/api/"
scraped_date: "2025-08-19T18:29:31.613593"
description: ""
platform: "sentry"
category: "error_monitoring"
stack: "fed_job_advisor"
note: "Documentation focused on Fed Job Advisor production deployment"
---
**Note: This documentation is focused on production deployment for Fed Job Advisor**

HomeAPI Reference Copy pageAPI ReferenceThe Sentry web API is used to access the Sentry platform programmatically. You can use the APIs to manage account-level resources, like organizations and teams, as well as manage and export data.If you're looking for information about the API surface for Sentry's SDKs, see the SDK Development docs.VersioningThe current version of the Sentry's web API is considered v0. Our public endpoints are generally stable, but beta endpoints are subject to change.Getting StartedAuthenticationPaginationPermissionsRate LimitsRequestsSentry API TutorialsTutorial: Create a Sentry Authentication TokenTutorial: Create and List Teams with the Sentry APIChoosing the Right API Base DomainWhile many of our APIs use sentry.io as the host for API endpoints, if you want to indicate a specific data storage location, you should use region-specific domains.US region is hosted on us.sentry.ioDE region is hosted on de.sentry.io.To find out which API resources are available on region-based domains, see what types of data are stored where for more information.PreviousSentry CLINextAuthenticationWas this helpful?Yes 👍No 👎How can we improve this page?Submit feedback