from playwright.sync_api import sync_playwright

def test_venue_facility_booking_stage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("\n--- Сценарій: Повний цикл бронювання на Stage з логіном та оплатою ---")

        # 1. Перехід на головну сторінку Stage
        page.goto("https://stage-dawri.pprnd.co/", timeout=60000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        # 2. Перемикаємо мову на EN
        print("1. Перемикаємо мову на EN...")
        en_button = page.get_by_text("EN", exact=True)
        if en_button.is_visible():
            en_button.click()
            page.wait_for_timeout(2000)

        # 3. Натискаємо SEARCH
        print("2. Натискаємо SEARCH...")
        search_button = page.get_by_role("button", name="SEARCH")
        search_button.click()
        page.wait_for_timeout(2000)

        # 4. Обираємо "venue stage"
        print("3. Обираємо 'venue stage'...")
        page.wait_for_selector("text=venue stage", timeout=15000)
        venue_stage = page.get_by_text("venue stage", exact=True)
        venue_stage.scroll_into_view_if_needed()
        venue_stage.click()
        page.wait_for_timeout(2000)

        # 5. Обираємо "facility stage"
        print("4. Обираємо 'facility stage'...")
        page.wait_for_selector("text=facility stage", timeout=15000)
        facility_stage = page.get_by_text("facility stage", exact=True)
        facility_stage.click()
        page.wait_for_timeout(2000)

        # 6. Натискаємо BOOK SERVICE
        print("5. Натискаємо 'BOOK SERVICE'...")
        book_service_btn = page.get_by_role("button", name="BOOK SERVICE")
        book_service_btn.click()
        page.wait_for_timeout(2000)

        # 7. Обираємо Single session
        print("6. Перевіряємо вибір 'Single session'...")
        single_session_radio = page.get_by_label("Single session")
        if not single_session_radio.is_checked():
            single_session_radio.check()
        page.wait_for_timeout(1500)

        # 8. Відкриваємо вибір часу
        print("7. Відкриваємо 'Choose time'...")
        choose_time_btn = page.locator("button.MuiButton-root:has-text('Choose time')").first
        choose_time_btn.click()
        page.wait_for_timeout(2000)

        # 9. Обираємо слот 08:00 - 08:05 з підсвічуванням
        print("8. Обираємо слот 08:00 - 08:05...")
        drawer = page.locator("div.MuiDrawer-root").filter(has_text="Choose time")
        drawer_paper = drawer.locator(".MuiDrawer-paper")
        drawer_paper.wait_for(state="visible", timeout=10000)
        page.wait_for_timeout(1000)

        slot_1 = drawer_paper.locator(".MuiGrid2-root > .MuiBox-root", has_text="08:00 - 08:05").first
        slot_1.scroll_into_view_if_needed()
        slot_1.evaluate("node => node.style.border = '3px solid red'")
        page.wait_for_timeout(1500)
        slot_1.click()
        page.wait_for_timeout(1500)

        # 10. Натискаємо 'CONTINUE' у модалці
        print("9. Натискаємо 'CONTINUE' у модалці...")
        modal_continue_btn = drawer_paper.get_by_role("button", name="Continue")
        modal_continue_btn.click()
        page.wait_for_timeout(2000)

        # 11. Натискаємо CONFIRM
        print("10. Натискаємо 'CONFIRM'...")
        confirm_btn_1 = page.locator("button:has-text('CONFIRM')").first
        confirm_btn_1.click()
        page.wait_for_timeout(2000)

        # ------------------- КРОК АВТОРИЗАЦІЇ -------------------
        # 12. Очищаємо шаблон телефону через JS та вводимо номер +380667362294
        print("11. Вводимо номер телефону +380667362294...")
        phone_input = page.locator("input[type='tel']")
        phone_input.wait_for(state="visible", timeout=10000)
        phone_input.click()
        page.wait_for_timeout(500)
        phone_input.evaluate("node => { node.value = ''; node.dispatchEvent(new Event('input', { bubbles: true })); }")
        phone_input.type("+380667362294", delay=100)
        page.wait_for_timeout(1000)

        # 13. Натискаємо CONTINUE
        print("12. Натискаємо 'CONTINUE' під формою телефону...")
        phone_continue_btn = page.get_by_role("button", name="CONTINUE")
        phone_continue_btn.click()
        page.wait_for_timeout(2000)

        # 14. Вводимо чотиризначний код 2294
        print("13. Вводимо код підтвердження 2294...")
        page.wait_for_selector("input", timeout=10000)
        otp_inputs = page.locator("input")
        if otp_inputs.count() > 1:
            for i, digit in enumerate("2294"):
                otp_inputs.nth(i).fill(digit)
        else:
            otp_inputs.first.fill("2294")
            
        page.wait_for_timeout(1000)

        # 15. Натискаємо CONFIRM після введення коду
        print("14. Натискаємо 'CONFIRM' після введення коду...")
        confirm_code_btn = page.get_by_role("button", name="CONFIRM")
        confirm_code_btn.click()
        page.wait_for_timeout(2500)

        # ------------------- КРОК ОПЛАТИ -------------------
        # 16. Натискаємо кнопку PAYMENT на наступній сторінці
        print("15. Натискаємо 'PAYMENT'...")
        page.wait_for_selector("button:has-text('PAYMENT')", timeout=15000)
        payment_btn = page.get_by_role("button", name="PAYMENT")
        payment_btn.click()
        page.wait_for_timeout(2000)

        # 17. Обираємо метод оплати (Гаманець)
        print("16. Обираємо метод оплати...")
        page.wait_for_selector("text=Payment options", timeout=15000)
        wallet_checkbox = page.locator("input[type='checkbox']").first
        if not wallet_checkbox.is_checked():
            wallet_checkbox.check()
        page.wait_for_timeout(1500)

        # 18. Натискаємо CONFIRM
        print("17. Натискаємо 'CONFIRM' для опції оплати...")
        confirm_payment_opt_btn = page.get_by_role("button", name="CONFIRM")
        confirm_payment_opt_btn.click()
        page.wait_for_timeout(2000)

        # 19. Підтверджуємо CONFIRM PAYMENT
        print("18. Підтверджуємо 'CONFIRM PAYMENT'...")
        confirm_final_btn = page.get_by_role("button", name="CONFIRM PAYMENT")
        confirm_final_btn.click()
        page.wait_for_timeout(2000)

        # 20. Перевірка успішності бронювання
        print("19. Перевіряємо успішність бронювання...")
        page.wait_for_selector("text=Booking details", timeout=20000)

        assert "booking-details" in page.url or page.locator("text=Upcoming").is_visible()
        print("✅ Тест успішно пройдено! Бронювання створено.")

        page.wait_for_timeout(10000)
        browser.close()

if __name__ == "__main__":
    test_venue_facility_booking_stage()
