import argparse
import logging
from datetime import datetime
from os import getenv, mkdir
from os.path import join
from shutil import rmtree

from cbi import start
from hdx.api.configuration import Configuration
from hdx.facades.keyword_arguments import facade
from hdx.utilities.downloader import Download
from hdx.utilities.easy_logging import setup_logging
from hdx.utilities.retriever import Retrieve

setup_logging()
logger = logging.getLogger()


VERSION = 1.0


def parse_args():
    parser = argparse.ArgumentParser(description="CBi Explorer")
    parser.add_argument("-ua", "--user_agent", default=None, help="user agent")
    parser.add_argument("-pp", "--preprefix", default=None, help="preprefix")
    parser.add_argument("-hs", "--hdx_site", default=None, help="HDX site to use")
    parser.add_argument("-od", "--output_dir", default="output", help="Output folder")
    parser.add_argument(
        "-sd", "--saved_dir", default="saved_data", help="Saved data folder"
    )
    parser.add_argument(
        "-sv", "--save", default=False, action="store_true", help="Save downloaded data"
    )
    parser.add_argument(
        "-usv", "--use_saved", default=False, action="store_true", help="Use saved data"
    )
    args = parser.parse_args()
    return args


def main(
    output_dir,
    saved_dir,
    save,
    use_saved,
    **ignore,
):
    logger.info(f"##### hdx-scraper-cbi-viz version {VERSION:.1f} ####")
    configuration = Configuration.read()
    rmtree(output_dir, ignore_errors=True)
    mkdir(output_dir)
    with Download() as downloader:
        retriever = Retrieve(
            downloader,
            configuration["fallback_dir"],
            saved_dir,
            output_dir,
            save,
            use_saved,
        )
        today = datetime.utcnow().isoformat()
        start(
            configuration,
            today,
            retriever,
            output_dir,
        )


if __name__ == "__main__":
    args = parse_args()
    user_agent = args.user_agent
    if user_agent is None:
        user_agent = getenv("USER_AGENT")
        if user_agent is None:
            user_agent = "hdx-scraper-iati-viz"
    preprefix = args.preprefix
    if preprefix is None:
        preprefix = getenv("PREPREFIX")
    hdx_site = args.hdx_site
    if hdx_site is None:
        hdx_site = getenv("HDX_SITE", "prod")
    facade(
        main,
        hdx_read_only=True,
        user_agent=user_agent,
        preprefix=preprefix,
        hdx_site=hdx_site,
        project_config_yaml=join("config", "project_configuration.yml"),
        output_dir=args.output_dir,
        saved_dir=args.saved_dir,
        save=args.save,
        use_saved=args.use_saved,
    )
