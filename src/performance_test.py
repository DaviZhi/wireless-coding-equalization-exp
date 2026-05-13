"""综合性能测试：编码与均衡效果对比。"""

from part1_channel_coding import run_coding_demo
from part2_equalization import run_equalization_demo


def main():
    run_coding_demo()
    run_equalization_demo()


if __name__ == '__main__':
    main()
