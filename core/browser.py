from playwright.async_api import async_playwright
from config.settings import Config

class BrowserManager:
    def __init__(self, config: Config):
        self.config = config
        self.browser = None
        self.page = None
        self.playwright = None

    async def setup(self):
        """Setup browser dengan persistent context"""
        try:
            print("[🔄] Launching browser...")
            self.playwright = await async_playwright().start()
            
            self.browser = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.config.user_data_dir,
                headless=self.config.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-web-security"
                ],
                viewport=self.config.viewport,
                ignore_https_errors=True
            )
            
            self.page = self.browser.pages[0] if self.browser.pages else await self.browser.new_page()
            print("[✅] Browser ready!")
            return True
            
        except Exception as e:
            print(f"[❌] Browser setup failed: {e}")
            return False

    async def close(self):
        """Close browser resources"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def goto(self, url, **kwargs):
        """Navigate to URL dengan default settings"""
        defaults = {"wait_until": "networkidle", "timeout": 30000}
        defaults.update(kwargs)
        return await self.page.goto(url, **defaults)

    async def wait_for_timeout(self, milliseconds):
        """Shortcut untuk wait timeout"""
        await self.page.wait_for_timeout(milliseconds)