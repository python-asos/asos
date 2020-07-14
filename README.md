A scheduler of stuff (ASOS)
====================

This is a task manager, sort of. Supports plugins for storage and for executors.

Configuration
-------------

Takes quite few parameters:

```json
{
  "uuid": "current_instance_name",
  "storage_plugin": "mysql"
}
```

Storage plugins
---------------

Should implement two methods:
1. Get all active tasks
2. Add a result of task execution

```python
class Storage():
	
	def get_tasks(self):
		return {task_id: task, ...}
	
	def add(self, task_id, task, env, result, dump=None):
		return True
```

Executor plugins
----------------

Does the actual work. The name of plugin should match a `task_type` field.

```python
class Executor():
	
	def do(self, task, env):
		return result, dump
	
```

Tasks
-----

Task objects represent tasks that need to be done. Should contain all additional parameters, required by your plugins.

```json
{
  "task_type": executor_plugin_name,
  "task_interval": 60,
  "additional_param": "value"
}
```
