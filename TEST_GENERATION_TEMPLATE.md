# Playwright Test Generation Template for B2B Manager (CanvasKit)

This template is derived from `add-vehicle.spec.ts` and `add-vehicle-silent.spec.ts`, optimized for the B2B Manager Flutter Web application. It addresses the challenges of CanvasKit rendering by prioritizing coordinate-based interactions and API-level verification.

## Usage
Copy the code block below into a new `.spec.ts` file in `tests_ts/scenarios/` and replace the `TODO` placeholders.

## Template Code

```typescript
import { test, expect } from '@playwright/test';

// ------------------------------
// 1. Configuration & Constants
// ------------------------------
const USER = process.env.TEST_USER ?? 'justine.chen@slc.com.tw';
const PASS = process.env.TEST_PASS ?? '111111';
const BASE_URL = process.env.TEST_BASE_URL ?? 'https://b2bmanager.staging.ssgsslc.com/';

// Viewport must be fixed to ensure coordinates are consistent
test.use({ viewport: { width: 1920, height: 1080 } });
// Set a reasonable timeout for complex flows (CanvasKit can be slow)
test.setTimeout(60_000);

test.describe('[Feature Name]', () => {
  test('[Test Case Description]', async ({ page }) => {
    // ------------------------------
    // Phase 1: Login
    // ------------------------------
    console.log('=== Step 1: Login ===');
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');

    // Standard Login Flow
    await page.getByLabel('電子信箱').fill(USER);
    await page.getByLabel('密碼').fill(PASS);
    await page.getByRole('button', { name: '登入' }).click();

    // Wait for redirect to home
    await page.waitForURL('**/home_page', { timeout: 20_000 });
    await page.waitForTimeout(3000); // Critical: Wait for Flutter engine to stabilize

    // ------------------------------
    // Phase 2: Navigation (Direct URL Preferred)
    // ------------------------------
    console.log('=== Step 2: Navigation ===');
    // Using direct URL is more reliable than menu clicking in CanvasKit
    // TODO: Replace [route_path] with actual path (e.g., car_page, driver_page)
    const targetUrl = `${BASE_URL}[route_path]`; 
    await page.goto(targetUrl);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(3000); // Wait for page content to render

    // ------------------------------
    // Phase 3: API Spy Setup
    // ------------------------------
    console.log('=== Step 3: API Monitoring Setup ===');
    // Capture request data for verification later
    let requestBody: any = null;
    let responseStatus: number = 0;

    // TODO: Replace [api_endpoint] with actual API path (e.g., **/cars, **/drivers)
    // TODO: Adjust method (POST/PUT/DELETE) as needed
    await page.route('**/[api_endpoint]', async route => {
      const req = route.request();
      // Only capture the relevant method
      if (req.method() === 'POST') {
        try {
            const postData = req.postData();
            if (postData) {
              requestBody = JSON.parse(postData);
              console.log('Captured Request Body:', requestBody);
            }
        } catch (e) {
            console.log('Error parsing request body:', e);
        }
      }
      
      // Continue request and capture response status
      const response = await route.fetch();
      responseStatus = response.status();
      await route.fulfill({ response });
    });

    // ------------------------------
    // Phase 4: UI Interaction (Coordinate & Keyboard)
    // ------------------------------
    console.log('=== Step 4: UI Interaction ===');
    
    // NOTE: Coordinates are based on 1920x1080 viewport.
    // Use `npm run test:your-test -- --headed` to debug coordinates if needed.

    // 1. Open Drawer/Dialog
    // TODO: Update X,Y for the "Add" button (usually top-right)
    // await page.mouse.click(1850, 157); 
    // await page.waitForTimeout(2000); // Wait for animation

    // 2. Fill Form
    // Example: Click input field and type
    // const drawerX = 1700;
    // let currentY = 130;
    
    // Field 1
    // await page.mouse.click(drawerX, currentY);
    // await page.keyboard.type('Test Value');
    // await page.waitForTimeout(500);
    // currentY += 70; // Move to next field

    // Field 2 (Dropdown)
    // await page.mouse.click(drawerX, currentY);
    // await page.waitForTimeout(1000); // Wait for dropdown
    // await page.mouse.click(drawerX, currentY + 100); // Select option
    
    // ------------------------------
    // Phase 5: Submission
    // ------------------------------
    console.log('=== Step 5: Submission ===');
    // Scroll if needed to reveal submit button
    // const viewport = page.viewportSize()!;
    // await page.mouse.move(1700, viewport.height - 150);
    // await page.mouse.wheel(0, 600);
    
    // Click Submit/Confirm
    // TODO: Update coordinates for submit button
    // await page.mouse.click(1848, 913); 
    // await page.waitForTimeout(1500); // Wait for Dialog

    // Confirm Dialog (if any)
    // await page.mouse.click(viewport.width / 2 + 90, viewport.height / 2 + 60);

    // ------------------------------
    // Phase 6: Verification
    // ------------------------------
    console.log('=== Step 6: Verification ===');
    
    // 1. Wait for API call processing
    await page.waitForTimeout(5000); 

    // 2. Verify Request Payload (Logic verification)
    // expect(requestBody).not.toBeNull();
    // expect(requestBody.someField).toBe('expectedValue');

    // 3. Verify Response Status (Success verification)
    // expect(responseStatus).toBeGreaterThanOrEqual(200);
    // expect(responseStatus).toBeLessThan(300);
  });
});
```

## Implementation Checklist

1.  **Coordinate Verification**:
    -   Use `npm run test:your-test -- --headed`
    -   Use `page.pause()` or screenshots to measure X,Y coordinates.
    -   Ensure standard `1920x1080` viewport.
2.  **API Identification**:
    -   Use browser DevTools (Network tab) to find the correct API endpoint and method.
3.  **Wait Strategy**:
    -   Always `waitForTimeout` after `goto`, clicks triggering animations, or network calls. Flutter Web UI updates are not always immediately reflected in the DOM (since there is no DOM).
4.  **Error Handling**:
    -   Ensure `try-catch` blocks inside `page.route` handlers to prevent test crashes on JSON parsing errors.
