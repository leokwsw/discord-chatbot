from src.logger.ConsoleHandler import ConsoleHandler
from src.logger.CustomFormatter import CustomFormatter
from src.logger.FileHandler import FileHandler
from src.logger.LoggerFactory import LoggerFactory

formatter = CustomFormatter()
file_handler = FileHandler('./logs')
console_handler = ConsoleHandler()
logger = LoggerFactory.create_logger(formatter, [file_handler, console_handler])