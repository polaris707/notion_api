import os
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
    return parser.parse_args().__dict__


def makeConfig(args):
    config_yaml_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "config.yaml")
    with open(config_yaml_path) as f:
        config = yaml.load(f, Loader=SafeLoader)
    
    # merge args and config
    for k in config.keys():
        if k in args:
            config[k] = args[k]
        elif k == "msg":
            config[k] = dict([(mk, args[mk] if args.get(mk) else mv) for mk, mv in config[k].items()])
    return config


def main(args):
    method = args.pop("method")
    config = makeConfig(args)

    if method == "create":
        return createPage(**config)
    elif method == "select":
        return selectPage(**config)
    elif method == "update":
        page_id = getPageId(**config)
        return updatePage(page_id, **config)
    elif method == "delete":
        page_id = getPageId(**config)
        return deletePage(page_id, **config)
    else:
        raise Exception("invalid method")


if __name__ == "__main__":
    args = parseArgs()
    pprint(main(args))
    # python . -m create
    # python . -m select
    # python . -m update -s completed -t finance
    # python . -m delete