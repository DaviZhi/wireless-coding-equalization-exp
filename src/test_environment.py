"""环境测试脚本。"""

import sys


def test_python_version():
    version = sys.version_info
    print(f'Python版本: {version.major}.{version.minor}.{version.micro}')
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print('[FAIL] Python版本过低，需要3.9或更高版本')
        return False
    print('[OK] Python版本符合要求')
    return True


def test_packages():
    packages = ['numpy', 'scipy', 'matplotlib', 'pytest']
    ok = True
    for package in packages:
        try:
            module = __import__(package)
            print(f'[OK] {package} {getattr(module, "__version__", "")} 已安装')
        except ImportError:
            print(f'[FAIL] {package} 未安装')
            ok = False
    return ok


def main():
    print('=' * 50)
    print('信道编码与信道均衡实验 - 环境测试')
    print('=' * 50)
    results = [test_python_version(), test_packages()]
    if all(results):
        print('环境配置正确')
    else:
        print('环境配置存在问题，请运行 pip install -r requirements.txt')


if __name__ == '__main__':
    main()
