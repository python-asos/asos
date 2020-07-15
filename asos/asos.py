#!/usr/bin/env python3
#
# Runs a task loop for a pre-defined amount of time.
# Returns stats to somewhere.
#
# v1.0 2020-07-14 Initial release (Pavel Kim)
# v1.1 2020-07-15 Threaded verion (Pavel Kim)

import importlib

import requests
import time
import datetime
import threading
import logging
import json
import os
from pprint import pprint


class WorkerThread(threading.Thread):

    def __init__(self, task_id, task, task_handler, storage_handler, env):
        super(WorkerThread, self).__init__()
        self._thread_id = None
        self.alive = True
        self.task_id = task_id
        self.task_type = task['task_type']
        self.task_interval = task['task_interval']
        self.task = task
        self.task_handler = task_handler
        self.storage_handler = storage_handler
        self.env = env

        logging.info("Created a worker thread for task '%s'" % self.task_id)

    def run(self):
        while self.alive:
            if self.task_interval == 0:
                self.alive = False
                logging.info("This is a one-time job %s" % self.task_id)

            logging.debug("Working %s on task %s" % (self.get_id(), self.task_id))
            
            result, dump = self.task_handler.do(self.task, self.env)
            logging.info("Executed task %s with result %s" % (self.task_id, result))
            logging.debug("Sleeping for %s seconds, until the next run of task %s" % (self.task_interval, self.task_id))

            logging.debug("Adding result of %s to the storage" % (self.task_id))
            self.storage_handler.add(self.task_id, self.task, self.env, result, dump)

            time.sleep(self.task_interval)

    def stop(self):
        self.alive = False
        logging.debug("Thread %s will stop soon." % self.get_id())

    def get_id(self):
        if self._thread_id is not None:
            return self._thread_id

        for thread_id, thread in threading._active.items():
            if thread is self:
                self._thread_id = thread_id

        return self._thread_id

class SupervisorTread(threading.Thread):

    def __init__(self, storage_handler, uuid):
        super(SupervisorTread, self).__init__()
        self._thread_id = None
        self.alive = True
        self.storage_handler = storage_handler
        self.workers = {}
        self.killed_workers = {}
        self.task_handlers = {}
        self.uuid = uuid

        self.env = {
            "uuid": self.uuid,
        }

    def run(self):
        while self.alive:

            tasks = self.storage_handler.get_tasks()

            for task_id in tasks.keys():
                logging.debug("Acquiring task %s" % task_id)
                
                if task_id in self.workers:                        

                    if self.workers[task_id]['task'] == tasks[task_id]:
                        logging.debug("Task %s is already executing, skipping." % task_id)

                        if not self.workers[task_id]['thread'].is_alive():
                            logging.error("Thread %s for task %s is dead!" % (self.workers[task_id]['thread'], task_id))
                        else:
                            continue
                    else:
                        logging.warning("Task %s updated on storage, recreating thread" % task_id)
                    
                    self.workers[task_id]['thread'].stop()
                    self.killed_workers[task_id] = self.workers[task_id]['thread']
                    self.workers.pop(task_id)

                task_type = tasks[task_id]['task_type']

                if task_type not in self.task_handlers:
                    logging.debug("Importing handler '%s' for task %s" % (task_id, task_type))
                    task_handler_plugin = importlib.import_module("asos_%s.plugin" % task_type)
                    task_handler_object = task_handler_plugin.Executor()
                    self.task_handlers[task_type] = task_handler_object
                else:
                    logging.debug("Task handler '%s' already imported, reusing." % (task_type))
                    task_handler_object = self.task_handlers[task_type]

                logging.debug("Creating a worker thread for task %s" % task_id)

                self.workers[task_id] = {
                    'thread': WorkerThread(task_id=task_id, task=tasks[task_id], task_handler=task_handler_object, storage_handler=self.storage_handler, env=self.env),
                    'task': tasks[task_id],
                }

                self.workers[task_id]['thread'].start()
            
            time.sleep(5)
    
    def get_id(self):

        if self._thread_id is not None:
            return self._thread_id

        for thread_id, thread in threading._active.items():
            if thread is self:
                self._thread_id = thread_id

        return self._thread_id

def main(storage_plugin, instance_uuid):
    logging.basicConfig(level=logging.INFO)

    storage_plugin = importlib.import_module("asos_%s.plugin" % storage_plugin)
    storage_object = storage_plugin.Storage()

    logging.info("Starting supervisor thread..")
    supervisor = SupervisorTread(storage_object, instance_uuid)
    supervisor.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main("datacollector", "local9")
