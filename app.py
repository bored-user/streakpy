import asyncio
import json
import os
import time

from pyppeteer import launch

page = browser = None
cwd = os.path.dirname(os.path.realpath(__file__))
language = json.load(open('languages/Norwegian.json', 'r'))


async def wait_loading(query, page=None):
    if page == None:
        page = globals()['page']

    element = await page.querySelector(query)

    while element == None:
        await page.screenshot({'path': 'realtime.png'})
        element = await page.querySelector(query)
        time.sleep(0.1)

    await page.screenshot({'path': 'realtime.png'})
    return element


async def login(username, password):
    await (await wait_loading('a[data-test=have-account]')).click()
    await (await page.querySelector("input[placeholder='Email or username']")).type(username)
    await (await page.querySelector("input[placeholder='Password']")).type(password)
    await (await page.querySelector('button[type=submit]')).click()


async def start_lesson():
    await (await wait_loading('div[data-test=skill-icon]')).click()
    await (await wait_loading('button[data-test=start-button]')).click()

    await wait_loading('button[data-test=quit-button]')


async def skip_exercise():
    skip_btn = await page.querySelector('button[data-test=player-skip]')
    can_skip = bool(await (page.evaluate("b => b.innerText === \"CAN'T LISTEN NOW\" || b.innerText === \"CAN'T SPEAK NOW\"", skip_btn))) if skip_btn != None else False

    if can_skip:
        await skip_btn.click()

    return can_skip


async def translate(sentence, language):
    browser = await launch()
    page = await browser.newPage()

    await page.goto(f'https://translate.google.com/?sl=auto&tl={language}&text={sentence}&op=translate')
    translation = await page.evaluate('node => node.innerText', (await wait_loading('span[jsname=jqKxS]', page)))

    await browser.close()
    return translation


async def get_sentence(): return (await page.querySelectorAllEval(
    'span[data-test=hint-sentence] > *', "words => encodeURIComponent(words.map(word => word.innerHTML).join(''))"))


async def solve_exercise():
    await page.screenshot({'path': 'realtime.png'})

    try:
        code = language['code'] if await page.querySelectorEval('h1[data-test=challenge-header] span', 'h => h.textContent') == 'Write this in Norwegian (Bokmål)' else 'en'
        sentence = await get_sentence()

        await (await page.querySelector('textarea[data-test=challenge-translate-input]')).type((await translate(sentence, code)) if not sentence in language['exceptions'] else language['exceptions'][sentence])
        await next_exercise()
    except:
        pass


async def check_mistake():
    mistake = await page.querySelector("div[data-test='blame blame-incorrect']")
    if mistake == None:
        return

    language['exceptions'] = {} if not 'exceptions' in language else language['exceptions']
    language['exceptions'][await get_sentence()] = (await page.evaluate('m => m.children[1].children[0].children[0].children[1]', mistake))


async def next_exercise():
    continue_btn = 'button[data-test=player-next]'

    await wait_loading(continue_btn)
    await (await page.querySelector(continue_btn)).click()


async def main():
    global browser
    global page

    browser = await launch()
    page = await browser.newPage()

    await page.setViewport({'width': 1920, 'height': 948})
    await page.goto('https://www.duolingo.com/?isLoggingIn=true')

    with open('auth/username') as username, open('auth/password') as password:
        await login(username.read(), password.read())

    await start_lesson()

    while True:
        await solve_exercise() if not await skip_exercise() else None
        await check_mistake()
        await next_exercise()

        if (((await page.querySelector('div[data-test=skill-tree]')) != None) and ((await page.querySelector('div[data-test=tree-section]')) != None) or (await page.querySelectorEval('button[data-test=quit-button]', "b => b.nextSibling.children[0].getAttribute('style').split('; ')[1].split(': ')[1].replace(';', '') == '100%'"))):
            os.remove('realtime.png')
            json.dump(language, open('languages/Norwegian.json', 'w'))
            break

        time.sleep(1)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    exit()
