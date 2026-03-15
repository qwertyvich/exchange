<!-- src/pages/ProfilePage.vue -->
<template>
  <div class="flex flex-col lg:gap-12 gap-6 lg:py-24 py-8 max-w-[1362px] container basis-full text-white">
    <div class="flex flex-col gap-2">
      <h2 class="md:text-5xl text-[28px] font-medium leading-[120%] max-md:text-center">
        Личный кабинет
      </h2>
    </div>

    <div class="flex max-lg:flex-col gap-6">
      <!-- LEFT SIDEBAR -->
      <aside
        class="flex flex-col gap-3 w-full lg:w-109 lg:bg-bg-tertiary lg:border border-border-secondary rounded-[28px] p-3 shrink-0 h-fit lg:sticky lg:top-3"
      >
        <div class="flex flex-col gap-2">
          <!-- Данные -->
          <button
            type="button"
            :data-state="activeTab === 'data' ? 'active' : 'inactive'"
            @click="activeTab = 'data'"
            class="inline-flex w-full items-center whitespace-nowrap text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary data-[state=active]:bg-bg-secondary-active lg:gap-2 gap-1.5 lg:p-6 p-4.5 lg:rounded-[28px] rounded-[22px] justify-start"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                 class="lucide lucide-circle-user-round lg:size-7 size-6" aria-hidden="true">
              <path d="M18 20a6 6 0 0 0-12 0"></path>
              <circle cx="12" cy="10" r="4"></circle>
              <circle cx="12" cy="12" r="10"></circle>
            </svg>
            <p class="md:text-xl text-base font-medium leading-[140%] lg:px-2 px-1.5 line-clamp-1 break-all">
              Данные
            </p>
          </button>

          <!-- История -->
          <button
            type="button"
            :data-state="activeTab === 'history' ? 'active' : 'inactive'"
            @click="activeTab = 'history'"
            class="inline-flex w-full items-center whitespace-nowrap text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary data-[state=active]:bg-bg-secondary-active lg:gap-2 gap-1.5 lg:p-6 p-4.5 lg:rounded-[28px] rounded-[22px] justify-start"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                 class="lucide lucide-clock3 lucide-clock-3 lg:size-7 size-6" aria-hidden="true">
              <path d="M12 6v6h4"></path>
              <circle cx="12" cy="12" r="10"></circle>
            </svg>
            <p class="md:text-xl text-base font-medium leading-[140%] lg:px-2 px-1.5 line-clamp-1 break-all">
              История обменов
            </p>
          </button>
          
        </div>
        <button
            v-if="isSuperuser"
            type="button"
            :data-state="activeTab === 'admin' ? 'active' : 'inactive'"
            @click="activeTab = 'admin'"
            class="inline-flex w-full items-center whitespace-nowrap text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary data-[state=active]:bg-bg-secondary-active lg:gap-2 gap-1.5 lg:p-6 p-4.5 lg:rounded-[28px] rounded-[22px] justify-start"
          >
            <!-- иконка “шестерёнка” -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="lucide lucide-settings lg:size-7 size-6" aria-hidden="true">
              <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1.11 1.79l-.16.08a2 2 0 0 1-2.18-.33l-.13-.12a2 2 0 0 0-2.83 0l-.31.31a2 2 0 0 0 0 2.83l.12.13a2 2 0 0 1 .33 2.18l-.08.16A2 2 0 0 1 2 13.78V14.22a2 2 0 0 0 2 2h.18a2 2 0 0 1 1.79 1.11l.08.16a2 2 0 0 1-.33 2.18l-.12.13a2 2 0 0 0 0 2.83l.31.31a2 2 0 0 0 2.83 0l.13-.12a2 2 0 0 1 2.18-.33l.16.08a2 2 0 0 1 1.11 1.79V22a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1.11-1.79l.16-.08a2 2 0 0 1 2.18.33l.13.12a2 2 0 0 0 2.83 0l.31-.31a2 2 0 0 0 0-2.83l-.12-.13a2 2 0 0 1-.33-2.18l.08-.16A2 2 0 0 1 22 14.22v-.44a2 2 0 0 0-2-2h-.18a2 2 0 0 1-1.79-1.11l-.08-.16a2 2 0 0 1 .33-2.18l.12-.13a2 2 0 0 0 0-2.83l-.31-.31a2 2 0 0 0-2.83 0l-.13.12a2 2 0 0 1-2.18.33l-.16-.08A2 2 0 0 1 13.78 4.18V4a2 2 0 0 0-2-2z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>

            <p class="md:text-xl text-base font-medium leading-[140%] lg:px-2 px-1.5 line-clamp-1 break-all">
              Админ
            </p>
          </button>

        <!-- Выйти (1:1) -->
        <button
          data-slot="button"
          class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none text-text-primary border border-border-primary hover:border-border-secondary data-[state=active]:bg-bg-active rounded-[18px] py-4"
          type="button"
          @click="logout"
        >
          <p class="md:text-base text-sm font-medium leading-[150%] px-1 text-text-tertiary">
            Выйти
          </p>
        </button>
      </aside>

      <!-- RIGHT CONTENT -->
      <div class="basis-full min-w-0">
        <!-- TAB: DATA -->
        <form
          v-if="activeTab === 'data'"
          class="flex flex-col gap-6 md:p-12 p-6 basis-full bg-bg-tertiary border border-border-secondary md:rounded-[28px] rounded-[22px] h-fit"
          @submit.prevent
        >
          <div class="flex flex-col gap-2">
            <!-- Имя профиля -->
            <div data-slot="form-item" class="grid gap-2">
              <div class="relative w-full">
                <input
                  v-model.trim="formName"
                  maxlength="10"
                  data-slot="form-control"
                  id="pf_name"
                  placeholder=" "
                  class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none"
                >
                <label
                  for="pf_name"
                  class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
                >
                  Имя профиля
                </label>
              </div>
            </div>

            <!-- Email readonly -->
            <div class="relative w-full">
              <input
                data-slot="input"
                id="pf_email"
                placeholder=" "
                class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none"
                readonly
                :value="me?.email || ''"
              >
              <label
                for="pf_email"
                class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
              >
                E-mail
              </label>
            </div>
          </div>
          <div data-slot="form-item" class="grid gap-2">
  <div class="relative w-full">
    <input
      v-model="currentPassword"
      data-slot="form-control"
      id="pf_current_password"
      placeholder=" "
      class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none"
      :type="showCurrentPass ? 'text' : 'password'"
      autocomplete="current-password"
    >
    <label
      for="pf_current_password"
      class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
    >
      Текущий пароль
    </label>

    <button
      type="button"
      class="absolute md:right-8 right-6 top-1/2 -translate-y-1/2 cursor-pointer text-icon-hover transition"
      @click="showCurrentPass = !showCurrentPass"
      aria-label="Показать/скрыть пароль"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
           fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
           class="lucide lucide-eye md:size-8 size-6" aria-hidden="true">
        <path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path>
        <circle cx="12" cy="12" r="3"></circle>
      </svg>
    </button>
  </div>
