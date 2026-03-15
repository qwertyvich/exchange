<!-- src/pages/RegistrationPage.vue -->
<template>
  <div
    class="flex flex-col items-center justify-center md:gap-12 gap-9 md:py-24 py-8 max-w-225 w-full self-center grow basis-full container text-white"
    style="min-height: calc(100dvh - 96px);"
  >
    <div class="w-full flex justify-center">
      <div
        class="bg-bg-tertiary border border-border-secondary md:rounded-[28px] rounded-[22px] w-full"
        style="max-width: 460px; width: calc(100% - 24px);"
      >
        <form @submit.prevent="onSubmit">
          <div class="flex flex-col md:gap-8 gap-4 md:px-7 md:py-10 px-6 pb-6 pt-5">
            <h3 class="md:text-[32px] text-2xl font-medium leading-[120%] text-center">
              Регистрация
            </h3>

            <!-- Fields -->
            <div class="flex flex-col md:gap-2 gap-1.5">
              <!-- Name -->
              <div data-slot="form-item" class="grid gap-2">
                <div class="relative w-full">
                  <input
                    v-model.trim="profileName"
                    maxlength="10"
                    data-slot="form-control"
                    id="reg_name"
                    name="name"
                    placeholder=" "
                    autocomplete="nickname"
                    :aria-invalid="showNameError"
                    @blur="touched.name = true"
                    :class="inputClass(showNameError)"
                    class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60"
                  >
                  <label
                    for="reg_name"
                    class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
                  >
                    Имя профиля
                  </label>
                </div>

                <p v-if="showNameError" class="text-danger md:text-sm text-xs font-medium">
                  {{ nameError }}
                </p>
              </div>

              <!-- Email -->
              <div data-slot="form-item" class="grid gap-2">
                <div class="relative w-full">
                  <input
                    v-model.trim="email"
                    data-slot="form-control"
                    id="reg_email"
                    name="email"
                    placeholder=" "
                    autocomplete="email"
                    inputmode="email"
                    :aria-invalid="showEmailError"
                    @blur="touched.email = true"
                    :class="inputClass(showEmailError)"
                    class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60"
                  >
                  <label
                    for="reg_email"
                    class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
                  >
                    E-mail
                  </label>
                </div>

                <p v-if="showEmailError" class="text-danger md:text-sm text-xs font-medium">
                  {{ emailError }}
                </p>
              </div>

              <!-- Password -->
              <div class="flex flex-col gap-3">
                <div data-slot="form-item" class="grid gap-2">
                  <div class="relative w-full">
                    <input
                      v-model="password"
                      data-slot="form-control"
                      id="reg_password"
                      name="password"
                      placeholder=" "
                      :type="showPassword ? 'text' : 'password'"
                      autocomplete="new-password"
                      :aria-invalid="showPasswordError"
                      @blur="touched.password = true"
                      :class="inputClass(showPasswordError)"
                      class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60"
                    >
                    <label
                      for="reg_password"
                      class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
                    >
                      Пароль
                    </label>

                    <button
                      type="button"
                      class="absolute md:right-8 right-6 top-1/2 -translate-y-1/2 cursor-pointer text-icon-hover transition"
                      :disabled="isSubmitting"
                      aria-label="Показать/скрыть пароль"
                      @click="showPassword = !showPassword"
                    >
                      <svg
                        v-if="!showPassword"
                        xmlns="http://www.w3.org/2000/svg"
                        width="24" height="24" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2"
                        stroke-linecap="round" stroke-linejoin="round"
                        class="md:size-8 size-6"
                        aria-hidden="true"
                      >
                        <path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                      <svg
                        v-else
                        xmlns="http://www.w3.org/2000/svg"
                        width="24" height="24" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2"
                        stroke-linecap="round" stroke-linejoin="round"
                        class="md:size-8 size-6"
                        aria-hidden="true"
                      >
                        <path d="M2 2l20 20"></path>
                        <path d="M6.71 6.71C4.68 8.13 3.18 10.02 2.46 12c1.3 3.42 4.6 7 9.54 7c1.43 0 2.77-.3 3.97-.82"></path>
                        <path d="M9.9 9.9a3 3 0 0 0 4.24 4.24"></path>
                        <path d="M14.12 14.12L9.88 9.88"></path>
                        <path d="M12 5c4.94 0 8.24 3.58 9.54 7c-.5 1.32-1.37 2.67-2.55 3.86"></path>
                      </svg>
                    </button>
                  </div>

                  <p v-if="showPasswordError" class="text-danger md:text-sm text-xs font-medium">
                    {{ passwordError }}
                  </p>
                </div>

                <!-- Confirm password -->
                <div data-slot="form-item" class="grid gap-2">
                  <div class="relative w-full">
                    <input
                      v-model="confirmPassword"
                      data-slot="form-control"
                      id="reg_confirm"
                      name="confirmPassword"
                      placeholder=" "
                      :type="showConfirm ? 'text' : 'password'"
                      autocomplete="new-password"
                      :aria-invalid="showConfirmError"
                      @blur="touched.confirm = true"
                      :class="inputClass(showConfirmError)"
                      class="md:text-xl text-base font-light leading-[140%] peer bg-bg-primary hover:bg-bg-hover border-border-secondary focus:border-border-active placeholder:text-text-tertiary flex w-full md:rounded-[28px] rounded-[22px] border md:px-8 md:pt-10 md:pb-4 px-6 pt-7 pb-3 transition-all duration-150 outline-none disabled:cursor-not-allowed disabled:opacity-60"
                    >
                    <label
                      for="reg_confirm"
                      class="md:text-base text-xs font-light leading-[150%] absolute pointer-events-none text-text-tertiary duration-200 transform md:-translate-y-1 -translate-y-0.5 md:top-5 top-3 z-10 origin-[0] md:left-8 left-6 md:peer-focus:-translate-y-1 peer-focus:-translate-y-0.5 peer-focus:scale-100 peer-placeholder-shown:not-peer-focus:top-1/2 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:scale-125"
                    >
                      Подтвердите пароль
                    </label>

                    <button
                      type="button"
                      class="absolute md:right-8 right-6 top-1/2 -translate-y-1/2 cursor-pointer text-icon-hover transition"
                      :disabled="isSubmitting"
                      aria-label="Показать/скрыть пароль"
                      @click="showConfirm = !showConfirm"
                    >
                      <svg
                        v-if="!showConfirm"
                        xmlns="http://www.w3.org/2000/svg"
                        width="24" height="24" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2"
                        stroke-linecap="round" stroke-linejoin="round"
                        class="md:size-8 size-6"
                        aria-hidden="true"
                      >
                        <path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                      <svg
                        v-else
                        xmlns="http://www.w3.org/2000/svg"
                        width="24" height="24" viewBox="0 0 24 24"
                        fill="none" stroke="currentColor" stroke-width="2"
                        stroke-linecap="round" stroke-linejoin="round"
                        class="md:size-8 size-6"
                        aria-hidden="true"
                      >
                        <path d="M2 2l20 20"></path>
                        <path d="M6.71 6.71C4.68 8.13 3.18 10.02 2.46 12c1.3 3.42 4.6 7 9.54 7c1.43 0 2.77-.3 3.97-.82"></path>
                        <path d="M9.9 9.9a3 3 0 0 0 4.24 4.24"></path>
                        <path d="M14.12 14.12L9.88 9.88"></path>
                        <path d="M12 5c4.94 0 8.24 3.58 9.54 7c-.5 1.32-1.37 2.67-2.55 3.86"></path>
                      </svg>
                    </button>
                  </div>

                  <p v-if="showConfirmError" class="text-danger md:text-sm text-xs font-medium">
                    {{ confirmError }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Submit -->
            <button
              data-slot="button"
              class="inline-flex w-full items-center justify-center gap-1.5 p-4 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 bg-brand hover:bg-brand-hover text-text-primary data-[state=active]:bg-brand-active data-[state=active]:text-text-inv-primary max-md:rounded-[22px] md:py-6 py-4.5"
              type="submit"
              :disabled="!canSubmit"
            >
              <p class="md:text-xl text-base font-medium leading-[140%]">
                {{ isSubmitting ? "Регистрация..." : "Зарегистрироваться" }}
              </p>
            </button>

            <!-- Back to login -->
            <RouterLink to="/login" class="w-full">
              <button
                data-slot="button"
                class="inline-flex w-full items-center justify-center gap-1.5 whitespace-nowrap rounded-[28px] text-sm font-medium transition-all duration-150 disabled:pointer-events-none disabled:opacity-20 [&_svg]:pointer-events-none shrink-0 [&_svg]:shrink-0 outline-none aria-invalid:ring-red-500/20 aria-invalid:border-red-500 text-text-primary hover:text-text-hover data-[state=active]:text-text-active md:p-0 p-0"
                type="button"
              >
                <span class="md:text-xl text-base font-light leading-[140%] text-text-secondary py-4 md:py-5">
                  Вход
                </span>
              </button>
            </RouterLink>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const profileName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");

const showPassword = ref(false);
const showConfirm = ref(false);
const isSubmitting = ref(false);

const touched = reactive({
  name: false,
  email: false,
  password: false,
  confirm: false,
});
const submitAttempted = ref(false);

// helpers
const emailFormatOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);

