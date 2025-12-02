class Config:
    def __init__(self):
        self.username = "089666310210"
        self.password = "anam1245"
        self.butik_value = "19"
        self.target_time = "07:00"
        self.click_advance_seconds = 3
        
        # URLs
        self.login_url = "https://antrean.logammulia.com/login"
        self.dashboard_url = "https://antrean.logammulia.com/users"
        self.antrean_url = "https://antrean.logammulia.com/antrean"
        
        # Browser settings
        self.user_data_dir = "/home/yoga/.config/BraveSoftware/Brave-Browser"
        self.headless = False
        self.viewport = {"width": 1200, "height": 800}
        
        # Timing settings
        self.refresh_interval = 30
        self.prep_time_offset = 70  # -70 seconds for preparation
        
    @property
    def credentials(self):
        return {"username": self.username, "password": self.password}