</div>
          <!-- Пароль -->
           
          <div class="flex flex-col gap-2">
            <div data-slot="form-item" class="grid gap-2">
              <div class="relative w-full">
                <input
                  v-model="newPassword"
                  data-slot="form-control"
                  id="pf_new_password"
                  placeholder=" "
                  class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none"
                  :type="showNewPass ? 'text' : 'password'"
                >
                <label
                  for="pf_new_password"
                  class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
                >
                  Новый пароль
                </label>

                <button
                  type="button"
                  class="absolute md:right-8 right-6 top-1/2 -translate-y-1/2 cursor-pointer text-icon-hover transition"
                  @click="showNewPass = !showNewPass"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                       fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                       class="lucide lucide-eye md:size-8 size-6" aria-hidden="true">
                    <path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                </button>
              </div>
            </div>

            <div data-slot="form-item" class="grid gap-2">
              <div class="relative w-full">
                <input
                  v-model="confirmPassword"
                  data-slot="form-control"
                  id="pf_confirm_password"
                  placeholder=" "
                  class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary aria-invalid:border-danger flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none"
                  :type="showConfirmPass ? 'text' : 'password'"
                >
                <label
                  for="pf_confirm_password"
                  class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
                >
                  Подтвердите пароль
                </label>

                <button
                  type="button"
                  class="absolute md:right-8 right-6 top-1/2 -translate-y-1/2 cursor-pointer text-icon-hover transition"
                  @click="showConfirmPass = !showConfirmPass"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                       fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                       class="lucide lucide-eye md:size-8 size-6" aria-hidden="true">
                    <path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <p v-if="saveError" class="text-danger md:text-base text-sm font-medium">{{ saveError }}</p>

          <div class="flex gap-3 flex-wrap">
            <button
              data-slot="button"
              class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none bg-brand hover:bg-brand-hover text-text-primary md:p-6 p-4.5 md:w-fit max-md:rounded-[22px]"
              type="button"
              :disabled="savingName || !canSaveName"
              @click="saveName"
            >
              <p class="md:text-xl text-base font-medium leading-[140%] px-1">
                {{ savingName ? "Сохранение..." : "Сохранить имя" }}
              </p>
            </button>

            <button
              data-slot="button"
              class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary border border-border-primary md:p-6 p-4.5 md:w-fit max-md:rounded-[22px]"
              type="button"
              :disabled="savingPass || !canSavePassword"
              @click="savePassword"
            >
              <p class="md:text-xl text-base font-medium leading-[140%] px-1">
                {{ savingPass ? "Сохранение..." : "Сохранить пароль" }}
              </p>
            </button>
          </div>
        </form>
        
        <!-- TAB: ADMIN -->
        <div
          v-else-if="activeTab === 'admin' && isSuperuser"
          class="flex flex-col gap-6 md:p-12 p-6 basis-full bg-bg-tertiary border border-border-secondary md:rounded-[28px] rounded-[22px] h-fit"
        >
          <!-- Подвкладки админки -->
          <div class="flex gap-2 flex-wrap">
            <button
              type="button"
              :data-state="adminTab === 'users' ? 'active' : 'inactive'"
              @click="adminTab = 'users'"
              class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[18px] py-4 px-5 border border-border-primary bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary data-[state=active]:bg-bg-secondary-active"
            >
              Пользователи
            </button>

            <button
              type="button"
              :data-state="adminTab === 'wallets' ? 'active' : 'inactive'"
              @click="adminTab = 'wallets'"
              class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[18px] py-4 px-5 border border-border-primary bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary data-[state=active]:bg-bg-secondary-active"
            >
              Кошельки
            </button>

            <button
            type="button"
            :data-state="adminTab === 'mode' ? 'active' : 'inactive'"
            @click="adminTab = 'mode'"
            class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[18px] py-4 px-5 border border-border-primary bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary data-[state=active]:bg-bg-secondary-active"
          >
            Режим
          </button>
          </div>

          <!-- Контент под вкладки -->
          <div v-if="adminTab === 'users'" class="flex flex-col gap-4">
          <div class="flex items-center justify-between gap-3 flex-wrap">
            <h3 class="md:text-2xl text-xl font-medium leading-[130%]">Пользователи</h3>

            <button
              type="button"
              class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[18px] py-3 px-4 border border-border-primary bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary"
              :disabled="loadingAdminUsers"
              @click="loadAdminUsers"
            >
              Обновить
            </button>
          </div>

          <div v-if="loadingAdminUsers" class="text-text-secondary md:text-base text-sm font-light leading-[150%]">
            Загрузка пользователей...
          </div>

          <div v-else-if="adminUsers.length === 0" class="text-text-secondary md:text-base text-sm font-light leading-[150%]">
            Пользователей нет.
          </div>

          <div v-else class="w-full overflow-x-auto">
        <!-- min-w чтобы таблица не ужималась и текст не лез на разделители -->
        <div class="min-w-[1100px]">
          <table class="w-full border-collapse">
            <thead class="text-text-tertiary">
              <tr class="text-left border-b border-border-secondary">
                <th class="px-4 py-3 font-light whitespace-nowrap">Имя</th>
                <th class="px-4 py-3 font-light whitespace-nowrap">E-mail</th>
                <th class="px-4 py-3 font-light whitespace-nowrap">Роль</th>
                <th class="px-4 py-3 font-light whitespace-nowrap">Super</th>
                <th class="px-4 py-3 font-light whitespace-nowrap">Регистрация</th>
                <th class="px-4 py-3 font-light whitespace-nowrap">Последний вход</th>
                <th class="px-4 py-3 font-light whitespace-nowrap text-right"> </th>
              </tr>
            </thead>

            <tbody>
              <template v-for="u in adminUsers" :key="u.id">
                <!-- строка пользователя -->
                <tr class="border-b border-border-secondary">
                  <td class="px-4 py-4 align-top whitespace-nowrap " style="border-bottom: 1px solid grey;">
                    <span class="font-medium">
                      {{ u.name }}
                    </span>
                  </td>

                  <!-- email: не ломаем строку, даём обрезку -->
                  <td class="px-4 py-4 align-top whitespace-nowrap" style="border-bottom: 1px solid grey;">
                    <span class="font-light text-text-secondary inline-block max-w-[320px] overflow-hidden text-ellipsis">
                      {{ u.email }}
                    </span>
                  </td>

                  <td class="px-4 py-4 align-top whitespace-nowrap" style="border-bottom: 1px solid grey;" >
                    <span class="font-light text-text-secondary">
                      {{ u.role }}
                    </span>
                  </td>

                  <td class="px-4 py-4 align-top whitespace-nowrap"  style="border-bottom: 1px solid grey;">
                    <span class="font-light" :class="u.is_superuser ? 'text-white' : 'text-text-secondary'">
                      {{ u.is_superuser ? "Да" : "Нет" }}
                    </span>
                  </td>

                  <td class="px-4 py-4 align-top whitespace-nowrap" style="border-bottom: 1px solid grey;">
                    <span class="font-light text-text-secondary">
                      {{ u.created_at ? formatDate(u.created_at) : "-" }}
                    </span>
                  </td>

                  <td class="px-4 py-4 align-top whitespace-nowrap" style="border-bottom: 1px solid grey;">
                    <span class="font-light text-text-secondary">
                      {{ u.last_login_at ? formatDate(u.last_login_at) : "-" }}
                    </span>
                  </td>

                  <td class="px-4 py-4 align-top whitespace-nowrap text-right" style="border-bottom: 1px solid grey;">
                    <button
                      type="button"
                      class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[14px] py-2 px-3 border border-border-primary bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary"
                      @click="toggleUserTickets(u.id)"
                    >
                      {{ expandedUserId === u.id ? "Скрыть обмены" : "Показать обмены" }}
                    </button>
                  </td>
                </tr>

                <!-- раскрывашка -->
                <tr v-if="expandedUserId === u.id">
                  <td colspan="7" class="pt-4 pb-5">
                    <div class="bg-bg-tertiary border border-border-secondary rounded-[22px] p-4">
                      <div
                        v-if="loadingUserTickets"
                        class="text-text-secondary md:text-base text-sm font-light leading-[150%]"
                      >
                        Загрузка обменов...
                      </div>

                      <div
                        v-else-if="userTickets.length === 0"
                        class="text-text-secondary md:text-base text-sm font-light leading-[150%]"
                      >
                        У пользователя нет обменов.
                      </div>

                      <div v-else class="max-w-full overflow-hidden">
                        <!-- скролл только внутри, а не всей страницы -->
                        <div class="w-full overflow-x-auto">
                          <!-- ширина таблицы больше контейнера -> появляется горизонтальный скролл -->
                          <div class="min-w-[1100px]">
                            <table class="w-full border-collapse">
                            <thead class="text-text-tertiary">
                              <tr class="text-left border-b border-border-secondary">
                                <th class="px-3 py-3 font-light whitespace-nowrap">ID</th>
                                <th class="px-3 py-3 font-light whitespace-nowrap">Статус</th>
                                <th class="px-3 py-3 font-light whitespace-nowrap">Дата</th>
                                <th class="px-3 py-3 font-light whitespace-nowrap">Вносит</th>
                                <th class="px-3 py-3 font-light whitespace-nowrap">Получает</th>
                              </tr>
                            </thead>

                            <tbody>
                              <tr
                                v-for="t in userTickets"
                                :key="t.id"
                                class="border-b border-border-secondary"
                              >
                                <td class="px-3 py-3 whitespace-nowrap">
                                  <a :href="`/tickets/${t.id}`" class="hover:underline font-medium">
                                    {{ shortTicketId(t.id) }}
                                  </a>
                                </td>

                                <td class="px-3 py-3 whitespace-nowrap">
                                  <span class="font-light text-text-secondary">
                                    {{ statusLabel(t.status) }}
                                  </span>
                                </td>

                                <td class="px-3 py-3 whitespace-nowrap">
                                  <span class="font-light text-text-secondary">
                                    {{ formatDate(t.created_at) }}
                                  </span>
                                </td>

                                <td class="px-3 py-3 whitespace-nowrap">
                                  <span class="font-light tabular-nums text-text-secondary">
                                    {{ t.give_amount }} {{ t.give_symbol }}
                                  </span>
                                </td>

                                <td class="px-3 py-3 whitespace-nowrap">
                                  <span class="font-light tabular-nums text-text-secondary">
                                    {{ t.get_amount }} {{ t.get_symbol }}
                                  </span>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                          </div>
                        </div>
                      </div>

                    </div>
                  </td>
                </tr> 
              </template>
            </tbody>
          </table>
        </div>
      </div>
        </div>
        <div v-else-if="adminTab === 'mode'" class="flex flex-col gap-6">
  <div class="flex items-center justify-between gap-3 flex-wrap">
    <h3 class="md:text-2xl text-xl font-medium leading-[130%]">Режим работы</h3>

    <button
      type="button"
      class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[18px] py-3 px-4 bg-brand hover:bg-brand-hover text-text-primary"
      :disabled="settingsSaving || settingsLoading"
      @click="saveAdminSettings"
    >
      {{ settingsSaving ? "Сохранение..." : "Сохранить" }}
    </button>
  </div>

  <div v-if="settingsLoading" class="text-text-secondary md:text-base text-sm font-light leading-[150%]">
    Загрузка settings.json...
  </div>

  <p v-else-if="settingsError" class="text-danger md:text-base text-sm font-medium">
    {{ settingsError }}
  </p>

  <div v-else class="bg-bg-primary border border-border-secondary rounded-[22px] p-5 flex flex-col gap-5">
    <div>
      <h4 class="md:text-xl text-base font-medium leading-[140%]">Выберите режим</h4>
      <p class="text-text-secondary md:text-base text-sm font-light leading-[150%] mt-1">
        Значение сохраняется в settings.json в поле mode.
      </p>
    </div>

    <label class="flex items-start gap-3 cursor-pointer">
      <input
        v-model="settingsForm.mode"
        type="radio"
        value="0"
        class="mt-1 size-4 shrink-0"
      >
      <div class="flex flex-col gap-1">
        <span class="md:text-lg text-base font-medium leading-[140%]">Крипта -> Фиат, крипта</span>
        <span class="text-text-secondary md:text-base text-sm font-light leading-[150%]">
          mode = "0"
        </span>
      </div>
    </label>

    <label class="flex items-start gap-3 cursor-pointer">
      <input
        v-model="settingsForm.mode"
        type="radio"
        value="1"
        class="mt-1 size-4 shrink-0"
      >
      <div class="flex flex-col gap-1">
        <span class="md:text-lg text-base font-medium leading-[140%]">Фиат, крипта -> Фиат, крипта</span>
        <span class="text-text-secondary md:text-base text-sm font-light leading-[150%]">
          mode = "1"
        </span>
      </div>
    </label>

    <label class="flex items-start gap-3 cursor-pointer">
      <input
        v-model="settingsForm.mode"
        type="radio"
        value="2"
        class="mt-1 size-4 shrink-0"
      >
      <div class="flex flex-col gap-1">
        <span class="md:text-lg text-base font-medium leading-[140%]">Фиат,usdt -> Фиат</span>
        <span class="text-text-secondary md:text-base text-sm font-light leading-[150%]">
          mode = "2"
        </span>
      </div>
    </label>
  </div>