// errors (строки)
const nameError = computed(() => {
  const v = profileName.value.trim();
  if (!v) return "Обязательное поле";
  if (v.length < 4) return "От 4 символов";
  if (v.length > 10) return "До 10 символов";
  return "";
});

const emailError = computed(() => {
  const v = email.value.trim();
  if (!v) return "Обязательное поле";
  if (!emailFormatOk(v)) return "Некорректный формат E-mail";
  return "";
});

const passwordError = computed(() => {
  const v = password.value;
  if (!v) return "Обязательное поле";
  if (v.length < 8) return "От 8 символов";
  return "";
});

const confirmError = computed(() => {
  const v = confirmPassword.value;
  if (!v) return "Обязательное поле";
  if (v !== password.value) return "Пароли не совпадают";
  return "";
});

// when to show errors
const showNameError = computed(() => (touched.name || submitAttempted.value) && !!nameError.value);
const showEmailError = computed(() => (touched.email || submitAttempted.value) && !!emailError.value);
const showPasswordError = computed(() => (touched.password || submitAttempted.value) && !!passwordError.value);

// confirm: если уже начали вводить confirm — показываем несовпадение сразу
const showConfirmError = computed(() => {
  const startedTyping = confirmPassword.value.length > 0;
  return (touched.confirm || submitAttempted.value || startedTyping) && !!confirmError.value;
});

// button enabled only when all ok
const canSubmit = computed(() => {
  return (
    !nameError.value &&
    !emailError.value &&
    !passwordError.value &&
    !confirmError.value &&
    !isSubmitting.value
  );
});

// add red border when invalid (если у тебя есть token border-danger — отлично)
// если нет, то хотя бы aria-invalid сработает через aria-invalid:border-danger в твоих классах
function inputClass(isInvalid) {
  return isInvalid ? "border-danger focus:border-danger" : "";
}

async function onSubmit() {
  submitAttempted.value = true;
  if (!canSubmit.value) return;

  isSubmitting.value = true;
  try {
    const res = await fetch("/api/registration", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        name: profileName.value.trim(),
        email: email.value.trim(),
        password: password.value,
      }),
    });

    if (!res.ok) return;

    // сразу логинимся
    const loginRes = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        email: email.value.trim(),
        password: password.value,
      }),
    });

    if (!loginRes.ok) return;

    const data = await loginRes.json();
    localStorage.setItem("token", data.access_token);
    window.dispatchEvent(new Event("auth-changed"));
    router.push("/");

  } catch (e) {
    console.error("registration error:", e);
  } finally {
    isSubmitting.value = false;
  }
}
</script>