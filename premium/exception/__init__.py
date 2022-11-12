import os
import sys

class PremiumException(Exception):

    @staticmethod
    def get_detailed_error_message(error_message:Exception, error_details:sys)->str:
        _,_,exec_tb=error_details.exc_info()
        exception_line_number=exec_tb.tb_frame.f_lineno
        try_line_number=exec_tb.tb_lineno
        file_name=exec_tb.tb_frame.f_code.co_filename

        error_message=f"Error occured in script [{file_name}] \n at try block LINE NUMBER: [{try_line_number}] and exception block LINE NUMBER:[{exception_line_number}] \n ERROR MESSAGE: [{error_message}]"

        return error_message

    def __init__(self, error_message:Exception, error_details:sys):
        super().__init__(error_message)
        self.error_message=PremiumException.get_detailed_error_message(error_message=error_message, error_details=error_details)


    def __str__(self):
        return self.error_message

    def __repr__(self):
        return PremiumException.__name__.str()


