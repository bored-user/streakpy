# Streakpy

Python script to keep Duoling streaks going. It works by accessing [the website](//duoling.com) on a headless-browser and practice the first (easiest) lesson. Until today (day 1), it only works with the Norwegian course (the one I'm currently taking). Maybe someday I'll add Latin, German or even Russian - which are the courses I intend on taking next.

Feel free to fork it and make it work with other courses, though.

### Dependencies

* [`pyppeteer`](//pypi.org/project/pyppeteer/)

### Setting up

In order to get this working, one needs to create a folder named `auth` on the repo's root, create a file named `username` (and write their username inside it) and one named `password` (obviously, with their password inside it). **Do not add any additional space/ newlines on these `auth/username` and `auth/password` files**.

As previously stated, **this script only works (so far) with the _Norwegian_ course**.<br><br>


Happy coding!
