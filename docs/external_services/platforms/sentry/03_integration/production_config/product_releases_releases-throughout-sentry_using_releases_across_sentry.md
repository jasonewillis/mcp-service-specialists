---
title: "Using Releases Across Sentry"
source_url: "https://docs.sentry.io/product/releases/releases-throughout-sentry/"
scraped_date: "2025-08-19T18:29:06.383406"
description: "Learn how to use releases throughout Sentry's product."
platform: "sentry"
category: "error_monitoring"
stack: "fed_job_advisor"
note: "Documentation focused on Fed Job Advisor production deployment"
---
**Note: This documentation is focused on production deployment for Fed Job Advisor**

HomeProduct WalkthroughsReleasesUsing Releases Across Sentry Copy pageUsing Releases Across SentryLearn how to use releases throughout Sentry's product.ChartsIn most charts, releases are grouped up and displayed as colored boxes underneath the chart. Hovering over the boxes shows a tooltip with the number of releases in that group. Clicking on a box opens a flyout drawer to let you explore the releases within that group.Releases List DrawerClicking on a release box underneath a chart opens a flyout drawer showing a zoomed-in view of the chart that was clicked on. This zoomed-in chart has the same time interval as the clicked releases box. There is also a table with a list of the releases inside that time interval. Selecting a single release from the chart or the table will open its details inside of the drawer.Release Details DrawerThe Release Details drawer gives a quick view of a release without leaving the current page. It shows new issues, commits, and files in the release. If you want to explore the Release further, you can click the "View Full Details" button in the top right corner of the flyout.Release Version LinkOutside of the Releases List page, hovering over any release version link will open a tooltip, showing a tiny preview of the release.Clicking the link will open the Release Details drawer with more details of the release, without leaving the current page.PreviousRelease HealthNextSentry ToolbarWas this helpful?Yes 👍No 👎How can we improve this page?Submit feedbackHelp improve this contentOur documentation is open source and available on GitHub. Your contributions are welcome, whether fixing a typo (drat!) or suggesting an update ("yeah, this would be better").How to contribute | Edit this page | Create a docs issue | Get support