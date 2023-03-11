DATABASE = {
    "host":"35.244.104.50",
    "user":"gunchul",
    "password":"rjscjfTHD11",
    "database":"test_kellydata"
}

PROJECTS = {
    # "root":"/home/kelly_je_kim/html",
    "root":"C:\\src\\kellydata_php",
}

def env_plot_path_get(menu, month):
    return PROJECTS["root"] + f"/images/{menu}/{month}.png"

def env_table_path_get(menu, month):
    return PROJECTS["root"] + f"/tables/{menu}/{month}.html"
