---
title: "Enriching Events | Sentry for Python"
source_url: "https://docs.sentry.io/platforms/python/enriching-events/"
scraped_date: "2025-08-19T18:27:45.906420"
description: "Enrich events with additional context to make debugging simpler."
platform: "sentry"
category: "error_monitoring"
stack: "fed_job_advisor"
note: "Documentation focused on Fed Job Advisor production deployment"
---
**Note: This documentation is focused on production deployment for Fed Job Advisor**

# Enriching Events | Sentry for Python

HomePlatformsPythonEnriching Events Copy pageEnriching EventsEnrich events with additional context to make debugging simpler.AttachmentsLearn more about how Sentry can store additional files in the same request as event attachments.BreadcrumbsLearn more about what Sentry uses to create a trail of events (breadcrumbs) that happened prior to an issue.ContextCustom contexts allow you to attach arbitrary data (strings, lists, dictionaries) to an event.ScopesSDKs will typically automatically manage the scopes for you in the framework integrations. Learn what a scope is and how you can use it to your advantage.TagsTags power UI features such as filters and tag-distribution maps. Tags also help you quickly access related events and view the tag distribution for a set of events.Transaction NameLearn how to set or override the transaction name to capture the user and gain critical pieces of information that construct a unique identity in Sentry.UsersLearn how to configure the SDK to capture the user and gain critical pieces of information that construct a unique identity in Sentry.PreviousIntegrationsNextAttachmentsWas this helpful?Yes 👍No 👎How can we improve this page?Submit feedbackHelp improve this contentOur documentation is open source and available on GitHub. Your contributions are welcome, whether fixing a typo (drat!) or suggesting an update ("yeah, this would be better").How to contribute | Edit this page | Create a docs issue | Get support Package DetailsLatest version: 2.35.0pypi:sentry-sdkRepository on GitHubAPI documentation