</div>
          <div v-else-if="adminTab === 'wallets'" class="flex flex-col gap-6">
  <div class="flex items-center justify-between gap-3 flex-wrap">
    <h3 class="md:text-2xl text-xl font-medium leading-[130%]">Настройки</h3>

    <div class="flex gap-2">
      <button
        type="button"
        class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[18px] py-3 px-4 border border-border-primary bg-bg-secondary hover:bg-bg-secondary-hover text-text-primary"
        :disabled="settingsLoading"
        @click="loadAdminSettings"
      >
        Обновить
      </button>

      <button
        type="button"
        class="inline-flex items-center justify-center gap-1.5 whitespace-nowrap rounded-[18px] py-3 px-4 bg-brand hover:bg-brand-hover text-text-primary"
        :disabled="settingsSaving || settingsLoading"
        @click="saveAdminSettings"
      >
        {{ settingsSaving ? "Сохранение..." : "Сохранить" }}
      </button>
    </div>
  </div>

  <div v-if="settingsLoading" class="text-text-secondary md:text-base text-sm font-light leading-[150%]">
    Загрузка settings.json...
  </div>

  <p v-else-if="settingsError" class="text-danger md:text-base text-sm font-medium">
    {{ settingsError }}
  </p>

  <div v-else class="flex flex-col gap-6">
    <!-- percent -->
     
    <!-- percent + limits -->
