import os
import psutil
import subprocess
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("RemoteOpsServer")

AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN", "")

@mcp.tool()
def get_system_health() -> str:
    """دریافت وضعیت لحظه‌ای مصرف پردازنده (CPU)، حافظه رم (RAM) و دیسک سرور"""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return (
        f"🖥️ CPU Usage: {cpu}%\n"
        f"💾 RAM: {ram.percent}% (Used: {ram.used // (1024**2)}MB / Total: {ram.total // (1024**2)}MB)\n"
        f"📁 Disk: {disk.percent}% (Free: {disk.free // (1024**3)}GB)"
    )

@mcp.tool()
def list_docker_containers() -> str:
    """مشاهده لیست کانتینرهای داکر، وضعیت اجرا و پورت‌های آنها"""
    try:
        res = subprocess.run(
            ["docker", "ps", "-a", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"],
            capture_output=True, text=True, check=True
        )
        return res.stdout if res.stdout.strip() else "هیچ کانتینری یافت نشد."
    except Exception as e:
        return f"خطا در ارتباط با داکر: {str(e)}"

@mcp.tool()
def get_container_logs(container_name: str, lines: int = 50) -> str:
    """مشاهده آخرین خطوط لاگ یک کانتینر مشخص برای دیباگ سریع"""
    try:
        res = subprocess.run(
            ["docker", "logs", "--tail", str(lines), container_name],
            capture_output=True, text=True, check=True
        )
        logs = res.stdout or res.stderr
        return logs if logs.strip() else "لاگی برای این کانتینر وجود ندارد."
    except Exception as e:
        return f"خطا در خواندن لاگ کانتینر {container_name}: {str(e)}"

@mcp.tool()
def restart_docker_container(container_name: str) -> str:
    """ری‌استارت کردن یک کانتینر داکر در سرور"""
    try:
        subprocess.run(
            ["docker", "restart", container_name],
            capture_output=True, text=True, check=True
        )
        return f"✅ کانتینر {container_name} با موفقیت ری‌استارت شد."
    except Exception as e:
        return f"❌ خطا در ری‌استارت کانتینر {container_name}: {str(e)}"

@mcp.tool()
def execute_command(command: str) -> str:
    """اجرای ایمن دستورات بش و خط فرمان روی سرور با تایم‌اوت ۳۰ ثانیه"""
    try:
        res = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        output = res.stdout if res.stdout else res.stderr
        return output if output.strip() else "دستور بدون خروجی متنی با موفقیت اجرا شد."
    except subprocess.TimeoutExpired:
        return "⚠️ اجرای دستور به دلیل طولانی شدن (بیش از ۳۰ ثانیه) متوقف شد."
    except Exception as e:
        return f"❌ خطا در اجرای دستور: {str(e)}"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"Starting FastMCP SSE Server on {host}:{port}...")
    mcp.run(transport="sse", host=host, port=port)
