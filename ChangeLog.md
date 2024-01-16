# OSHit ChangeLog

## v0.4.0

**Released: 2024-01-16**

- Added support for loading and displaying polls.

## v0.3.0

**Released: 2024-01-15**

- Added a quick way of visiting links within comments.

## v0.2.0

**Released: 2023-01-07**

- Tweaked the look of comment cards in the comments dialog.
- Expanding the replies of a comment is now an open/close toggle.

## v0.1.1

**Released: 2023-01-01**

- Made the gathering of items from the API less greedy, limiting the number
  of concurrent connections (yes, 500+ connections all at once is kind of a
  bad idea who knew?). Default limit is 50.
- Added a configuration option to the configuration file for the above.
- Added a connection timeout setting to the configuration file; hopefully
  useful for folk who are on slower connections.

## v0.1.0

**Released: 2023-01-01**

- Initial release.

[//]: # (ChangeLog.md ends here)
