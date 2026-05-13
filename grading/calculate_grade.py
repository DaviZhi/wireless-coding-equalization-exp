"""总评分计算脚本。"""

import json
import os
import re
import subprocess
import sys


MAX_SCORE = 100


def run_command(command, timeout=60):
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        errors='replace',
        timeout=timeout,
    )


def parse_pytest_summary(output):
    counts = {'passed': 0, 'failed': 0, 'skipped': 0, 'error': 0, 'errors': 0}
    for key in counts:
        match = re.search(rf'(\d+)\s+{key}\b', output)
        if match:
            counts[key] = int(match.group(1))
    return counts['passed'], sum(counts.values())


def run_pytest(test_file, name):
    try:
        result = run_command([sys.executable, '-m', 'pytest', test_file, '-v', '--tb=short'])
        output = result.stdout + '\n' + result.stderr
        passed, total = parse_pytest_summary(output)
        if total == 0:
            print(f'  ❌ {name}测试结果解析失败')
            print(output[-1200:])
            return 0, 1
        return passed, total
    except subprocess.TimeoutExpired:
        print(f'  ⏱️ {name}测试超时')
        return 0, 1
    except Exception as error:
        print(f'  ❌ {name}测试运行失败: {error}')
        return 0, 1


def component_score(passed, total, function_score, artifact_score):
    if total <= 0:
        return 0
    function_tests = max(total - 1, 1)
    function_passed = min(passed, function_tests)
    score = function_score * function_passed / function_tests
    if passed == total:
        score += artifact_score
    return int(round(score))


def environment_score():
    try:
        result = run_command([sys.executable, 'src/test_environment.py'], timeout=30)
        if result.returncode == 0 and '环境配置正确' in result.stdout:
            print('  ✅ 环境测试通过: +5分')
            return 5
    except Exception:
        pass
    print('  ❌ 环境测试失败: 0分')
    return 0


def report_score():
    try:
        result = run_command([sys.executable, 'grading/check_report.py'], timeout=20)
        match = re.search(r'最终报告得分:\s*(\d+)', result.stdout)
        if match:
            score = int(match.group(1))
            print(f'  报告得分: {score}/15')
            return score
    except Exception:
        pass
    print('  ❌ 报告检查失败: 0分')
    return 0


def pylint_score():
    try:
        result = run_command([
            sys.executable, '-m', 'pylint',
            'src/part1_channel_coding.py', 'src/part2_equalization.py', '--score=y'
        ], timeout=40)
        match = re.search(r'Your code has been rated at ([\d.\-]+)/10', result.stdout)
        if match:
            raw = float(match.group(1))
            if raw >= 8.0:
                print(f'  ✅ 代码质量优秀 ({raw}/10): +5分')
                return 5
            if raw >= 5.0:
                print(f'  ⚠️ 代码质量一般 ({raw}/10): 0分')
                return 0
            print(f'  ❌ 代码质量较差 ({raw}/10): -10分')
            return -10
    except Exception:
        pass
    print('  ℹ️ pylint检查跳过: 0分')
    return 0


def optional_bonus():
    bonus = 0
    try:
        with open('src/part1_channel_coding.py', 'r', encoding='utf-8') as file:
            content = file.read()
        if '选做：请实现卷积码编码' not in content and '选做：请实现 Viterbi' not in content:
            bonus += 10
            print('  ✅ 卷积码/Viterbi选做已实现: +10分')
    except Exception:
        pass
    if bonus == 0:
        print('  ℹ️ 未完成选做任务: 0分')
    return bonus


def calculate_grade():
    print('=' * 60)
    print('信道编码与信道均衡实验 - 自动评分系统')
    print('=' * 60)
    total = 0

    print('\n1️⃣ 环境配置测试 (5分)')
    env = environment_score()
    total += env

    print('\n2️⃣ Part 1：信道编码测试 (35分)')
    passed, count = run_pytest('grading/test_part1_coding.py', 'Part 1')
    part1 = component_score(passed, count, function_score=25, artifact_score=10)
    print(f'  通过测试: {passed}/{count}')
    print('  评分规则: 函数正确性25分 + 结果图10分')
    print(f'  得分: {part1}/35')
    total += part1

    print('\n3️⃣ Part 2：信道均衡测试 (35分)')
    passed, count = run_pytest('grading/test_part2_equalization.py', 'Part 2')
    part2 = component_score(passed, count, function_score=25, artifact_score=10)
    print(f'  通过测试: {passed}/{count}')
    print('  评分规则: 函数正确性25分 + 结果图10分')
    print(f'  得分: {part2}/35')
    total += part2

    print('\n4️⃣ 实验报告检查 (15分)')
    report = report_score()
    total += report

    print('\n5️⃣ 代码质量检查')
    quality = pylint_score()
    total += quality

    print('\n6️⃣ 选做任务加分')
    bonus = optional_bonus()
    total += bonus

    total = max(0, min(total, MAX_SCORE))
    if total >= 90:
        grade = 'A (优秀)'
    elif total >= 80:
        grade = 'B (良好)'
    elif total >= 70:
        grade = 'C (中等)'
    elif total >= 60:
        grade = 'D (及格)'
    else:
        grade = 'F (不及格)'

    print('\n' + '=' * 60)
    print(f'总分: {total}/{MAX_SCORE}')
    print(f'等级: {grade}')
    print('=' * 60)

    report_data = {
        'total_score': total,
        'max_score': MAX_SCORE,
        'grade': grade,
        'breakdown': {
            'environment': env,
            'part1_coding': part1,
            'part2_equalization': part2,
            'report': report,
            'code_quality': quality,
            'bonus': bonus,
        },
    }
    with open('grade_report.json', 'w', encoding='utf-8') as file:
        json.dump(report_data, file, indent=2, ensure_ascii=False)
    print('详细评分报告已保存到: grade_report.json')
    return total


if __name__ == '__main__':
    calculate_grade()
