"""Processors module"""
import abc
import logging
import sys
import traceback
from multiprocessing import Process


class ProcessorWorkManager(abc.ABC):
    """Work manager abstract class"""

    @abc.abstractmethod
    def run(self) -> None:
        """Run work manager"""
        pass

    @abc.abstractmethod
    def stop(self) -> None:
        """Stop work manager"""
        pass


class ProcessorWorker:
    """Process worker class"""

    def __init__(self, processor_work_manager: ProcessorWorkManager):
        self._running = True
        self.processor_work_manager = processor_work_manager

    def run(self):
        """Run worker"""
        while self._running:
            try:
                self.process()
            except Exception:
                logging.error(traceback.format_exception(*sys.exc_info()))
                continue

    def process(self):
        """Call process on queue"""
        self.processor_work_manager.run()

    def join(self):
        """Join processes"""
        self._running = False


class ProcessorManager:
    """Processor manager"""

    worker_class = ProcessorWorker

    def __init__(
        self, processor_work_manager: ProcessorWorkManager, num_of_processor: int
    ):
        self._num_of_processor = num_of_processor
        self._processes = []
        self._processor_workers = []

        for index in range(num_of_processor):
            processor_worker = ProcessorWorker(processor_work_manager)
            processor = Process(target=self._work, args=(index,))
            self._processor_workers.append(processor_worker)
            self._processes.append(processor)

    def _work(self, index):
        """Run work"""
        worker = self._processor_workers[index]
        worker.run()

    def start(self):
        """Start processes"""
        for process in self._processes:
            logging.info("Start process: %s", process)
            process.start()

    def stop(self):
        """Stop processes"""
        for processor_worker in self._processor_workers:
            processor_worker.join()

        for process in self._processes:
            process.join()
