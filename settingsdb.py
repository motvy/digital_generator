import config
import utils

import os
import sqlite3


class SettingsDb():
    def __init__(self):
        db_path = config.db_path

        if not db_path:
            raise Exception('Path files db is empty. See config')

        self.conn = None

        if os.path.exists(db_path):
            print('Connect files db %s', db_path)

            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()

        else:
            fpath = os.path.dirname(db_path)
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            print('Create cache db %s', db_path)

            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()

            self.cursor.execute('''CREATE TABLE GlobalSettings (
                                    frequency INTEGER
                                    , amplitude INTEGER
                                    , length INTEGER
                                )''')

            self.cursor.execute('''CREATE TABLE SpecificPatternSettings (
                                    channel INTEGER
                                    , period INTEGER
                                    , k INTEGER
                                    , delay INTEGER
                                )''')
            
            g_settings = config.DEFAULT_GLOBAL_SETTINGS
            self.cursor.execute("INSERT INTO GlobalSettings values(?,?,?)", (g_settings['frequency']['default'], g_settings['amplitude']['default'], g_settings['length']['default']))

            sp_settings = config.DEFAULT_SPECIFIC_PATTERN_SETTINGS
            for i in range(8):
                self.cursor.execute("INSERT INTO SpecificPatternSettings values(?,?,?,?)", (i, sp_settings['period'], sp_settings['k'], sp_settings['delay']))

            self.conn.commit()

    def __del__(self):	
        if self.cursor != None:		
            self.cursor.close()		
        if self.conn != None:
            self.conn.close()

    def get_global_settings(self):
        self.cursor.execute("SELECT * FROM GlobalSettings")
        res = self.cursor.fetchone()
        if res:
            res = utils.GlobalSettings._make(res)

        return res

    def set_global_frequency(self, frequency):
        self.cursor.execute("UPDATE GlobalSettings SET frequency=?", (frequency,))
        self.conn.commit()

    def set_global_amplitude(self, amplitude):
        self.cursor.execute("UPDATE GlobalSettings SET amplitude=?", (amplitude,))
        self.conn.commit()

    def set_global_length(self, length):
        self.cursor.execute("UPDATE GlobalSettings SET length=?", (length,))
        self.conn.commit()

    def get_specific_pattern_settings(self, channel):
        self.cursor.execute("SELECT period, k, delay FROM SpecificPatternSettings WHERE channel=?", (channel,))
        res = self.cursor.fetchone()
        if res:
            res = utils.SpecificPatternSettings._make(res)

        return res

    def set_specific_pattern_period(self, channel, period):
        self.cursor.execute("UPDATE SpecificPatternSettings SET period=? WHERE channel=?", (period, channel))
        self.conn.commit()

    def set_specific_pattern_k(self, channel, k):
        self.cursor.execute("UPDATE SpecificPatternSettings SET k=? WHERE channel=?", (k, channel))
        self.conn.commit()

    def set_specific_pattern_delay(self, channel, delay):
        self.cursor.execute("UPDATE SpecificPatternSettings SET delay=? WHERE channel=?", (delay, channel))
        self.conn.commit()