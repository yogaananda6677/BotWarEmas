import time
import datetime

class TimeHelper:
    @property
    def current_time(self):
        return datetime.datetime.now()

    @property 
    def current_timestamp(self):
        return time.time()

    def parse_target_time(self, target_time_str):
        """Parse target time string ke datetime object"""
        now = self.current_time
        target = datetime.datetime.strptime(target_time_str, "%H:%M")
        return now.replace(
            hour=target.hour, 
            minute=target.minute, 
            second=0, 
            microsecond=500000  # +0.5 seconds
        )

    def format_time_diff(self, time_diff):
        """Format time difference untuk display"""
        return f"{int(time_diff)}s"