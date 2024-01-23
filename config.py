DEFAULT_GLOBAL_SETTINGS = {
    'frequency': {'min': 2, 'max': 2000000, 'default': 1000},
    'amplitude': {'min': 18, 'max': 44, 'default': 18},
    'length': {'min': 2, 'max': 16384, 'default': 16}, 
    'frequency_source': {'default': 0}
}

FREQUENCY_LIST = [2, 10, 100, 500, 1000, 5000, 10000, 16000, 25000, 50000, 100000]

DEFAULT_SPECIFIC_PATTERN_SETTINGS = {
    'period': 1,
    'k': 50,
    'delay': 0,
}

DEFAULT_SPECIFIC_USER_SETTINGS = {
    'value': "0"*32
}

PLOT_COLORS = ['black', 'red', 'orange', 'brown', 'green', 'blue', 'indigo', 'violet']

db_path = r'D:\Python\digital_generator\settings.db'
app_icon_path = r''