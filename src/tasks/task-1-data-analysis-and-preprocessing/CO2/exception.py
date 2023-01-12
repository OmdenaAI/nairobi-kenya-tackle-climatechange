import sys, os


def error_message_detail(error, error_detail: sys):
    a, _, exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f'''Error occured in python script name [{file_name}] 
                        \nException class:  [{a}]
                        \nError Line: [{exc_tb.tb_lineno}]
                        \nError message: [{str(error)}]'''
    return error_message


class CO2_Exception(Exception):

    def __init__(self, error_message, error_detail: sys):
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        return self.error_message
