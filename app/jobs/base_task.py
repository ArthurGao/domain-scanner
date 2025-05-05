from abc import ABC, abstractmethod

class BaseTask(ABC):
    @abstractmethod
    def execute(self):
        pass