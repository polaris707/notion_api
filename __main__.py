import os
import sys
import pathlib
import yaml
import argparse
import datetime
from pprint import pprint
from yaml.loader import SafeLoader
from notion.database.page.crud import createPage, selectPage, getPageId, updatePage, deletePage    


def parseArgs():
    parser = argparse.ArgumentParser(description="crud notion database page")
    parser.add_argument("-m", "--method", required=True)
    parser.add_argument("-i", "--icon")
    parser.add_argument("-T", "--title")
    parser.add_argument("-s", "--status")
    parser.add_argument("-t", "--tag", nargs="*")
    parser.add_argument("-d", "--due_date", default=datetime.datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("-c", "--config_file", default="config.yaml")
    return parser.parse_args().__dict__


def makeConfig():
    args = parseArgs()
    config_yaml_path = os.path.join(pathlib.Path(__file__).parent.resolve(), args["config_file"])
    with open(config_yaml_path) as f:
        config = yaml.load(f, Loader=SafeLoader)
    
    # merge args and config
    config["method"] = args["method"]
    for k in config.keys():
        if k in args:
            config[k] = args[k]
        elif k == "msg":
            config[k] = dict([(mk, args[mk] if args.get(mk) else mv) for mk, mv in config[k].items()])
    return config


def main(method, **kwargs):
    if method == "create":
        return createPage(**kwargs)
    elif method == "select":
        return selectPage(**kwargs)
    elif method == "update":
        page_id = getPageId(**kwargs)
        return updatePage(page_id, **kwargs)
    elif method == "delete":
        page_id = getPageId(**kwargs)
        return deletePage(page_id, **kwargs)
    else:
        raise Exception("invalid method")


if __name__ == "__main__":
    config = makeConfig()
    pprint(config)
    pprint(main(**config))
    # python . -m create
    # python . -m select
    # python . -m update -s completed -t finance
    # python . -m delete