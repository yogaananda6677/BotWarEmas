class LoginPage:
    def __init__(self, browser_manager):
        self.browser = browser_manager
        self.config = browser_manager.config

    async def is_login_page(self):
        """Cek apakah di halaman login"""
        return "login" in self.browser.page.url

    async def is_logged_in(self):
        """Cek status login berdasarkan URL"""
        current_url = self.browser.page.url
        if "users" in current_url:
            print("[✅] Already logged in - Dashboard detected")
            return True
        elif "login" in current_url:
            print("[❌] Not logged in - Login page detected")
            return False
        else:
            print(f"[⚠️] Unknown state - URL: {current_url}")
            return False

    async def fill_credentials(self):
        """Isi username dan password"""
        try:
            await self.browser.page.wait_for_selector('input[name="username"]', timeout=5000)
            await self.browser.page.fill('input[name="username"]', self.config.username)
            await self.browser.wait_for_timeout(200)
            await self.browser.page.fill('input[name="password"]', self.config.password)
            print("[✅] Credentials filled!")
            return True
        except Exception as e:
            print(f"[❌] Error filling credentials: {e}")
            return False

    async def click_remember_me(self):
        """Klik remember me checkbox"""
        try:
            remember = await self.browser.page.query_selector('label.form-check-label:has-text("Remember me")')
            if remember:
                await remember.click()
                print("[✅] Remember Me checked!")
            return True
        except:
            return False
        
    async def check_captcha(self):
        """Coba CAPTCHA otomatis dulu, kalau gagal langsung manual."""
        page = self.browser.page

        try:
            # 1. Cari iframe reCAPTCHA
            recaptcha_frame_el = await page.query_selector('iframe[src*="google.com/recaptcha"]')
            if recaptcha_frame_el:
                frame = await recaptcha_frame_el.content_frame()
                if frame:
                    checkbox = await frame.query_selector('.recaptcha-checkbox-border, .recaptcha-checkbox-checkmark')
                    
                    if checkbox:
                        await checkbox.click()
                        print("[✓] reCAPTCHA checkbox clicked!")
                        await page.wait_for_timeout(3000)

                        # Cek solved atau tidak
                        is_solved = await frame.evaluate("""() => {
                            const response = document.querySelector('#g-recaptcha-response');
                            return response && response.value && response.value.length > 0;
                        }""")

                        if is_solved:
                            print("[🎉] reCAPTCHA solved automatically!")
                            return True

                    print("[⚠️] reCAPTCHA not solved → switching to manual...")
                else:
                    print("[⚠️] Cannot access reCAPTCHA frame → manual needed")
            else:
                print("[ℹ️] No reCAPTCHA detected on the page.")
                return True  # Tidak ada CAPTCHA → lanjut saja

        except Exception as e:
            print(f"[❌] Automatic CAPTCHA failed: {e}")

        # --- 2. FALLBACK MANUAL ---
        print("[🛡️] Manual CAPTCHA required!")
        await self.wait_for_manual_captcha()
        return True

    

    async def wait_for_manual_captcha(self):
        """Tunggu user selesaikan CAPTCHA manual"""
        print("\n" + "🛡️" * 60)
        print("🛡️           MANUAL CAPTCHA REQUIRED")
        print("🛡️" * 60)
        print("Please complete in browser:")
        print("1. ✅ Complete the CAPTCHA challenge")
        print("2. 🖼️ Solve image challenge if appears") 
        print("3. 🎯 Press ENTER here when done")
        print("🛡️" * 60)
        
        input()
        print("[✅] Continuing after manual CAPTCHA...")
        return True

    async def submit_login(self):
        """Submit form login"""
        try:
            submit_btn = await self.browser.page.query_selector('button[type="submit"], .btn-primary, .btn-login')
            if submit_btn:
                await submit_btn.click()
                print("[✅] Login submitted!")
                await self.browser.wait_for_timeout(1000)
                return True
            return False
        except Exception as e:
            print(f"[❌] Error submitting login: {e}")
            return False

    async def login(self):
        """Proses login lengkap"""
        print("[🔐] Starting login process...")
        
        # Navigate ke login page
        await self.browser.goto(self.config.login_url)

        # Cek apakah sudah login
        if await self.is_logged_in():
            return True
            
        if not await self.is_login_page():
            print("[⚠️] Not on login page, checking status...")
            return await self.is_logged_in()
        
        # Isi form login
        if not await self.fill_credentials():
            return False
            
        # Remember me
        await self.click_remember_me()
        
        # Manual CAPTCHA
        await self.check_captcha()
        
        # Submit login
        if not await self.submit_login():
            return False
            
        # Verifikasi login berhasil
        await self.browser.wait_for_timeout(2000)
        return await self.is_logged_in()