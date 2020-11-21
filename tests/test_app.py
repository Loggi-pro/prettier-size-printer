import os
import pytest
from src import run, Arguments

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

AVR_ELF_FILE_PATH: str = os.path.join(dname, 'data/avr.elf')
STM32_ELF_FILE_PATH: str = os.path.join(dname, 'data/stm32.elf')
AVR_MCU: str = 'atmega168p'
STM32_MCU: str = 'stm32f303vc'


def check_env(var):
    if (not var in os.environ):
        assert False, f'setup env variable {var}, that content path to avr-size/arm-size tool'


def test_nosizetool_should_throw():
    check_env('PATH_TO_EZSTACK')
    PATH_TO_EZSTACK = os.environ['PATH_TO_EZSTACK']
    arg = Arguments(size='', elf=AVR_ELF_FILE_PATH,
                    ezstack=PATH_TO_EZSTACK, mcu=AVR_MCU, maxflash=0, maxram=0)
    with pytest.raises(FileNotFoundError):
        run(arg)


def test_noelffile_should_throw():
    check_env('PATH_TO_AVR_SIZE_TOOL')
    check_env('PATH_TO_EZSTACK')
    PATH_TO_AVR_SIZE_TOOL = os.environ['PATH_TO_AVR_SIZE_TOOL']
    PATH_TO_EZSTACK = os.environ['PATH_TO_EZSTACK']
    arg = Arguments(size=PATH_TO_AVR_SIZE_TOOL, elf='',
                    ezstack=PATH_TO_EZSTACK, mcu=AVR_MCU, maxflash=0, maxram=0)
    with pytest.raises(FileNotFoundError) as e:
        run(arg)


def test_no_mcu_should_throw():
    check_env('PATH_TO_AVR_SIZE_TOOL')
    check_env('PATH_TO_EZSTACK')
    PATH_TO_AVR_SIZE_TOOL = os.environ['PATH_TO_AVR_SIZE_TOOL']
    PATH_TO_EZSTACK = os.environ['PATH_TO_EZSTACK']
    arg = Arguments(size=PATH_TO_AVR_SIZE_TOOL, elf=AVR_ELF_FILE_PATH,
                    ezstack=PATH_TO_EZSTACK, mcu="", maxflash=0, maxram=0)
    with pytest.raises(TypeError):
        run(arg)


def test_wrong_mcu_should_throw():
    check_env('PATH_TO_AVR_SIZE_TOOL')
    check_env('PATH_TO_EZSTACK')
    PATH_TO_AVR_SIZE_TOOL = os.environ['PATH_TO_AVR_SIZE_TOOL']
    PATH_TO_EZSTACK = os.environ['PATH_TO_EZSTACK']
    arg = Arguments(size=PATH_TO_AVR_SIZE_TOOL, elf=AVR_ELF_FILE_PATH,
                    ezstack=PATH_TO_EZSTACK, mcu='123', maxflash=0, maxram=0)
    with pytest.raises(Exception):
        run(arg)


def test_avr_no_ezstack_should_calc():
    check_env('PATH_TO_AVR_SIZE_TOOL')
    PATH_TO_AVR_SIZE_TOOL = os.environ['PATH_TO_AVR_SIZE_TOOL']
    arg = Arguments(size=PATH_TO_AVR_SIZE_TOOL, elf=AVR_ELF_FILE_PATH,
                    ezstack='', mcu=AVR_MCU, maxflash=0, maxram=0)
    size_result = run(arg)
    assert size_result.ezstack_used == False
    assert size_result.program_size == 224.0
    assert size_result.program_percent == 4.0
    assert size_result.data_size == 0
    assert size_result.data_percent == 0


def test_avr_ezstack_should_calc():
    check_env('PATH_TO_AVR_SIZE_TOOL')
    check_env('PATH_TO_EZSTACK')
    PATH_TO_AVR_SIZE_TOOL = os.environ['PATH_TO_AVR_SIZE_TOOL']
    PATH_TO_EZSTACK = os.environ['PATH_TO_EZSTACK']
    arg = Arguments(size=PATH_TO_AVR_SIZE_TOOL, elf=AVR_ELF_FILE_PATH,
                    ezstack=PATH_TO_EZSTACK, mcu=AVR_MCU, maxflash=0, maxram=0)
    size_result = run(arg)
    assert size_result.ezstack_used == True
    assert size_result.program_size == 224.0
    assert size_result.program_percent == 4.0
    assert size_result.data_size == 214.0
    assert size_result.data_percent == 20.9


def test_stm32_ezstack_should_calc_without_ezstack():
    check_env('PATH_TO_STM32_SIZE_TOOL')
    check_env('PATH_TO_EZSTACK')
    PATH_TO_STM32_SIZE_TOOL = os.environ['PATH_TO_STM32_SIZE_TOOL']
    PATH_TO_EZSTACK = os.environ['PATH_TO_EZSTACK']
    arg = Arguments(size=PATH_TO_STM32_SIZE_TOOL, elf=STM32_ELF_FILE_PATH,
                    ezstack=PATH_TO_EZSTACK, mcu=STM32_MCU, maxflash=2000, maxram=100)
    size_result = run(arg)
    assert size_result.ezstack_used == False
    assert size_result.program_size == 1143.0
    assert size_result.program_percent == 1143.0/2000.0*100.0
    assert size_result.data_size == 0
    assert size_result.data_percent == 0