<div class="bg-bg-primary border border-border-secondary rounded-[22px] p-5">
  <h4 class="md:text-xl text-base font-medium leading-[140%]">Комиссия и лимиты ещё и баннер тут</h4>
  <p class="text-text-secondary md:text-base text-sm font-light leading-[150%] mt-1">
    percent — комиссия сервиса (%). Лимиты — в USD.
  </p>

  <div class="mt-4 grid md:grid-cols-2 grid-cols-1 gap-3">
    <!-- percent -->
     <div class="relative w-full md:col-span-2">
      <input
        v-model="settingsForm.banner"
        placeholder=" "
        class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none"
      >
      <label
        class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
      >
        banner
      </label>
    </div>
    <div class="relative w-full">
      <input
        v-model="settingsForm.percent"
        placeholder=" "
        class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none"
      >
      <label
        class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
      >
        percent
      </label>
    </div>

    <!-- giveMin -->
    <div class="relative w-full">
      <input v-model="settingsForm.giveMin" placeholder=" "
        class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
      <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
        giveMin (USD)
      </label>
    </div>

    <!-- giveMax -->
    <div class="relative w-full">
      <input v-model="settingsForm.giveMax" placeholder=" "
        class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
      <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
        giveMax (USD)
      </label>
    </div>

    <!-- getMin -->
    <div class="relative w-full">
      <input v-model="settingsForm.getMin" placeholder=" "
        class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
      <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
        getMin (USD)
      </label>
    </div>

    <!-- getMax -->
    <div class="relative w-full">
      <input v-model="settingsForm.getMax" placeholder=" "
        class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
      <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
        getMax (USD)
      </label>
    </div>
  </div>
</div>

    <!-- info -->
    <div class="bg-bg-primary border border-border-secondary rounded-[22px] p-5">
      <h4 class="md:text-xl text-base font-medium leading-[140%]">Контакты (info)</h4>
      <p class="text-text-secondary md:text-base text-sm font-light leading-[150%] mt-1">
        Эти значения будут использоваться на странице контактов.
      </p>

      <div class="mt-4 grid md:grid-cols-2 grid-cols-1 gap-3">
        <div class="relative w-full">
          <input v-model="settingsForm.info.Telegram_oper" placeholder=" "
                 class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
          <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
            Telegram_oper
          </label>
        </div>

        <div class="relative w-full">
          <input v-model="settingsForm.info.Telegram_chanel" placeholder=" "
                 class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
          <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
            Telegram_chanel
          </label>
        </div>

        <div class="relative w-full">
          <input v-model="settingsForm.info.Session_id" placeholder=" "
                 class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
          <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
            Session_id
          </label>
        </div>

        <div class="relative w-full">
          <input v-model="settingsForm.info.Tox" placeholder=" "
                 class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
          <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
            Tox
          </label>
        </div>
      </div>
    </div>
    <!-- bot -->
