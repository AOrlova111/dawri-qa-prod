from playwright.sync_api import sync_playwright

def test_user_login_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("1. Відкриваємо сайт Dawri...")
        page.goto("https://dawri.pprnd.co/")
        page.wait_for_timeout(2000)
        
        print("2. Змінюємо мову на англійську (EN)...")
        page.click('text="EN"')
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        
        print("3. Натискаємо на гамбургер-меню...")
        page.locator('button:has(svg path[d*="M1 7.66732"])').click()
        page.wait_for_timeout(1500)
        
        print("4. Кликаємо на опцію Sign Up / Sign In у меню...")
        page.get_by_text("Sign Up", exact=False).first.click()
        page.wait_for_timeout(2000)
        
        print("5. Вводимо номер телефону...")
        # Шукаємо поле вводу (input усередині форми логіну)
        phone_input = page.locator('input[type="tel"], input[placeholder*="phone" i], form input').last
        phone_input.click()
        # Видаляємо старий текст бекспейсами
        for _ in range(15):
            phone_input.press("Backspace")
        
        # Вводимо номер без плюса (або з плюсом, якщо поле саме підлаштовує)
        phone_input.fill("380667362294")
        page.wait_for_timeout(1000)
        
        print("6. Натискаємо кнопку SIGN UP/SIGN IN...")
        page.click('button:has-text("SIGN UP")', timeout=3000)
        page.wait_for_timeout(3000)
        
        print("7. Вводимо постійний SMS-код 2294...")
        code_input = page.locator('input[type="text"], input[maxlength], input').first
        code_input.click()
        code_input.fill("2294")
        page.wait_for_timeout(1000)
        
        print("8. Підтверджуємо код...")
        page.click('button:has-text("Verify"), button:has-text("Confirm"), button:has-text("Sign In"), button:has-text("Continue")', timeout=3000)
        page.wait_for_timeout(4000)
        
        print("9. Авторизація успішно завершена!")
        browser.close()
