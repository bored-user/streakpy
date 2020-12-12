# streakpy

Python script to keep Duoling streaks going. It works by accessing [the website](//duoling.com) on a headless-browser and practice the first (easiest) lesson. Until today (day 1), it only works with the Norwegian course (the one I'm currently taking). Maybe someday I'll add Latin, German or even Russian - which are the courses I intend on taking next.

Feel free to fork it and make it work with other courses, though.

### Dependencies

* [`pyppeteer`](//pypi.org/project/pyppeteer/)

### Setting up

In order to get this working, one needs to create a folder named `auth` on the repo's root, create a file named `username` (and write their username inside it) and one named `password` (obviously, with their password inside it). **Do not add any additional space/ newlines on these `auth/username` and `auth/password` files**.

As previously stated, **this script only works (so far) with the _Norwegian_ course**.
Edit: Even though I haven't tested, technically speaking, it'd possible to support other languages by creating a file with the language name and `json` extension (e.g `Norwegian.json`, `German.json`, `Russian.json`) inside the `languages` folder and make the script (`app.py`) load it on line 10 (where there currently is a `language = json.load(open('languages/Norwegian.json'))` command). Just switch `Norwegian.json` by `[YOUR_LANGUAGE_HERE_WITHOUT_BRACKETS].json`. Remember to write the language code on a property called `code` (inside the `json` file), Duolingo `url`, and `name` (see below), just like on `Norwegian.json`.

### languages/[language].json file

On the `languages/[language].json` file, there are some fields which I'd like to go in depth about.
* `url` is the url to be accessed by the script - normally, the first lesson of a course.
* `name` is literally the language name in English (e.g `Norwegian`, `German`, `Portuguese`, `Englihsh`, `Polish`, etc - **with a capital letter**).
* The `code` key is meant to identify the language code used by Google Translator.
* The `exceptions` object is a cheap way to make exceptions when Google Translator gets the translation wrong. Roughly speaking, sometimes, Google Translator messes things up, making the script to fail on the exercise. Duolingo's learning system, however, don't just "forget" wrong exercises. They get passed all the way to the end of the queue of exercises. That means that, when Google Translator gets a translation wrong, if nothing else happened, it'd keep getting the translation wrong, and Duoling would keep appending the wrong exercise to the back of the queue - generating what's known as an infinite loop.<br>
To avoid this, I created the `exceptions` object works kinda like this: When it a sentence should be translated, the script first looks into the `exceptions` object to make sure that the key isn't there. If it is, it (script) uses it (listed exception). If not, it translates with Google Translator. If the translation is wrong, it reads the correct translation (provided by Duolingo) and adds it to the `exceptions` object, avoiding future infinite loops.

### realtime.png

Originally, this was just a debugging thing. The script took a screenshot (aprox.) every time the page refreshed, so I could just sit there and watch as the page was refreshed and the screenshot was overwritten; kind of a video. But then, I noticed it's extremely useful, because it allows me to know what the script is doing (and it's very funny to just run the script and watch as the video progresses); so, I decided to let it there. Everytime the script finishes (every one round of exercises), `realtime.png` is deleted.