<div class="bg-bg-primary border border-border-secondary rounded-[22px] p-5">
  <h4 class="md:text-xl text-base font-medium leading-[140%]">Бот (bot)</h4>
  <p class="text-text-secondary md:text-base text-sm font-light leading-[150%] mt-1">
    Настройки Telegram-бота. Осторожно: токен — чувствительные данные.
  </p>

  <div class="mt-4 grid md:grid-cols-2 grid-cols-1 gap-3">
    <!-- API_TOKEN -->
    <div class="relative w-full md:col-span-2">
      <input
        v-model="settingsForm.bot.API_TOKEN"
        placeholder=" "
        class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none"
      >
      <label
        class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
      >
        API_TOKEN
      </label>
    </div>

    <!-- CHAT_ID -->
    <div class="relative w-full">
      <input
        v-model="settingsForm.bot.CHAT_ID"
        placeholder=" "
        class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none"
      >
      <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
        CHAT_ID
      </label>
    </div>

    <!-- MESS_CHAT -->
    <div class="relative w-full">
      <input
        v-model="settingsForm.bot.MESS_CHAT"
        placeholder=" "
        class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none"
      >
      <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
        MESS_CHAT
      </label>
    </div>

    <!-- domain -->
    <div class="relative w-full md:col-span-2">
      <input
        v-model="settingsForm.bot.domain"
        placeholder=" "
        class="md:text-xl text-base font-light leading-[140%] peer bg-bg-tertiary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none"
      >
      <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">
        domain
      </label>
    </div>
  </div>
</div>
    <!-- deposit_wallets -->
    <div class="bg-bg-primary border border-border-secondary rounded-[22px] p-5">
      <h4 class="md:text-xl text-base font-medium leading-[140%]">Кошельки (deposit_wallets)</h4>
      <p class="text-text-secondary md:text-base text-sm font-light leading-[150%] mt-1">
        Адреса для приёма средств по currency_backend_id.
      </p>

      <div class="mt-4 grid gap-3">
        <div
          v-for="(obj, key) in settingsForm.deposit_wallets"
          :key="key"
          class="bg-bg-tertiary border border-border-secondary rounded-[22px] p-4"
        >
          <div class="flex items-center justify-between gap-3 mb-2">
          <div class="md:text-xl text-base font-medium leading-[140%]">
            {{ obj?.name || `ID: ${key}` }}
          </div>
          <div class="text-text-tertiary text-sm font-light">#{{ key }}</div>
        </div>


          <div class="relative w-full">
            <input
              v-model="settingsForm.deposit_wallets[key].address"
              placeholder=" "
              class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none"
            >
            <label
              class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
            >
              address
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- fiat_in -->
    <div class="bg-bg-primary border border-border-secondary rounded-[22px] p-5">
      <h4 class="md:text-xl text-base font-medium leading-[140%]">Карты (fiat_in)</h4>
      <p class="text-text-secondary md:text-base text-sm font-light leading-[150%] mt-1">
        Реквизиты для приёма RUB + лимиты и курс.
      </p>

      <div class="mt-4 grid gap-3">
        <div
          v-for="(obj, key) in settingsForm.fiat_in"
          :key="key"
          class="bg-bg-tertiary border border-border-secondary rounded-[22px] p-4"
        >
          <div class="text-text-tertiary text-sm font-light mb-3">ID: {{ key }}</div>

          <div class="grid md:grid-cols-2 grid-cols-1 gap-3">
            <div class="relative w-full">
              <input v-model="settingsForm.fiat_in[key].card_id" placeholder=" "
                     class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
              <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">card_id</label>
            </div>

            <div class="relative w-full">
              <input v-model="settingsForm.fiat_in[key].bank_name" placeholder=" "
                     class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
              <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">bank_name</label>
            </div>

            <div class="relative w-full">
              <input v-model="settingsForm.fiat_in[key].FIO" placeholder=" "
                     class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
              <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">FIO</label>
            </div>

            <div class="relative w-full">
              <input v-model="settingsForm.fiat_in[key].rate" placeholder=" "
                     class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
              <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">rate</label>
            </div>

            <div class="relative w-full">
              <input v-model="settingsForm.fiat_in[key].from" placeholder=" "
                     class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
              <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">from</label>
            </div>

            <div class="relative w-full">
              <input v-model="settingsForm.fiat_in[key].to" placeholder=" "
                     class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
              <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">to</label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- fiat_out -->
    <div class="bg-bg-primary border border-border-secondary rounded-[22px] p-5">
      <h4 class="md:text-xl text-base font-medium leading-[140%]">Fiat out (fiat_out)</h4>
      <p class="text-text-secondary md:text-base text-sm font-light leading-[150%] mt-1">
       курсы валют к usd
      </p>

      <div class="mt-4 grid gap-3">
        <div
          v-for="(obj, key) in settingsForm.fiat_out"
          :key="key"
          class="bg-bg-tertiary border border-border-secondary rounded-[22px] p-4"
        >
          <div class="text-text-tertiary text-sm font-light mb-2">ID: {{ key }}</div>

          <div class="relative w-full max-w-[260px]">
            <input v-model="settingsForm.fiat_out[key].rate" placeholder=" "
                   class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active flex w-full md:rounded-[28px] rounded-[22px] border md:px-6 md:pt-10 md:pb-4 px-5 pt-7 pb-3 transition-all duration-150 outline-none">
            <label class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-6 left-5 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125">rate</label>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
        </div>


        <!-- TAB: HISTORY -->
        <div v-else class="flex flex-col gap-2 basis-full h-fit">
          <div v-if="loadingTickets" class="text-text-secondary md:text-base text-sm font-light leading-[150%]">
            
          </div>

          <div v-else-if="tickets.length === 0" class="text-text-secondary md:text-base text-sm font-light leading-[150%]">
            Пока нет обменов.
          </div>

          <div v-else class="flex flex-col gap-2">
            <div
              v-for="t in tickets"
              :key="t.id"
              class="flex flex-col xl:gap-8 gap-6 xl:p-8 p-6 bg-bg-tertiary border border-border-secondary xl:rounded-[28px] rounded-[22px]"
            >
              <!-- header line -->
              <div class="flex max-md:flex-col md:gap-8 gap-6">
                <div class="flex flex-col md:gap-2 gap-1.5 basis-full">
                  <span class="md:text-base text-sm font-light leading-[150%]">
                    {{ formatDate(t.created_at) }}
                  </span>

                  <!-- clickable short id -->
                  <a
                    class="md:text-[32px] text-2xl font-medium leading-[120%] hover:underline break-all"
                    :href="`/tickets/${t.id}`"
                  >
                    {{ shortTicketId(t.id) }}
                  </a>
                </div>

                <div class="flex flex-col md:gap-2 gap-1.5 basis-full md:text-right">
                  <!-- timer -->
                  <p
                    v-if="showTimer(t.status)"
                    class="md:text-xl text-base font-medium leading-[140%] text-danger"
                    :class="ticketTimer(t) === 'Истекло время на отправку средств' ? '' : 'tabular-nums'"
                  >
                    {{ ticketTimer(t) }}
                  </p>

                  <!-- status -->
                  <p
                      v-if="!(t.status === 'new' && ticketTimer(t) === EXPIRED_TEXT)"
                      class="md:text-xl text-base font-medium leading-[140%] text-text-secondary"
                    >
                      {{ statusLabel(t.status) }}
                    </p>
                </div>
              </div>

              <!-- amounts block -->
              <div class="flex max-md:flex-col items-center md:gap-6 gap-2 relative w-full">
                <!-- give -->
                <div class="flex gap-2 items-center bg-bg-tertiary border border-border-secondary backdrop-blur-xl md:p-6 p-6 md:rounded-[28px] rounded-[22px] md:basis-full w-full">
                  <div class="flex md:gap-4 gap-3 items-center grow">
                    <img
                      v-if="iconByBackendId(t.give_currency_backend_id)"
                      :alt="t.give_symbol"
                      loading="lazy"
                      width="36"
                      height="36"
                      decoding="async"
                      class="md:size-9 size-8 object-contain"
                      :src="iconByBackendId(t.give_currency_backend_id)"
                      style="color: transparent;"
                    >
                    <h4 class="md:text-2xl text-xl font-medium leading-[130%] tabular-nums">
                      {{ t.give_amount }}
                    </h4>
                  </div>
                  <span class="md:text-base text-sm font-light leading-[150%] text-text-secondary">
                    {{ t.give_symbol }}
                  </span>
                </div>

                <!-- arrow -->
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                     stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                     class="lucide lucide-arrow-right md:size-7 size-12 max-md:border border-border-secondary backdrop-blur-xl shrink-0 max-md:absolute left-1/2 top-1/2 max-md:-translate-x-1/2 max-md:-translate-y-1/2 max-md:rotate-90 max-md:bg-bg-tertiary rounded-[14px] max-md:p-3 z-10"
                     aria-hidden="true">
                  <path d="M5 12h14"></path>
                  <path d="m12 5 7 7-7 7"></path>
                </svg>

                <!-- get -->
                <div class="flex gap-2 items-center bg-bg-tertiary border border-border-secondary backdrop-blur-xl md:p-6 p-6 md:rounded-[28px] rounded-[22px] md:basis-full w-full">
                  <div class="flex md:gap-4 gap-3 items-center grow">
                    <img
                      v-if="iconByBackendId(t.get_currency_backend_id)"
                      :alt="t.get_symbol"
                      loading="lazy"
                      width="36"
                      height="36"
                      decoding="async"
                      class="md:size-9 size-8 object-contain"
                      :src="iconByBackendId(t.get_currency_backend_id)"
                      style="color: transparent;"
                    >
                    <h4 class="md:text-2xl text-xl font-medium leading-[130%] tabular-nums">
                      {{ t.get_amount }}
                    </h4>
                  </div>
                  <span class="md:text-base text-sm font-light leading-[150%] text-text-secondary">
                    {{ t.get_symbol }}
                  </span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onBeforeUnmount, ref, watch } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const activeTab = ref("data"); // data | history
