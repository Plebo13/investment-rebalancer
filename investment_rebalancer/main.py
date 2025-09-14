from pydantic_yaml import parse_yaml_raw_as
import yaml

from investment_rebalancer.model import ETFList, ETF


def main():
    with open("configs/config.yml", "r") as config_file:
        config_yml = yaml.safe_load(config_file)

    etf_list = ETFList()
    for etf in config_yml["etfs"]:
        etf_list.append(parse_yaml_raw_as(ETF, str(etf)))

    etf_list.rebalance()


if __name__ == "__main__":
    main()
