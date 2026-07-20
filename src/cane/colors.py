import seaborn as sns

# Seaborn colorblind
colors = sns.color_palette("colorblind")
sns_idx = {
    cname: i
    for i, cname in
    enumerate(["darkblue", "orange", "green", "red", "violet", "brown", "pink", "gray", "yellow", "lightblue"])
}

# https://www.nature.com/articles/nmeth.1618

# latest mapping (Dec 2025)
from cane.colors import colors, sns_idx

colormap_by_species = {
    "co2": colors[sns_idx["brown"]],
    "nox": colors[sns_idx["red"]],
    "h2o": colors[sns_idx["lightblue"]],
    "contrail": colors[sns_idx["darkblue"]],
    "total": colors[sns_idx["violet"]],
}
