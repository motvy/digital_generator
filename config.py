DEFAULT_GLOBAL_SETTINGS = {
    'frequency': {'min': 1, 'max': 100, 'default': 10},
    'amplitude': {'min': 18, 'max': 44, 'default': 18},
    'length': {'min': 2, 'max': 255, 'default': 16}, 
}

DEFAULT_SPECIFIC_PATTERN_SETTINGS = {
    'period': 1,
    'k': 50,
    'delay': 0, 
}

PLOT_COLORS = ['black', 'red', 'orange', 'brown', 'green', 'blue', 'indigo', 'violet']

db_path = r'D:\python\motvy\digital_generator\settings.db'