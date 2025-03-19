import asyncio
import logging
from argparse import ArgumentParser
from aiopath import AsyncPath
import aioshutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

async def create_subfolder_for_extension(output_folder, extension):
    subfolder = output_folder / extension[1:].lower()
    if not await subfolder.exists():
        await subfolder.mkdir(parents=True, exist_ok=True)
    return subfolder

async def copy_file(file_path, output_folder):
    try:
        extension = file_path.suffix.lower()
        if extension:
            subfolder = await create_subfolder_for_extension(output_folder, extension)
            destination = subfolder / file_path.name
            await aioshutil.copy(file_path, destination)
            logger.info(f"Файл {file_path} скопійовано в {destination}")
    except Exception as e:
        logger.error(f"Помилка при копіюванні {file_path}: {e}")

async def read_folder(source_folder, output_folder):
    try:
        async for item in source_folder.iterdir():
            if await item.is_dir():
                await read_folder(item, output_folder)
            elif await item.is_file():
                await copy_file(item, output_folder)
    except Exception as e:
        logger.error(f"Помилка при обробці {source_folder}: {e}")

async def main():
    parser = ArgumentParser(description="Сортування файлів по розширенням.")
    parser.add_argument('source', type=str, help="Шлях до вихідної папки")
    parser.add_argument('output', type=str, help="Шлях до цільової папки")
    args = parser.parse_args()

    source_folder = AsyncPath(args.source)
    output_folder = AsyncPath(args.output)

    if not await source_folder.exists() or not await source_folder.is_dir():
        logger.error(f"Вихідна папка {source_folder} не існує або не є директорією.")
        return

    if not await output_folder.exists():
        await output_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Цільова папка {output_folder} створена.")

    await read_folder(source_folder, output_folder)

if __name__ == '__main__':
    asyncio.run(main())