"""The simulation experiments of the HCTZ model and their groups.

They are the registry of `MODEL`, the experiments its commands simulate.
"""

from sbmlsim.experiment import SimulationExperiment

from pkdb_models.models.hctz import MODEL
from pkdb_models.models.hctz.experiments.misc import (
    BloodPressureExperiment,
    DoseDependencyExperiment,
)
from pkdb_models.models.hctz.experiments.scans.scan_parameters import HCTZParameterScan
from pkdb_models.models.hctz.experiments.studies import (
    Anderson1961,
    Azumaya1990,
    Barbhaiya1982,
    Barbhaiya1982a,
    Beermann1976,
    Beermann1977a,
    Beermann1979,
    Devineni2014,
    # Dussol2005,
    # Ernst2006,
    Giudicelli1987,
    Heise2015,
    Howes1991,
    Hsiao2015,
    Hunninghake1986,
    # Januszewicz1959,
    Jeon2012,
    Jordo1979,
    Knauf1995,
    Koytchev2004,
    Niemeyer1983,
    Nilsen1989,
    Niopas2004,
    Patel1984,
    Ripley2000,
    Vaidyanathan2006,
    Weir1998,
    Williams1982,
)

EXPERIMENTS: dict[str, list[type[SimulationExperiment]]] = {
    "studies": [
        Anderson1961,
        Azumaya1990,
        Barbhaiya1982,
        Barbhaiya1982a,
        Beermann1976,
        Beermann1977a,
        Beermann1979,
        Devineni2014,
        # Dussol2005,
        # Ernst2006,
        Giudicelli1987,
        Heise2015,
        Howes1991,
        Hsiao2015,
        Hunninghake1986,
        # Januszewicz1959,
        Jeon2012,
        Jordo1979,
        Knauf1995,
        Koytchev2004,
        Niemeyer1983,
        Nilsen1989,
        Niopas2004,
        Patel1984,
        Ripley2000,
        Vaidyanathan2006,
        Weir1998,
        Williams1982,
    ],
    "iv": [
        Anderson1961,
        Beermann1976,
        # Januszewicz1959,
    ],
    "renal_impairment": [
        Anderson1961,
        Niemeyer1983,
        Beermann1979,
        # Dussol2005,
    ],
    "cardiac_impairment": [
        Anderson1961,
        Niemeyer1983,
        Beermann1979,
    ],
    "hepatic_impairment": [
        Anderson1961,
    ],
    "pharmacodynamics": [
        Beermann1977a,
        # Dussol2005,
        # Ernst2006,
        # Januszewicz1959,
        Jeon2012,
        Knauf1995,
        Nilsen1989,
        Patel1984,
        Ripley2000,
        Williams1982,
    ],
    "misc": [
        BloodPressureExperiment,
        DoseDependencyExperiment,
    ],
    "scans": [
        HCTZParameterScan,
    ],
}
EXPERIMENTS["all"] = EXPERIMENTS["studies"] + EXPERIMENTS["misc"] + EXPERIMENTS["scans"]


if __name__ == "__main__":
    MODEL.run_simulation_experiments(EXPERIMENTS["all"], MODEL.simulation_dir / "all")