const adminTab = ref("users"); // users | wallets | mode
watch(activeTab, (v) => {
  if (v === "history") loadTickets();
  if (v === "admin" && !isSuperuser.value) activeTab.value = "data";
});
const me = ref(null);
const isSuperuser = computed(() => !!me.value?.is_superuser);

const tickets = ref([]);
const loadingTickets = ref(false);
const adminUsers = ref([]);
const loadingAdminUsers = ref(false);

const expandedUserId = ref(null);      // какой пользователь раскрыт
const userTickets = ref([]);           // тикеты раскрытого пользователя
const loadingUserTickets = ref(false);
const formName = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const currentPassword = ref("");
function getTicketLifetimeSeconds(ticket) {
  if (Number(ticket?.give_currency_backend_id) === 2101) {
    return 20 * 60; // 20 минут
  }
  return 3 * 60 * 60; // 3 часа
}

const EXPIRED_TEXT = "Истекло время на отправку средств";
const showNewPass = ref(false);
const showConfirmPass = ref(false);
const showCurrentPass = ref(false);

const savingName = ref(false);
const savingPass = ref(false);
const saveError = ref("");


const settingsLoading = ref(false);
const settingsError = ref("");
const settingsSaving = ref(false);

// сюда грузим то, что пришло с бэка
const settings = ref(null);

// это то, что редактируем в инпутах (копия)
const settingsForm = ref({
  mode: "0",
  banner: "",
  percent: "",
  giveMin: "",
  giveMax: "",
  getMin: "",
  getMax: "",
  info: {
    Telegram_oper: "",
    Telegram_chanel: "",
    Session_id: "",
    Tox: "",
  },
  bot: {
    API_TOKEN: "",
    CHAT_ID: "",
    MESS_CHAT: "",
    domain: "",
  },
  deposit_wallets: {},
  fiat_in: {},
  fiat_out: {},
});

