from .Simulator import Simulator
import time


from research.SimulationMode import SimulationMode

class EpisodeSimulator(Simulator):

    def __init__(self,
                    client, 
                    terminalSignalers=None, 
                    onTickers=None, 
                    onEnders=None, 
                    useThreads=False, 
                    sleep=0.05, 
                    simulationMode=SimulationMode.SYNCHRONOUS
                ):

        super().__init__(
            client=client,
            onTickers=onTickers,
            onEnders=onEnders,
            useThreads=useThreads,
            sleep=sleep,
            simulationMode=simulationMode
        )

        self.terminalSignalers = [] 
        if terminalSignalers is not None:
            self.terminalSignalers = terminalSignalers # this methods needs to be called to check for terminal states

    
    def _isDone(self):
        for terminalSignaler in self.terminalSignalers:
            if terminalSignaler():
                return True
        return False
    

    
    def loop(self, maxTicks):

        try:
            for i in range(maxTicks):
                self.tick(i)
                if self._isDone():
                    raise Exception("Episode finished")
                time.sleep(self.sleep)
                
        except Exception as e:
            # traceback.print_exc()
            self.logger.exception(e)
        finally:
            self.onEnd()

    def tick(self, i):

        if self.simulationMode == SimulationMode.SYNCHRONOUS:
            world_snapshot = self.world.tick() # synchronous mode
            print(f'world_snapshot: {world_snapshot}, i: {i}')
        if self.simulationMode == SimulationMode.ASYNCHRONOUS:
            world_snapshot = self.world.wait_for_tick() # asynchronous mode 
        
        if i % 100 == 0:
            print(f"world ticks {i}")
        for onTicker in self.onTickers:
            onTicker(world_snapshot)
