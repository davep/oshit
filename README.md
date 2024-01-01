# OSHit -- Get your hit of the Orange Site in the terminal

## Introduction

OSHit is a read-only terminal-based client for HackerNews. It provides the
ability to view all the top/recent items in the major categories, as well as
allowing viewing comments and user details. Where relevant, bindings are
always available to open the relevant view on HackerNews itself in your web
browser.

Please note that this client *isn't* designed to allow reading any and all
stories on HackerNews, it's about reading what's current "hot" or new,
within the categories provided by [their
API](https://github.com/HackerNews/API).

## Installing

The package can be installed using [`pipx`](https://pypa.github.io/pipx/):

```sh
$ pipx install oshit
```

Once installed run the `oshit` command.

## Main features

When run up the opening display is a list of items, the initial list being
the current top stories and jobs on HackerNews. Other lists available, via
shortcut keys or via tabs at the top of the screen, are "New", "Best",
"Ask", "Show" and "Jobs".

![The main index](https://raw.githubusercontent.com/davep/oshit/main/images/oshit-index.png)

Pressing <kbd>u</kbd> when viewing a job or a comment will open a dialog
that shows the details of the user who posted the item.

![Viewing user details](https://raw.githubusercontent.com/davep/oshit/main/images/oshit-user-dialog.png)

When viewing a story or job and pressing <kbd>c</kbd> a dialog will open
that will let you view and navigate its comments.

![Viewing comments](https://raw.githubusercontent.com/davep/oshit/main/images/oshit-comments.png)

## Getting help

If you need help, or have any ideas, please feel free to [raise an
issue](https://github.com/davep/oshit/issues) or [start a
discussion](https://github.com/davep/oshit/discussions).

## TODO

Things I'm considering adding or addressing:

- [ ] Some degree of caching of items to reduce API hits.
- [ ] Expand the text-cleaning code to handle links, etc.
- [ ] Look at some "markup" of comments, eg: make quoted text more obvious.
- [ ] Add searching
  - [ ] Amongst the current view
  - [ ] Amongst loaded comments within comment view
  - [ ] All of history ([`hn.algolia.com`](https://hn.algolia.com/api))

[//]: # (README.md ends here)
