# Remote MCP Server for Coolify (US & Iran)

یک سرور MCP سبک و بهینه با پایتون (FastMCP) و ترنسپورت SSE برای استقرار روی سرورهای کولیفای و اتصال به هوش مصنوعی (Gemini / Antigravity / Claude Desktop).

## امکانات (Tools)
- `get_system_health`: مانیتورینگ منابع سرور (CPU, RAM, Disk).
- `list_docker_containers`: مشاهده وضعیت کانتینرهای فعال و متوقف شده.
- `get_container_logs`: خواندن مستقیم لاگ کانتینرها برای خطایابی هوشمند.
- `restart_docker_container`: ری‌استارت خودکار کانتینر در صورت بروز مشکل.
- `execute_command`: اجرای دستورات خط فرمان روی سرور.

---

## ۱. تنظیمات DNS در Cloudflare
در پنل کلودفلر، برای دامنه‌تان (مثلاً `rpim.ir`) دو رکورد بسازید:
- **سرور آمریکا:**
  - Type: `A`
  - Name: `mcp-us`
  - Target: آی‌پی سرور آمریکا (`209.145.63.253`)
  - Proxy status: خاکستری (DNS Only) یا نارنجی (Proxied)
- **سرور ایران:**
  - Type: `A`
  - Name: `mcp-ir`
  - Target: آی‌پی سرور ایران (`78.157.51.14`)
  - Proxy status: خاکستری (DNS Only)

---

## ۲. استقرار روی کولیفای (Coolify)
1. وارد پنل Coolify بشوید.
2. به بخش **Projects** رفته و **+ New Resource** -> **Application** را انتخاب کنید.
3. مسیر پوشه `mcp-server` را به عنوان Build Context یا مخزن گیت انتخاب کنید.
4. در تنظیمات:
   - **Domains:** `https://mcp-us.yourdomain.com` (یا `https://mcp-ir.yourdomain.com`)
   - **Exposed Port:** `8000`
   - **Volumes:** `/var/run/docker.sock:/var/run/docker.sock`
   - **Environment Variables:** `MCP_AUTH_TOKEN=your_strong_secret_key`
5. دکمه **Deploy** را بزنید.

---

## ۳. اتصال کلاینت محلی (Gemini / Antigravity)
در فایل کانفیگ MCP:
```json
{
  "mcpServers": {
    "us-server": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--stream",
        "https://mcp-us.yourdomain.com/sse"
      ]
    },
    "iran-server": {
      "command": "npx",
      "args": [
        "-y",
        "supergateway",
        "--stream",
        "https://mcp-ir.yourdomain.com/sse"
      ]
    }
  }
}
```
