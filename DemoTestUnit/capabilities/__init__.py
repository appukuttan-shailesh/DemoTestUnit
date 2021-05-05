import sciunit

# ===============================================================================

class SomaProducesMembranePotential(sciunit.Capability):
    """Enables recording membrane potential from soma """

    def get_soma_membrane_potential(self, tstop):
        """
        Run simulation for time 'tstop', specified in ms, while 
        recording the somatic membrane potential.
        Must return a dict of the form:
        	{'T': list1, 'V': list2 } where,
        		list1 = time series (in ms)
        		list2 = membrane potential series (in mV)
        """
        raise NotImplementedError()
        
    # this will be used by our second test (test for input resistance)    
    def get_soma_membrane_potential_eFEL_format(self, tstop, start, stop):
        traces = self.get_soma_membrane_potential(tstop)
        efel_trace = {'T' : traces['T'],
                      'V' : traces['V'],
                      'stim_start' : [start],
                      'stim_end'   : [stop]}
        return efel_trace

# ===============================================================================

class SomaReceivesStepCurrent(sciunit.Capability):
    """ Enables step current stimulus into soma """

    def inject_soma_square_current(self, current):
        """
        Input current is specified in the form of a dict with keys:
            'delay'     : (value in ms),
            'duration'  : (value in ms),
            'amplitude' : (value in nA)
        """
        raise NotImplementedError()

# ===============================================================================