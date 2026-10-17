"""HCTZ templates."""

from pkpdsim.templates import terms_of_use
from sbmlutils.factory import (
    Creator,
    ModelUnits,
    UnitDefinition,
    Units,
)

__all__ = ["U", "creators", "model_units", "terms_of_use"]


class U(Units):
    """UnitDefinitions."""

    mmole = UnitDefinition("mmole")
    min = UnitDefinition("min")
    mg = UnitDefinition("mg")
    per_min = UnitDefinition("per_min", "1/min")
    per_min_l = UnitDefinition("per_min_l", "1/min/liter")
    m2 = UnitDefinition("m2", "meter^2")
    mM = UnitDefinition("mM", "mmole/liter")
    mmole_per_min = UnitDefinition("mmole_per_min", "mmole/min")
    mmole_per_min_l = UnitDefinition("mmole_per_min_l", "mmole/min/liter")
    g_per_mole = UnitDefinition("g_per_mole", "g/mole")
    l_per_min = UnitDefinition("l_per_min", "l/min")
    l_per_min_mmole = UnitDefinition("l_per_min_mmole", "l/min/mmole")


model_units = ModelUnits(
    time=U.min,
    extent=U.mmole,
    substance=U.mmole,
    length=U.meter,
    area=U.m2,
    volume=U.liter,
)

creators = [
    Creator(
        familyName="Schwaiger",
        givenName="Amanda",
        email="amanda.lim@charite.de",
        organization="Charité - Universitätsmedizin Berlin, Charitéplatz 1, 10117 Berlin, Germany",
    ),
    Creator(
        familyName="König",
        givenName="Matthias",
        email="koenigmx@hu-berlin.de",
        organization="Humboldt-University Berlin, Faculty of Life Science, Institute for Biology, Biology, Berlin; University Lübeck; University Hospital Schleswig-Holstein, Campus Lübeck, First Department of Medicine, Germany",
        site="https://livermetabolism.com",
    ),
]
