"""实验报告完整性检查。"""

import os
import re


REPORT_NAMES = ['REPORT.md', 'report.md', 'Report.md']
REQUIRED_SECTIONS = ['实验目的', '实验原理', '实验方法', '实验结果', '结果分析', '实验心得']


def find_report():
    for name in REPORT_NAMES:
        if os.path.exists(name):
            return name
    return None


def check_report_content(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    score = 0
    feedback = []

    if len(content) >= 1000:
        score += 3
        feedback.append(f'[OK] 字数达标 ({len(content)}字)')
    else:
        feedback.append(f'[WARN] 字数不足 ({len(content)}字，建议至少1000字)')

    sections_found = sum(1 for section in REQUIRED_SECTIONS if section in content)
    score += sections_found * 2
    feedback.append(f'📋 章节完整性: {sections_found}/{len(REQUIRED_SECTIONS)}')

    image_refs = re.findall(r'!\[.*?\]\(.*?\)', content)
    if len(image_refs) >= 3:
        score += 2
        feedback.append(f'[OK] 包含足够结果图 ({len(image_refs)}张)')
    else:
        feedback.append(f'[WARN] 结果图不足 ({len(image_refs)}张，建议至少3张)')

    if 'AI' in content or 'Copilot' in content or '人工智能' in content:
        score += 1
        feedback.append('[OK] 包含 AI 使用说明')

    if '参考' in content:
        score += 1
        feedback.append('[OK] 包含参考资料')

    return min(score, 15), feedback


def generate_report_score():
    print('=' * 50)
    print('实验报告检查')
    print('=' * 50)
    path = find_report()
    if path is None:
        print('[FAIL] 未找到 REPORT.md')
        print('最终报告得分: 0')
        return 0

    print(f'[OK] 找到报告文件: {path}')
    score, feedback = check_report_content(path)
    for item in feedback:
        print(' ', item)
    print(f'最终报告得分: {score}')
    return score


if __name__ == '__main__':
    generate_report_score()
