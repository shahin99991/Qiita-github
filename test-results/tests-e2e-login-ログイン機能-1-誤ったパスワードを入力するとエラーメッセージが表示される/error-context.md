# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: tests/e2e/login.spec.ts >> ログイン機能 (#1) >> 誤ったパスワードを入力するとエラーメッセージが表示される
- Location: tests/e2e/login.spec.ts:32:7

# Error details

```
Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
Call log:
  - navigating to "/login", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | /**
  4  |  * Work Item #1 - ログイン機能
  5  |  * --------------------------------------------------
  6  |  * ユーザーとして、メールアドレスとパスワードを入力してログインし、
  7  |  * ダッシュボードへ遷移できる。
  8  |  *
  9  |  * 【受け入れ条件】
  10 |  * - 正しい認証情報でログインできること
  11 |  * - 誤ったパスワードでエラーメッセージが表示されること
  12 |  * - 3回連続失敗でアカウントがロックされること
  13 |  */
  14 | 
  15 | test.describe('ログイン機能 (#1)', () => {
  16 |   test.beforeEach(async ({ page }) => {
> 17 |     await page.goto('/login');
     |                ^ Error: page.goto: Protocol error (Page.navigate): Cannot navigate to invalid URL
  18 |   });
  19 | 
  20 |   // 受け入れ条件1: 正しい認証情報でログインできること
  21 |   test('正しい認証情報でログインするとダッシュボードへ遷移できる', async ({ page }) => {
  22 |     await page.getByLabel('メールアドレス').fill('user@example.com');
  23 |     await page.getByLabel('パスワード').fill('correct-password');
  24 |     await page.getByRole('button', { name: 'ログイン' }).click();
  25 | 
  26 |     // ダッシュボードへ遷移することを確認
  27 |     await expect(page).toHaveURL('/dashboard');
  28 |     await expect(page.getByRole('heading', { name: 'ダッシュボード' })).toBeVisible();
  29 |   });
  30 | 
  31 |   // 受け入れ条件2: 誤ったパスワードでエラーメッセージが表示されること
  32 |   test('誤ったパスワードを入力するとエラーメッセージが表示される', async ({ page }) => {
  33 |     await page.getByLabel('メールアドレス').fill('user@example.com');
  34 |     await page.getByLabel('パスワード').fill('wrong-password');
  35 |     await page.getByRole('button', { name: 'ログイン' }).click();
  36 | 
  37 |     // ログイン画面に留まりエラーメッセージが表示されることを確認
  38 |     await expect(page).toHaveURL('/login');
  39 |     await expect(
  40 |       page.getByText('メールアドレスまたはパスワードが正しくありません')
  41 |     ).toBeVisible();
  42 |   });
  43 | 
  44 |   // 受け入れ条件3: 3回連続失敗でアカウントがロックされること
  45 |   test('3回連続でログインに失敗するとアカウントがロックされる', async ({ page }) => {
  46 |     const emailInput = page.getByLabel('メールアドレス');
  47 |     const passwordInput = page.getByLabel('パスワード');
  48 |     const loginButton = page.getByRole('button', { name: 'ログイン' });
  49 | 
  50 |     // 3回連続で誤ったパスワードを入力する
  51 |     for (let i = 0; i < 3; i++) {
  52 |       await emailInput.fill('user@example.com');
  53 |       await passwordInput.fill('wrong-password');
  54 |       await loginButton.click();
  55 |     }
  56 | 
  57 |     // アカウントロックのメッセージが表示され、ボタンが無効になることを確認
  58 |     await expect(
  59 |       page.getByText('アカウントがロックされました')
  60 |     ).toBeVisible();
  61 |     await expect(loginButton).toBeDisabled();
  62 |   });
  63 | });
  64 | 
```