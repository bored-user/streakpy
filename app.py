import asyncio
import os
import time

from pyppeteer import launch

page = browser = None
cwd = os.path.dirname(os.path.realpath(__file__))


async def wait_loading(query):
    element = await page.querySelector(query)

    while element == None:
        await page.screenshot({'path': 'wait.png'})
        element = await page.querySelector(query)
        time.sleep(0.1)

    return element


async def login(username, password):
    await (await wait_loading('a[data-test=have-account]')).click()

    # Replace with your email/ username and password
    await (await page.querySelector("input[placeholder='Email or username']")).type(username)
    await (await page.querySelector("input[placeholder='Password']")).type(password)
    await (await page.querySelector('button[type=submit]')).click()


async def start_lesson():
    await (await wait_loading('div[data-test=skill-icon]')).click()
    await (await wait_loading('button[data-test=start-button]')).click()

    await wait_loading('button[data-test=quit-button]')


async def skip_exercise():
    skip_btn = await page.querySelector('button[data-test=player-skip]')
    can_skip = await page.evaluate("() => document.querySelector('button[data-test=player-skip]') === null ? 'None' : document.querySelector('button[data-test=player-skip]').innerHTML === 'Can\'t listen now'") != 'None' or await page.evaluate("() => document.querySelector(\"div[data-test='challenge challenge-name'] img\") === null ? 'None': ''") != 'None'

    await skip_btn.click() if can_skip else None
    return can_skip


async def solve_exercise():
    pass


async def next_exercise():
    continue_btn = 'button[data-test=player-next]'
    
    await wait_loading(continue_btn)
    await (await page.querySelector(continue_btn)).click()

async def main():
    global browser
    global page

    browser = await launch()
    page = await browser.newPage()
    f = open('auth/username')
    username = f.read()
    f.close()
    f = open('auth/password')
    password = f.read()
    f.close()

    await page.setViewport({'width': 1920, 'height': 948})
    await page.goto('https://www.duolingo.com/?isLoggingIn=true')
    await login(username, password)
    await start_lesson()

    while True:
        if not await skip_exercise():
            await solve_exercise()

        next_exercise()

        time.sleep(2)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