// ===== icons mapping (твои пути) =====
const ICON_BY_BACKEND_ID = {
  1: "/img/bit.svg?v=032",
  2: "/img/ether.svg?v=032",
  3: "/img/tether_trc20.svg?v=032",
  4: "/img/tether_erc20.svg?v=032",
  5: "/img/tether_bnb.svg?v=032",
  6: "/img/tether_solana.svg?v=032",
  7: "/img/dai.svg?v=032",
  8: "/img/usdc.svg?v=032",
  9: "/img/solana-sol-logo.png?v=032",
  10: "/img/lite.svg?v=032",
  11: "/img/tron.svg?v=032",
  12: "/img/doge.svg?v=032",

  // RUB methods
  2001: "/img/sbp.svg?v=032",
  2011: "/img/qr_sber.svg?v=032",
  2002: "/img/sber.svg?v=032.svg",
  2003: "/img/alpha.svg?v=032",
  2010: "/img/rub_nal.svg?v=032",
  2101: "/img/sbp.svg?v=032",
};

function iconByBackendId(id) {
  return ICON_BY_BACKEND_ID[Number(id)] || "";
}

// ===== timer (red) =====
const nowMs = ref(Date.now());
let tickTimer = null;

function formatHMS(totalSeconds) {
  const s = Math.max(0, Math.floor(totalSeconds));
  const hh = String(Math.floor(s / 3600)).padStart(2, "0");
  const mm = String(Math.floor((s % 3600) / 60)).padStart(2, "0");
  const ss = String(s % 60).padStart(2, "0");
  return `${hh}:${mm}:${ss}`;
}

function showTimer(status) {
  return status === "new";
}

function ticketTimer(ticket) {
  const t0 = new Date(ticket?.created_at).getTime();
  if (!Number.isFinite(t0)) return "00:00:00";

  const lifetime = getTicketLifetimeSeconds(ticket);
  const elapsed = (nowMs.value - t0) / 1000;
  const left = lifetime - elapsed;

  if (left <= 0) return "Истекло время на отправку средств";
  return formatHMS(left);
}

function isExpired(ticket) {
  const t0 = new Date(ticket?.created_at).getTime();
  if (!Number.isFinite(t0)) return false;

  const lifetime = getTicketLifetimeSeconds(ticket);
  const elapsed = (nowMs.value - t0) / 1000;

  return elapsed >= lifetime;
}

// ===== helpers =====
function getToken() {
  return localStorage.getItem("token") || "";
}

function authHeaders(opts = {}) {
  const t = getToken();
  const headers = { ...(opts.headers || {}) };

  // content-type только когда есть body
  if (opts.body && !headers["Content-Type"]) headers["Content-Type"] = "application/json";
  // authorization только если токен реально есть
  if (t) headers.Authorization = `Bearer ${t}`;

  return headers;
}

async function api(url, opts = {}) {
  return fetch(url, {
    ...opts,
    credentials: "include",
    headers: authHeaders(opts),
  });
}

async function loadMe() {
  const t = getToken();
  if (!t) {
    router.push("/login");
    return false;
  }

  const res = await api("/api/me", { method: "GET" });
  if (!res.ok) {
    localStorage.removeItem("token");
    window.dispatchEvent(new Event("auth-changed"));
    router.push("/login");
    return false;
  }

  me.value = await res.json();
  formName.value = me.value?.name || "";
  return true;
}

async function loadTickets() {
  const t = getToken();
  if (!t) {
    tickets.value = [];
    return;
  }

  loadingTickets.value = true;
  try {
    const res = await api("/api/my/tickets", { method: "GET" });
    if (!res.ok) {
      tickets.value = [];
      return;
    }
    const data = await res.json();
    tickets.value = Array.isArray(data) ? data : [];
  } finally {
    loadingTickets.value = false;
  }
}

async function loadAdminUsers() {
  if (!isSuperuser.value) return;

  loadingAdminUsers.value = true;
  try {
    const res = await api("/api/admin/users", { method: "GET" });
    if (!res.ok) {
      adminUsers.value = [];
      return;
    }
    const data = await res.json();
    adminUsers.value = Array.isArray(data) ? data : [];
  } finally {
    loadingAdminUsers.value = false;
  }
}

async function loadAdminSettings() {
  settingsLoading.value = true;
  settingsError.value = "";
  try {
    const res = await api("/api/admin/settings", { method: "GET" });
    if (!res.ok) {
      let d = "";
      try { d = (await res.json())?.detail || ""; } catch {}
      settingsError.value = d || "Не удалось загрузить settings.json";
      return;
    }

    const data = await res.json();
    settings.value = data;

    // ✅ важно: делаем “редактируемую копию”
    settingsForm.value = {
    mode: String(data?.mode ?? "0"),
    banner: data?.banner ?? "",
    percent: data?.percent ?? "",
    giveMin: data?.giveMin ?? "",
    giveMax: data?.giveMax ?? "",
    getMin: data?.getMin ?? "",
    getMax: data?.getMax ?? "",
    info: {
      Telegram_oper: data?.info?.Telegram_oper ?? "",
      Telegram_chanel: data?.info?.Telegram_chanel ?? "",
      Session_id: data?.info?.Session_id ?? "",
      Tox: data?.info?.Tox ?? "",
    },

    bot: {
      API_TOKEN: data?.bot?.API_TOKEN ?? "",
      CHAT_ID: data?.bot?.CHAT_ID ?? "",
      MESS_CHAT: data?.bot?.MESS_CHAT ?? "",
      domain: data?.bot?.domain ?? "",
    },

    deposit_wallets: data?.deposit_wallets ?? {},
    fiat_in: data?.fiat_in ?? {},
    fiat_out: data?.fiat_out ?? {},
};
  } catch (e) {
    settingsError.value = "Ошибка сети при загрузке settings.json";
  } finally {
    settingsLoading.value = false;
  }
}

