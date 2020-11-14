import time 

class GameClock():
    paused_time = 0
    time_offset = 0
    paused = False

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

    def get_internal_time(self):
        return time.perf_counter()

    def get_external_time(self):
        if self.is_paused():
            return self.in_seconds(self.paused_time - self.time_offset)
        return self.in_seconds(time.perf_counter() - self.time_offset)

    def in_seconds(self,time):
        return int(time)

    def is_paused(self):
        return self.paused

    def pause(self):
        if self.is_paused() == False:
            self.paused = True
            self.paused_time = self.get_internal_time()

    def resume(self):
        if self.is_paused():
            self.time_offset += self.get_internal_time() - self.paused_time 
            self.paused = False
        

    def await_next_cycle(self):
        # Function has excess lag (on windows) of up to .8 seconds at a 60 cycle/s framerate
        wake_at = self.get_internal_time() + self.get_cycle_length()
        time.sleep(self.get_cycle_length())
        while(self.get_internal_time() < wake_at):
            time.sleep(.0001)
