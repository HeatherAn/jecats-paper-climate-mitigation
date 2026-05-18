import seaborn as sns

# https://colorbrewer2.org/#type=sequential&scheme=YlGnBu&n=5
# colorblind safe
# print friendly
YlGnBu = [
    "#ffffcc",  # yellow
    "#a1dab4",  # green
    "#41b6c4",  # blue-green
    "#2c7fb8",  # blue
    "#253494"  # dark blue
]

# Tableau colors
colormap_tab = {
    "ref (BADA3 Thales)": "tab:purple",
    "BADA3": "tab:blue",
    "BADA4": "tab:orange",
    "OpenAP": "tab:red",
    "Poll-Schumann": "tab:green",
}

# Seaborn colorblind
colors = sns.color_palette("colorblind")
sns_idx = {
    cname: i
    for i, cname in
    enumerate(["darkblue", "orange", "green", "red", "violet", "brown", "pink", "gray", "yellow", "lightblue"])
}

colormap_sns = {
    "ref (BADA3 Thales)": colors[6],  #
    "BADA3": colors[0],  #
    "BADA4": colors[1],  # orange
    "OpenAP": colors[3],  # red
    "Poll-Schumann": colors[2],  # green
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
