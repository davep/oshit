# OSHit ChangeLog

## v0.2.0

**Released: WiP**

- Tweaked the look of comment cards in the comments dialog.

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
