from config.settings import Config
from core.browser import BrowserManager
from pages.login_page import LoginPage
from pages.antrean_page import AntreanPage

class CorrectFlowBot:
    def __init__(self):
        self.config = Config()
        self.browser_manager = None
        self.login_page = None
        self.antrean_page = None

    async def initialize(self):
        """Initialize semua komponen"""
        self.browser_manager = BrowserManager(self.config)
        if not await self.browser_manager.setup():
            return False
            
        self.login_page = LoginPage(self.browser_manager)
        self.antrean_page = AntreanPage(self.browser_manager)
        return True

    async def run_login(self):
        """Jalankan proses login"""
        print("\n" + "=" * 50)
        print("[1️⃣] STEP 1: LOGIN PROCESS")
        print("=" * 50)
        return await self.login_page.login()

    async def run_antrean(self):
        """Jalankan proses antrean"""
        print("\n" + "=" * 50)
        print("[2️⃣] STEP 2: ANTREAN PROCESS") 
        print("=" * 50)
        return await self.antrean_page.process_antrean()

    async def run(self):
        """Main execution flow"""
        print("🚀 CORRECT FLOW BOT STARTED")
        print(f"📧 Username: {self.config.username}")
        print(f"🏪 Butik: {self.config.butik_value}")
        print(f"⏰ Target Time: {self.config.target_time} (Client Time)")
        
        # Initialize
        if not await self.initialize():
            return False

        try:
            # Login
            if not await self.run_login():
                return False

            # Antrean
            success = await self.run_antrean()
            
            if success:
                print("\n" + "✅" * 20)
                print("✅ BOT COMPLETED SUCCESSFULLY!")
                print("✅" * 20)
            else:
                print("\n❌ Bot finished with issues")
            
            return success
            
        except Exception as e:
            print(f"[❌] Main execution error: {e}")
            return False
        finally:
            print("\n💤 Browser remains open...")
            print("🛑 Close manually when done")
            input("Press ENTER to exit script...")