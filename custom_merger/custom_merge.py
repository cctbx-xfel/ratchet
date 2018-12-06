from __future__ import division
from xfel.merging.command_line.merge import Script as ScriptBase

class Script(ScriptBase):
  def run(self):
    from xfel.merging import application
    import importlib

    # Create the workers using the factories
    workers = []
    for step in ['input', 'modify']:
      factory = importlib.import_module('xfel.merging.application.'+step+'.factory')
      workers.extend(factory.factory.from_parameters(self.params))

    from rsrh import rsrh
    workers.append(rsrh(self.params))

    # Perform phil validation up front
    for worker in workers:
      worker.validate()

    # Do the work
    experiments = reflections = None
    while(workers):
      worker = workers.pop(0)
      experiments, reflections = worker.run(experiments, reflections)

    print ('Done')

if __name__ == '__main__':
  script = Script()
  result = script.run()
  print ("OK")
