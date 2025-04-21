import asyncio
from playwright.async_api import async_playwright
from faker import Faker
import time
import sys


async def run():
    # Get URL from argv or ask the user, and strip whitespace
    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
    else:
        url = input("Introduce la URL a probar: ").strip()
    fake = Faker()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to the provided URL
        await page.goto(url)
        # Wait for the form inputs to be visible
        await page.wait_for_selector('input[name="first_name"]')

        # Generate random data
        first = fake.first_name()
        last = fake.last_name()
        email = fake.email()

        # Fill the form
        await page.fill('input[name="first_name"]', first)
        await page.fill('input[name="last_name"]', last)
        await page.fill('input[name="email"]', email)

        # Submit the form
        await page.click('button[type="submit"][form="intruqt-user-details-form"]')
        # Wait for navigation or next screen
        await page.wait_for_load_state("networkidle")

        print(f"✅ Form submitted with: {first} {last}, {email}")

        # Click the “Start” button and wait for the next screen
        await page.click('button:has-text("Start")')
        await page.wait_for_load_state("networkidle")

        await page.wait_for_selector(
            'div[role="progressbar"][aria-valuenow="100"]',
            timeout=3_600_000,  # 60 minutos en ms
        )
        await asyncio.sleep(5)
        await page.click('button.bg-lab-action-primary:has-text("Start")')
        await page.wait_for_load_state("networkidle")
        print("✅ Second Start clicked and background processing completed")

        await asyncio.sleep(5)

        await page.keyboard.type('yes "" | ./attack.sh')
        await page.keyboard.press("Enter")
        print('✅ Comando `yes "" | ./attack.sh` enviado')

        await asyncio.sleep(10 * 60)

        await browser.close()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
