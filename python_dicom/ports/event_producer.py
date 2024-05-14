from abc import ABC, abstractmethod

class EventProducer(ABC):

    def __init__(self, log_service=None):

        self.__log_service = log_service

    @property
    def log_service(self):
        return self.__log_service

    @log_service.setter
    def log_service(self, log_service):
        self.__log_service = log_service

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def flush(self, event):
        """
        Flush (actually publish) the events.
        """
        pass
