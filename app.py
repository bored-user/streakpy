import asyncio
import json
import os
import time

from pyppeteer import launch

duolingo = browser = None
cwd = os.path.dirname(os.path.realpath(__file__))
language = json.load(open('languages/Norwegian.json', 'r'))


async def wait_loading(query, page=None):
    if page == None:
        page = globals()['duolingo']

    element = await page.querySelector(query)

    while element == None:
        await page.screenshot({'path': 'realtime.png'})
        element = await page.querySelector(query)
        time.sleep(0.1)

    await page.screenshot({'path': 'realtime.png'})
    return element


async def login(username, password):
    await (await wait_loading('a[data-test=have-account]')).click()
    await (await duolingo.querySelector("input[placeholder='Email or username']")).type(username)
    await (await duolingo.querySelector("input[placeholder='Password']")).type(password)
    await (await duolingo.querySelector('button[type=submit]')).click()

    print('Logged in!')


async def start_lesson():
    await wait_loading('div[data-test=skill-icon]')
    await duolingo.goto(language['url'])
    await wait_loading('button[data-test=quit-button]')

    print('Started lesson!\n')


async def skip_exercise():
    skip_btn = await duolingo.querySelector('button[data-test=player-skip]')
    can_skip = bool(await (duolingo.evaluate("b => b.innerText === \"CAN'T LISTEN NOW\" || b.innerText === \"CAN'T SPEAK NOW\"", skip_btn))) if skip_btn != None else False

    if can_skip:
        await skip_btn.click()
        print('Skipped speaking/ listening exercise!')

    return can_skip


async def translate(sentence, language, translator):
    await translator.goto(f'https://translate.google.com/?sl=auto&tl={language}&text={sentence}&op=translate')
    translation = await translator.evaluate('node => node.innerText', (await wait_loading('span[jsname=jqKxS]', translator)))

    return translation


async def get_sentence(): return (await duolingo.querySelectorAllEval('span[data-test=hint-sentence] > *', "words => encodeURIComponent(words.map(word => word.innerHTML).join(''))"))


async def solve_exercise(translator):
    await duolingo.screenshot({'path': 'realtime.png'})

    try:
        code = language['code'] if language['name'] in await duolingo.querySelectorEval('h1[data-test=challenge-header] span', 'h => h.textContent') else 'en'
        sentence = await get_sentence()

        await (await duolingo.querySelector('textarea[data-test=challenge-translate-input]')).type((await translate(sentence, code, translator)) if not sentence in language['exceptions'] else language['exceptions'][sentence])
        await click_next()

        print('Solved writting exercise!')
    except:
        pass


async def check_mistake():
    mistake = await duolingo.querySelector("div[data-test='blame blame-incorrect']")
    if mistake == None:
        return

    sentence = await get_sentence()
    correct_form = await duolingo.evaluate('m => m.children[1].children[0].children[0].children[1].textContent', mistake)

    language['exceptions'] = {} if not 'exceptions' in language else language['exceptions']
    language['exceptions'][sentence] = correct_form

    print(f'Found an exception:\n    -> Input: {sentence}\n    -> Correct form: {correct_form}\nAlready added to exception list!')


async def click_next():
    continue_btn = 'button[data-test=player-next]'

    await wait_loading(continue_btn)
    await (await duolingo.querySelector(continue_btn)).click()


async def tidy_up():
    os.remove('realtime.png')
    json.dump(language, open('languages/Norwegian.json', 'w'))

    while duolingo.url != 'https://www.duolingo.com/learn':
        await click_next()
        time.sleep(0.1)

    time.sleep(2)
    await browser.close()


async def main():
    print('Starting...')

    global browser
    global duolingo

    browser = await launch()
    duolingo = await browser.newPage()
    translator = await browser.newPage()

    await duolingo.setViewport({'width': 1920, 'height': 948})
    await translator.setViewport({'width': 1920, 'height': 948})

    await duolingo.goto('https://www.duolingo.com/')

    with open('auth/username') as username, open('auth/password') as password:
        await login(username.read(), password.read())

    await start_lesson()

    while True:
        await solve_exercise(translator) if not await skip_exercise() else None
        await check_mistake()
        await click_next()

        if await duolingo.querySelectorEval('button[data-test=quit-button]', "b => b.nextSibling.children[0].style.width == '100%'"):
            await tidy_up()
            break

        time.sleep(2)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

    print('\nFinished! Bye!')
    exit()
