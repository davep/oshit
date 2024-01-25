# OSHit ChangeLog

## v0.7.0

**Released: 2024-01-25**

- Added the option to turn off the title-bar-based updating display of the
  age of the items.
- Fixed not being able to change tabs with left/right during a reload.

## v0.6.0

**Released: 2024-01-23**

- Simplified the header bar, disabling Textual's mouse toggle of the height,
  and removing the "icon" in the top left corner.

## v0.5.0

**Released: 2024-01-17**

- Added support for optional numbering of items in each list.
  ([#11](https://github.com/davep/oshit/issues/11))
- Added support for placing caps on the number of items to fetch in each
  list. ([#11](https://github.com/davep/oshit/issues/11))

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
