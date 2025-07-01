# OSHit ChangeLog

## v1.0.0

**Released: 2025-07-01**

- Updated for more recent versions of Textual.
  ([#36](https://github.com/davep/oshit/pull/36))
  ([#37](https://github.com/davep/oshit/pull/37))

## v0.12.5

**Released: 2025-06-30**

- Fix a crash due to an article missing a `score` and `title`.
  ([#34](https://github.com/davep/oshit/pull/34))

## v0.12.4

**Released: 2024-08-02**

- Fixed a crash when the HackerNews API returns `null` for an otherwise
  valid and available story.

## v0.12.3

**Released: 2024-07-24**

- Fixed a crash when the HackerNews API returns `null` for an otherwise
  valid and available story.

## v0.12.2

**Released: 2024-06-23**

- Pinned Textual.

## v0.12.1

**Released: 2024-06-16**

- Added a configuration dialog for tweaking the story fetching concurrency
  values.

## v0.12.0

**Released: 2024-06-09**

- Unpinned Textual, fixed a couple of issues the recent versions have
  introduced, and attempted to undo questionable upstream cosmetic choices.

## v0.11.2

**Released: 2024-05-24**

- Pinned Textual to <=0.60.1 due to ongoing problems with later versions.

## v0.11.1

**Released: 2024-03-10**

- Distribution update to support installation with Homebrew.

## v0.11.0

**Released: 2024-03-09**

- Once the first viewed tab has loaded, other tabs will start to load in the
  background (one after the other) as the user reads the first.
- Added a config option to turn off the above.
- Fixed a non-awaited-coroutine warning that could happen when quitting
  while loading items. ([#26](https://github.com/davep/oshit/issues/26))

## v0.10.0

**Released: 2024-02-28**

- Added option to search locally-loaded items and place the results in a
  search tab.
- Allowed Python 3.12.

## v0.9.0

**Released: 2024-02-09**

- Article text and poll answers are no longer "sticky"
  ([#21](https://github.com/davep/oshit/issues/21))

## v0.8.0

**Released: 2024-02-04**

- Added support for loading and viewing text associated with an item.
  ([#17](https://github.com/davep/oshit/issues/17))

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