async function saveAdminSettings() {
  settingsSaving.value = true;
  settingsError.value = "";
  try {
    const payload = {
    mode: String(settingsForm.value.mode ?? "0"),
    banner: settingsForm.value.banner,
    percent: settingsForm.value.percent,
    giveMin: settingsForm.value.giveMin,
    giveMax: settingsForm.value.giveMax,
    getMin: settingsForm.value.getMin,
    getMax: settingsForm.value.getMax,
    info: settingsForm.value.info,
    bot: settingsForm.value.bot,
    deposit_wallets: settingsForm.value.deposit_wallets,
    fiat_in: settingsForm.value.fiat_in,
    fiat_out: settingsForm.value.fiat_out,
  };

    const res = await api("/api/admin/settings", {
      method: "PUT",
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      let d = "";
      try { d = (await res.json())?.detail || ""; } catch {}
      settingsError.value = d || "Не удалось сохранить settings.json";
      return;
    }

    // перезагрузим, чтобы увидеть что реально записалось
    await loadAdminSettings();
  } catch (e) {
    settingsError.value = "Ошибка сети при сохранении settings.json";
  } finally {
    settingsSaving.value = false;
  }
}

async function toggleUserTickets(userId) {
  // закрыть если уже открыт
  if (expandedUserId.value === userId) {
    expandedUserId.value = null;
    userTickets.value = [];
    return;
  }

  expandedUserId.value = userId;
  userTickets.value = [];
  loadingUserTickets.value = true;

  try {
    const res = await api(`/api/admin/users/${userId}/tickets`, { method: "GET" });
    if (!res.ok) {
      userTickets.value = [];
      return;
    }
    const data = await res.json();
    userTickets.value = Array.isArray(data) ? data : [];
  } finally {
    loadingUserTickets.value = false;
  }
}

// обновляем тикеты при событии с главной
function onTicketsChanged() {
  loadTickets();
}

// грузим тикеты каждый раз при открытии вкладки history
watch(activeTab, (v) => {
  if (v === "history") loadTickets();
  if (v === "admin" && isSuperuser.value) {
    // когда открыли админку — по умолчанию users
    if (adminTab.value === "users") loadAdminUsers();
  }
});
watch(adminTab, (v) => {
  if (activeTab.value !== "admin") return;
  if (!isSuperuser.value) return;

  if (v === "users") loadAdminUsers();
  if (v === "wallets" || v === "mode") loadAdminSettings();
});

// ===== profile save rules =====
const canSaveName = computed(() => {
  const v = formName.value.trim();
  return v.length >= 4 && v.length <= 10 && v !== (me.value?.name || "");
});

const canSavePassword = computed(() => {
  if (currentPassword.value.length < 1) return false;
  if (newPassword.value.length < 8) return false;
  if (newPassword.value !== confirmPassword.value) return false;
  return true;
});

async function saveName() {
  if (!canSaveName.value || savingName.value) return;
  saveError.value = "";
  savingName.value = true;
  try {
    // если сделаешь ручку — заработает:
    // PATCH /api/profile/name { name }
    const res = await api("/api/profile/name", {
      method: "PATCH",
      body: JSON.stringify({ name: formName.value.trim() }),
    });

    if (!res.ok) {
      saveError.value = "Не удалось сохранить имя";
      return;
    }

    await loadMe();
    window.dispatchEvent(new Event("auth-changed"));
  } catch {
    saveError.value = "Не удалось сохранить имя";
  } finally {
    savingName.value = false;
  }
}

async function savePassword() {
  if (!canSavePassword.value || savingPass.value) return;

  saveError.value = "";
  savingPass.value = true;

  try {
    const res = await api("/api/profile/password", {
      method: "PATCH",
      body: JSON.stringify({
        current_password: currentPassword.value,
        new_password: newPassword.value,
        confirm_password: confirmPassword.value,
      }),
    });

    if (!res.ok) {
      // покажем реальную причину с бэка
      let detail = "";
      try {
        const j = await res.json();
        detail = j?.detail || "";
      } catch (_) {}

      // человеко-понятные сообщения
      if (detail === "wrong current password") {
        saveError.value = "Неверный текущий пароль";
      } else if (detail === "password too short") {
        saveError.value = "Пароль должен быть от 8 символов";
      } else if (detail === "passwords do not match") {
        saveError.value = "Пароли не совпадают";
      } else if (detail === "not authenticated") {
        saveError.value = "Нужно войти заново";
      } else {
        saveError.value = "Не удалось сохранить пароль";
      }

      // на всякий случай лог в консоль
      console.log("change password failed:", res.status, detail);
      return;
    }

    // ✅ очистка после успеха
    currentPassword.value = "";
    newPassword.value = "";
    confirmPassword.value = "";
  } catch (e) {
    console.error("change password error:", e);
    saveError.value = "Не удалось сохранить пароль";
  } finally {
    savingPass.value = false;
  }
}

function logout() {
  localStorage.removeItem("token");
  window.dispatchEvent(new Event("auth-changed"));
  router.push("/");
}

// ===== formatting =====

// дата без секунд (похоже на оригинал: "04.03.2026, 19:17")
function formatDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return d.toLocaleString("ru-RU", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// #eaaf...159
function shortTicketId(id) {
  const s = String(id || "");
  if (s.length <= 10) return `#${s}`;
  return `#${s.slice(0, 4)}...${s.slice(-3)}`;
}

function statusLabel(s) {
  const map = {
    new: "Ожидаем получение средств",
    not_confirmed: "Ожидайте подтверждение",
    cancelled: "Отменён",
    completed: "Подтверждён",
  };
  return map[s] || s;
}

onMounted(async () => {
  // таймер для красных часов
  tickTimer = setInterval(() => (nowMs.value = Date.now()), 1000);

  const ok = await loadMe();
  if (ok) {
    // тикеты нужны только для вкладки history (но можно оставить как было)
    await loadTickets();

    // ✅ если суперюзер и уже на админке → подтягиваем пользователей
    if (isSuperuser.value && activeTab.value === "admin" && adminTab.value === "users") {
      await loadAdminUsers();
    }
  }

  window.addEventListener("tickets-changed", onTicketsChanged);
});

onBeforeUnmount(() => {
  if (tickTimer) clearInterval(tickTimer);
  window.removeEventListener("tickets-changed", onTicketsChanged);
});
</script>