import { test, expect } from '@playwright/test';
import { readFileSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { randomUUID } from 'node:crypto';

const env = Object.fromEntries(readFileSync(new URL('../../.env', import.meta.url), 'utf8').trim().split('\n').map(line => {
  const at=line.indexOf('='); return [line.slice(0,at),line.slice(at+1)];
}));
let original, auth;
test.beforeAll(async ({request}) => {
  const login=await request.post('/api/login',{data:{email:env.ADMIN_EMAIL,password:env.ADMIN_PASSWORD}});
  expect(login.ok()).toBeTruthy(); auth={Authorization:`Bearer ${(await login.json()).access_token}`};
  const settings=await request.get('/api/admin/settings',{headers:auth}); original=await settings.json();
});
test.afterAll(async ({request}) => {
  if(original) expect((await request.put('/api/admin/settings',{headers:auth,data:original})).ok()).toBeTruthy();
});

for(const mode of ['0','1','2']) {
  test(`mode ${mode}: correct first render, pictures, non-modal currency list and scrolling`, async ({page,request}) => {
    expect((await request.put('/api/admin/settings',{headers:auth,data:{...original,mode}})).ok()).toBeTruthy();
    const errors=[],settingsCalls=[],externalCalls=[];
    page.on('pageerror',e=>errors.push(e.message));
    page.on('request',r=>{if(r.url().includes('/api/settings/public'))settingsCalls.push(r.url()); if(/coingecko|kraken|cbr\.ru/.test(r.url()))externalCalls.push(r.url());});
    // Force a slow initial response; no default mode may be mounted underneath.
    await page.route('**/api/settings/public',async route=>{ await new Promise(r=>setTimeout(r,350)); await route.continue(); });
    await page.addInitScript(()=>{
      window.seenModes=[];
      new MutationObserver(()=>document.querySelectorAll('[data-exchange-mode]').forEach(el=>{window.seenModes.push(el.dataset.exchangeMode);})).observe(document,{childList:true,subtree:true});
    });
    await page.goto('/');
    await expect(page.locator('.loaderOverlay')).toHaveCount(0);
    await expect(page.locator(`[data-exchange-mode="${mode}"]`)).toBeVisible();
    expect(await page.evaluate(()=>[...new Set(window.seenModes)])).toEqual([mode]);
    expect(settingsCalls).toHaveLength(1); expect(externalCalls).toHaveLength(0);
    await expect.poll(()=>page.locator('img').evaluateAll(es=>es.filter(e=>e.getAttribute('loading') !== 'lazy' && (!e.complete || !e.naturalWidth)).map(e=>e.src))).toEqual([]);
    await page.locator('#give-input').fill(mode==='0'?'1':'5000');
    await expect(page.locator('#get-input')).not.toHaveValue('');
    await page.getByRole('button',{name:'Выбрать валюту (получаете)',exact:true}).click();
    await expect(page.locator('[data-currency-menu]')).toBeVisible();
    const list=page.locator('[data-currency-scroll]');
    const pageBefore=await page.locator('.appScroll').evaluate(el=>el.scrollTop);
    await list.hover(); await page.mouse.wheel(0,180);
    await expect.poll(()=>list.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
    expect(await page.locator('.appScroll').evaluate(el=>el.scrollTop)).toBe(pageBefore);
    await list.evaluate(el=>{el.scrollTop=el.scrollHeight;});
    await page.mouse.wheel(0,300); await page.waitForTimeout(100);
    expect(await page.locator('.appScroll').evaluate(el=>el.scrollTop)).toBe(pageBefore);
    const before=await page.locator('.appScroll').evaluate(el=>el.scrollTop);
    await page.mouse.move(50,600);await page.mouse.wheel(0,300);
    await expect.poll(()=>page.locator('.appScroll').evaluate(el=>el.scrollTop)).toBeGreaterThan(before);
    // The first click outside must focus the field and close the list.
    await page.locator('#telegram').click();
    await expect(page.locator('[data-currency-menu]')).toHaveCount(0);
    await expect(page.locator('#telegram')).toBeFocused();
    await page.screenshot({path:`test-results/mode-${mode}.png`,fullPage:true});
    const language=page.locator('header [data-language-menu]').first();
    await language.locator('summary').click();await language.locator('button[lang=en]').click();
    await expect(page.getByRole('button',{name:'Exchange now',exact:true})).toBeVisible();
    await expect(page.locator('main')).not.toContainText('Вносите');
    expect(errors).toEqual([]);
  });
}

test('mobile header closes from the backdrop; controls still work on reopen',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.goto('/');
  await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  const trigger=page.locator('header button[aria-expanded]');
  await trigger.click(); await expect(page.getByRole('button',{name:'Закрыть меню'})).toBeVisible();
  await page.mouse.click(5,800);
  await expect(page.getByRole('button',{name:'Закрыть меню'})).toHaveCount(0);
  await expect(page.locator('body')).not.toHaveClass(/overlay-open/);
  await trigger.click();await page.getByRole('button',{name:'Закрыть меню'}).click();
  await expect(page.locator('body')).not.toHaveClass(/overlay-open/);
});

test('reviews are prefetched once and reused during navigation',async({page})=>{
  const errors=[];let calls=0;
  page.on('pageerror',e=>errors.push(e.message));
  page.on('request',r=>{if(r.url().includes('/api/reviews/public'))calls++;});
  await page.goto('/');await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  await expect.poll(()=>calls).toBe(1);
  await page.getByRole('link',{name:'Отзывы',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Отзывы о сервисе',exact:true})).toBeVisible();
  await expect(page.locator('body')).not.toContainText('Пока отзывов нет.');
  await page.getByRole('link',{name:'Обмен',exact:true}).click();
  await page.getByRole('link',{name:'Отзывы',exact:true}).click();
  expect(calls).toBe(1);expect(errors).toEqual([]);
});

test('admin setting labels, manual rate preview and save feedback',async({page})=>{
  await page.goto('/');await page.evaluate(t=>localStorage.setItem('token',t),auth.Authorization.slice(7));
  await page.goto('/profile');await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  await page.getByRole('button',{name:'Админ',exact:true}).click();
  await page.getByRole('button',{name:'Настройки обмена',exact:true}).click();
  await expect(page.getByRole('heading',{name:'Управление обменником'})).toBeVisible();
  await page.getByRole('button',{name:'Курсы',exact:true}).click();
  await expect(page.locator('.ratePreview')).toContainText('1 ');
  // No user-visible configuration is changed by this check.
  await page.getByRole('button',{name:'Сохранить изменения',exact:true}).click();
  await expect(page.getByRole('status')).toContainText('Изменения сохранены');
  await page.screenshot({path:'test-results/admin.png',fullPage:true});
});

for (const width of [390, 1280, 1440]) {
  test(`language menu dimensions and persistent EN preference at ${width}px`, async ({page, request}) => {
    expect((await request.put('/api/admin/settings',{headers:auth,data:{...original,mode:'2'}})).ok()).toBeTruthy();
    await page.setViewportSize({width,height:900});
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto('/');await expect(page.locator('.loaderOverlay')).toHaveCount(0);
    await page.locator('#give-input').fill('5000');
    const amount=await page.locator('#get-input').inputValue();
    const picker=page.locator('header [data-language-menu]').first();
    await picker.locator('summary').click();
    const trigger=await picker.locator('summary').boundingBox();
    const menu=await picker.locator('.languageOptions').boundingBox();
    const option=await picker.locator('button[lang=en]').boundingBox();
    expect(Math.abs(trigger.width-menu.width)).toBeLessThan(1);
    expect(Math.abs(trigger.height-option.height)).toBeLessThan(1);
    await picker.locator('button[lang=en]').click();
    await expect(page.locator('html')).toHaveAttribute('lang','en');
    await expect(page.locator('#give-input')).toHaveValue('5000');
    await expect(page.locator('#get-input')).toHaveValue(amount);
    await expect(page.getByRole('button',{name:'Exchange now',exact:true})).toBeVisible();
    await expect(page.getByRole('button',{name:'Choose currency to receive',exact:true})).toBeVisible();
    expect(await page.evaluate(()=>localStorage.getItem('palma.locale'))).toBe('en');
    await page.reload();await expect(page.locator('.loaderOverlay')).toHaveCount(0);
    await expect(picker.locator('summary')).toContainText('EN');
    if(width >= 1280) {
      const panels=await page.locator('header').first().evaluate(el=>[...el.children].filter(child=>getComputedStyle(child).display !== 'none' && child.tagName === 'DIV').map(child=>child.getBoundingClientRect().toJSON()));
      for(let i=1;i<panels.length;i++) expect(panels[i].left).toBeGreaterThanOrEqual(panels[i-1].right-1);
    }
    await page.screenshot({path:`test-results/english-${width}.png`,fullPage:true});
    await page.goto('/registration');await expect(page.locator('.loaderOverlay')).toHaveCount(0);
    await expect(page.getByRole('button',{name:'Sign up',exact:true})).toBeVisible();
    await page.goto('/faq');await expect(page.locator('.loaderOverlay')).toHaveCount(0);
    await expect(page.getByRole('heading',{name:'How soon will I receive cash after payment?',level:4})).toBeVisible();
    await picker.locator('summary').click();await picker.locator('button[lang=ru]').click();
    await expect(page.getByRole('heading',{name:'Как быстро я получу наличные после оплаты?',level:4})).toBeVisible();
    await page.goto('/rules');await expect(page.locator('.loaderOverlay')).toHaveCount(0);
    await expect(page.locator('main')).toContainText('Настоящие правила регулируют порядок и условия обмена криптовалют в нашем обменном пункте.');
    expect(errors).toEqual([]);
  });
}


test('language selection also works inside the expanded mobile panel',async({page})=>{
  await page.setViewportSize({width:390,height:844});await page.goto('/');
  await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  await page.locator('header button[aria-expanded]').click();
  const panel=page.locator('[data-mobile-navigation]');
  const language=panel.locator('[data-language-menu]');
  await language.locator('summary').click();
  const trigger=await language.locator('summary').boundingBox();
  const options=await language.locator('.languageOptions').boundingBox();
  expect(Math.abs(trigger.width-options.width)).toBeLessThan(1);
  await language.locator('button[lang=en]').click();
  await expect(panel.getByRole('link',{name:'Reviews',exact:true})).toBeVisible();
  await page.mouse.click(5,800);await expect(panel).toHaveCount(0);
  await expect(page.locator('header [data-language-menu] summary')).toContainText('EN');
});

test('mobile glass menu animates from above and leaves upwards', async ({page}) => {
  await page.setViewportSize({width:390,height:844}); await page.goto('/');
  await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  await page.locator('header button[aria-expanded]').click();
  const overlay=page.locator('[data-mobile-navigation]');
  await expect(overlay).toHaveClass(/glass-menu-enter-active/);
  await expect(overlay).not.toHaveClass(/glass-menu-enter-active/);
  const panel=overlay.locator('.glassNavigationPanel');
  expect(await panel.evaluate(el=>getComputedStyle(el).transform)).toBe('none');
  await page.getByRole('button',{name:'Закрыть меню'}).click();
  await expect(overlay).toHaveClass(/glass-menu-leave-active/);
  expect(await overlay.evaluate(el=>getComputedStyle(el).pointerEvents)).toBe('none');
  await expect(overlay).toHaveCount(0);
});

test('currency glass panel reveals downwards and stays below its field while scrolling', async ({page}) => {
  await page.setViewportSize({width:390,height:740}); await page.goto('/');
  await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  await page.getByRole('button',{name:'Выбрать валюту (получаете)',exact:true}).click();
  const panel=page.locator('[data-currency-menu]');
  const overlay=panel.locator('..');
  await expect(overlay).toHaveClass(/glass-dropdown-enter-active/);
  await expect(overlay).not.toHaveClass(/glass-dropdown-enter-active/);
  const field=page.locator('label[for="get-input"]');
  const assertBelow=async()=>{
    await expect.poll(async()=>{
      const bottom=await field.evaluate(el=>el.getBoundingClientRect().bottom);
      return Math.abs(await overlay.evaluate(el=>parseFloat(el.style.top))-bottom-8);
    }).toBeLessThan(1);
  };
  await assertBelow();
  // Move the field close to the bottom: the list must shrink below it, never flip above it.
  await field.evaluate(el=>{
    const scroller=document.querySelector('.appScroll');
    scroller.scrollTop+=el.getBoundingClientRect().bottom-(window.innerHeight-64);
  });
  await assertBelow();
  const before=await overlay.evaluate(el=>parseFloat(el.style.top));
  await page.locator('.appScroll').evaluate(el=>{el.scrollTop+=120;});
  await assertBelow();
  expect(await overlay.evaluate(el=>parseFloat(el.style.top))).toBeLessThan(before);
  await page.keyboard.press('Escape');
  await expect(overlay).toHaveClass(/glass-dropdown-leave-active/);
  expect(await panel.evaluate(el=>getComputedStyle(el).pointerEvents)).toBe('none');
  await expect(panel).toHaveCount(0);
});

test('closing a currency list preserves its contents and allows immediate reopen', async ({page}) => {
  await page.goto('/');await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  const trigger=page.getByRole('button',{name:'Выбрать валюту (вносите)',exact:true});
  await trigger.click();
  const panel=page.locator('[data-currency-menu]');
  await expect(panel.locator('..')).not.toHaveClass(/glass-dropdown-enter-active/);
  const contents=await panel.innerText();
  await page.keyboard.press('Escape');
  await expect(panel.locator('..')).toHaveClass(/glass-dropdown-leave-active/);
  expect(await panel.innerText()).toBe(contents);
  await trigger.click();
  await expect(page.locator('[data-currency-menu]')).toHaveCount(1);
  await expect(panel).toBeVisible();
  // The give list covers the left column; use the uncovered right-hand field.
  await page.locator('#wallet').click();
  await expect(page.locator('#wallet')).toBeFocused();
  await expect(panel).toHaveCount(0);
});

test('glass motion respects the system reduced-motion preference', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.setViewportSize({width:390,height:844});await page.goto('/');
  await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  await page.locator('header button[aria-expanded]').click();
  const panel=page.locator('[data-mobile-navigation]');
  await expect(panel).toBeVisible();
  expect(await panel.evaluate(el=>Math.max(...getComputedStyle(el).transitionDuration.split(',').map(parseFloat)))).toBeLessThanOrEqual(.001);
  await page.getByRole('button',{name:'Закрыть меню'}).click();await expect(panel).toHaveCount(0);
  await page.getByRole('button',{name:'Выбрать валюту (получаете)',exact:true}).click();
  await expect(page.locator('[data-currency-menu]')).toBeVisible();
  await page.keyboard.press('Escape');await expect(page.locator('[data-currency-menu]')).toHaveCount(0);
});

for (const mode of ['0', '1', '2']) {
  test(`mode ${mode}: selecting currencies by click and touch actually changes both fields`, async ({browser,request}) => {
    expect((await request.put('/api/admin/settings',{headers:auth,data:{...original,mode}})).ok()).toBeTruthy();
    for (const mobile of [false,true]) {
      const context=await browser.newContext({viewport:{width:mobile?390:1440,height:900},hasTouch:mobile,isMobile:mobile});
      const page=await context.newPage();
      const errors=[];page.on('pageerror',error=>errors.push(error.message));
      try {
        await page.goto(test.info().project.use.baseURL || 'http://localhost:5173');
        await expect(page.locator('.loaderOverlay')).toHaveCount(0);
        for (const [side,index] of [['give',1],['get',mode==='0'?'last':mode==='1'?2:1]]) {
          const label=side==='give'?'Выбрать валюту (вносите)':'Выбрать валюту (получаете)';
          const trigger=page.getByRole('button',{name:label,exact:true});
          const input=page.locator(`#${side}-input`);
          const before=await input.getAttribute('placeholder');
          const iconBefore=await trigger.locator('img').getAttribute('src');
          if(mobile)await trigger.tap();else await trigger.click();
          const options=page.locator('[data-currency-menu] button');
          const option=index==='last'?options.last():options.nth(index);
          const symbol=await option.locator('span').last().innerText();
          if(mobile)await option.tap();else await option.click();
          await expect(page.locator('[data-currency-menu]')).toHaveCount(0);
          const after=await input.getAttribute('placeholder');
          const iconAfter=await trigger.locator('img').getAttribute('src');
          expect(after?.includes(symbol)||iconAfter!==iconBefore).toBeTruthy();
          expect(after!==before||iconAfter!==iconBefore).toBeTruthy();
        }
        expect(errors).toEqual([]);
      } finally {await context.close();}
    }
  });
}

test('a quick currency click during the opening animation is not lost', async ({page,request}) => {
  expect((await request.put('/api/admin/settings',{headers:auth,data:{...original,mode:'2'}})).ok()).toBeTruthy();
  await page.setViewportSize({width:390,height:844});await page.goto('/');
  await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  await page.getByRole('button',{name:'Выбрать валюту (получаете)',exact:true}).click();
  const option=page.locator('[data-currency-menu] button').nth(1);
  const box=await option.boundingBox();
  await page.mouse.click(box.x+box.width/2,box.y+box.height/2);
  await expect(page.locator('#get-input')).toHaveAttribute('placeholder','0 THB');
  await expect(page.locator('[data-currency-menu]')).toHaveCount(0);
});

for (const width of [320, 390, 932, 1440]) {
  test(`review pagination remains centred with stable width at ${width}px`, async ({page}) => {
    await page.setViewportSize({width,height:900});await page.goto('/review');
    await expect(page.locator('.loaderOverlay')).toHaveCount(0);
    const pager=page.getByRole('navigation',{name:'Навигация по отзывам'});
    await expect(pager).toBeVisible();
    const geometry=async()=>page.locator('.reviewsColumn').evaluate(column=>{
      const root=column.closest('.reviewsLayout');const pager=column.querySelector('.reviewsPagination');
      const c=column.getBoundingClientRect(),r=root.getBoundingClientRect(),p=pager.getBoundingClientRect();
      return {columnWidth:c.width,columnX:c.x,pagerWidth:p.width,pagerX:p.x,offset:(p.x+p.width/2)-(c.x+c.width/2),pageOverflow:document.querySelector('.appScroll').scrollWidth-document.querySelector('.appScroll').clientWidth};
    });
    const initial=await geometry();
    for(let i=0;i<6;i++)await pager.getByRole('button',{name:'Следующая страница',exact:true}).click();
    await expect(pager.locator('[aria-current=page]')).toHaveText('7');
    const seventh=await geometry();
    expect(Math.abs(seventh.offset)).toBeLessThan(1);
    expect(Math.abs(seventh.columnWidth-initial.columnWidth)).toBeLessThan(1);
    expect(Math.abs(seventh.columnX-initial.columnX)).toBeLessThan(1);
    expect(Math.abs(seventh.pagerX-initial.pagerX)).toBeLessThan(1);
    expect(seventh.pageOverflow).toBe(0);
    for(let i=0;i<6;i++)await pager.getByRole('button',{name:'Предыдущая страница',exact:true}).click();
    await expect(pager.locator('[aria-current=page]')).toHaveText('1');
    await expect(pager.getByRole('button',{name:'Предыдущая страница',exact:true})).toBeDisabled();
    await page.screenshot({path:`test-results/reviews-${width}.png`,fullPage:true});
  });
}

const workspace=fileURLToPath(new URL('../../',import.meta.url));
const desktopDocker='/Applications/Docker.app/Contents/Resources/bin/docker';
const dockerBinary=process.env.DOCKER_BIN || (existsSync(desktopDocker)?desktopDocker:'docker');
function backendCommand(code,args=[]){
  return execFileSync(dockerBinary,['compose','-f','docker-compose.prod.yml','exec','-T','backend','python','-c',code,...args],{cwd:workspace,encoding:'utf8'}).trim();
}
function removeTestRequest(marker){
  backendCommand('import sys; from app.db import SessionLocal; from app.models import Ticket; db=SessionLocal(); db.query(Ticket).filter(Ticket.telegram=="@local_e2e", Ticket.payout_details==sys.argv[1]).delete(); db.commit(); db.close()',[marker]);
}

for(const member of [false,true]){
  test(`${member?'member':'guest'} can submit the real form, reload the request and ${member?'confirm':'cancel'} it`, async({browser,request})=>{
    test.skip(env.TELEGRAM_ENABLED !== 'false','Live local request checks require disabled Telegram');
    test.skip(backendCommand('import os; print(os.getenv("TELEGRAM_ENABLED","false").lower())') !== 'false','Do not send real notifications during tests');
    expect((await request.put('/api/admin/settings',{headers:auth,data:{...original,mode:'2'}})).ok()).toBeTruthy();
    const marker=`LOCAL E2E SUBMISSION ${randomUUID()}`;
    const context=await browser.newContext({baseURL:test.info().project.use.baseURL,viewport:{width:1440,height:1000}});
    const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
    try{
      if(member)await page.addInitScript(token=>localStorage.setItem('token',token),auth.Authorization.slice(7));
      await page.goto('/');await expect(page.locator('.loaderOverlay')).toHaveCount(0);
      await page.locator('#give-input').fill('5000');await page.locator('#telegram').fill('@local_e2e');await page.locator('#wallet').fill(marker);
      const created=page.waitForResponse(r=>r.url().endsWith('/api/tickets')&&r.request().method()==='POST');
      const loaded=page.waitForResponse(r=>/\/api\/tickets\/[a-f0-9]{32}$/.test(r.url())&&r.request().method()==='GET');
      await page.getByRole('button',{name:'Обменять',exact:true}).click();
      expect((await created).status()).toBe(200);
      await expect(page).toHaveURL(/\/tickets\/[a-f0-9]{32}$/);
      const response=await loaded;expect(response.status()).toBe(200);
      expect(!!response.request().headers().authorization).toBe(member);
      await expect(page.locator('main')).toContainText(marker);
      const reloaded=page.waitForResponse(r=>/\/api\/tickets\/[a-f0-9]{32}$/.test(r.url())&&r.request().method()==='GET');
      await page.reload();expect((await reloaded).status()).toBe(200);
      await expect(page.locator('main')).toContainText(marker);
      if(member){
        const file=page.locator('input[type=file]').first();await expect(file).toBeEnabled();
        await file.setInputFiles({name:'local-receipt.png',mimeType:'image/png',buffer:Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScLbtAAAAABJRU5ErkJggg==','base64')});
      }
      const action=member?'confirm':'cancel';
      const changed=page.waitForResponse(r=>r.url().endsWith(`/${action}`)&&r.request().method()==='PATCH');
      await page.getByRole('button',{name:member?'Подтвердить перевод':'Отменить сделку',exact:true}).click();
      const update=await changed;expect(update.status()).toBe(200);
      expect(!!update.request().headers().authorization).toBe(member);
      if(member)expect(update.request().headers()['content-type']).toContain('multipart/form-data; boundary=');
      await expect(page.locator('main')).toContainText(member?'Ожидайте подтверждения':'Сделка отменена');
      expect(errors).toEqual([]);
    }finally{await context.close();removeTestRequest(marker);}
  });
}

test('a failed quote shows its message and the exchange form can retry',async({page,request})=>{
  expect((await request.put('/api/admin/settings',{headers:auth,data:{...original,mode:'2'}})).ok()).toBeTruthy();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('**/api/quote',route=>route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({detail:'Курс направления временно недоступен'})}));
  await page.goto('/');await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  await page.locator('#give-input').fill('5000');await page.locator('#telegram').fill('@local_e2e');await page.locator('#wallet').fill('LOCAL MOCKED QUOTE ERROR');
  const button=page.getByRole('button',{name:'Обменять',exact:true});await button.click();
  await expect(page.locator('main')).toContainText('Курс направления временно недоступен');
  await expect(button).toBeEnabled();expect(errors).toEqual([]);
});

test('glass samples the page backdrop throughout its opening transition',async({page})=>{
  await page.goto('/');await expect(page.locator('.loaderOverlay')).toHaveCount(0);
  await page.getByRole('button',{name:'Выбрать валюту (получаете)',exact:true}).click();
  const anchor=page.locator('[data-currency-popover]');
  await expect(anchor).toHaveClass(/glass-dropdown-enter-active/);
  const samples=await anchor.evaluate(async root=>{
    const data=[];for(let i=0;i<8;i++){
      const layer=getComputedStyle(root);const surface=getComputedStyle(root.querySelector('[data-currency-menu]'));
      data.push({opacity:layer.opacity,willChange:layer.willChange,blur:surface.backdropFilter||surface.webkitBackdropFilter});
      await new Promise(resolve=>requestAnimationFrame(resolve));
    }return data;
  });
  for(const sample of samples){expect(sample.opacity).toBe('1');expect(sample.willChange).not.toContain('opacity');expect(sample.blur).toContain('blur(26px)');}
  await expect(anchor).not.toHaveClass(/glass-dropdown-enter-active/);
});
