import { test, expect } from "@playwright/test";

/**
 * Work Item #1 - ログイン機能
 * --------------------------------------------------
 * ユーザーとして、メールアドレスとパスワードを入力してログインし、
 * ダッシュボードへ遷移できる。
 *
 * 【受け入れ条件】
 * - 正しい認証情報でログインできること
 * - 誤ったパスワードでエラーメッセージが表示されること
 * - 3回連続失敗でアカウントがロックされること
 */

test.describe("ログイン機能 (#1)", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/login");
  });

  // 受け入れ条件1: 正しい認証情報でログインできること
  test("正しい認証情報でログインするとダッシュボードへ遷移できる", async ({
    page,
  }) => {
    await page.getByLabel("メールアドレス").fill("user@example.com");
    await page.getByLabel("パスワード").fill("correct-password");
    await page.getByRole("button", { name: "ログイン" }).click();

    // ダッシュボードへ遷移することを確認
    await expect(page).toHaveURL("/dashboard");
    await expect(
      page.getByRole("heading", { name: "ダッシュボード" }),
    ).toBeVisible();
  });

  // 受け入れ条件2: 誤ったパスワードでエラーメッセージが表示されること
  test("誤ったパスワードを入力するとエラーメッセージが表示される", async ({
    page,
  }) => {
    await page.getByLabel("メールアドレス").fill("user@example.com");
    await page.getByLabel("パスワード").fill("wrong-password");
    await page.getByRole("button", { name: "ログイン" }).click();

    // ログイン画面に留まりエラーメッセージが表示されることを確認
    await expect(page).toHaveURL("/login");
    await expect(
      page.getByText("メールアドレスまたはパスワードが正しくありません"),
    ).toBeVisible();
  });

  // 受け入れ条件3: 3回連続失敗でアカウントがロックされること
  test("3回連続でログインに失敗するとアカウントがロックされる", async ({
    page,
  }) => {
    const emailInput = page.getByLabel("メールアドレス");
    const passwordInput = page.getByLabel("パスワード");
    const loginButton = page.getByRole("button", { name: "ログイン" });

    // 3回連続で誤ったパスワードを入力する
    for (let i = 0; i < 3; i++) {
      await emailInput.fill("user@example.com");
      await passwordInput.fill("wrong-password");
      await loginButton.click();
    }

    // アカウントロックのメッセージが表示され、ボタンが無効になることを確認
    await expect(page.getByText("アカウントがロックされました")).toBeVisible();
    await expect(loginButton).toBeDisabled();
  });
});
