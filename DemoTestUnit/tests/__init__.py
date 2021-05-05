import sciunit
import efel
import numpy

import os
import json
import matplotlib
# To avoid figures being plotted on screen (we wish to save to file directly)
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import DemoTestUnit.capabilities as cap

# ===============================================================================

class RestingPotential(sciunit.Test):
    """Test the cell's resting membrane potential"""
    score_type = sciunit.scores.ZScore
    description = ("Test the cell's resting membrane potential")

    def __init__(self,
                 observation={'mean':None, 'std':None},
                 name="Resting Membrane Potential Test"):
        self.required_capabilities += (cap.SomaProducesMembranePotential,)
        sciunit.Test.__init__(self, observation, name)

    def validate_observation(self, observation):
        try:
            assert len(observation.keys()) == 2
            for key, val in observation.items():
                assert key in ["mean", "std"]
                assert (isinstance(val, int) or isinstance(val, float))
        except Exception:
            raise sciunit.errors.ObservationError(
                ("Observation must return a dictionary of the form:"
                 "{'mean': NUM1, 'std': NUM2}"))

    def generate_prediction(self, model):
        self.trace = model.get_soma_membrane_potential(tstop=50.0)
        prediction = numpy.mean(self.trace['V'])
        return prediction

    def compute_score(self, observation, prediction):
        score = sciunit.scores.ZScore.compute(observation, prediction)
        return score
    
    def bind_score(self, score, model, observation, prediction):
        self.figures = []
        self.target_dir = os.path.join("./validation_results", self.name, model.name)
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        # create relevant output files
        # 1. JSON data: observation, prediction, score, run_times
        validation_data = {
            "observation": observation,
            "prediction": prediction,
            "score": score.score,
        }
        with open(os.path.join(self.target_dir, 'basic_data.json'), 'w') as f:
            json.dump(validation_data, f, indent=4)
        self.figures.append(os.path.join(self.target_dir, 'basic_data.json'))
        
        # 2. JSON data: save Vm vs t traces
        with open(os.path.join(self.target_dir, 'trace_data.json'), 'w') as f:
            json.dump(self.trace, f, indent=4)
        self.figures.append(os.path.join(self.target_dir, 'trace_data.json'))
        
        # 3. Vm traces as PDF
        fig = plt.figure()
        plt.plot(self.trace["T"], self.trace["V"])
        plt.title("Somatic Vm vs t")
        plt.xlabel("Time (ms)")
        plt.ylabel("Membrane potential (mV)")
        plt.show()
        fig.savefig(os.path.join(self.target_dir, "trace_plot.pdf"))
        self.figures.append(os.path.join(self.target_dir, "trace_plot.pdf"))
        
        score.related_data["figures"] = self.figures
        return score

# ===============================================================================

class InputResistance(sciunit.Test):
    """Test the cell's input resistance"""
    score_type = sciunit.scores.ZScore
    description = ("Test the cell's input resistance")

    def __init__(self,
                 observation={'mean':None, 'std':None},
                 name="Input Resistance Test"):
        self.required_capabilities += (cap.SomaReceivesStepCurrent, cap.SomaProducesMembranePotential,)
        sciunit.Test.__init__(self, observation, name)

    def validate_observation(self, observation):
        try:
            assert len(observation.keys()) == 2
            for key, val in observation.items():
                assert key in ["mean", "std"]
                assert (isinstance(val, int) or isinstance(val, float))
        except Exception:
            raise sciunit.errors.ObservationError(
                ("Observation must return a dictionary of the form:"
                 "{'mean': NUM1, 'std': NUM2}"))

    def generate_prediction(self, model):
        efel.reset()
        model.inject_soma_square_current(current={'delay':20.0,
                                                  'duration':50.0,
                                                  'amplitude':-5.0})
        self.trace = model.get_soma_membrane_potential_eFEL_format(tstop=100.0,
                                                              start=20.0,
                                                              stop =70.0)
        efel.setDoubleSetting('stimulus_current', -5.0)
        prediction = efel.getFeatureValues([self.trace], ['ohmic_input_resistance_vb_ssse'])[0]["ohmic_input_resistance_vb_ssse"][0]
        return prediction

    def compute_score(self, observation, prediction):
        score = sciunit.scores.ZScore.compute(observation, prediction)
        return score

    def bind_score(self, score, model, observation, prediction):
        self.figures = []
        self.target_dir = os.path.join("./validation_results", self.name, model.name)
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        # create relevant output files
        # 1. JSON data: observation, prediction, score, run_times
        validation_data = {
            "observation": observation,
            "prediction": prediction,
            "score": score.score,
        }
        with open(os.path.join(self.target_dir, 'basic_data.json'), 'w') as f:
            json.dump(validation_data, f, indent=4)
        self.figures.append(os.path.join(self.target_dir, 'basic_data.json'))
        
        # 2. JSON data: save Vm vs t traces
        with open(os.path.join(self.target_dir, 'trace_data.json'), 'w') as f:
            json.dump(self.trace, f, indent=4)
        self.figures.append(os.path.join(self.target_dir, 'trace_data.json'))
        
        # 3. Vm traces as PDF
        fig = plt.figure()
        plt.plot(self.trace["T"], self.trace["V"])
        plt.title("Somatic Vm vs t")
        plt.xlabel("Time (ms)")
        plt.ylabel("Membrane potential (mV)")
        plt.show()
        fig.savefig(os.path.join(self.target_dir, "trace_plot.pdf"))
        self.figures.append(os.path.join(self.target_dir, "trace_plot.pdf"))
        
        score.related_data["figures"] = self.figures
        return score

# ===============================================================================
