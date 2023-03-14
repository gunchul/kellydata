import platform

DATABASE = {
    "host":"35.244.104.50",
    "user":"gunchul",
    "password":"rjscjfTHD11",
    "database":"test_kellydata"
}

PROJECTS = {
    "gunchul-XPS-13-9343_root":"/home/gunchul/src/kellydata_php",
    "gunchul-XPS-13-9343_web_driver":"/home/gunchul/bin/chromedriver/chromedriver_linux64_111",
    "GUNCHUL-PC_root":"C:\\src\\kellydata_php",
    "GUNCHUL-PC_web_driver":"C:\\bin\\chromedriver_win32_111\\chromedriver.exe",
}

def env_plot_path_get(menu, month):
    return PROJECTS[f"{platform.node()}_root"] + f"/images/{menu}/{month}.png"

def env_table_path_get(menu, month):
    return PROJECTS[f"{platform.node()}_root"] + f"/tables/{menu}/{month}.html"

def web_driver_path_get():
    return PROJECTS[f"{platform.node()}_web_driver"]

if __name__ == "__main__":
    print(platform.node())
    print(env_plot_path_get("auction", 12))
    print(env_table_path_get("auction", 12))
    print(web_driver_path_get())

