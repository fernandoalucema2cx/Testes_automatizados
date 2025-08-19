import os
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright


# Configuração do ambiente
BASE_URL = os.getenv("BASE_URL", "https://interno-dev.monitoriadequalidade.com.br")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
RETRIES = int(os.getenv("RETRIES", "1"))
WORKERS = int(os.getenv("WORKERS", "1"))
DEFAULT_TIMEOUT = 120000  # 120 segundos para ações e screenshots

# Diretórios de saída
OUTPUT_DIR = Path("test-results")
VIDEOS_DIR = OUTPUT_DIR / "videos"
TRACES_DIR = OUTPUT_DIR / "traces"
SCREENSHOTS_DIR = OUTPUT_DIR / "screenshots"

for d in [VIDEOS_DIR, TRACES_DIR, SCREENSHOTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# Browser e Page
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        yield browser
        browser.close()

@pytest.fixture
def page(request, browser):
    test_name = request.node.name

    # Cria contexto para vídeo e trace
    context = browser.new_context(
        record_video_dir=str(VIDEOS_DIR),
        record_video_size={"width": 1280, "height": 720}
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()

    yield page

    # Verifica se o teste falhou
    failed = hasattr(request.node, "rep_call") and getattr(request.node.rep_call, "failed", False)

    # Captura screenshot e vídeo **antes de fechar**
    if failed:
        # Screenshot
        screenshot_path = SCREENSHOTS_DIR / f"{test_name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        print(f" Screenshot salvo: {screenshot_path}")

        # Vídeo
        video_files = list(VIDEOS_DIR.glob("**/*.webm"))
        if video_files:
            final_video_path = VIDEOS_DIR / f"{test_name}.webm"
            os.rename(video_files[-1], final_video_path)
            print(f"📹 Vídeo salvo: {final_video_path}")
        else:
            print("⚠ Nenhum vídeo encontrado para este teste.")

    # Fecha página e contexto (necessário para finalizar vídeo e trace)
    page.close()
    context.tracing.stop(path=TRACES_DIR / f"{test_name}-trace.zip")
    context.close()

# Hook para capturar status do teste
def pytest_runtest_makereport(item, call):
    if "page" in item.fixturenames:
        setattr(item, "rep_" + call.when, call)
