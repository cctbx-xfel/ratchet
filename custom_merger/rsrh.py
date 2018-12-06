from __future__ import print_function, division
from dials.array_family import flex
from xfel.merging.application.worker import worker
from dials.array_family import flex
import math
ln2 = math.log(2)

class rsrh(worker):
  """
  Computes the polarazation correction as defined by Kahn 1982.

  Modifies the intensity.sum.value and intensity.sum.variance columns
  in place.
  """
  def run(self, experiments, reflections):
    result = flex.reflection_table()

    for expt_id, experiment in enumerate(experiments):
      refls = reflections.select(reflections['id'] == expt_id)

      A = flex.mat3_double(len(refls), experiment.crystal.get_A())
      s0 = flex.vec3_double(len(refls), experiment.beam.get_s0())
      q = A * refls['miller_index'].as_vec3_double()
      rh = (q + s0).norms() - 1/experiment.beam.get_wavelength()
      eta = 2*math.pi/180 * experiment.crystal.get_half_mosaicity_deg()
      rs = (1/experiment.crystal.get_domain_size_ang()) + (eta/2/refls['d'])

      p_G = flex.exp(-2*ln2*rh**2/rs**2)

      dp_G_drs = p_G * 4 * ln2 * rh**2 / rs**2

      refls['rh'] = rh
      refls['rs'] = rs
      refls['p_G'] = p_G
      refls['dp_G_drs'] = dp_G_drs

      result.extend(refls)

    return experiments, result

if __name__ == '__main__':
  from xfel.merging.application.worker import exercise_worker
  exercise_worker(polarization)
