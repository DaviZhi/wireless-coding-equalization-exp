"""Generate and publish a GitHub homework tracking table."""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDENTS_FILE = ROOT / 'course_management' / 'students.csv'
TRACKING_FILE = ROOT / 'course_management' / 'homework_tracking.csv'
TRACKING_MARKDOWN = ROOT / 'course_management' / 'HOMEWORK_TRACKING.md'
COMMENT_MARKER = '<!-- homework-tracker:managed -->'
DEFAULT_HOMEWORK_NAME = '无线通信技术实验 02：信道编码与信道均衡'


def read_students():
    with STUDENTS_FILE.open('r', encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))


def api_request(path, method='GET', data=None):
    token = os.environ.get('GITHUB_TOKEN')
    repository = os.environ.get('GITHUB_REPOSITORY')
    if not token or not repository:
        return None

    url = f'https://api.github.com/repos/{repository}{path}'
    body = None if data is None else json.dumps(data).encode('utf-8')
    request = urllib.request.Request(url, data=body, method=method)
    request.add_header('Accept', 'application/vnd.github+json')
    request.add_header('Authorization', f'Bearer {token}')
    request.add_header('X-GitHub-Api-Version', '2022-11-28')
    if body is not None:
        request.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status == 204:
                return None
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        detail = error.read().decode('utf-8', errors='replace')
        print(f'GitHub API request failed: {method} {path} -> {error.code} {detail}', file=sys.stderr)
        return None


def paged_api(path):
    items = []
    page = 1
    while True:
        separator = '&' if '?' in path else '?'
        data = api_request(f'{path}{separator}per_page=100&page={page}')
        if not data:
            break
        items.extend(data)
        if len(data) < 100:
            break
        page += 1
    return items


def normalize_login(login):
    return (login or '').strip().lstrip('@').lower()


def pr_status(pull_request):
    if pull_request.get('merged_at'):
        return 'merged'
    return pull_request.get('state', '')


def latest_grade(issue_number):
    comments = paged_api(f'/issues/{issue_number}/comments')
    grade = ''
    for comment in comments:
        body = comment.get('body') or ''
        if '自动评分结果' not in body:
            continue
        match = re.search(r'总分[:：]\s*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)', body)
        if match:
            grade = f'{match.group(1)}/{match.group(2)}'
    return grade


def collect_pull_requests():
    pull_requests = paged_api('/pulls?state=all&sort=updated&direction=desc')
    for pull_request in pull_requests:
        pull_request['parsed_grade'] = latest_grade(pull_request['number'])
    return pull_requests


def match_student_prs(student, pull_requests):
    github_login = normalize_login(student.get('GitHub用户名'))
    student_id = (student.get('学号') or '').strip()
    student_name = (student.get('姓名') or '').strip()
    matches = []
    for pull_request in pull_requests:
        author = normalize_login((pull_request.get('user') or {}).get('login'))
        branch = ((pull_request.get('head') or {}).get('ref') or '').lower()
        title = pull_request.get('title') or ''
        if github_login and author == github_login:
            matches.append(pull_request)
        elif not github_login and student_id and (student_id in branch or student_id in title):
            matches.append(pull_request)
        elif not github_login and student_name and student_name in title:
            matches.append(pull_request)
    return matches


def build_rows(students, pull_requests):
    rows = []
    for student in students:
        matches = match_student_prs(student, pull_requests)
        latest = matches[0] if matches else None
        latest_pr = ''
        latest_state = ''
        latest_score = ''
        grading_status = '待提交'
        latest_time = ''
        submission_count = 0

        if latest:
            latest_pr = f"#{latest['number']} {latest.get('html_url', '')}".strip()
            latest_state = pr_status(latest)
            latest_score = latest.get('parsed_grade') or ''
            grading_status = '已评分' if latest_score else '未评分'
            latest_time = latest.get('updated_at') or ''
            submission_count = int(latest.get('commits') or 0)

        rows.append({
            '序号': student.get('序号', ''),
            '学号': student.get('学号', ''),
            '姓名': student.get('姓名', ''),
            'GitHub用户名': student.get('GitHub用户名', ''),
            '是否提交代码': '是' if latest else '否',
            'PR数量': str(len(matches)),
            '提交次数': str(submission_count),
            '最新PR': latest_pr,
            '最新PR状态': latest_state,
            '最新评分': latest_score,
            '评分状态': grading_status,
            '最近提交时间': latest_time,
            '备注': student.get('备注', ''),
        })
    return rows


def write_csv(rows):
    fieldnames = ['序号', '学号', '姓名', 'GitHub用户名', '是否提交代码', 'PR数量', '提交次数', '最新PR', '最新PR状态', '最新评分', '评分状态', '最近提交时间', '备注']
    with TRACKING_FILE.open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_link(value):
    if not value.startswith('#') or ' ' not in value:
        return value
    number, url = value.split(' ', 1)
    return f'[{number}]({url})' if url else number


def build_markdown(rows):
    homework_name = os.environ.get('HOMEWORK_NAME', DEFAULT_HOMEWORK_NAME)
    submitted = sum(1 for row in rows if row['是否提交代码'] == '是')
    graded = sum(1 for row in rows if row['评分状态'] == '已评分')
    lines = [
        COMMENT_MARKER,
        f'# {homework_name}作业实时跟踪表',
        '',
        f'- 学生总数：{len(rows)}',
        f'- 已提交代码：{submitted}',
        f'- 已获得评分：{graded}',
        '',
        '| 序号 | 学号 | 姓名 | GitHub | 是否提交代码 | PR数量 | 提交次数 | 最新PR | 状态 | 最新评分 | 评分状态 | 最近提交时间 | 备注 |',
        '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |',
    ]
    for row in rows:
        github = row['GitHub用户名']
        github_cell = f'@{github}' if github else ''
        values = [
            row['序号'], row['学号'], row['姓名'], github_cell, row['是否提交代码'],
            row['PR数量'], row['提交次数'], markdown_link(row['最新PR']), row['最新PR状态'],
            row['最新评分'], row['评分状态'], row['最近提交时间'], row['备注'],
        ]
        lines.append('| ' + ' | '.join(value.replace('|', '\\|') for value in values) + ' |')
    lines.extend(['', '_本表由 GitHub Actions 自动更新。_'])
    return '\n'.join(lines) + '\n'


def write_markdown(markdown):
    TRACKING_MARKDOWN.write_text(markdown, encoding='utf-8')
    summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary:
        Path(summary).write_text(markdown, encoding='utf-8')


def publish_issue_comment(markdown):
    issue_number = os.environ.get('TRACKING_ISSUE_NUMBER')
    if not issue_number:
        return
    comments = paged_api(f'/issues/{issue_number}/comments')
    managed_comment = next((comment for comment in comments if COMMENT_MARKER in (comment.get('body') or '')), None)
    if managed_comment:
        api_request(f"/issues/comments/{managed_comment['id']}", method='PATCH', data={'body': markdown})
    else:
        api_request(f'/issues/{issue_number}/comments', method='POST', data={'body': markdown})


def main():
    students = read_students()
    pull_requests = collect_pull_requests() if os.environ.get('GITHUB_TOKEN') else []
    rows = build_rows(students, pull_requests)
    markdown = build_markdown(rows)
    write_csv(rows)
    write_markdown(markdown)
    publish_issue_comment(markdown)
    print(f'已生成 {len(rows)} 名学生的作业跟踪表。')


if __name__ == '__main__':
    main()