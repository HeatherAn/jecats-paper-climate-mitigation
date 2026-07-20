from pycontrails import Flight, MetDataset
from pycontrails.physics.jet import fuel_burn
from pycontrails.ext.bada import BADAFlight

bada_3_path = "/path/to/bada3" # TODO
bada_3_path = "/Users/jsmretschnig/bada/BADA 3.16"


def compute_aircraft_performance(flight: Flight, pl: MetDataset) -> Flight:
    bada_model = BADAFlight(met=pl, params={
        "fill_low_altitude_with_isa_temperature": True,
        "fill_low_altitude_with_zero_wind": True,
        "bada3_path": bada_3_path,
        "bada4_path": None,
        "bada_priority": 3,
    })
    flight = bada_model.eval(flight)

    flight.update({"fuel_burn": fuel_burn(flight["fuel_flow"], flight.segment_duration())})
    return flight
