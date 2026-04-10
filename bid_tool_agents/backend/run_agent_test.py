#!/usr/bin/env python3
"""
快速运行单个Agent测试的脚本

用法:
    python run_agent_test.py parser          # 运行parser测试
    python run_agent_test.py compliance      # 运行compliance测试
    python run_agent_test.py all             # 运行所有测试
"""
import sys
import os
import subprocess
import argparse

# 颜色定义
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def print_status(msg, status="info"):
    """打印状态"""
    if status == "success":
        print(f"{GREEN}✓ {msg}{RESET}")
    elif status == "error":
        print(f"{RED}✗ {msg}{RESET}")
    elif status == "warning":
        print(f"{YELLOW}⚠ {msg}{RESET}")
    else:
        print(f"  {msg}")


def run_tests(agent_name: str, verbose: bool = False):
    """运行测试"""
    test_path = f"tests/agents/test_{agent_name}.py"

    if not os.path.exists(test_path):
        print_status(f"测试文件不存在: {test_path}", "error")
        return False

    # 构建pytest命令
    cmd = [
        sys.executable, "-m", "pytest",
        test_path,
        "-v" if verbose else "-q",
        "--tb=short",
        "--color=yes"
    ]

    print_status(f"运行测试: {agent_name}", "info")
    print()

    result = subprocess.run(cmd, cwd=os.path.dirname(__file__))

    if result.returncode == 0:
        print_status(f"测试通过: {agent_name}", "success")
        return True
    else:
        print_status(f"测试失败: {agent_name}", "error")
        return False


def list_agents():
    """列出所有Agent"""
    print("\n可测试的Agent:")
    agents = [
        ("parser", "文档解析Agent"),
        ("compliance", "合规审查Agent"),
        ("comparison", "比对分析Agent"),
        ("qualification", "资质核验Agent"),
        ("risk", "风险识别Agent"),
        ("evaluation", "辅助评标Agent"),
        ("expert", "专家抽取Agent"),
        ("archive", "档案管理Agent"),
        ("statistics", "统计分析Agent"),
    ]

    for name, desc in agents:
        print(f"  {name:20} - {desc}")

    print()


def main():
    parser = argparse.ArgumentParser(description="运行Agent测试")
    parser.add_argument(
        "agent",
        nargs="?",
        default="all",
        help="Agent名称 (如 parser, compliance)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    parser.add_argument("-l", "--list", action="store_true", help="列出所有Agent")

    args = parser.parse_args()

    if args.list:
        list_agents()
        return

    if args.agent == "all":
        # 运行所有测试
        agents = [
            "parser", "compliance", "comparison",
            "qualification", "risk", "evaluation",
            "expert", "archive", "statistics"
        ]

        print(f"{'='*50}")
        print("运行所有Agent测试")
        print(f"{'='*50}\n")

        results = {}
        for agent in agents:
            results[agent] = run_tests(agent, args.verbose)

        # 汇总
        print(f"\n{'='*50}")
        print("测试汇总")
        print(f"{'='*50}")

        passed = sum(1 for v in results.values() if v)
        total = len(results)

        for agent, success in results.items():
            status = "✓ PASS" if success else "✗ FAIL"
            color = GREEN if success else RED
            print(f"{color}{status}{RESET} - {agent}")

        print(f"\n通过: {passed}/{total}")

        sys.exit(0 if passed == total else 1)
    else:
        # 运行单个测试
        success = run_tests(args.agent, args.verbose)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
