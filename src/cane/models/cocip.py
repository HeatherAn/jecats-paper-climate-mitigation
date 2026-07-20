import pandas as pd
from pycontrails.models.humidity_scaling import ExponentialBoostHumidityScaling

# to combat ERA5 ice-supersaturation under-representation
humidity_scaling = ExponentialBoostHumidityScaling(
    rhi_adj=0.9779,
    rhi_boost_exponent=1.635,
    clip_upper=1.65,
)
