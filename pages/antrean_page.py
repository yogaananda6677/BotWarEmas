import datetime
import asyncio
from utils.helpers import TimeHelper

class AntreanPage:
    def __init__(self, browser_manager):
        self.browser = browser_manager
        self.config = browser_manager.config
        self.time_helper = TimeHelper()

    async def navigate_to_antrean(self):
        """Klik Menu Antrean"""
        try:
            print("[📍] Looking for Menu Antrean button...")
            menu_btn = await self.browser.page.query_selector('a:has-text("Menu Antrean")')
            
            if menu_btn:
                await menu_btn.click()
                print("[✅] Clicked Menu Antrean!")
                await self.browser.wait_for_timeout(1000)
                return True
            return False
        except Exception as e:
            print(f"[❌] Error navigating to antrean: {e}")
            return False

    async def select_butik(self):
        """Pilih butik"""
        try:
            await self.browser.page.wait_for_selector("#site", timeout=10000)
            await self.browser.page.select_option("#site", value=self.config.butik_value)
            print("[✅] Butik selected!")
            
            # Submit pemilihan butik
            submit_btn = await self.browser.page.query_selector('.btn-primary, button[type="submit"]')
            if submit_btn:
                await submit_btn.click()
                print("[✅] Butik submitted!")
                await self.browser.wait_for_timeout(1000)
                return True
            return False
        except Exception as e:
            print(f"[❌] Error selecting butik: {e}")
            return False

    async def select_time_option(self):
        """Pilih opsi waktu pertama"""
        try:
            select_element = await self.browser.page.query_selector('#wakda')
            if select_element:
                await select_element.select_option(index=1)
                print("[✅] Selected first available time option")
                return True
            return False
        except Exception as e:
            print(f"[❌] Error selecting time: {e}")
            return False

    async def click_ambil_antrean(self):
        """Klik button Ambil Antrean"""
        try:
            ambil_btn = await self.browser.page.query_selector(
                '.btn-warning:has-text("Ambil Antrean"), button:has-text("Ambil Antrean")'
            )
            if ambil_btn:
                await ambil_btn.click()
                print("[✅] Ambil Antrean clicked!")
                return True
            return False
        except Exception as e:
            print(f"[❌] Error clicking ambil antrean: {e}")
            return False
        
    # async def cek_butik_kuota(self):
    #     try:
    #         cek_btn_penuh = await self.browser.page.query_selector(
    #             '.btn-secondary:has-text("Penuh"), button:has-text("Penuh")'
    #         )
    #         if cek_btn_penuh:
    #             await ambil_btn.click()
    #             print("[✅] Ambil Antrean clicked!")
    #             return True
    #         return False
    #     except Exception as e:
    #         print(f"[❌] Error clicking ambil antrean: {e}")
    #         return False

    async def wait_for_target_time(self):
        """Tunggu waktu target dengan persiapan"""
        target_time = self.config.target_time
        print(f"[⏰] Target: {target_time} | Preparation@-{self.config.prep_time_offset}s")
        
        time_selected = False
        last_refresh = self.time_helper.current_timestamp
        
        while True:
            now = self.time_helper.current_time
            current_str = now.strftime("%H:%M:%S")
            
            target = self.time_helper.parse_target_time(target_time)
            time_diff = (target - now).total_seconds()
            
            # 🎯 TARGET REACHED
            if time_diff <= self.config.click_advance_seconds:
                print(f"[🎯] TARGET TIME! Submitting... ({current_str})")
                return True
            
            # ⏰ SELECT WAKTU dan 🛡️ MANUAL CAPTCHA di waktu persiapan
            elif 0 < time_diff <= self.config.prep_time_offset and not time_selected:
                print(f"[⏰] Preparation time: Selecting arrival time... ({current_str})")
                if await self.select_time_option():
                    time_selected = True
                    print("[✅] Time selected!")
                
                print(f"\n[🛡️] Preparation time: MANUAL CAPTCHA REQUIRED! ({current_str})")
                print("[👤] Please complete CAPTCHA manually in browser NOW!")
                print(f"[⏳] You have {int(time_diff)} seconds until target time...")
            
            # 🔄 AUTO REFRESH (sebelum waktu persiapan, setiap interval)
            elif time_diff > self.config.prep_time_offset and \
                 (self.time_helper.current_timestamp - last_refresh) >= self.config.refresh_interval:
                print(f"[🔄] Refreshing... ({current_str})")
                await self.browser.page.reload()
                await self.browser.wait_for_timeout(1000)
                last_refresh = self.time_helper.current_timestamp
            
            # 📊 Progress update
            if time_diff <= 120 and int(time_diff) % 30 == 0:
                status = "TIME✓" if time_selected else ""
                print(f"[⏳] {int(time_diff)}s left... {status}")
            
            await asyncio.sleep(0.1)  # More responsive loop

    async def process_antrean(self):
        """Jalankan proses antrean lengkap"""
        print("\n[🎯] Starting antrean process...")
        
        # Navigate ke antrean
        if not await self.navigate_to_antrean():
            return False
        
        # Pilih butik
        if not await self.select_butik():
            return False
        
        # Tunggu dan submit dengan timing presisi
        print("[⏰] Waiting for precise timing...")
        await self.wait_for_target_time()
        
        # Submit final
        success = await self.click_ambil_antrean()
        
        if success:
            print("[✅] Antrean submitted successfully!")
            await self.browser.wait_for_timeout(3000)
        else:
            print("[❌] Failed to submit antrean")
            
        return success