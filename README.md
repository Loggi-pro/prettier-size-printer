# Prettier firmware size printer

Print size of used FLASH and RAM storage of avr and stm firmware by elf file.
Allow to print used percents, and RAM usage of stack with help of `ezstack`.

# Usage

**--size=**\<path to toolchain size tool\>  
**--elf=**\<path to elf file\>  
**--ezstack=**\<path to stack analyzer _ezstack_\> *optional  
**--mcu=**\<name of mcu, supported all avr mcu and `stm32...`\>  
**--maxflash=**\<maximum size of flash. Needs for stm32 mcu. If specified prints used percents\> *optional  
**--maxram=**\<maximum size of ram. Needs for stm32 mcu. If specified prints used percents\> \*optional

## Example

```cmd
python size_printer.py --size=path/to/avr-size.exe --elf=path/to/firmware.elf --ezstack=path/to/ezstack.exe --mcu="atmega168p"
```

## Result

```c
Device: atmega168p. Program data: 224 bytes (4.0%). RAM usage: 214 bytes (20.9%).
```

## From CMake

```cmake
set (PATH_TO_UTILITY size_printer.py)
set (PATH_TO_EZSTACK ezstack.exe)
add_custom_command(
	TARGET ${EXECUTABLE_NAME} POST_BUILD
	COMMAND
		${PYTHON_EXECUTABLE} ${PATH_TO_UTILITY}
		--size=${CMAKE_SIZE}
		--elf=${OUTPUT_DIR}/${elf_file}
		--ezstack=${PATH_TO_EZSTACK}
		--mcu=${MCU}
		)
)
```

## Tests

Before run tests, set ENVIRONMENT VARIABLES (by `.env` file for example):

```
PATH_TO_AVR_SIZE_TOOL = <avr-size.exe>
PATH_TO_STM32_SIZE_TOOL = <arm-none-eabi-size.exe>
PATH_TO_EZSTACK = <ezstack.exe>
```
