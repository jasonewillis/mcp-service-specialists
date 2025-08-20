---
title: "Tutorial: Create a Sentry Authentication Token"
source_url: "https://docs.sentry.io/api/guides/create-auth-token/"
scraped_date: "2025-08-19T18:29:31.613966"
description: ""
platform: "sentry"
category: "error_monitoring"
stack: "fed_job_advisor"
note: "Documentation focused on Fed Job Advisor production deployment"
---
**Note: This documentation is focused on production deployment for Fed Job Advisor**

HomeAPI ReferenceTutorial: Create a Sentry Authentication Token Copy pageTutorial: Create a Sentry Authentication TokenTo use Sentry's APIs, you must have an authentication token. This tutorial walks you through creating an organizational auth token through an internal integration. Sentry recommends using organizational auth tokens whenever possible, as they aren't linked to specific user accounts.See our documentation on authentication to learn more about the different types of authentication tokens available.PrerequisitesA Sentry account with an organization-level role of Manager or Admin.Create an Internal IntegrationInternal integrations are used to create custom Sentry integrations for your organization. They can also be used to create and manage your organization tokens.Open sentry.ioClick "Settings" in the left menu to open the Organization Settings page.Click "Custom Integrations" in the left side panel to create a new internal integration and org-level auth token.Press the "Create New Integration" button.Make sure "Internal Integration" is selected in the modal and press "Next".Enter a name for your integration.Create a API Authentication TokenUnder "Permissions" select the permissions required for the APIs you wish to call.Each API endpoint docs page lists the required permissions, in the "Scopes" section. For example, the Create a New Project endpoint requires project:write permissions or higher.Click "Save Changes".Scroll down to the bottom of the page and copy the generated token under "Tokens".Keep your auth token around on your clipboard or in an environment variable to use in API calls.PreviousTutorial: Create and List Teams with the Sentry APINextAuthenticationWas this helpful?Yes 👍No 👎How can we improve this page?Submit feedback