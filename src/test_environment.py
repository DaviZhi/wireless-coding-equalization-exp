"""环境测试脚本。"""

import struct
import sys


def test_python_architecture():
    bits = struct.calcsize('P') * 8
    print(f'Python 指针宽度: {bits} 位')
    if bits < 64:
        print(
            '[WARN] 当前为 32 位 Python。SciPy 在 Windows 上通常无官方 pip 轮子，'
            '会继续尝试源码编译并失败。请卸载后安装 64 位 Python，或使用 Miniconda（64 位）。'
        )
        return False
    print('[OK] 64 位 Python，可正常安装 SciPy 等预编译包')
    return True


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
    results = [test_python_version(), test_python_architecture(), test_packages()]
    if all(results):
        print('环境配置正确')
    else:
        print('环境配置存在问题，请运行 pip install -r requirements.txt')


if __name__ == '__main__':
    main()
