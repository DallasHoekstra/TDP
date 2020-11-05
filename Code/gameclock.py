import time 

class GameClock():
    def __init__(self, fps):
        self.fps = fps
        self.current_time = time.perf_counter()

    def tick(self):
        self.await_next_cycle()

    def set_fps(self, fps):
        self.fps = fps
        
    def get_fps(self):
        return self.fps

    def get_cycle_length(self):
        return round(1/self.fps, 4)

    def get_current_time(self):
        return time.perf_counter()

    def in_seconds(self,time):
        return int(time)

    def await_next_cycle(self):
        # Function has excess lag (on windows) of up to .8 seconds at a 60 cycle/s framerate
        wake_at = self.get_current_time() + self.get_cycle_length()
        time.sleep(self.get_cycle_length())
        while(self.get_current_time() < wake_at):
            time.sleep(.0001)
